class World  {
    constructor(worldData, players){
        this.tileSize = 50;
        this.playerSpriteSize = 30;

        this.fieldTypes = worldData.field_types;
        this.map = [];
        this.createFields(worldData.size);
        this.paintFields(worldData.map);

        this.players = {};
        this.createPlayers(players);
        this.updatePlayers(players, true);
    }

    createFields(size){
        // get and clear map container
        let mapContainerDiv = document.getElementById('map-container');
        //mapContainerDiv.style.position = 'relative';
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
            mapContainerDiv.insertBefore(player.sprite, mapContainerDiv.firstChild);
            // change its appearance
            player.sprite.style.height = this.playerSpriteSize + 'px';
            player.sprite.style.width = this.playerSpriteSize + 'px';
            player.sprite.style.background = 'yellow';
            player.sprite.textContent = player['name'];
            // and set positioning
            player.sprite.style.display = 'inline-block';
            player.sprite.style.position = 'absolute';
            // save whole player object
            this.players[player['name']] = player;
        }
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
                    player.sprite.style.left = pos[0] + 'px';
                    player.sprite.style.top = pos[1] + 'px';
                }
            }
        }
    }

    getPlayerCoordinates(position){
        let rect = this.map[position[0]][position[1]].getBoundingClientRect();
        return [window.scrollX + rect.left, window.scrollY + rect.top];
    }
}
