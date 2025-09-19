const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const {readFile, readJSON, writeJSON} =require('./files');


const app = express();

app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

const PORT = 8000;

const books = [{
  "id":1,
  "title":"Lord of The Rings",
  "author":"JRR Tolkien"
}];

app.get('/api/books', function (req, res) {
  console.log("Endpoint /api/books received a GET request.");
  //res.type("text").send("Books app");
  res.json(books);
});

app.post('/api/books', (req, res) => {
  const { title, author } = req.body;
  if (!title || !author) {
    console.log("Error 400. Title and author required");
    return res.status(400).json({ error: 'Title and author required' });
  }
  const newBook = { id: books.length + 1, title, author };
  books.push(newBook); 
  console.log("Code 201. Book created successful");
  res.status(201).json(newBook); // HTTP 201 Created successful response status code
});

app.listen(PORT, () => {
    console.log(`Books app listening on port ${PORT}`);
});