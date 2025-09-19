const fs = require('fs');

function writeFile() {
    // hola.txt 파일에 'Hola mundo'라는 문자열을 작성
    // 콜백기반
    fs.writeFile('hola.txt', 'Hola mundo', (err) => {
        if (err) {
            console.log(`Error: ${err}`);
        } else {
            console.log('File successfully written!');
        }
    });
}

function readFile() {
    // hola.txt 파일을 읽고 내용을 콘솔에 출력
    // 콜백기반
    fs.readFile('hola.txt', 'utf8', (err, contents) => {
        if (err) {
            console.log(`Error: ${err}`);
        } else {
            console.log(contents);
        }
    });
}

function readFilePromises() {
    // hola.txt 파일을 읽고 내용을 콘솔에 출력
    // Promise 기반 즉 promise 객체를 반호나함
    // then()으로 읽은 내용을 받고 catch()로 에러를 처리

    // fs.promises.readFile()는 Promise 객체를 반환하고 그 객체를 contents 변수에 저장
    let contents = fs.promises.readFile('hola.txt', 'utf8');
    contents
        .then(console.log) // 읽은 파일 내용이 콘솔에 출력됨
        .then(() => { console.log('Done reading file!'); }) // 파일 읽기가 완료되면 메시지를 출력
        .catch(err => console.log(`Error: ${err}`)); // 에러가 발생하면 catch 블록에서 처리됨
}

// then().catch() 체인 보다 가독성이 뛰어남
// 동기 코드처럼 자연스럽게 작서할 수 있어 유지보수에 유리
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