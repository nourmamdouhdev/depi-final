import { useState } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function useForecast() {
  const [file, setFile] = useState(null);
  const [horizon, setHorizon] = useState(30);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState(null);

  const processForecast = async (uploadFile, selectedHorizon) => {
    if (!uploadFile) {
      setError("Please select a valid CSV file.");
      return;
    }
    
    setError('');
    setLoading(true);

    const formData = new FormData();
    formData.append('file', uploadFile);
    formData.append('horizon', selectedHorizon);

    try {
      const response = await axios.post(`${API_URL}/api/forecast`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResults(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "An error occurred during forecasting.");
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setFile(null);
    setResults(null);
    setError('');
  };

  return {
    file,
    setFile,
    horizon,
    setHorizon,
    loading,
    error,
    results,
    processForecast,
    reset
  };
}
