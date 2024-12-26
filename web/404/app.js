const express = require('express');
const app = express();

// Middleware to handle 404 errors
app.use((req, res, next) => {
  const hiddenFlag = '<!-- FLAG: i-CES{404_Fa1lED_tO_TRIcK_y0U} -->';  // Hidden flag inside HTML comment
  const notFoundHtml = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>404 Not Found</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          text-align: center;
          padding: 50px;
        }
        h1 {
          font-size: 3rem;
        }
        p {
          font-size: 1.2rem;
          opacity:50;
        }
      </style>
    </head>
    <body>
      <h1>404 - Page Not Found</h1>
      <p>Sorry, the page you are looking for does not exist.</p>
      <p style="color: white;">!view page source/inspect!</p>
      ${hiddenFlag}
    </body>
    </html>
  `;

  res.status(404).send(notFoundHtml);
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
