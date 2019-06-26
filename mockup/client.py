## taken from https://github.com/websocket-client/websocket-client
import websocket

websocket.enableTrace(True)
ws = websocket.create_connection("ws://0.0.0.0:8000/")
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Receiving...")
result = ws.recv()
print("Received '%s'" % result)
ws.close()

