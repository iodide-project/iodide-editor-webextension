from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class SimpleEcho(WebSocket):
    def handleMessage(self):
        # echo message back to client
        self.sendMessage(self.data+" serverfile")
    def handleConnected(self):
        print(self.address, 'connected')
    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 8000, SimpleEcho)
server.serveforever()
## don't forget to close

