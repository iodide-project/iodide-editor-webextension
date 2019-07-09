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


    @pynvim.command('StartComm', nargs='*', range='')
    def start_comm(self,args,range):
        self.com_clear =True
        server = SimpleWebSocketServer('', 9876, SimpleEcho)
        threading.Thread(target=server.serveforever).start()
        ## in background setup timer to send whole buffer to iodide every 5 seconds
        self.server = server

    @pynvim.autocmd('InsertLeave', pattern='*', eval='expand("<afile>")', sync=True)
    def exit_insert(self,filename):
        self.send_whole_document()


    @pynvim.autocmd('TextChangedI', pattern='*', eval='expand("<afile>")', sync=True)
    def on_text_change(self, filename):
        if not self.com_clear:
            return None
        ## grab the last character created
        cursor_position = self.nvim.current.window.cursor
        character_entered = self.nvim.current.buffer[cursor_position[0]-1][cursor_position[1]-1] ## cursor position's first argument is 1 index based, must go down by one for the active line
        ## the second index is zero based, but the cursor col will have just increased by 1 when the text changes
        ## need to decrease the line cursor position for iodide's translation
        msg_object = {"pos":[cursor_position[0]-1,cursor_position[1]-1],"type":"INSERT_TEXT","text":character_entered}
        all_connections[-1].sm(json.dumps(msg_object))
