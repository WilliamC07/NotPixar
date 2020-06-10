import {drawFromPpm} from './draw-from-ppm.js'; 
console.log(ppmResponse);
console.log("hello");
let hasLikedLocal = hasLiked;
console.log(hasLikedLocal);

const size = ppmResponse.match(/\S+/g)[1];
console.log(size);
const scale = Math.round(625 / size);
console.log(scale);
drawFromPpm(scale, ppmResponse, "view-canvas");

const submit = () => {
    const id = window.location.pathname.split("/").pop();
    const input = document.getElementById("comment");

    if (input.value === ""){
        input.style.border = "1px solid red";
        input.placeholder = "Please enter a comment";
    } else {
        input.style.border = "1px solid green";
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
                input.value = "";
                setTimeout(() => {
                    alert.style.display = 'none';
                    alert.classList.remove('alert-success');
                    alert.innerHTML = "";
                }, 3000);
            } else {
                if (res.status == 403){
                    window.location.replace('/login')
                }
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
            const newComments = responseDoc.getElementById('comments-container');
            const commentsContainer = document.getElementById("comments-container");
            commentsContainer.parentNode.replaceChild(newComments, commentsContainer);
        });
    }
};

 
const id = window.location.pathname.split("/")[2];
const button = document.getElementById('like');
if (hasLikedLocal === "True"){
    button.classList.remove('btn-outline-danger');
    button.classList.add('btn-danger');
}
const counter = document.getElementById('likes-counter');
const like = () => {
    console.log(hasLikedLocal);
    if(hasLikedLocal === 'False'){
        button.classList.remove('btn-outline-danger');
        button.classList.add('btn-danger');
        counter.innerHTML = (parseInt(counter.innerHTML) + 1);
        hasLikedLocal = "True";
    } else {
        button.classList.remove('btn-danger');
        button.classList.add('btn-outline-danger');
        counter.innerHTML = (parseInt(counter.innerHTML) - 1);
        hasLikedLocal = "False";
    };
    fetch(`/api/${id}/like`, {
        method: "POST",
    }).then(res => {
        console.log(res);
    })
};

document.getElementById("comment").addEventListener("keyup", function(event) {
    console.log(event.keyCode);
    if (event.keyCode === 13) {
        submit();
    }
});
document.getElementById("submit").addEventListener('click', submit);
document.getElementById("like").addEventListener('click', like);
