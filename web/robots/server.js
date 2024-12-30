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
    res.setHeader('X-Link-to-next', 'ip/secret.php');
    res.setHeader('X-Next-Challenge', 'allowed_command{mJpRi4NkBdbjtAIqsULI8QkQ0z9T2XsXlLtUQSgRTQsjuIOL2OrFyzljdfNVEvI9ADgaM4EWB1srAvxcFuqMbg==}');
    res.sendFile(path.join(__dirname, 'nothere.html'));
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
