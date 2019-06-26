
// the different types of messages to send along to iodide. Based on what the editor plugin says the user is up to we would use one or another of these

let insertText = (text,cursorPos) => {
    return JSON.stringify({
        exMessageType:"INSERT_TEXT",
        cursorPosition:cursorPos,
        text,
    })
}

// the whole buffer replace function

let replaceAll = (text) => {
    return JSON.stringify({
        exMessageType:"REPLACE_ALL",
        text,
    })
}


function postToIodide(externalEditorMessageEvent,iodideEditorMessageEvent) {
    //  case section to decide on the function to call
    // translate the message event into an action that changes the iodide editor
    console.log("debug first parameter",externalEditorMessageEvent)
    let externalEditorAction 
    switch (externalEditorMessageEvent.type) { // type will be the result of processing before hand
        // these aren't actually what the editor is going to communicate in the final form
        case "INSERT_TEXT":
            console.log("using insert text type")
            externalEditorAction = insertText(externalEditorMessageEvent.data,externalEditorMessageEvent.pos)
            break;
        default:
            console.log("using replace all type")
            externalEditorAction = replaceAll(externalEditorMessageEvent.data)
    }
    iodideEditorMessageEvent.ports[0].postMessage(externalEditorAction)
}


(function startIoConnect() {
    if (!window) {
        console.log("wasn't ready")
        setTimeout(startIoConnect,1000)
    }
    console.log("ready")
    // must think of how to connect the websocket up again to use that text as input
    window.addEventListener("message",(e)=> {
        if (e.source== window && e.data && e.data.direction=="iodide-to-extension"){
            console.log("received object from window in extension")
            console.log(e)
            console.log(e.data.message)
            // need to try getting the port out of this and communicating to the editor
            // port is accessible off e object
            console.log("returning message")
          const s = new WebSocket("ws://localhost:9876");
          s.onopen = e => {
            console.log("no more wait")
            console.log(`opened ${e}`);
          };
          // s.onclose = function(e) { alert("closed");console.log(e) }
            
        // when extension socket receives a message from the editor plugin's end of the socket just automatically pass into the message channel 
            // to send it along to iodide's editor
          s.onmessage = messageEvent => {
              // will call function to post the correct iodide message object 
              // !! hard coding the type for development work
              // trim down and modify the extension messageevent
              let modifiedEvent = {
                  data:messageEvent.data,
            }
              modifiedEvent.type = "INSERT_TEXT"
              modifiedEvent.pos = 5 // !! probably will require line and column info in the actual implementation
              postToIodide(modifiedEvent,e)
          };
        }
})
})()
