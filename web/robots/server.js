const express = require('express');
const path = require('path');

const app = express();

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Define routes for each HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/login.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'login.html'));
});

app.get('/signup.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'signup.html'));
});

app.get('/sytle.css', (req, res) => {
    res.sendFile(path.join(__dirname, 'styles.css'));
});

app.get('/robots.txt', (req, res) => {
    res.sendFile(path.join(__dirname, 'robots.txt'));
});

app.get('/nothere.html', (req, res) => {
    res.setHeader('X-Flag', 'i-CES{CH4ll3N63_8y_0xz3r08y73}');
    res.setHeader('X-content-type-option', '127.0.0.1');
    res.setHeader('X-Content-Encoding', '64KouIWDAwiqT3fJ3QOSHK05GeEIPlqfD30iLlzJ9zrYXS6mFTxjjhDxGSyofzEpinuQj2apyUr759OUv5tEX0ap0Ck8oUs/F2KfMimJj74=');
    res.setHeader('Arthur', '0xz3r08y73');
    res.sendFile(path.join(__dirname, 'nothere.html'));
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
