# Future Prediction App

A complete full-stack web application for generating astrology-style future predictions using the OpenAI API.

## Requirements
- Node.js
- MongoDB
- OpenAI API Key

## Setup Instructions

### 1. Backend Setup
```bash
cd server
npm install
```
Create a `.env` file in the `server` directory (use `.env.example` as a template):
```
PORT=5000
MONGODB_URI=mongodb://localhost:27017/astrology
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET=your_secret
ADMIN_PASSWORD=admin123
```
Start backend:
```bash
npm run dev
```

### 2. Frontend Setup
```bash
cd client
npm install
```
Create a `.env` file in the `client` directory:
```
VITE_API_URL=http://localhost:5000/api
```
Start frontend:
```bash
npm run dev
```

## Admin Access
Go to `/admin/login` and use the password defined in `ADMIN_PASSWORD`.
