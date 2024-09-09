import React, { useEffect, useState } from 'react';
import { TestResponse } from '../types/apiTypeChecker';
import axiosInstance from './services/ApiHandler';

const App: React.FC = () => {
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axiosInstance.get<TestResponse>('/test');
        setMessage(response.data.message);
      } catch (err) {
        setError('Error fetching data');
        console.error("error :", err);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">API Data:</h1>
      {error && <p className="text-red-500">{error}</p>}
      {message && <p className="text-green-500">{message}</p>}
    </div>
  );
};

export default App;
