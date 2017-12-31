(function () {
    var states = {'waiting': 'waiting', 'game_on': 'game_on',
                  'finished': 'finished', 'game_start': 'game_start'}
    var game = {'state': states.waiting, waitingForResponse: false}
    var ws = new WebSocket('ws://' + location.host + '/websocket');

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

    // bind arrow keys --------------------------------------------------------

    document.addEventListener('keypress', (event) => {
        action = {'ArrowUp': 'up', 'ArrowDown': 'down', 'ArrowLeft': 'left', 'ArrowRight': 'right'}[event.key];
        if (!action || game.state != states.game_on){return null}
        event.preventDefault();
        if (game.waitingForResponse){return null}
        dct = {'game': game.name, 'player': game.player, 'action': action}
        game.waitingForResponse = true;
        ws.send(JSON.stringify(dct));
    });


    // handle return messages -------------------------------------------------

    ws.onmessage = function(event){
        gdt = JSON.parse(event.data);
        console.log('server: ', gdt);

        // handling errors
        if (gdt.errors){
            for (err of gdt.errors){
                alert(err)
            }
        }

        // update game state
        if (gdt.state){game.state = gdt.state}

        // waiting for players
        if (gdt.state == states.waiting){
            document.getElementById('form').style.display = 'none';
            document.getElementById('waiting').style.display = 'block';
            document.getElementById('game-canvas').style.display = 'none';
            document.getElementById('finished').style.display = 'none';

            gameTitlesE = document.getElementsByClassName('js-game-name');
            for (gte of gameTitlesE){
                gte.textContent = gdt.name;
            }

            playersListE = document.getElementsByClassName('js-players-list');
            for (ple of playersListE){
                while (ple.firstChild) {
                    ple.removeChild(ple.firstChild);
                }
                for (playerDct of gdt.players){
                    li = document.createElement("li");
                    li.textContent = playerDct.name + ' ' + playerDct.look.icon;
                    if (playerDct.name == gdt.owner){
                        li.textContent += ' (owner)'
                    }
                    color = playerDct.look.color;
                    rgb = 'rgb(' + color[0] + ',' + color[1] + ',' + color[2] + ')';
                    li.style.color = rgb;
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

            winnerName = 'No winners here :(';
            for (ple of gdt.players){
                if (ple.is_winner) {winnerName = ple.name;break}
            }

            document.getElementById('winner-name').textContent = winnerName;
        }
        else if (gdt.state == states.game_start){
            document.getElementById('form').style.display = 'none';
            document.getElementById('waiting').style.display = 'none';
            document.getElementById('game-canvas').style.display = 'block';
            document.getElementById('finished').style.display = 'none';

            game.world = new World(gdt.world, gdt.players, game.player);
            game.state = states.game_on;
        }
        else if (gdt.state == states.game_on){
            if (gdt.action == 'move'){
                // remember current player position to check if he really moved
                var oldPosition = game.world.currentPlayer.position;
                // convert response to something i might feed to `updatePlayers`
                dt = [{'name': gdt.player, 'position': gdt.position}];
                // move his sprite
                game.world.updatePlayers(dt);
                if (gdt.player == game.world.currentPlayer.name){
                    currPosition = game.world.currentPlayer.position;
                    if (oldPosition[0] == currPosition[0] && oldPosition[1] == currPosition[1]){
                        // don't block player if move wasn't allowed
                        game.waitingForResponse = false;
                        return null;
                    }
                    // notify server, that this move is complete
                    game.waitingForResponse = true;
                    setTimeout(function(){
                        ws.send(JSON.stringify({'action': 'move-confirm',
                            'game': game.name, 'player': game.player
                        }));
                    }, 1000);
                }
            } else if (gdt.action == 'settle'){
                // update players
                game.world.update(gdt.world, gdt.players);
                // mark that this player can move again
                if (gdt.player == game.player){
                    game.waitingForResponse = false;
                }
            }
        }
    };
})();
