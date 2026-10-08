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
