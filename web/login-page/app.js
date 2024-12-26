const express = require("express");
const cookieParser = require("cookie-parser");

const app = express();

// Use cookie parser middleware
app.use(cookieParser());

// Serve the main HTML page
app.get("/", (req, res) => {
  res.status(404).send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Login Page</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100vh;
          margin: 0;
          background-color: #f0f0f0;
        }
        h1 {
          margin-bottom: 20px;
        }
        form {
          display: flex;
          flex-direction: column;
          width: 300px;
        }
        label {
          margin-bottom: 5px;
          font-weight: bold;
        }
        input {
          margin-bottom: 15px;
          padding: 8px;
          font-size: 16px;
          border: 1px solid #ccc;
          border-radius: 4px;
        }
        button {
          padding: 10px;
          font-size: 16px;
          background-color: #007bff;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }
        button:hover {
          background-color: #0056b3;
        }
      </style>
      <script>
        window.onload = async function() {
          try {
            const profileId = Math.floor(Math.random() * 10) + 1; // Random profile ID from 1 to 10
            const response = await fetch('/github/main/' + profileId);
            const data = await response.json();
            console.log('Profile:', data.profile);
          } catch (error) {
            console.error('Error fetching the profile:', error);
          }
        };
      </script>
    </head>
    <body>
      <h1>Login Page</h1>
      <form action="/login" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <button type="submit">Login</button>
      </form>
    </body>
    </html>
  `);
});

app.post("/login", (req, res) => {
    // In a real application, validate credentials here
    res.send("Login successful!");
  });

// Handle the /profile/main/15 route
app.get("/github/main/15", (req, res) => {
  const profileId = req.params.id;
  const profile = { id: profileId, flag: 'aS1DRVN7eW9VOF8kM0NSRTdfRjFANl8xNV9IM3IzfQ==' };
  res.cookie('profile', JSON.stringify(profile), { httpOnly: true });
  res.status(200).json({ profile });
});

// Handle other /profile/main/:id routes
app.get("/github/main/:id", (req, res) => {
    const profileId = req.params.id;
    const messages = [
        "Keep going, you're almost there!",
        "Oops, not the right one, try again!",
        "You're doing great, but not this time.",
        "Almost there! Give it another flip.",
        "Nice effort! Better luck next time.",
        "You're closer than before, keep pushing!",
        "Almost had it! Give it one more shot.",
        "Stay positive, you'll get it next time.",
        "Nice try, don't be discouraged!",
        "You're on the right path, keep going!",
        "So close! Just a little tweak might do it.",
        "You're doing fantastic, just a bit more!",
        "Almost there! One more step to success.",
        "Keep working at it, success is near.",
        "Great attempt! Don't stop now!",
        "You've got this, don't lose hope.",
        "So close! A bit more effort will get you there.",
        "You're doing better, stay consistent!",
        "Nearly there! Focus and try again.",
        "Keep pushing! Victory is just ahead.",
        "Excellent effort! You're getting closer.",
        "Almost nailed it! Keep at it.",
        "You're doing better, don't give up!",
        "Stay focused, you're almost there!",
        "Almost perfect! One more time, you can do it.",
        "Fantastic attempt! The next one will be it."
      ];      
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    res.status(200).send(`
       <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Flip Game</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100vh;
          margin: 0;
          background-color: #f0f0f0;
        }
        h1 {
          margin-bottom: 20px;
        }
        .card-container {
          display: grid;
          grid-template-columns: repeat(4, 100px);
          gap: 10px;
        }
        .card {
          width: 100px;
          height: 150px;
          background-color: #0066cc;
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 10px;
          cursor: pointer;
          perspective: 1000px;
          position: relative;
        }
        .card.flip {
          transform: rotateY(180deg);
        }
        .card-inner {
          position: relative;
          width: 100%;
          height: 100%;
          transform: rotateY(180deg);
          transition: transform 0.6s;
        }
        .card .front, .card .back {
          position: absolute;
          width: 100%;
          height: 100%;
          backface-visibility: hidden;
        }
        .card .front {
          background-color: #0066cc;
          color: white;
        }
        .card .back {
          background-color: #f0f0f0;
          color: black;
          transform: rotateY(180deg);
        }
        .message {
          display: none;
          position: absolute;
          bottom: 10px;
          width: 100%;
          text-align: center;
          color: white;
        }
        .card.flip .message {
          display: block;
        }
      </style>
    </head>
    <script>
        window.onload = async function() {
          try {
            const profileId = Math.floor(Math.random() * 10) + 1; // Random profile ID from 1 to 10
            const response = await fetch('/profile/main/' + profileId);
            const data = await response.json();
            console.log('Profile:', data.profile);
          } catch (error) {
            console.error('Error fetching the profile:', error);
          }
        };
      </script>
    <body>
      <h1>Flip Cards Game</h1>
      <div class="card-container">
        ${Array.from({ length: 16 }).map((_, index) => `
          <div class="card" onclick="this.classList.toggle('flip'); setTimeout(() => this.classList.remove('flip'), 2000)">
            <div class="card-inner">
              <div class="front">${index + 1}</div>
              <div class="back">Try Again!</div>
              <div class="message">${messages[Math.floor(Math.random() * messages.length)]}</div>
            </div>
          </div>
        `).join('')}
      </div>
    </body>
    </html>
    `);
  });


// Catch-all for undefined routes
app.use((req, res) => {
  res.status(404).send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>404 - Not Found</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100vh;
          margin: 0;
          background-color: #ffefef;
        }
        h1 {
          color: #ff4d4d;
        }
        p {
          color: #ff9999;
        }
      </style>
    </head>
    <body>
      <h1>404 - Page Not Found</h1>
      <p>The page you are looking for does not exist.</p>
    </body>
    </html>
  `);
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});
