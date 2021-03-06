class World  {
    constructor(worldData, players, currentPlayerName){
        this.tileSize = 50;
        this.spriteSize = 24;

        this.fieldTypes = worldData.field_types;
        this.map = [];
        this.createFields(worldData.size);
        this.paintFields(worldData.map);

        this.players = {};
        this.createPlayers(players);
        this.currentPlayer = this.players[currentPlayerName]
        this.updatePlayers(players, true);

    }

    update(worldData, players){
        this.paintFields(worldData.map);
        this.updatePlayers(players);
    }

    createFields(size){
        // get and clear map container
        let mapContainerDiv = document.getElementById('map-container');
        while (mapContainerDiv.firstChild) {
            mapContainerDiv.removeChild(mapContainerDiv.firstChild);
        }
        mapContainerDiv.style.width = '' + this.tileSize * size[0] + 'px';
        // make sure map is empty
        this.map = [];
        // add fields to container and underlying data array
        let y = size[1];
        while (y > 0){
            let row = [];
            let x = size[0];
            while (x > 0){
                let field = document.createElement('div');
                field.style.width = this.tileSize + 'px';
                field.style.height = this.tileSize + 'px';
                field.style.display = 'inline-block';
                row.push(field);
                mapContainerDiv.appendChild(field);
                x -= 1;
            }
            this.map.push(row)
            y -= 1;
        }
    }

    paintFields(map){
        let y = 0;
        while (y < map.length){
            let dataRow = map[y];
            let elemRow = this.map[y];
            let x = 0;
            while (x < dataRow.length){
                let dataField = dataRow[x];
                let elemField = elemRow[x];
                let fieldType = this.fieldTypes[dataField];
                // apply style
                elemField.textContent = dataField;
                let color = 'rgb(' + fieldType.color[0] + ',' + fieldType.color[1] + ',' + fieldType.color[2] + ', 1)';
                elemField.style.background = color;
                x += 1;
            }
            y += 1;
        }
    }

    createPlayers(players){
        let mapContainerDiv = document.getElementById('map-container');
        for (let player of players){
            // crate sprite
            player.sprite = document.createElement('div');
            player.sprite.classList.add('player-sprite');
            mapContainerDiv.insertBefore(player.sprite, mapContainerDiv.firstChild);
            // change its appearance
            player.sprite.style.height = this.spriteSize + 'px';
            player.sprite.style.width = this.spriteSize + 'px';
            player.sprite.style.display = 'table-cell';
            player.sprite.style['vertical-align'] = 'middle';
            player.sprite.style['text-align'] = 'center';
            this.setPlayerLook(player, player['look'])
            // and set positioning
            player.sprite.style.display = 'inline-block';
            player.sprite.style.position = 'absolute';
            // save whole player object
            this.players[player['name']] = player;
        }
    }

    setPlayerLook(player, look){
        // change its appearance
        player.sprite.textContent = look['icon'];
        let color = look['color']
        let rgb = 'rgb(' + color[0] + ',' + color[1] + ',' + color[2] + ')'
        player.sprite.style.color = rgb;
        rgb = 'rgb(' + (255 - color[0]) + ',' + (255 - color[1]) + ',' + (255 - color[2]) + ')'
        player.sprite.style.background = rgb;
    }

    updatePlayers(players, forceReposition){
        for (let player of players){
            let curr = this.players[player['name']]
            for (let attr in player){
                if (forceReposition || (attr == 'position'
                        && (curr.position[0] != player.position[0]
                           || curr.position[1] != player.position[1]))){
                    // calculate new position
                    let pos = this.getPlayerCoordinates(player.position)
                    curr.sprite.style.left = pos[0] + 'px';
                    curr.sprite.style.top = pos[1] + 'px';
                } else if ( attr == 'look' ){
                    this.setPlayerLook(curr, player['look'])
                }
                curr[attr] = player[attr];
                if (player.connected === false){
                    for (li of document.getElementsByClassName("player-" + player.name)){
                        li.style.textDecoration = 'line-through';
                    }
                }
            }
        }
        // center map on current player
        let x = this.currentPlayer.sprite.style.left.replace('px', '');
        let y = this.currentPlayer.sprite.style.top.replace('px', '');
        x = Number(x) - screen.availWidth / 2;
        y = Number(y) - screen.availHeight / 2;
        window.scroll({top: y, left: x, behavior: 'smooth'});
    }

    getPlayerCoordinates(position){
        let rect = this.map[position[0]][position[1]].getBoundingClientRect();
        let off = this.tileSize / 2 - this.spriteSize / 2
        let left = window.scrollX + rect.left + off;
        let right = window.scrollY + rect.top + off;
        return [left, right];
    }
}
