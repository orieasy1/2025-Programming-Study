const fs = require('fs');

function writeFile() {
    fs.writeFile('hola.txt', 'Hola mundo', (err) => {
        if (err) {
            console.log(`Error: ${err}`);
        } else {
            console.log('File successfully written!');
        }
    });
}

function readFile() {
    fs.readFile('hola.txt', 'utf8', (err, contents) => {
        if (err) {
            console.log(`Error: ${err}`);
        } else {
            console.log(contents);
        }
    });
}

function readFilePromises() {
    let contents = fs.promises.readFile('hola.txt', 'utf8');
    contents
        .then(console.log)
        .then(() => { console.log('Done reading file!'); })
        .catch(err => console.log(`Error: ${err}`));
}

async function readFileAsynAwait() {
    try {
        let contents = await fs.promises.readFile('hola.txt', 'utf8');
        console.log(contents);
        console.log('Done reading file!');
    }
    catch (err) {
        console.log(`Error: ${err}`)
    }
}

// Read JSON file and return parsed object
async function readJSON(filePath) {
    const data = await fs.promises.readFile(filePath, 'utf8');
    return JSON.parse(data);
}

// Write object to JSON file
async function writeJSON(filePath, jsonObject) {
    const data = JSON.stringify(jsonObject);
    await fs.promises.writeFile(filePath, data);
}

// writeFile();
// readFile();
// readFilePromises();

module.exports = {
    readFile,
    readJSON,
    writeJSON
}