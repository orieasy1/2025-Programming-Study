
let whackedBugs = 0;
document.addEventListener("DOMContentLoaded", function(){    
    const bugs = document.querySelectorAll("#bug-container img");
    const score = document.getElementById("score");
    bugs.forEach((bug)=>{
        bug.addEventListener("click", ()=>{            
            //if (bug.className !== 'whacked') {                
            if (!bug.classList.contains("whacked")){
                bug.src= "bug-whacked.png";
                //bug.className= 'whacked';
                bug.classList.add('whacked');
                whackedBugs++;                
                console.log(score);
                if (whackedBugs < bugs.length){
                    score.textContent = whackedBugs;
                }else{
                    this.querySelector("#game p").textContent = "All bugs have been whacked!";
                }
                
            }
        });
    });

});