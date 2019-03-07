console.log("background running")
var tries =10 
let executor = ()=> {
    browser.tabs.executeScript({file:"./content_scripts/index.js"})
    if (tries > 0) {
        console.log("still waiting")
        tries--
        setTimeout(executor,2000)
    }
}
executor()
