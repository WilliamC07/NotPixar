import {drawFromPpm} from './draw-from-ppm.js'; 
const imagesData = JSON.parse(images);
// console.log(images)
console.log(imagesData);
// const c = document.getElementById('preview-1');
// ctx = c.getContext('2d');
imagesData.map((imageObject, i) => {
    const container = document.getElementById(`image-container-${i}`);
    container.addEventListener('click', () => {
        window.location.replace("/view-art/" + imageObject.art_id);
    })

    const size = imageObject.image.match(/\S+/g)[1];
    console.log(size);
    const scale = Math.round(250 / size);
    console.log(scale);
    drawFromPpm(scale, imageObject.image, `preview-${i}`);

});

