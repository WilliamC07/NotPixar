export function drawFromPpm (scale, ppmString, canvasId){
    const ppmArray = ppmString.match(/\S+/g);
    const squareSize = ppmArray[1];
    ppmArray.splice(0, 4);
    // ppmArray.map((num) => {
    //     const toReturn = parseInt(num);
    //     console.log(toReturn);
    //     return toReturn;
    // });

    console.log(ppmArray);
    const rgbClusters = segmentArray(ppmArray, 3);
    const finalArray = segmentArray(rgbClusters, squareSize);
    console.log(finalArray);

    drawFromData(finalArray, scale, 'view-canvas')

};

// Helper Functions
const segmentArray = (array, subArraySize) => {
    let toReturn = [];
    let cluster = [];
    let counter = 0;
    array.map((dataPoint) => {
        cluster.push(dataPoint);
        if(counter === (subArraySize - 1)){
            toReturn.push(cluster);
            cluster = [];
            counter = 0;
        } else {
            counter ++;
        };
    });
    return toReturn;
};

function componentToHex(c) {
    const hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
};  
function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
};

function RGBToHex(r,g,b) {
    r = r.toString(16);
    g = g.toString(16);
    b = b.toString(16);
  
    if (r.length == 1)
      r = "0" + r;
    if (g.length == 1)
      g = "0" + g;
    if (b.length == 1)
      b = "0" + b;
  
    return "#" + r + g + b;
  };

const drawFromData = (dataParam, scale, canvasId) => {
    document.getElementById(canvasId).style.border = '1px solid black';
    console.log(dataParam);
    dataParam.map((row, i) => {
        row.map((col, j) => {
            const context = document.getElementById(canvasId).getContext('2d');
            const topLeftPoint = [(j * scale), 
                                    (i * scale)];
            // console.log(col[0], col[1], col[2]);
            // console.log(RGBToHex(col[0], col[1], col[2]));
            context.fillStyle = (RGBToHex(parseInt(col[0]), parseInt(col[1]), parseInt(col[2])));
            context.fillRect(topLeftPoint[0], topLeftPoint[1], scale, scale);     
        });
    });
};
