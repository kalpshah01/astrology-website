import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
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

  const SectionCard = ({ title, icon, content, className = '' }: { title: string, icon: string, content: string, className?: string }) => {
    if (!content) return null;
    return (
      <div className={`bg-brand-dark/80 backdrop-blur-md p-8 rounded-3xl border border-brand-accent/20 shadow-xl shadow-brand-accent/5 hover:border-brand-accent/40 transition-colors ${className}`}>
        <h3 className="text-2xl font-serif text-brand-accent mb-4 flex items-center gap-3">
          <span>{icon}</span> {title}
        </h3>
        <div className="prose prose-invert prose-amber max-w-none prose-p:text-brand-light/90 prose-p:leading-relaxed prose-li:text-brand-light/90 prose-strong:text-white">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-brand-dark relative overflow-hidden py-16">
      <div className="absolute inset-0 bg-stars pointer-events-none"></div>
      
      <div className="relative z-10 container mx-auto px-4 max-w-7xl">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-serif text-brand-accent mb-6">
            Welcome, {data.firstName}
          </h1>
          <p className="text-brand-light/80 mb-2">Born: {new Date(data.birthDate).toLocaleDateString()}</p>
          <p className="text-brand-light/80 mb-2">Birth Place: {data.birthPlace.city}, {data.birthPlace.country}</p>
          {!data.birthTime.isUnknown && <p className="text-brand-light/80">Time: {data.birthTime.hour}:{data.birthTime.minute?.toString().padStart(2, '0')} {data.birthTime.period}</p>}
        </motion.div>

        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="space-y-8">
          
          {/* Top Row: Summary */}
          <SectionCard title="Your Astrological Blueprint" icon="🌟" content={prediction.summary || prediction.markdown} />

          {/* Grid Layout for details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <SectionCard title="Personality & Superpowers" icon="🔮" content={prediction.personality} />
            <SectionCard title="Career & Ambition" icon="💼" content={prediction.career} />
            <SectionCard title="Love & Relationships" icon="❤️" content={prediction.love || prediction.relationships} />
            <SectionCard title="Wealth & Finance" icon="💰" content={prediction.finance} />
            <SectionCard title="Travel & Destiny" icon="✈️" content={prediction.travel} />
            <SectionCard title="Health & Vitality" icon="🌿" content={prediction.healthAndWellness} />
          </div>

          {/* Strengths & Challenges Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {prediction.strengths?.length > 0 && (
              <div className="bg-brand-dark/80 backdrop-blur-md p-8 rounded-3xl border border-green-500/30 shadow-xl">
                <h3 className="text-2xl font-serif text-green-400 mb-4 flex items-center gap-3">✨ Core Strengths</h3>
                <ul className="space-y-3">
                  {prediction.strengths.map((s: string, i: number) => (
                    <li key={i} className="flex items-start text-brand-light/90"><span className="mr-3 text-green-400">✦</span> {s}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {prediction.challenges?.length > 0 && (
              <div className="bg-brand-dark/80 backdrop-blur-md p-8 rounded-3xl border border-orange-500/30 shadow-xl">
                <h3 className="text-2xl font-serif text-orange-400 mb-4 flex items-center gap-3">⚡ Growth Challenges</h3>
                <ul className="space-y-3">
                  {prediction.challenges.map((c: string, i: number) => (
                    <li key={i} className="flex items-start text-brand-light/90"><span className="mr-3 text-orange-400">✦</span> {c}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Bottom Row: Timeline */}
          <SectionCard title="Your 5-Year Timeline" icon="📅" content={prediction.timeline || prediction.futureOutlook} />

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
