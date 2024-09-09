// App.tsx

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
    <div>
      <h1>API Data:</h1>
      {error && <p>{error}</p>}
      {message && <p>{message}</p>}
    </div>
  );
};

export default App;
