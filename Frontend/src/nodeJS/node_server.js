// server.js
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();

app.get('/api/images', (req, res) => {
  const imagesFolder = path.join(__dirname, '../images');
  fs.readdir(imagesFolder, (err, files) => {
    if (err) {
      console.error('Error reading images folder:', err);
      res.status(500).json({ error: 'Internal Server Error' });
      return;
    }

    const imageUrls = files.map(file => `../images/${file}`);
    res.json({ images: imageUrls });
  });
});

app.listen(6000, () => {
  console.log('Server is running on port 6000');
});
