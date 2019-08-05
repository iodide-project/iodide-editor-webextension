import pynvim
## TODO look into why is this imported twice?
import threading
import json
import time
import datetime
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

all_messages= ""
all_connections =[]
nvims = []
## apparently self.data is a json like object
class SimpleEcho(WebSocket):
    def update(self,info):
        nvims[0].buffers[1][:] =info.split("\n")
        ## note that this will also trigger a buffer change, so it will auto update the editor one more time
    def handleMessage(self):
        if len(nvims) >0:
            nvims[0].async_call(self.update,self.data)
    def sm(self,message):
        self.sendMessage(message)
    def handleConnected(self):
        print(self.address, 'connected')
        all_connections.append(self)
    def handleClose(self):
        print(self.address, 'closed')


import pynvim
@pynvim.plugin
class TestPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.prev_pos= [0,0]
        self.com_clear=False ## specifies whether the user has activated communication

    def send_whole_document(self):
        ## the default behavior without a specific tyep is to replace the iomd_content
        msg_object = {"text":"\n".join(self.nvim.current.buffer[:])}
        all_connections[-1].sm(json.dumps(msg_object))

    @pynvim.command('CloseComm', nargs='*', range='')
    def close_comm(self,args,range):
        self.server.close()

    @pynvim.command('EvalRequest',nargs='*',range='')
    def eval_req(self,args,range):
        msg_object = {"type":"EVAL_CHUNK"}
        all_connections[-1].sm(json.dumps(msg_object))


    @pynvim.command('StartComm', nargs='*', range='')
    def start_comm(self,args,range):
        self.com_clear =True
        ## register the keyboard mapping to send requests to the web browser 
        self.nvim.command("nnoremap <C-e> :EvalRequest<CR>")

        ## register to receive buffer change events
        ## setup the server
        nvims.append(self.nvim)
        server = SimpleWebSocketServer('', 9876, SimpleEcho)
        threading.Thread(target=server.serveforever).start()
        ## in background setup timer to send whole buffer to iodide every 5 seconds
        self.server = server
        ## begin the next message checker
        ## might have to be in async_call? 

    
    @pynvim.autocmd('InsertEnter', pattern='*', eval='expand("<afile>")', sync=True)
    def enter_insert(self,filename):
        self.prev_pos = self.nvim.current.window.cursor
        self.prev_pos[1]+=1 ## the normal cursor position is used which isn't correct
    @pynvim.autocmd('InsertLeave', pattern='*', eval='expand("<afile>")', sync=True)
    def exit_insert(self,filename):
        if self.com_clear:
            self.send_whole_document()




    @pynvim.autocmd('TextChangedI', pattern='*', eval='expand("<afile>")', sync=True)
    def on_text_change(self, filename):
        if not self.com_clear:
            return None
        ## grab the last character created
        cursor_position = self.nvim.current.window.cursor
        ## figure out if text changed from a backspace or deletion
        ## deletion is if the text changes but the col position stays the same

        self.nvim.out_write("{}\n".format(cursor_position))
        self.nvim.out_write("{}\n".format(self.col_pos))
        if self.prev_pos[1] > cursor_position[1] and self.prev_pos[0] == cursor_position[0] :
            self.prev_pos = cursor_position
            ## emit a deletion event
            msg_object = {"pos":[cursor_position[0]-1,cursor_position[1]+1],"type":"DELETE_TEXT","numCharsToDelete":1}
            all_connections[-1].sm(json.dumps(msg_object))
            return 
        self.col_pos = cursor_position[1]
        line = self.nvim.current.buffer[cursor_position[0]-1]
        self.nvim.out_write("{}line\n".format(line))
        if line == "":
            ## send a newline character to iodide
            msg_object = {"pos":[cursor_position[0]-1,cursor_position[1]],"type":"INSERT_TEXT","text":"\n"}
        else :
        ## if we have a newline there's nothing new to send yet
            character_entered = self.nvim.current.buffer[cursor_position[0]-1][cursor_position[1]-1] ## cursor position's first argument is 1 index based, must go down by one for the active line
            ## the second index is zero based, but the cursor col will have just increased by 1 when the text changes
            ## need to decrease the line cursor position for iodide's translation
            msg_object = {"pos":[cursor_position[0]-1,cursor_position[1]-1],"type":"INSERT_TEXT","text":character_entered}
            self.nvim.out_write("text {}\n".format(character_entered))
        all_connections[-1].sm(json.dumps(msg_object))
