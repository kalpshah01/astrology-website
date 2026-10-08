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
