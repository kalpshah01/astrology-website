import { Request, Response, NextFunction } from 'express';
import { supabase } from '../config/supabase';
import { GoogleGenAI } from '@google/genai';

export const createPrediction = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const { firstName, lastName, birthDate, birthPlace, birthTime } = req.body;
    
    // Insert into Supabase
    const { data: newPrediction, error } = await supabase
      .from('predictions')
      .insert([
        {
          first_name: firstName,
          last_name: lastName,
          birth_date: birthDate,
          birth_place: birthPlace,
          birth_time: birthTime,
          status: 'processing'
        }
      ])
      .select()
      .single();

    if (error) throw error;

    res.status(202).json({ success: true, data: { id: newPrediction.id } });

    // Process asynchronously
    generatePrediction(newPrediction.id, req.body);

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

    await supabase
      .from('predictions')
      .update({
        prediction: result,
        status: 'completed',
        open_ai_model: successfulModel
      })
      .eq('id', id);

  } catch (error: any) {
    console.error('Prediction Generation Error:', error);
    await supabase
      .from('predictions')
      .update({
        status: 'failed',
        error_message: error.message || 'An unknown error occurred during generation'
      })
      .eq('id', id);
  }
};

export const getPrediction = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const { id } = req.params;

    const { data: prediction, error } = await supabase
      .from('predictions')
      .select('*')
      .eq('id', id)
      .single();

    if (error || !prediction) {
      res.status(404).json({ success: false, message: 'Prediction not found' });
      return;
    }

    // Map database fields back to frontend expected structure
    const formattedData = {
      ...prediction,
      firstName: prediction.first_name,
      lastName: prediction.last_name,
      birthDate: prediction.birth_date,
      birthPlace: prediction.birth_place,
      birthTime: prediction.birth_time,
      openAIModel: prediction.open_ai_model
    };

    res.json({ success: true, data: formattedData });
  } catch (error) {
    next(error);
  }
};
