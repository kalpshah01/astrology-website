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
      <div className="min-h-screen flex flex-col items-center justify-center bg-brand-dark relative overflow-hidden">
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
          className="text-xl md:text-2xl font-light tracking-wider text-brand-accent/80 text-center px-4"
        >
          {loadingText}
        </motion.p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-brand-dark relative overflow-hidden text-brand-light">
      <div className="absolute inset-0 bg-stars"></div>
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-brand-accent/10 blur-[120px] rounded-full"></div>
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-brand-secondary/10 blur-[120px] rounded-full"></div>
      
      <div className="relative z-10 container mx-auto px-4 py-16">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center max-w-3xl mx-auto mb-16"
        >
          <div className="flex justify-center mb-6">
            <Sparkles className="text-brand-accent w-12 h-12" />
          </div>
          <h1 className="text-5xl md:text-7xl font-serif mb-6 text-brand-accent drop-shadow-md">
            Discover What Your Future Holds
          </h1>
          <p className="text-lg md:text-xl text-brand-light/70 font-light leading-relaxed">
            Enter your birth details and discover a personalized reading about your personality, career, relationships, finances, and future possibilities.
          </p>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="max-w-2xl mx-auto bg-[#0a1324]/80 backdrop-blur-xl p-8 rounded-3xl border border-brand-accent/20 shadow-2xl shadow-brand-accent/5"
        >
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-brand-light/70 mb-2">First Name</label>
                <input required {...register('firstName')} className="w-full bg-[#060b16] border border-brand-accent/20 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent transition-colors" placeholder="First Name" />
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-light/70 mb-2">Last Name</label>
                <input required {...register('lastName')} className="w-full bg-[#060b16] border border-brand-accent/20 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent transition-colors" placeholder="Last Name" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-brand-light/70 mb-2">Birth Date</label>
              <input required type="date" {...register('birthDate')} className="w-full bg-[#060b16] border border-brand-accent/20 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent transition-colors [color-scheme:dark]" />
            </div>

            <div className="space-y-4">
              <label className="block text-sm font-medium text-brand-light/70">Birth Place</label>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input required {...register('birthPlace.city')} placeholder="City" className="w-full bg-[#060b16] border border-brand-accent/20 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent" />
                <input required {...register('birthPlace.state')} placeholder="State" className="w-full bg-[#060b16] border border-brand-accent/20 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent" />
                <input required {...register('birthPlace.country')} placeholder="Country" className="w-full bg-[#060b16] border border-brand-accent/20 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent" />
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <label className="block text-sm font-medium text-brand-light/70">Birth Time</label>
                <label className="flex items-center text-sm text-brand-light/50 cursor-pointer">
                  <input type="checkbox" {...register('birthTime.isUnknown')} className="mr-2 rounded border-brand-accent/20 bg-[#060b16] text-brand-accent focus:ring-brand-accent" />
                  I don't know my exact birth time
                </label>
              </div>
              {!isUnknownTime && (
                <div className="flex gap-4">
                  <input type="number" min="1" max="12" {...register('birthTime.hour')} placeholder="HH" className="w-24 bg-[#060b16] border border-brand-accent/20 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent" />
                  <span className="text-2xl text-brand-light/50 py-2">:</span>
                  <input type="number" min="0" max="59" {...register('birthTime.minute')} placeholder="MM" className="w-24 bg-[#060b16] border border-brand-accent/20 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent" />
                  <select {...register('birthTime.period')} className="bg-[#060b16] border border-brand-accent/20 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-accent appearance-none">
                    <option value="AM">AM</option>
                    <option value="PM">PM</option>
                  </select>
                </div>
              )}
            </div>

            <button type="submit" className="w-full bg-gradient-to-r from-brand-accent to-amber-500 hover:from-amber-400 hover:to-amber-300 text-brand-dark font-bold py-4 rounded-xl transition-all shadow-lg shadow-brand-accent/25 hover:shadow-brand-accent/40 mt-8 flex items-center justify-center gap-2">
              <Star className="w-5 h-5 text-brand-dark" />
              Predict My Future
            </button>
          </form>
        </motion.div>
      </div>
    </div>
  );
}
