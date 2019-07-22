import pynvim
## TODO look into why is this imported twice?
import threading
import json
import time
import datetime
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

all_connections =[]
class SimpleEcho(WebSocket):
    def handleMessage(self):
        # echo message back to client
        self.sendMessage(self.data)
    def sm(self,message):
        self.sendMessage(message)
    def handleConnected(self):
        print(self.address, 'connected')
        all_connections.append(self)
    def handleClose(self):
        print(self.address, 'closed')


#@pynvim.plugin
#class Communicator(object):
#    def __init__(self,nvim):
#        self.nvim = nvim
#    
#
#    @pynvim.autocmd('BufEnter', pattern='*.py', eval='expand("<afile>")', sync=True)
#    def on_textchanged(self, filename):
#            self.nvim.out_write("contents changing, calling send to socket")
#            self.sock(nvim.current.buffer[:])
#
#

import pynvim
@pynvim.plugin
class TestPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim
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
        server = SimpleWebSocketServer('', 9876, SimpleEcho)
        threading.Thread(target=server.serveforever).start()
        ## in background setup timer to send whole buffer to iodide every 5 seconds
        self.server = server
        ## begin the next message checker
        ## might have to be in async_call?
        self.keep_checking = True
        threading.Thread(target=self.check_messages).start()

    def set_listen(self):
        self.nvim.request("nvim_buf_attach",1,True,{})

    def next_message(self):
        response = self.nvim.next_message() 
        self.nvim.out_write(response +"\n")
        return response

    def check_messages(self):
        self.nvim.async_call(self.set_list)
        while True:
            ## will block
            if self.keep_checking:
                response = self.nvim.async_call(self.next_message)
                self.nvim.async_call(self.send_whole_document)

            


    @pynvim.autocmd('InsertEnter', pattern='*', eval='expand("<afile>")', sync=True)
    def enter_insert(self,filename):
        if self.com_clear:
            self.send_whole_document()

    @pynvim.autocmd('InsertLeave', pattern='*', eval='expand("<afile>")', sync=True)
    def exit_insert(self,filename):
        if self.com_clear:
            self.send_whole_document()


    ## changes that should be like big blocks of lines getting put in and deleted
    @pynvim.autocmd('TextChanged', pattern='*', eval='expand("<afile>")', sync=True)
    def on_lines_shift(self,filename):
        ## if we don't have connection yet
        if self.com_clear:
            self.send_whole_document()


    @pynvim.autocmd('TextChangedI', pattern='*', eval='expand("<afile>")', sync=True)
    def on_text_change(self, filename):
        if not self.com_clear:
            return None
        ## grab the last character created
        cursor_position = self.nvim.current.window.cursor
        line = self.nvim.current.buffer[cursor_position[0]-1]
        ## if we have a newline there's nothing new to send yet
        if not line:
            return
        character_entered = self.nvim.current.buffer[cursor_position[0]-1][cursor_position[1]-1] ## cursor position's first argument is 1 index based, must go down by one for the active line
        ## the second index is zero based, but the cursor col will have just increased by 1 when the text changes
        ## need to decrease the line cursor position for iodide's translation
        msg_object = {"pos":[cursor_position[0]-1,cursor_position[1]-1],"type":"INSERT_TEXT","text":line}
        all_connections[-1].sm(json.dumps(msg_object))
