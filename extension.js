
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const WebSocket = require("ws");
const vscode = require('vscode');

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	let ws = new WebSocket.Server({ port: 9876 })
	let sender
	ws.on("connection", (ws) => {
		ws.on("message", (msg) => {
			console.log("got message")
		})
		sender = ws
	})
	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
  let prevPos = [0,0]
	console.log('Congratulations, your extension "io-ex-ed" is tooo active! run!');
	vscode.window.onDidChangeTextEditorSelection((e)=> {
    prevPos = [e.selections[0].start.line,e.selections[0].start.character]
    console.log("setting pos ",prevPos)
	})
	vscode.workspace.onDidChangeTextDocument((e) => {
		let charChange = e.contentChanges[0].text
		let col = e.contentChanges[0].range.start.character
		let line = e.contentChanges[0].range.start.line
		console.log("line", line)
		console.log("column", col)
		console.log("char ", charChange)
		// calculate the index of change as single number instead of line and col, 
		// makes insertion in iodide easier, fewer corner cases
		// get the document contents, count columns in lines above current one, then add the column count, perhaps need to include the newline chars too
		let flatInd = e.document.getText().split("\n").slice(0, line).reduce((acc, cur) => {
			acc += cur + "\n"
			return acc
		}, "").length + col
		let text = e.document.getText().slice(0, flatInd) + "-" + charChange + "-" + e.document.getText().slice(flatInd + 1)
		console.log("inserted", text)
		// construct an object to send to the extension
		let msgOb
		if (charChange !== "") {
			msgOb = {
				pos: [line, col, flatInd],
				type: "INSERT_TEXT",
				text: charChange
			}
			if (sender){
				sender.send(JSON.stringify(msgOb))
			}
			
		} else {
      if (col === prevPos[1]) {
        // this is a delete key event
        // send the exact flatInd if its backspace pretend that we moved one char back and then performed a deletion
		console.log("deletion",col,prevPos);
		
		msgOb = {
          type:"DELETE_TEXT",
          pos:[line,col,flatInd],
          numChars:1,
        }
      } else {
        // this is a backspace key event
		console.log("backspace",col,prevPos);
		msgOb = {
          type:"DELETE_TEXT",
          pos:[line,col,flatInd],
          numChars:1,
        }
      }
      if (sender) {
        sender.send(JSON.stringify(msgOb))
      }
    }
	})
	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('extension.helloWorld', function () {
		// The code you place here will be executed every time your command is executed

		// Display a message box to the user
		vscode.window.showInformationMessage('Hello World! this all done is a now active program');
	});

	context.subscriptions.push(disposable);
}
exports.activate = activate;

// this method is called when your extension is deactivated
function deactivate() { }

module.exports = {
	activate,
	deactivate
}
