/*import express from 'express';
import multer from 'multer';
import cors from 'cors';
import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();
const PORT = 5000;

// Enable CORS to connect React to Node.js
app.use(cors());

// File path configuration
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Multer setup to handle image upload
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, './uploads');
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});
const upload = multer({ storage: storage });

// POST route to upload image and trigger Python script
app.post('/upload', upload.single('image'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  // Absolute path of the uploaded image
  const imagePath = path.join(__dirname, 'uploads', req.file.filename);

  // Execute Python script
  const pythonProcess = exec(`python find_match.py "${imagePath}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Exec error: ${error}`);
      return res.status(500).json({ error: 'Failed to execute Python script' });
    }

    // Extract output from Python script
    const output = stdout.trim().split(',');
    const foodItem = output[0];
    const similarity = parseFloat(output[1]);

    // Send response to React
    res.json({
      food_item: foodItem,
      calories: Math.floor(Math.random() * 500 + 100),  // Dummy calories for now
      similarity: similarity.toFixed(2)
    });
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
*/


import express from 'express';
import multer from 'multer';
import cors from 'cors';
import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const app = express();
const PORT = 5000;

// Enable CORS to connect React to Node.js
app.use(cors());

// File path configuration
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Multer setup to handle image upload
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, './uploads');
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});
const upload = multer({ storage: storage });

// POST route to upload image and trigger Python script
app.post('/upload', upload.single('image'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  // Absolute path of the uploaded image
  const imagePath = path.join(__dirname, 'uploads', req.file.filename);

  // Execute Python script and capture JSON output
  exec(`python find_match.py "${imagePath}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Exec error: ${error}`);
      return res.status(500).json({ error: 'Failed to execute Python script' });
    }

    // ✅ Parse JSON response from Python script
    try {
      const responseData = JSON.parse(stdout);
      res.json(responseData);
    } catch (parseError) {
      console.error(`Parse error: ${parseError}`);
      res.status(500).json({ error: 'Failed to parse Python script response' });
    }

    // ✅ Optional: Delete the uploaded image after processing
    fs.unlink(imagePath, (err) => {
      if (err) console.error('Failed to delete image:', err);
    });
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

