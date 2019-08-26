
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
	let ws = new WebSocket.Server({port:8080})
	let sender
	ws.on("connection",(ws)=> {
		ws.on("message",(msg)=> {
			console.log("got message")
		})
		sender = ws
	})
	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "io-ex-ed" is tooo active! run!');
	vscode.workspace.onDidChangeTextDocument((e)=> {
		console.log("line",e.contentChanges[0].range.start.line)
		console.log("column",e.contentChanges[0].range.start.character)
		console.log("char ", e.contentChanges[0].text)
		if (sender){
			sender.send(e.contentChanges[0].text)
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
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
