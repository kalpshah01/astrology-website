import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';

export default function AdminPredictionDetails() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    api.get(`/admin/predictions/${id}`).then((res) => {
      setData(res.data.data);
    }).catch(console.error);
  }, [id]);

  if (!data) return <div className="text-white p-8">Loading...</div>;

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-8">
      <div className="max-w-4xl mx-auto">
        <Link to="/admin" className="text-brand-accent hover:underline mb-8 inline-block">&larr; Back to Dashboard</Link>
        <div className="bg-gray-900 p-8 rounded-2xl border border-gray-800 mb-8">
          <h2 className="text-2xl mb-6">User Details</h2>
          <pre className="text-gray-300 text-sm overflow-x-auto">
            {JSON.stringify({
              name: `${data.firstName} ${data.lastName}`,
              birthDate: data.birthDate,
              birthPlace: data.birthPlace,
              birthTime: data.birthTime,
              status: data.status,
              error: data.errorMessage,
              created: data.createdAt
            }, null, 2)}
          </pre>
        </div>
        
        {data.prediction && (
          <div className="bg-gray-900 p-8 rounded-2xl border border-gray-800">
            <h2 className="text-2xl mb-6">AI Response</h2>
            <pre className="text-gray-300 text-sm overflow-x-auto">
              {JSON.stringify(data.prediction, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
