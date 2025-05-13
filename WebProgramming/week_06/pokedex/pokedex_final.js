document.addEventListener("DOMContentLoaded", () => {
    const btnFetch = qs("button");
    btnFetch.onclick = fetchPokemon;
});

/**
 * Fetches Pokémon data and 
 */
async function fetchPokemon() {
    let name = id("pokemon-name").value.toLowerCase().trim();
    if (name === "") {
        alert("Enter a Pokémon name.");
        return;
    }

    try {
        let response = await fetch(`https://pokeapi.co/api/v2/pokemon/${name}`);
        await statusCheck(response)
        response = await response.json();
        addPokemonToPokedex(response)
    } catch (err) {
        console.log(err);
        alert("Could not find that Pokémon.");
    }
}

/**
 * adds a card to the DOM
 */
async function addPokemonToPokedex(pokemonData) {
    const card = createPokemonCard(pokemonData);
    id("pokedex").appendChild(card);
    id("pokemon-name").value = ""; // clear input
    checkNumDisplayed();
    return pokemonData;
}

/**
 * check the status of the response from fetch
 */
async function statusCheck(res) {
    if (!res.ok) {
        throw new Error(await res.text());
    }
    return res;
}

/**
 * Creates and returns a Pokémon card element
 */
function createPokemonCard(data) {
    let card = document.createElement("article");
    let title = document.createElement("h1");
    let content = document.createElement("p");
    let img = document.createElement("img");

    // Set content
    title.textContent = "Name: " + data.name;
    content.textContent = `Height: ${data.height} | Weight: ${data.weight} | Types: ${data.types.map(t => t.type.name).join(", ")}`;
    img.src = data.sprites.front_default;
    img.alt = data.name;
    img.width = 100;

    // Build card
    card.appendChild(img);
    card.appendChild(title);
    card.appendChild(content);

    // Style and behavior
    card.classList.add("pokemon-card");
    card.addEventListener("dblclick", removePokemon);

    return card;
}

/**
 * Removes selected Pokémon card
 */
function removePokemon() {
    this.remove(); // "this" refers to the article element
    checkNumDisplayed();
}

/**
 * Limits to 4 Pokémon, disables input & button if needed
 */
function checkNumDisplayed() {
    let cards = qsa(".pokemon-card");
    let num = cards.length;
    let button = qs("button");
    let input = id("pokemon-name");

    if (num >= 4) {
        button.disabled = true;
        input.disabled = true;
    } else {
        button.disabled = false;
        input.disabled = false;
    }
}

/**
 * Helper functions
 */
function id(id) {
    return document.getElementById(id);
}

function qs(selector) {
    return document.querySelector(selector);
}

function qsa(query) {
    return document.querySelectorAll(query);
}
