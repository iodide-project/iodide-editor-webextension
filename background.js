console.log("background running")
var tries =10 
let executor = ()=> {
    //let ws = new WebSocket("ws://localhost:9876")
    browser.tabs.executeScript({file:"./content_scripts/index.js"})
    //ws.onopen= ()=> {
    //    ws.send("hi")
    //    console.log("started")
    //}
    //ws.onmessage = e=> {
    //    console.log("reply",e.data)
    //}
}
browser.windows.getCurrent().addEventListener("load",executor)
