const pokemonUrl = "https://pokeapi.co/api/v2/pokemon/gengar";

/*
fetch(pokemonUrl)
.then(response => response.json())
.then(data => {
console.log(data.name);
console.log(data.height);
console.log(data.weight);
data.types.forEach(type => {
console.log(type.type.name);
});
})
.catch(error => {
console.error("Error fetching Pokemon data:", error);
});
*/

async function fetchPokemon() {
  try {
    const response = await fetch(pokemonUrl);
    const data = await response.json();

    console.log(data.name);
    console.log(data.height);
    console.log(data.weight);
    data.types.forEach(type => {
      console.log(type.type.name);
    });
  } catch (error) {
    console.error("Error fetching Pokemon data:", error);
  }
}

loadPokemon();

