import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import SimulationControls from './components/SimulationControls';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
  const [simData, setSimData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [params, setParams] = useState({
    T_sim: 50.0,
    SIGMA_INIT: 0.5,
    RHO: 0.95
  });

  useEffect(() => {
    fetchParameters();
  }, []);

  const fetchParameters = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/parameters');
      setParams({
        ...params,
        ...response.data
      });
    } catch (err) {
      console.error('Error fetching parameters:', err);
    }
  };

  const runSimulation = async (newParams) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:5000/api/simulate', newParams);
      setSimData(response.data.data);
    } catch (err) {
      setError('Failed to run simulation: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>UAV Formation Control - DECM Simulator</h1>
        <p>Dynamic Event-Triggered Communication Mechanism</p>
      </header>

      <div className="container">
        <SimulationControls onRun={runSimulation} loading={loading} params={params} />

        {error && <div className="error-message">{error}</div>}

        {loading && <div className="loading">Running simulation...</div>}

        {simData && <ResultsDisplay data={simData} />}
      </div>
    </div>
  );
}

export default App;
