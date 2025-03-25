
document.addEventListener("DOMContentLoaded", ()=> {

    //better code
    document.querySelectorAll("button").forEach(function(button){
        button.onclick = function(){
            let h1 = document.querySelector("h1");
            h1.style.color= button.id;
        }
    })

    // bad code implementatiom
    /*
    let btn_red = document.querySelector("#red");
    let btn_blue = document.querySelector("#blue");
    let btn_green = document.querySelector("#green");

    btn_red.addEventListener("click",function(){
        let h1 = document.querySelector("h1");
        h1.style.color ="red";
    });

    btn_blue.addEventListener("click",function(){
        let h1 = document.querySelector("h1");
        h1.style.color ="blue";
    });

    btn_.addEventListener("click",function(){
        let h1 = document.querySelector("h1");
        h1.style.color ="green";
    });
    */
});