document.addEventListener("DOMContentLoaded", ()=> {

    const bugs = document.querySelectorAll("#bug-container img");

    bugs.forEach((bug) => {
        bug.onclick = function(){
            bug.src = "bug-whacked.png";
            bug.classList.add("whacked");

        }
    });
});