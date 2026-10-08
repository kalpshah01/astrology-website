import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { supabase } from '../config/supabase';

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

const mapDatabaseRow = (prediction: any) => ({
  ...prediction,
  firstName: prediction.first_name,
  lastName: prediction.last_name,
  birthDate: prediction.birth_date,
  birthPlace: prediction.birth_place,
  birthTime: prediction.birth_time,
  openAIModel: prediction.open_ai_model,
  createdAt: prediction.created_at
});

export const getPredictions = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const { data: predictions, error } = await supabase
      .from('predictions')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) throw error;

    const mapped = predictions.map(mapDatabaseRow);
    res.json({ success: true, data: mapped });
  } catch (error) {
    next(error);
  }
};

export const getPredictionById = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const { data: prediction, error } = await supabase
      .from('predictions')
      .select('*')
      .eq('id', req.params.id)
      .single();

    if (error || !prediction) {
      res.status(404).json({ success: false, message: 'Not found' });
      return;
    }
    
    res.json({ success: true, data: mapDatabaseRow(prediction) });
  } catch (error) {
    next(error);
  }
};
