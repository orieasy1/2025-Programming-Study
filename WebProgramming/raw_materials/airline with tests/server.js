const app = require('./app');

const PORT = 8080;

// Start Server 
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
