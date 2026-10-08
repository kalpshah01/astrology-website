import express from 'express';
import { createPrediction, getPrediction } from '../controllers/prediction.controller';

const router = express.Router();

router.post('/', createPrediction);
router.get('/:id', getPrediction);

export default router;
