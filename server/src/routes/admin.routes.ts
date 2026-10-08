import express from 'express';
import { loginAdmin, getPredictions, getPredictionById } from '../controllers/admin.controller';
import { protect } from '../middleware/auth.middleware';

const router = express.Router();

router.post('/login', loginAdmin);
router.get('/predictions', protect, getPredictions);
router.get('/predictions/:id', protect, getPredictionById);

export default router;
