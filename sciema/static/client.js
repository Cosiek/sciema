(function () {
    var ws = new WebSocket('ws://127.0.0.1:8888/websocket');

    ws.onopen = function(){console.log('Halo serwer!');};
    ws.onmessage = function(event){console.log(event.data);};

    var send = document.getElementById('send');
    send.addEventListener('click', function () {
        ws.send("Hej!")
    });
})();
