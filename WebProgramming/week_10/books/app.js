const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();

app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

const PORT = 8080;

const books = [{
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald"
}, {
    "id": 2,
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee"
}, {
    "id": 3,
    "title": "1984",
    "author": "George Orwell"
}, {
    "id": 4,
    "title": "Pride and Prejudice",
    "author": "Jane Austen"
}, {
    "id": 5,
    "title": "The Catcher in the Rye",
    "author": "J.D. Salinger"
}, {
    "id": 6,
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien"
}, {
    "id": 7,
    "title": "Fahrenheit 451",
    "author": "Ray Bradbury"
}];

app.get('/api/books', function (req, res) {
    console.log('Endpoint /api/books received a GET request');
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
    console.log(`Server is running on http://localhost:${PORT}`);
});