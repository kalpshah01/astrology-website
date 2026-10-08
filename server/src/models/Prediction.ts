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
