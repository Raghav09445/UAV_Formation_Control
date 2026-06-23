import React from 'react';
import TrajectoryChart from './charts/TrajectoryChart';
import BroadcastChart from './charts/BroadcastChart';
import BandwidthChart from './charts/BandwidthChart';
import './ResultsDisplay.css';

function ResultsDisplay({ data }) {
  return (
    <div className="results-display">
      <div className="summary-stats">
        <div className="stat-card">
          <h3>Bandwidth Reduction</h3>
          <div className="stat-value">{data.bandwidth_reduction.toFixed(1)}%</div>
        </div>
        <div className="stat-card">
          <h3>Total Broadcasts</h3>
          <div className="stat-value">{data.total_broadcasts}</div>
        </div>
        <div className="stat-card">
          <h3>Periodic Baseline</h3>
          <div className="stat-value">{data.periodic_broadcasts}</div>
        </div>
        <div className="stat-card">
          <h3>Simulation Steps</h3>
          <div className="stat-value">{data.steps}</div>
        </div>
      </div>

      <div className="charts-grid">
        <TrajectoryChart data={data} />
        <BroadcastChart data={data} />
        <BandwidthChart data={data} />
      </div>
    </div>
  );
}

export default ResultsDisplay;
