import pynvim
import threading
import os
os.sys.path.append("/tmp/simple-websocket-server")

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


    @pynvim.command('StartComm', nargs='*', range='')
    def start_comm(self,args,range):
        self.com_clear =True
        server = SimpleWebSocketServer('', 9876, SimpleEcho)
        print("starting serve forever, could run into trouble")
        threading.Thread(target=server.serveforever).start()
        print("started threead")
        self.server = server

    @pynvim.autocmd('TextChangedI', pattern='*', eval='expand("<afile>")', sync=True)
    def on_text_change(self, filename):
        if not self.com_clear:
            return None
        self.nvim.out_write('testplugin is in ' + filename + '\n')
        all_connections[-1].sm("\n".join(self.nvim.current.buffer[:]))
