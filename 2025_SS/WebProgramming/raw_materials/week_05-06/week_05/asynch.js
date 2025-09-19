/* const doSomething = (cb) => {
    console.log('Doing something...');
    cb();
};

const nextStep = () => {
    console.log('Callback called');
    return "callback called";
};


doSomething(nextStep); */

//timers
document.addEventListener('DOMContentLoaded', init);
function init() {
    id("demo-btn").addEventListener("click", delayedMessage);
    repeatedMessage();
}

function delayedMessage() {
    id("output-text").textContent = "It's gonna be legend...wait for it...";
    setTimeout(sayHello, 5000);
}

function sayHello() { // called when the timer goes off
    id("output-text").textContent = "dary... Legendary!";
}

//intervals
let timerId = null; // stores ID of interval timer
function repeatedMessage() {
    timerId = setInterval(sayAnnyeong, 1000);
}

function sayAnnyeong() {
    id("timer-text").textContent += "안녕!";
}


//helper functions
function id(id) {
    return document.getElementById(id);
}

function qs(selector) {
    return document.querySelector(selector);
}

function qsa(selector) {
    return document.querySelectorAll(selector);
}