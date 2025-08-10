fetch('https://pokeapi.co/api/v2/pokemon/gengar')
  .then(response => response.json())
  .then(json => console.log(json))
  .catch(error => console.log(error));

async function myFetch(url) {
    try {
        let response = await fetch(url);
        let jsonFile = await response.json();
        console.log(jsonFile);
    }
    catch (e) {
        console.log(e);
    }

}

myFetch('https://pokeapi.co/api/v2/pokemon/pikachu')

function setTimeoutPromise(time) {
    function executorFunction(resolve, reject) {
        setTimeout(function () {
            resolve();
        }, time);
    }

    return new Promise(executorFunction);
}

console.log('Before setTimeoutPromise');
setTimeoutPromise(5000).then(function () {
    console.log('five second later');
});
console.log('After setTimeoutPromise');