import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

export default function AdminDashboard() {
  const [predictions, setPredictions] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const res = await api.get('/admin/predictions');
        setPredictions(res.data.data);
      } catch (err) {
        navigate('/admin/login');
      }
    };
    fetchPredictions();
  }, [navigate]);

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-serif text-brand-accent">Admin Dashboard</h1>
          <button 
            onClick={() => { localStorage.removeItem('adminToken'); navigate('/admin/login'); }}
            className="text-gray-400 hover:text-white"
          >
            Logout
          </button>
        </div>

        <div className="grid grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-900 p-6 rounded-2xl border border-gray-800">
            <div className="text-gray-400 text-sm mb-2">Total Predictions</div>
            <div className="text-3xl">{predictions.length}</div>
          </div>
        </div>

        <div className="bg-gray-900 rounded-2xl border border-gray-800 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-800 text-gray-400 text-sm">
                <th className="p-4 font-medium">Name</th>
                <th className="p-4 font-medium">Date</th>
                <th className="p-4 font-medium">Location</th>
                <th className="p-4 font-medium">Status</th>
                <th className="p-4 font-medium">Action</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map((p: any) => (
                <tr key={p._id} className="border-t border-gray-800 hover:bg-gray-800/50 transition-colors">
                  <td className="p-4">{p.firstName} {p.lastName}</td>
                  <td className="p-4">{new Date(p.createdAt).toLocaleDateString()}</td>
                  <td className="p-4">{p.birthPlace.city}, {p.birthPlace.country}</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded text-xs ${p.status === 'completed' ? 'bg-green-900/50 text-green-400' : p.status === 'failed' ? 'bg-red-900/50 text-red-400' : 'bg-yellow-900/50 text-yellow-400'}`}>
                      {p.status}
                    </span>
                  </td>
                  <td className="p-4">
                    <Link to={`/admin/predictions/${p._id}`} className="text-brand-accent hover:underline text-sm">View</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
