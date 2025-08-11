const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const path = require('path');

const app = express();
const port = process.env.PORT || 5001;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from the React app
app.use(express.static(path.join(__dirname, '../frontend/build')));

// MongoDB connection string - replace with your own
const mongoURI = 'mongodb://localhost:27017/';

mongoose.connect(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('MongoDB connected'))
.catch(err => console.error('MongoDB connection error:', err));

// Mongoose schema and model for clown data
const clownSchema = new mongoose.Schema({
  name: { type: String, required: true },
  color: { type: String, required: true },
  age: { type: Number, required: true }
});

const Clown = mongoose.model('Clown', clownSchema);

// Mongoose schema and model for user data
const userSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true }
});

const User = mongoose.model('User', userSchema);

// Sample route
app.get('/', (req, res) => {
  res.send('Doctor Portal Backend is running');
});

// API endpoint to add clown data
app.post('/api/clowns', async (req, res) => {
  try {
    const clown = new Clown(req.body);
    const savedClown = await clown.save();
    res.status(201).json(savedClown);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

// API endpoint to get all clown data
app.get('/api/clowns', async (req, res) => {
  try {
    const clowns = await Clown.find();
    res.json(clowns);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// User registration endpoint
app.post('/api/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;
    const existingUser = await User.findOne({ $or: [{ username }, { email }] });
    if (existingUser) {
      return res.status(400).json({ message: 'Username or email already exists' });
    }
    const hashedPassword = await bcrypt.hash(password, 10);
    const newUser = new User({ username, email, password: hashedPassword });
    await newUser.save();
    res.status(201).json({ message: 'User registered successfully' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// User login endpoint
app.post('/api/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    const user = await User.findOne({ username });
    if (!user) {
      return res.status(400).json({ message: 'Invalid username or password' });
    }
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(400).json({ message: 'Invalid username or password' });
    }
    // Generate JWT token (optional)
    const token = jwt.sign({ userId: user._id }, 'your_jwt_secret', { expiresIn: '1h' });
    res.json({ message: 'Login successful', token });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/build/index.html'));
});

app.listen(port, () => {
  console.log(`Server is running on port: ${port}`);
});
