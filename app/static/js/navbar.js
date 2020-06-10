document.getElementById("username-search-btn").addEventListener("click", (e) => {
    e.preventDefault();
    window.location.href = "/profile/" + document.getElementById("username-input-field").value;
});