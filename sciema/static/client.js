(function () {
    var ws = new WebSocket('ws://127.0.0.1:8888/websocket');

    ws.onopen = function(){console.log('Halo serwer!')};

    // events binding ---------------------------------------------------------
    var send = document.getElementById('new-game-start');
    send.addEventListener('click', function () {
        playerName = document.getElementById('player-name');
        gameName = document.getElementById('new-game-name');
        data = {
            'action': 'new_game',
            'game': gameName.value,
            'player': playerName.value
        };
        ws.send(JSON.stringify(data));
    });

    var joinButtons = document.getElementsByClassName('js-join');
    for (joinButton of joinButtons){
        joinButton.addEventListener('click', function(){
            playerName = document.getElementById('player-name');
            data = {
                'action': 'join_game',
                'game': this.dataset.game,
                'player': playerName.value
            };
            ws.send(JSON.stringify(data));
        })
    }

    // handle return messages -------------------------------------------------

    ws.onmessage = function(event){
        gdt = JSON.parse(event.data);
        console.log(gdt);

        // handling errors
        if (gdt.errors){
            for (err of gdt.errors){
                alert(err)
            }
        }
    };
})();
