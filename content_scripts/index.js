(function connectSock() {
  const s = new WebSocket("wss://localhost:9876");
  s.onopen = e => {
    console.log("no more wait")
    console.log(`opened ${e}`);
  };
  // s.onclose = function(e) { alert("closed");console.log(e) }
  s.onmessage = e => {
    console.log(`got: ${e.data}`);
    window.wrappedJSObject.ACTIVE_CODEMIRROR.setValue(e.data);
  };
})();
