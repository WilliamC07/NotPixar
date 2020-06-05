let FILL_COLOR = '#000000';
let FILL_RGB_ARRAY = [0, 0, 0];
let ARTWORK_TITLE = "";
let GRID_SIZE = 25;
let data = [];
const initData = () => {
    data = [];
    for (let i = 0; i < GRID_SIZE; i++){
        let row = []
        for (let j = 0; j < GRID_SIZE; j++){
            row.push([255, 255, 255]);
        };
        data.push(row);
    };
};
initData();
console.log(data);
const c = document.getElementById('artCanvas');

const setColorIndicator = () => {
    function hexToRgb(hex) {
        var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? [
            parseInt(result[1], 16),
            parseInt(result[2], 16),
            parseInt(result[3], 16)
        ] : null;
    }
    FILL_RGB_ARRAY = hexToRgb(FILL_COLOR);
    // console.log(FILL_RGB_ARRAY);
    document.getElementById('color-indicator').style.backgroundColor = FILL_COLOR;
};

const drawGrid = (canvasElement) => {
    initData();
    console.log(data);
    canvasElement.width = 25 * GRID_SIZE;
    canvasElement.height = 25 * GRID_SIZE;
    var canvasContext = canvasElement.getContext('2d');
    canvasContext.clearRect(0, 0, c.width, c.height);
    for (i = 0; i < (GRID_SIZE * 25 + 2); i += 25) {
        canvasContext.moveTo(0, i);
        canvasContext.lineTo(c.width, i);
        canvasContext.stroke();
    };
    for (i = 0; i < (GRID_SIZE * 25 + 2); i += 25) {
        canvasContext.moveTo(i, 0);
        canvasContext.lineTo(i,c.width);
        canvasContext.stroke();
    };
};


const startDrawing = (canvasElement) => {
    const getMousePosition = (canvas, event) => { 
        let rect = canvas.getBoundingClientRect(); 
        let x = Math.floor((event.clientX - rect.left) / 25); 
        let y = Math.floor((event.clientY - rect.top) / 25); 
        console.log("Coordinate x: " + x,  
                    "Coordinate y: " + y); 
        return [x, y];
    };
    const fillPixel = (coordinatesArray) => {
        // setting the pixel in the data
        data[coordinatesArray[1]][coordinatesArray[0]] = FILL_RGB_ARRAY;
        console.log(data);
        const context = canvasElement.getContext('2d');
        const topLeftPoint = [(coordinatesArray[0] * 25 + 1), 
                                (coordinatesArray[1] * 25 + 1)];
        context.fillStyle = FILL_COLOR;
        context.fillRect(topLeftPoint[0], topLeftPoint[1], 23, 23);
    };
    canvasElement.addEventListener('click', (e) => {
        fillPixel(getMousePosition(canvasElement, e));
    });
};


function componentToHex(c) {
    const hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
};  
function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
};

const submit = () => {
    let requestString = `P3 ${GRID_SIZE} ${GRID_SIZE} 255`;
    console.log(data);
    data.map((row) => {
        row.map((col) => {
            col.map((rgbValue) => {
                requestString = requestString.concat(` ${rgbValue}`);
            });
        });
    });
    // console.log(requestString);
    if(ARTWORK_TITLE !== ""){
        const requestBody = {
            title: ARTWORK_TITLE,
            image: requestString
        };
        console.log(requestBody);
        fetch('/api/image/create', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        }).then(res => {
            console.log(res);
            if(res.ok){
               return res.json();
            }
        }).then(artId => {
            console.log(artId.id);
            // Simulate an HTTP redirect:
            window.location.replace("/view-art/" + artId.id);
        });
    } else {
        const title = document.getElementById('title');
        const alert = document.getElementById('js-alert');
        title.style.border = "1px solid red";
        title.placeholder = "Please enter a title";
        alert.innerHTML = "Please enter a title";
        alert.style.display = "block";

        window.scrollTo(0, 0);
    };
};
const drawFromData = (dataParam, canvasElement) => {
    dataParam.map((row, i) => {
        row.map((col, j) => {
            const context = canvasElement.getContext('2d');
            const topLeftPoint = [(j * 25 + 1), 
                                    (i * 25 + 1)];
            context.fillStyle = (rgbToHex(col[0], col[1], col[2]));
            context.fillRect(topLeftPoint[0], topLeftPoint[1], 23, 23);     
        });
    });
};

document.getElementById('color-red').addEventListener('click', () => {FILL_COLOR = '#ff0000'; setColorIndicator();});
document.getElementById('color-green').addEventListener('click', () => {FILL_COLOR = '#00ff00'; setColorIndicator();});
document.getElementById('color-blue').addEventListener('click', () => {FILL_COLOR = '#0000ff'; setColorIndicator();});
document.getElementById('color-white').addEventListener('click', () => {FILL_COLOR = '#ffffff'; setColorIndicator();});
document.getElementById('color-black').addEventListener('click', () => {FILL_COLOR = '#000000'; setColorIndicator();});
document.getElementById('clear-canvas').addEventListener('click', () => {
    // initData();
    // console.log(data);
    drawGrid(c);
});
document.getElementById('submit').addEventListener('click', submit);
document.getElementById('title').addEventListener('change', e => {
    ARTWORK_TITLE = e.target.value;
});
document.getElementById('grid-size-select').addEventListener('change', e => {
    GRID_SIZE = e.target.value;
    drawGrid(c);
});

drawGrid(c);
startDrawing(c);
