import {drawFromPpm} from './draw-from-ppm.js'; 
const imagesData = JSON.parse(images);
// console.log(images)
console.log(imagesData);
// const c = document.getElementById('preview-1');
// ctx = c.getContext('2d');
imagesData.map((imageObject, i) => {
    const container = document.getElementById(`image-container-${i}`);
    const likeButton = document.getElementById(`like-button-${i}`);
    const likeCounter = document.getElementById(`num-likes-${i}`);
    container.addEventListener('click', () => {
        window.location.replace("/view-art/" + imageObject.art_id);
    });
    if(imageObject.hasLiked){
        likeButton.classList.remove('btn-outline-danger');
        likeButton.classList.add('btn-danger');
    }

    likeButton.addEventListener('click', () => {
        if(likeButton.classList.contains('btn-outline-danger')){
            likeButton.classList.remove('btn-outline-danger');
            likeButton.classList.add('btn-danger');
            likeCounter.innerHTML = parseInt(likeCounter.innerHTML) + 1;
        } else {
            likeButton.classList.remove('btn-danger');
            likeButton.classList.add('btn-outline-danger');
            likeCounter.innerHTML = parseInt(likeCounter.innerHTML) - 1;
        };
        fetch(`/api/${imageObject.art_id}/like`, {
            method: "POST",
        }).then(res => {
            console.log(res);
            if(res.redirected === true){
                window.location.replace(res.url);
            };

        });        
    });

    const size = imageObject.image.match(/\S+/g)[1];
    console.log(size);
    const scale = Math.round(250 / size);
    console.log(scale);
    drawFromPpm(scale, imageObject.image, `preview-${i}`);
});


