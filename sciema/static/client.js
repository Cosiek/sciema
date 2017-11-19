(function () {
    var states = {'waiting': 'waiting', 'game_on': 'game_on',
                  'finished': 'finished',}
    var game = {}
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
        game.name = data.game
        game.player = data.player
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
            game.name = data.game
            game.player = data.player  // note - this requires validation from server!
            ws.send(JSON.stringify(data));
        })
    }

    var startButton = document.getElementById('start-play');
    startButton.addEventListener('click', function(){
        data = {
            'action': 'run_game',
            'game': game.name,
            'player': game.player
        };
        ws.send(JSON.stringify(data));
    });

    var endGameButton = document.getElementById('end-game');
    endGameButton.addEventListener('click', function(){
        ws.send(JSON.stringify({
            'action': 'end-game',
            'game': game.name,
            'player': game.player
        }));
    })

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

        // waiting for players
        if (gdt.state == states.waiting){
            document.getElementById('form').style.display = 'none';
            document.getElementById('waiting').style.display = 'block';
            document.getElementById('game-canvas').style.display = 'none';
            document.getElementById('finished').style.display = 'none';

            gameTitlesE = document.getElementsByClassName('js-game-name');
            for (gte of gameTitlesE){
                gte.innerHTML = gdt.name;
            }

            playersListE = document.getElementsByClassName('js-players-list');
            for (ple of playersListE){
                while (ple.firstChild) {
                    ple.removeChild(ple.firstChild);
                }
                for (playerDct of gdt.players){
                    li = document.createElement("li");
                    li.innerHTML = playerDct.name;
                    if (playerDct.name == gdt.owner){
                        li.innerHTML += ' (owner)'
                    }
                    ple.appendChild(li);
                }
            }
        }
        // game finished (for one reason or another)
        else if (gdt.state == states.finished){
            document.getElementById('form').style.display = 'none';
            document.getElementById('waiting').style.display = 'none';
            document.getElementById('game-canvas').style.display = 'none';
            document.getElementById('finished').style.display = 'block';

            winnerName = document.getElementById('winner-name');
            winnerName.innerHTML = gdt.winner;
        }
        else if (gdt.state == states.game_on){
            document.getElementById('form').style.display = 'none';
            document.getElementById('waiting').style.display = 'none';
            document.getElementById('game-canvas').style.display = 'block';
            document.getElementById('finished').style.display = 'none';

            game.world = new World(gdt.world, gdt.players);
        }
    };
})();
