var FILL_COLOR = '#000000';
var FILL_RGB_ARRAY = [0, 0, 0];
var data = [];
const initData = () => {
    data = [];
    for (let i = 0; i < 25; i++){
        let row = []
        for (let j = 0; j < 25; j++){
            row.push([255, 255, 255]);
        };
        data.push(row);
    };
};
initData();
console.log(data);
const c = document.getElementById('artCanvas');
document.getElementById('color-red').addEventListener('click', () => {FILL_COLOR = '#ff0000'; setColorIndicator();});
document.getElementById('color-green').addEventListener('click', () => {FILL_COLOR = '#00ff00'; setColorIndicator();});
document.getElementById('color-blue').addEventListener('click', () => {FILL_COLOR = '#0000ff'; setColorIndicator();});
document.getElementById('color-white').addEventListener('click', () => {FILL_COLOR = '#ffffff'; setColorIndicator();});
document.getElementById('color-black').addEventListener('click', () => {FILL_COLOR = '#000000'; setColorIndicator();});
document.getElementById('clear-canvas').addEventListener('click', () => {
    c.getContext('2d').clearRect(0, 0, c.width, c.height);
    initData();
    console.log(data);
    drawGrid(c);
});
document.getElementById('draw').addEventListener('click', () => {
    drawFromData(data ,c);
});

var setColorIndicator = () => {
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

var drawGrid = (canvasElement) => {
    var canvasContext = canvasElement.getContext('2d');
    for (i = 0; i < 700; i += 25) {
        canvasContext.moveTo(0, i);
        canvasContext.lineTo(c.width, i);
        canvasContext.stroke();
    };
    for (i = 0; i < 700; i += 25) {
        canvasContext.moveTo(i, 0);
        canvasContext.lineTo(i,c.width);
        canvasContext.stroke();
    };
};


var startDrawing = (canvasElement) => {
    var getMousePosition = (canvas, event) => { 
        let rect = canvas.getBoundingClientRect(); 
        let x = Math.floor((event.clientX - rect.left) / 25); 
        let y = Math.floor((event.clientY - rect.top) / 25); 
        console.log("Coordinate x: " + x,  
                    "Coordinate y: " + y); 
        return [x, y];
    };
    var fillPixel = (coordinatesArray) => {
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
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
};  
function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
};

var drawFromData = (dataParam, canvasElement) => {
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
drawGrid(c);
startDrawing(c);
