
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
	let filling
	let ioChangeCount = 0
	ws.on("connection", (ws) => {
		ws.on("message", (msg) => {
			console.log("got message", msg)
			let editor = vscode.window.activeTextEditor;

			if (editor) {
				let document = editor.document;
				let selection = editor.selection;

				// Get the word within the selection
				// wait half sec for the last editor can't catch all changes

				editor.edit(editBuilder => {
					editBuilder.replace(new vscode.Range(0, 0, document.lineCount, 0), `${msg}`);
					filling = Date.now()

				});
			}
		})
		sender = ws
	})
	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	let prevPos = [0, 0]
	console.log('Congratulations, your extension "io-ex-ed" is tooo active! run!');
	vscode.window.onDidChangeTextEditorSelection((e) => {
		prevPos = [e.selections[0].start.line, e.selections[0].start.character]
		console.log("setting pos ", prevPos)
	})
	vscode.workspace.onDidChangeTextDocument((e) => {
		console.log(e)
		// iterate over the contentChanges array
		for (let change of e.contentChanges) {
			let text = change.text
			if (Date.now() - filling < 500) {
				// 
				console.log(filling, "filling in")
				return
			}
			let col = change.range.start.character
			let line = change.range.start.line
			console.log("line", line)
			console.log("column", col)
			// calculate the index of change as single number instead of line and col, 
			// makes insertion in iodide easier, fewer corner cases
			// get the document contents, count columns in lines above current one, then add the column count, perhaps need to include the newline chars too
			let msgObj
			// emit all the necessary deletion events
			// technicallly the deletion and insertion could be seen as the same message with varying text values
			msgObj = {
				pos: [line, col],
				type: "INSERT_TEXT",
				rangeInfo: {
					len: change.rangeLength,
					offset: change.rangeOffset // when is this multiarrayed?
				},
				text,
			}
			if (sender) {
				sender.send(JSON.stringify(msgObj))
			}

		}
	})
	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	vscode.commands.registerCommand('extension.executeChunk', function () {
		console.log("executing")
		if (sender) {
			sender.send(JSON.stringify({
				type: "EVAL_CHUNK"
			}))
		}
	})
	let disposable = vscode.commands.registerCommand('extension.connectIodide', function () {
		// The code you place here will be executed every time your command is executed

		// Display a message box to the user
		vscode.window.showInformationMessage('you have connected to iodide');
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
