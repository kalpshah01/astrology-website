import { Request, Response, NextFunction } from 'express';
import Prediction from '../models/Prediction';
import { GoogleGenAI } from '@google/genai';

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
    const client = new GoogleGenAI({
      apiKey: process.env.GEMINI_API_KEY,
    });

    const prompt = `You are a professional astrologer providing a thoughtful, modern reading.
    Do NOT present the result as scientifically proven fact. Use framing like "Astrology-inspired guidance".
    
    Birth Details:
    Name: ${data.firstName} ${data.lastName}
    Date: ${data.birthDate}
    Place: ${data.birthPlace.city}, ${data.birthPlace.state}, ${data.birthPlace.country}
    Time: ${data.birthTime.isUnknown ? 'Unknown' : `${data.birthTime.hour}:${data.birthTime.minute} ${data.birthTime.period}`}
    
    Return a JSON response strictly adhering to this structure. Write EVERY section in a warm, conversational, premium tone. Use EMOJIS, bolding, and bullet points within the text.
    {
      "summary": "Overall conversational summary of their cosmic blueprint...",
      "personality": "Detailed reading of their traits and superpowers...",
      "career": "In-depth career and ambition guidance...",
      "finance": "Money and wealth outlook...",
      "love": "Love, relationships, marriage timeline, and future spouse details...",
      "travel": "Travel, relocation, and abroad opportunities...",
      "timeline": "A year-by-year timeline for the next 5 years (format with emojis)...",
      "strengths": ["...", "..."],
      "challenges": ["...", "..."]
    }`;

    const models = ['gemini-3.5-flash-lite', 'gemini-3.8-flash', 'gemini-3.1-flash-lite'];
    
    let result: any = null;
    let successfulModel = '';
    let lastError: any = null;

    for (const model of models) {
      try {
        console.log(`Attempting prediction with model: ${model}`);
        const interaction = await client.interactions.create({
          model: model,
          input: prompt,
          response_format: {
            type: "text",
            mime_type: "application/json"
          }
        });

        result = JSON.parse(interaction.output_text || '{}');
        successfulModel = model;
        break; // Successfully generated, break out of loop
      } catch (err: any) {
        console.error(`Model ${model} failed:`, err.message || err);
        lastError = err;
        // Continue to the next model in the array
      }
    }

    if (!result) {
      throw lastError || new Error('All models failed to generate a prediction.');
    }

    await Prediction.findByIdAndUpdate(id, {
      prediction: result,
      status: 'completed',
      openAIModel: successfulModel
    });

  } catch (error: any) {
    console.error('Prediction Generation Error:', error);
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
