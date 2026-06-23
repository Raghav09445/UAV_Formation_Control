import React from 'react';
import Plot from 'react-plotly.js';

function BandwidthChart({ data }) {
  return (
    <div className="chart-container">
      <h3>Bandwidth Comparison</h3>
      <Plot
        data={[
          {
            x: ['Periodic', 'DECM'],
            y: [data.periodic_broadcasts, data.total_broadcasts],
            type: 'bar',
            marker: { color: ['#cccccc', '#0056b3'] }
          }
        ]}
        layout={{
          title: `Bandwidth Reduction: ${data.bandwidth_reduction.toFixed(1)}%`,
          yaxis: { title: 'Total Broadcasts' },
          height: 400
        }}
        style={{ width: '100%' }}
      />
    </div>
  );
}

export default BandwidthChart;
