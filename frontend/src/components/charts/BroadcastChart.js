import React from 'react';
import Plot from 'react-plotly.js';

function BroadcastChart({ data }) {
  const uavLabels = Array.from({ length: data.n_uavs }, (_, i) => `UAV ${i + 1}`);

  return (
    <div className="chart-container">
      <h3>Broadcasts per UAV</h3>
      <Plot
        data={[
          {
            x: uavLabels,
            y: data.broadcast_counts,
            type: 'bar',
            marker: { color: '#0056b3' }
          }
        ]}
        layout={{
          title: 'Total Broadcast Count per UAV',
          xaxis: { title: 'UAV' },
          yaxis: { title: 'Broadcasts' },
          height: 400
        }}
        style={{ width: '100%' }}
      />
    </div>
  );
}

export default BroadcastChart;
