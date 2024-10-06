"use client";
import { useState } from 'react';
import { Button } from "@/components/ui/button";

export default function Home() {
  const [jsonInput, setJsonInput] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonInput,
      });

      if (!response.ok) {
        throw new Error('Error: ' + response.statusText);
      }

      const result = await response.json();
      setPrediction(result.prediction);
      setError(null); 
    } catch (err) {
      setError(err.message);
      setPrediction(null); 
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-lg p-6 bg-white rounded-md shadow-lg">
        <h1 className="text-xl font-semibold text-center mb-4">Upload JSON Data</h1>

        <form onSubmit={handleSubmit}>
          <textarea
            className="w-full h-40 p-2 border border-gray-300 rounded-md"
            placeholder="Paste your JSON data here..."
            value={jsonInput}
            onChange={(e) => setJsonInput(e.target.value)}
            required
          />

          <Button type="submit" className="w-full mt-4">
            Submit
          </Button>
        </form>

        {error && <p className="mt-4 text-red-500">{error}</p>}
        {prediction && <p className="mt-4 text-green-500">Prediction: {prediction}</p>}
      </div>
    </div>
  );
}
