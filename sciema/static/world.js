class World  {
    constructor(worldData){
        this.tileSize = 50;

        this.fieldTypes = worldData.field_types;
        this.map = [];
        this.createFields(worldData.size);
        this.paintFields(worldData.map);
    }

    createFields(size){
        // get and clear map container
        var mapContainerDiv = document.getElementById('map-container');
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
}
