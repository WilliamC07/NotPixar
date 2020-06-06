import {drawFromPpm} from './draw-from-ppm.js'; 
console.log(ppmResponse);
console.log("hello");

const size = ppmResponse.match(/\S+/g)[1];
console.log(size);
const scale = Math.round(625 / size);
console.log(scale);
drawFromPpm(scale, ppmResponse, "view-canvas");

