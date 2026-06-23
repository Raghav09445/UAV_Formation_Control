import React, { useState } from 'react';
import './SimulationControls.css';

function SimulationControls({ onRun, loading, params }) {
  const [T_sim, setT_sim] = useState(50.0);
  const [SIGMA_INIT, setSigmaInit] = useState(0.5);
  const [RHO, setRho] = useState(0.95);

  const handleSubmit = (e) => {
    e.preventDefault();
    onRun({ T_sim, SIGMA_INIT, RHO });
  };

  return (
    <div className="controls-panel">
      <h2>Simulation Parameters</h2>
      <form onSubmit={handleSubmit}>
        <div className="control-group">
          <label>Simulation Time (s)</label>
          <input
            type="number"
            value={T_sim}
            onChange={(e) => setT_sim(parseFloat(e.target.value))}
            step="10"
            min="10"
            max="200"
          />
          <span className="help-text">Total simulation duration</span>
        </div>

        <div className="control-group">
          <label>Initial Threshold σ(0)</label>
          <input
            type="number"
            value={SIGMA_INIT}
            onChange={(e) => setSigmaInit(parseFloat(e.target.value))}
            step="0.1"
            min="0.1"
            max="1.0"
          />
          <span className="help-text">Initial dynamic event threshold</span>
        </div>

        <div className="control-group">
          <label>Contraction Rate ρ</label>
          <input
            type="number"
            value={RHO}
            onChange={(e) => setRho(parseFloat(e.target.value))}
            step="0.01"
            min="0.9"
            max="0.99"
          />
          <span className="help-text">Threshold decay rate per step</span>
        </div>

        <button type="submit" disabled={loading} className="run-button">
          {loading ? 'Running...' : 'Run Simulation'}
        </button>
      </form>

      <div className="system-info">
        <h3>System Configuration</h3>
        <ul>
          <li>UAVs: {params.N_UAVS || 5}</li>
          <li>Formation Radius: {params.FORMATION_RADIUS || 1.0} m</li>
          <li>Angular Velocity: {params.OMEGA || 0.5} rad/s</li>
          <li>Center Velocity: {params.CENTER_VELOCITY || 0.3} m/s</li>
        </ul>
      </div>
    </div>
  );
}

export default SimulationControls;
