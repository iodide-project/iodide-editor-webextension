## iodide-editor-webextension
This project serves to communicate between iodide and a supported external editor such as neovim. Guidelines and documentation is provided to allow for the inclusion of other editor plugins that can then similarly control an iodide notebook remotely. The flow of information will eventually support bidirectional document syncronization, but at the moment all the work has been done in the external editor -> Iodide direction. 

The process begins with an editor plugin detecting one of two things: text changed in the buffer, or an eval chunk request. It then communicates with a websocket server running on the local machine which of these events occured with information such as cursor position, and text strings where appropriate. This local websocket server then communicates the event to a webextension loaded in the browser 

### Setting up
While this extension is under development it is recommended that this repo is cloned and the ```web-ext run``` command is executed in the directory with the ```manifest.json``` file. At the time of completion the webextension will be available through the standard add-ons installation route. Support for communicating with the webextension is still experimental, and exists in this [iodide-fork](https://github.com/DevinBayly/iodide). The suggested course here is to clone this fork and start up a local Iodide server which will then connect to a previously setup localhost websocket server running on the port ```9876```.

### Editor to Websocket Server
#### websocket server recommendation (python)
The example neovim plugin uses the [dpallot websocket library](https://github.com/dpallot/simple-websocket-server/blob/master/SimpleWebSocketServer/SimpleWebSocketServer.py). This server is started when the plugin loads, and message objects such as 

```
msg_object = {"pos":[cursor_position[0]-1,cursor_position[1]-1],"type":"INSERT_TEXT","text":character_entered}
```
or 
```
msg_object = {"type":"EVAL_CHUNK"}
```
are sent as JSON strings with the ```websocket_connection.sm(msg_object)``` method



#### Supported events
So far these are the only events that the editor plugin can communicate about with the websocket server and subsequently the Iodide notebook.

* detection of keystrokes
  * this is done character by character, and must include cursor position information in the message object. If line and column numbering starts at 1 subtract from the position as shown in the code snippet above.
* eval chunk keymapping
  * this event doesn't require any additional information to be sent in the message object besides the type

### Websocket server to Webextension communication
message types

```
msg_object = {"pos":[line,col],"type":"INSERT_TEXT","text":character_entered}
```
or 
```
msg_object = {"type":"EVAL_CHUNK"}
```



