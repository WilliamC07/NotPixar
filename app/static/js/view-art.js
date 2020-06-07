import {drawFromPpm} from './draw-from-ppm.js'; 
console.log(ppmResponse);
console.log("hello");

const size = ppmResponse.match(/\S+/g)[1];
console.log(size);
const scale = Math.round(625 / size);
console.log(scale);
drawFromPpm(scale, ppmResponse, "view-canvas");

document.getElementById("submit").addEventListener('click', () => {
    const id = window.location.pathname.split("/").pop();
    const input = document.getElementById("comment");
    const requestBody = {
        art_id: id,
        content: input.value
    };

    fetch('/api/comment/create', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
    }).then(res => {
        const alert = document.getElementById('comment-alert');
        console.log(res);
        if (res.ok) {
            // window.location.reload(true);
            alert.innerHTML = "Your comment has been shared.";
            alert.classList.add('alert-success');
            alert.style.display = 'block';
            setTimeout(() => {
                alert.style.display = 'none';
                alert.classList.remove('alert-success');
                alert.innerHTML = "";
            }, 3000);
        } else {
            alert.classList.remove('alert-success');
            alert.classList.add('alert-danger');
            alert.innerHTML = 'There has been an error';
            alert.style.display = 'block'
            setTimeout(() => {
                alert.style.display = 'none';
                alert.classList.remove('alert-danger');
                alert.innerHTML = "";
            }, 3000);
        }
        return fetch(`/view-art/${id}`);
    }).then(res => {
        console.log(res);
        return res.text();
    }).then(responseString => {
        console.log(responseString);
        const parser = new DOMParser();
        const responseDoc = parser.parseFromString(responseString, "text/html");
        const newComments = responseDoc.getElementById('comments-container').children;
        const commentsContainer = document.getElementById("comments-container");
        commentsContainer.appendChild(newComments[newComments.length-1])
    });


});
