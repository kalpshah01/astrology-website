import os
import json

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

base_dir = r"d:\zunck\Women\future"
server_dir = os.path.join(base_dir, "server")
client_dir = os.path.join(base_dir, "client")

# SERVER FILES
server_pkg = {
  "name": "future-server",
  "version": "1.0.0",
  "main": "src/app.ts",
  "scripts": {
    "start": "ts-node src/app.ts",
    "dev": "nodemon src/app.ts",
    "build": "tsc"
  },
  "dependencies": {
    "bcryptjs": "^2.4.3",
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.19.2",
    "express-rate-limit": "^7.3.1",
    "helmet": "^7.1.0",
    "jsonwebtoken": "^9.0.2",
    "mongoose": "^8.4.1",
    "openai": "^4.49.1",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/bcryptjs": "^2.4.6",
    "@types/cors": "^2.8.17",
    "@types/express": "^4.17.21",
    "@types/jsonwebtoken": "^9.0.6",
    "@types/node": "^20.14.2",
    "nodemon": "^3.1.3",
    "ts-node": "^10.9.2",
    "typescript": "^5.4.5"
  }
}
write_file(os.path.join(server_dir, "package.json"), json.dumps(server_pkg, indent=2))

server_tsconfig = {
  "compilerOptions": {
    "target": "es2022",
    "module": "commonjs",
    "rootDir": "./src",
    "outDir": "./dist",
    "esModuleInterop": True,
    "forceConsistentCasingInFileNames": True,
    "strict": True,
    "skipLibCheck": True
  }
}
write_file(os.path.join(server_dir, "tsconfig.json"), json.dumps(server_tsconfig, indent=2))

write_file(os.path.join(server_dir, ".env.example"), '''
PORT=5000
MONGODB_URI=mongodb://localhost:27017/astrology
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET=your_jwt_secret_key
ADMIN_PASSWORD=admin123
''')

write_file(os.path.join(server_dir, "src/app.ts"), '''
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { connectDB } from './config/database';
import predictionRoutes from './routes/prediction.routes';
import adminRoutes from './routes/admin.routes';
import { errorHandler } from './middleware/error.middleware';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(helmet());
app.use(cors());
app.use(express.json());

connectDB();

app.use('/api/predictions', predictionRoutes);
app.use('/api/admin', adminRoutes);

app.use(errorHandler);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
''')

write_file(os.path.join(server_dir, "src/config/database.ts"), '''
import mongoose from 'mongoose';

export const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/astrology');
    console.log(`MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.error(`Error: ${(error as Error).message}`);
    process.exit(1);
  }
};
''')

write_file(os.path.join(server_dir, "src/models/Prediction.ts"), '''
import mongoose, { Document, Schema } from 'mongoose';

export interface IPrediction extends Document {
  firstName: string;
  lastName: string;
  birthDate: Date;
  birthPlace: {
    city: string;
    state: string;
    country: string;
  };
  birthTime: {
    hour: number;
    minute: number;
    period: string;
    isUnknown: boolean;
  };
  prediction: any;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  openAIModel: string;
  errorMessage?: string;
  createdAt: Date;
  updatedAt: Date;
}

const predictionSchema = new Schema({
  firstName: { type: String, required: true },
  lastName: { type: String, required: true },
  birthDate: { type: Date, required: true },
  birthPlace: {
    city: { type: String, required: true },
    state: { type: String },
    country: { type: String, required: true }
  },
  birthTime: {
    hour: { type: Number },
    minute: { type: Number },
    period: { type: String, enum: ['AM', 'PM'] },
    isUnknown: { type: Boolean, default: false }
  },
  prediction: { type: Schema.Types.Mixed },
  status: { type: String, enum: ['pending', 'processing', 'completed', 'failed'], default: 'pending' },
  openAIModel: { type: String },
  errorMessage: { type: String }
}, { timestamps: true });

export default mongoose.model<IPrediction>('Prediction', predictionSchema);
''')

write_file(os.path.join(server_dir, "src/middleware/error.middleware.ts"), '''
import { Request, Response, NextFunction } from 'express';

export const errorHandler = (err: any, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    success: false,
    message: err.message || 'Server Error',
  });
};
''')

write_file(os.path.join(server_dir, "src/middleware/auth.middleware.ts"), '''
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export const protect = (req: Request, res: Response, next: NextFunction) => {
  let token;
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    try {
      token = req.headers.authorization.split(' ')[1];
      const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret');
      (req as any).admin = decoded;
      next();
    } catch (error) {
      res.status(401).json({ success: false, message: 'Not authorized, token failed' });
    }
  } else {
    res.status(401).json({ success: false, message: 'Not authorized, no token' });
  }
};
''')

write_file(os.path.join(server_dir, "src/routes/prediction.routes.ts"), '''
import express from 'express';
import { createPrediction, getPrediction } from '../controllers/prediction.controller';

const router = express.Router();

router.post('/', createPrediction);
router.get('/:id', getPrediction);

export default router;
''')

write_file(os.path.join(server_dir, "src/routes/admin.routes.ts"), '''
import express from 'express';
import { loginAdmin, getPredictions, getPredictionById } from '../controllers/admin.controller';
import { protect } from '../middleware/auth.middleware';

const router = express.Router();

router.post('/login', loginAdmin);
router.get('/predictions', protect, getPredictions);
router.get('/predictions/:id', protect, getPredictionById);

export default router;
''')

write_file(os.path.join(server_dir, "src/controllers/admin.controller.ts"), '''
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import Prediction from '../models/Prediction';

export const loginAdmin = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const { password } = req.body;
    const adminPassword = process.env.ADMIN_PASSWORD || 'admin123';
    
    if (password === adminPassword) {
      const token = jwt.sign({ role: 'admin' }, process.env.JWT_SECRET || 'secret', { expiresIn: '1d' });
      res.json({ success: true, token });
    } else {
      res.status(401).json({ success: false, message: 'Invalid credentials' });
    }
  } catch (error) {
    next(error);
  }
};

export const getPredictions = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const predictions = await Prediction.find().sort({ createdAt: -1 });
    res.json({ success: true, data: predictions });
  } catch (error) {
    next(error);
  }
};

export const getPredictionById = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const prediction = await Prediction.findById(req.params.id);
    if (!prediction) {
      res.status(404).json({ success: false, message: 'Not found' });
      return;
    }
    res.json({ success: true, data: prediction });
  } catch (error) {
    next(error);
  }
};
''')

write_file(os.path.join(server_dir, "src/controllers/prediction.controller.ts"), '''
import { Request, Response, NextFunction } from 'express';
import Prediction from '../models/Prediction';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export const createPrediction = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const { firstName, lastName, birthDate, birthPlace, birthTime } = req.body;
    
    const newPrediction = await Prediction.create({
      firstName,
      lastName,
      birthDate,
      birthPlace,
      birthTime,
      status: 'processing'
    });

    res.status(202).json({ success: true, data: { id: newPrediction._id } });

    // Process asynchronously
    generatePrediction(newPrediction._id.toString(), newPrediction);

  } catch (error) {
    next(error);
  }
};

const generatePrediction = async (id: string, data: any) => {
  try {
    const prompt = `You are a professional astrologer providing a thoughtful, modern reading.
    Do NOT present the result as scientifically proven fact. Use framing like "Astrology-inspired guidance".
    Avoid claiming certainty about death, illness, exact events, guaranteed wealth, etc.
    
    Birth Details:
    Name: ${data.firstName} ${data.lastName}
    Date: ${data.birthDate}
    Place: ${data.birthPlace.city}, ${data.birthPlace.state}, ${data.birthPlace.country}
    Time: ${data.birthTime.isUnknown ? 'Unknown' : `${data.birthTime.hour}:${data.birthTime.minute} ${data.birthTime.period}`}
    
    Return a JSON response strictly adhering to this structure:
    {
      "summary": "...",
      "personality": "...",
      "career": "...",
      "finance": "...",
      "relationships": "...",
      "healthAndWellness": "...",
      "strengths": ["...", "...", "..."],
      "challenges": ["...", "...", "..."],
      "futureOutlook": "...",
      "guidance": ["...", "...", "..."]
    }`;

    const completion = await openai.chat.completions.create({
      messages: [{ role: "system", content: prompt }],
      model: "gpt-3.5-turbo",
      response_format: { type: "json_object" }
    });

    const result = JSON.parse(completion.choices[0].message.content || '{}');

    await Prediction.findByIdAndUpdate(id, {
      prediction: result,
      status: 'completed',
      openAIModel: 'gpt-3.5-turbo'
    });

  } catch (error: any) {
    await Prediction.findByIdAndUpdate(id, {
      status: 'failed',
      errorMessage: error.message
    });
  }
};

export const getPrediction = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const prediction = await Prediction.findById(req.params.id);
    if (!prediction) {
      res.status(404).json({ success: false, message: 'Prediction not found' });
      return;
    }
    res.json({ success: true, data: prediction });
  } catch (error) {
    next(error);
  }
};
''')

# CLIENT FILES
client_pkg = {
  "name": "future-client",
  "private": True,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "@hookform/resolvers": "^3.6.0",
    "axios": "^1.7.2",
    "framer-motion": "^11.2.10",
    "lucide-react": "^0.394.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-hook-form": "^7.51.5",
    "react-router-dom": "^6.23.1",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.4",
    "typescript": "^5.4.5",
    "vite": "^5.2.0"
  }
}
write_file(os.path.join(client_dir, "package.json"), json.dumps(client_pkg, indent=2))

write_file(os.path.join(client_dir, "vite.config.ts"), '''
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
''')

write_file(os.path.join(client_dir, "tailwind.config.js"), '''
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: '#0f172a',
          light: '#f8fafc',
          accent: '#8b5cf6',
          secondary: '#3b82f6'
        }
      }
    },
  },
  plugins: [],
}
''')

write_file(os.path.join(client_dir, "postcss.config.js"), '''
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
''')

write_file(os.path.join(client_dir, "index.html"), '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Discover Your Future | Personalized Astrology Reading</title>
  </head>
  <body class="bg-brand-dark text-brand-light font-sans min-h-screen">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
''')

write_file(os.path.join(client_dir, "src/index.css"), '''
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer utilities {
  .bg-stars {
    background-image: radial-gradient(circle at center, #ffffff 1px, transparent 1px);
    background-size: 50px 50px;
    opacity: 0.1;
  }
}
''')

write_file(os.path.join(client_dir, "src/main.tsx"), '''
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
''')

write_file(os.path.join(client_dir, "src/App.tsx"), '''
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Prediction from './pages/Prediction';
import AdminDashboard from './pages/AdminDashboard';
import AdminLogin from './pages/AdminLogin';
import AdminPredictionDetails from './pages/AdminPredictionDetails';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/prediction/:id" element={<Prediction />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin/predictions/:id" element={<AdminPredictionDetails />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App;
''')

write_file(os.path.join(client_dir, "src/services/api.ts"), '''
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('adminToken');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
''')

write_file(os.path.join(client_dir, ".env.example"), '''
VITE_API_URL=http://localhost:5000/api
''')

write_file(os.path.join(client_dir, "src/pages/Home.tsx"), '''
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import api from '../services/api';
import { Moon, Star, Sparkles } from 'lucide-react';

export default function Home() {
  const { register, handleSubmit, watch } = useForm();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [loadingText, setLoadingText] = useState('');

  const isUnknownTime = watch('birthTime.isUnknown');

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      setLoadingText('Reading your birth details...');
      setTimeout(() => setLoadingText('Analyzing your cosmic profile...'), 2000);
      setTimeout(() => setLoadingText('Preparing your personalized reading...'), 4000);

      const res = await api.post('/predictions', {
        ...data,
        birthTime: {
          ...data.birthTime,
          hour: parseInt(data.birthTime.hour) || 0,
          minute: parseInt(data.birthTime.minute) || 0
        }
      });
      
      const predictionId = res.data.data.id;
      
      // Wait for completion via polling
      const poll = setInterval(async () => {
        const checkRes = await api.get(`/predictions/${predictionId}`);
        if (checkRes.data.data.status === 'completed') {
          clearInterval(poll);
          navigate(`/prediction/${predictionId}`);
        } else if (checkRes.data.data.status === 'failed') {
          clearInterval(poll);
          alert('Failed to generate prediction');
          setLoading(false);
        }
      }, 3000);

    } catch (err) {
      console.error(err);
      alert('An error occurred');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-[#0a0a0f] relative overflow-hidden">
        <div className="absolute inset-0 bg-stars"></div>
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
          className="mb-8"
        >
          <Moon size={64} className="text-brand-accent" />
        </motion.div>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          key={loadingText}
          className="text-xl md:text-2xl font-light tracking-wider text-purple-200 text-center px-4"
        >
          {loadingText}
        </motion.p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f] relative overflow-hidden">
      <div className="absolute inset-0 bg-stars"></div>
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-purple-900/30 blur-[120px] rounded-full"></div>
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-blue-900/30 blur-[120px] rounded-full"></div>
      
      <div className="relative z-10 container mx-auto px-4 py-16">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center max-w-3xl mx-auto mb-16"
        >
          <div className="flex justify-center mb-6">
            <Sparkles className="text-brand-accent w-12 h-12" />
          </div>
          <h1 className="text-5xl md:text-7xl font-serif mb-6 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">
            Discover What Your Future Holds
          </h1>
          <p className="text-lg md:text-xl text-gray-400 font-light leading-relaxed">
            Enter your birth details and discover a personalized reading about your personality, career, relationships, finances, and future possibilities.
          </p>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="max-w-2xl mx-auto bg-gray-900/60 backdrop-blur-xl p-8 rounded-3xl border border-gray-800 shadow-2xl"
        >
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">First Name</label>
                <input required {...register('firstName')} className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent transition-colors" placeholder="First Name" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">Last Name</label>
                <input required {...register('lastName')} className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent transition-colors" placeholder="Last Name" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Birth Date</label>
              <input required type="date" {...register('birthDate')} className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent transition-colors [color-scheme:dark]" />
            </div>

            <div className="space-y-4">
              <label className="block text-sm font-medium text-gray-400">Birth Place</label>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input required {...register('birthPlace.city')} placeholder="City" className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent" />
                <input required {...register('birthPlace.state')} placeholder="State" className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent" />
                <input required {...register('birthPlace.country')} placeholder="Country" className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent" />
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <label className="block text-sm font-medium text-gray-400">Birth Time</label>
                <label className="flex items-center text-sm text-gray-500 cursor-pointer">
                  <input type="checkbox" {...register('birthTime.isUnknown')} className="mr-2 rounded border-gray-700 bg-gray-800 text-brand-accent focus:ring-brand-accent" />
                  I don't know my exact birth time
                </label>
              </div>
              {!isUnknownTime && (
                <div className="flex gap-4">
                  <input type="number" min="1" max="12" {...register('birthTime.hour')} placeholder="HH" className="w-24 bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent" />
                  <span className="text-2xl text-gray-500 py-2">:</span>
                  <input type="number" min="0" max="59" {...register('birthTime.minute')} placeholder="MM" className="w-24 bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent" />
                  <select {...register('birthTime.period')} className="bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent appearance-none">
                    <option value="AM">AM</option>
                    <option value="PM">PM</option>
                  </select>
                </div>
              )}
            </div>

            <button type="submit" className="w-full bg-gradient-to-r from-brand-accent to-brand-secondary hover:from-purple-500 hover:to-blue-500 text-white font-medium py-4 rounded-xl transition-all shadow-lg shadow-brand-accent/25 hover:shadow-brand-accent/40 mt-8 flex items-center justify-center gap-2">
              <Star className="w-5 h-5" />
              Predict My Future
            </button>
          </form>
        </motion.div>
      </div>
    </div>
  );
}
''')

write_file(os.path.join(client_dir, "src/pages/Prediction.tsx"), '''
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import api from '../services/api';

export default function Prediction() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    api.get(`/predictions/${id}`).then((res) => {
      setData(res.data.data);
    }).catch(console.error);
  }, [id]);

  if (!data || data.status !== 'completed') return <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center text-white">Loading...</div>;

  const { prediction } = data;

  const Section = ({ title, content }: { title: string, content: string }) => (
    <div className="bg-gray-900/60 backdrop-blur p-8 rounded-3xl border border-gray-800 mb-8">
      <h3 className="text-2xl font-serif text-brand-accent mb-4">{title}</h3>
      <p className="text-gray-300 leading-relaxed">{content}</p>
    </div>
  );

  return (
    <div className="min-h-screen bg-[#0a0a0f] relative overflow-hidden py-16">
      <div className="absolute inset-0 bg-stars pointer-events-none"></div>
      
      <div className="relative z-10 container mx-auto px-4 max-w-4xl">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-serif text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400 mb-6">
            Welcome, {data.firstName}
          </h1>
          <p className="text-gray-400 mb-2">Born: {new Date(data.birthDate).toLocaleDateString()}</p>
          <p className="text-gray-400 mb-2">Birth Place: {data.birthPlace.city}, {data.birthPlace.country}</p>
          {!data.birthTime.isUnknown && <p className="text-gray-400">Time: {data.birthTime.hour}:{data.birthTime.minute?.toString().padStart(2, '0')} {data.birthTime.period}</p>}
        </motion.div>

        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
          <Section title="Your Overall Reading" content={prediction.summary} />
          <Section title="Your Personality" content={prediction.personality} />
          <div className="grid md:grid-cols-2 gap-8 mb-8">
            <Section title="Career & Professional Life" content={prediction.career} />
            <Section title="Money & Financial Outlook" content={prediction.finance} />
          </div>
          <Section title="Love & Relationships" content={prediction.relationships} />
          <Section title="Health & Wellness" content={prediction.healthAndWellness} />

          <div className="grid md:grid-cols-2 gap-8 mb-8">
            <div className="bg-gray-900/60 p-8 rounded-3xl border border-gray-800">
              <h3 className="text-xl font-serif text-green-400 mb-4">Your Strengths</h3>
              <ul className="space-y-3">
                {prediction.strengths?.map((s: string, i: number) => (
                  <li key={i} className="flex items-start text-gray-300"><span className="mr-2 text-green-400">•</span> {s}</li>
                ))}
              </ul>
            </div>
            <div className="bg-gray-900/60 p-8 rounded-3xl border border-gray-800">
              <h3 className="text-xl font-serif text-orange-400 mb-4">Potential Challenges</h3>
              <ul className="space-y-3">
                {prediction.challenges?.map((c: string, i: number) => (
                  <li key={i} className="flex items-start text-gray-300"><span className="mr-2 text-orange-400">•</span> {c}</li>
                ))}
              </ul>
            </div>
          </div>

          <Section title="Future Outlook" content={prediction.futureOutlook} />

          <div className="mt-16 p-6 border-t border-gray-800 text-center">
            <p className="text-sm text-gray-500 max-w-2xl mx-auto">
              This reading is intended for entertainment and personal reflection.
              Astrology-based interpretations are not scientifically proven predictions
              and should not be used as a substitute for professional medical,
              legal, financial, or other expert advice.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
''')

write_file(os.path.join(client_dir, "src/pages/AdminLogin.tsx"), '''
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function AdminLogin() {
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.post('/admin/login', { password });
      localStorage.setItem('adminToken', res.data.token);
      navigate('/admin');
    } catch (err) {
      alert('Login failed');
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center text-white px-4">
      <form onSubmit={handleLogin} className="bg-gray-900 p-8 rounded-2xl border border-gray-800 w-full max-w-md">
        <h2 className="text-2xl mb-6 font-serif text-center">Admin Login</h2>
        <input 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter Admin Password"
          className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 mb-6 focus:outline-none focus:border-brand-accent"
        />
        <button type="submit" className="w-full bg-brand-accent hover:bg-purple-600 py-3 rounded-lg font-medium transition-colors">
          Login
        </button>
      </form>
    </div>
  );
}
''')

write_file(os.path.join(client_dir, "src/pages/AdminDashboard.tsx"), '''
import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

export default function AdminDashboard() {
  const [predictions, setPredictions] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const res = await api.get('/admin/predictions');
        setPredictions(res.data.data);
      } catch (err) {
        navigate('/admin/login');
      }
    };
    fetchPredictions();
  }, [navigate]);

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-serif text-brand-accent">Admin Dashboard</h1>
          <button 
            onClick={() => { localStorage.removeItem('adminToken'); navigate('/admin/login'); }}
            className="text-gray-400 hover:text-white"
          >
            Logout
          </button>
        </div>

        <div className="grid grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-900 p-6 rounded-2xl border border-gray-800">
            <div className="text-gray-400 text-sm mb-2">Total Predictions</div>
            <div className="text-3xl">{predictions.length}</div>
          </div>
        </div>

        <div className="bg-gray-900 rounded-2xl border border-gray-800 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-800 text-gray-400 text-sm">
                <th className="p-4 font-medium">Name</th>
                <th className="p-4 font-medium">Date</th>
                <th className="p-4 font-medium">Location</th>
                <th className="p-4 font-medium">Status</th>
                <th className="p-4 font-medium">Action</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map((p: any) => (
                <tr key={p._id} className="border-t border-gray-800 hover:bg-gray-800/50 transition-colors">
                  <td className="p-4">{p.firstName} {p.lastName}</td>
                  <td className="p-4">{new Date(p.createdAt).toLocaleDateString()}</td>
                  <td className="p-4">{p.birthPlace.city}, {p.birthPlace.country}</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded text-xs ${p.status === 'completed' ? 'bg-green-900/50 text-green-400' : p.status === 'failed' ? 'bg-red-900/50 text-red-400' : 'bg-yellow-900/50 text-yellow-400'}`}>
                      {p.status}
                    </span>
                  </td>
                  <td className="p-4">
                    <Link to={`/admin/predictions/${p._id}`} className="text-brand-accent hover:underline text-sm">View</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
''')

write_file(os.path.join(client_dir, "src/pages/AdminPredictionDetails.tsx"), '''
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';

export default function AdminPredictionDetails() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    api.get(`/admin/predictions/${id}`).then((res) => {
      setData(res.data.data);
    }).catch(console.error);
  }, [id]);

  if (!data) return <div className="text-white p-8">Loading...</div>;

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-8">
      <div className="max-w-4xl mx-auto">
        <Link to="/admin" className="text-brand-accent hover:underline mb-8 inline-block">&larr; Back to Dashboard</Link>
        <div className="bg-gray-900 p-8 rounded-2xl border border-gray-800 mb-8">
          <h2 className="text-2xl mb-6">User Details</h2>
          <pre className="text-gray-300 text-sm overflow-x-auto">
            {JSON.stringify({
              name: `${data.firstName} ${data.lastName}`,
              birthDate: data.birthDate,
              birthPlace: data.birthPlace,
              birthTime: data.birthTime,
              status: data.status,
              error: data.errorMessage,
              created: data.createdAt
            }, null, 2)}
          </pre>
        </div>
        
        {data.prediction && (
          <div className="bg-gray-900 p-8 rounded-2xl border border-gray-800">
            <h2 className="text-2xl mb-6">AI Response</h2>
            <pre className="text-gray-300 text-sm overflow-x-auto">
              {JSON.stringify(data.prediction, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
''')

write_file(os.path.join(base_dir, "README.md"), '''
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
''')

print("Scaffolding complete.")
