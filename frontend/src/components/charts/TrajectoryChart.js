import React from 'react';
import Plot from 'react-plotly.js';

function TrajectoryChart({ data }) {
  const traces = [];
  const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];

  for (let i = 0; i < data.n_uavs; i++) {
    const x = data.positions.map(pos => pos[i][0]);
    const y = data.positions.map(pos => pos[i][1]);

    traces.push({
      x: x,
      y: y,
      mode: 'lines',
      name: `UAV ${i + 1}`,
      line: { color: colors[i] }
    });
  }

  const center_x = data.centers.map(c => c[0]);
  const center_y = data.centers.map(c => c[1]);
  traces.push({
    x: center_x,
    y: center_y,
    mode: 'lines',
    name: 'Center',
    line: { color: 'black', dash: 'dash', width: 2 }
  });

  return (
    <div className="chart-container">
      <h3>UAV Formation Trajectories</h3>
      <Plot
        data={traces}
        layout={{
          title: 'XY Position Trajectories',
          xaxis: { title: 'X Position (m)' },
          yaxis: { title: 'Y Position (m)' },
          hovermode: 'closest',
          height: 400
        }}
        style={{ width: '100%' }}
      />
    </div>
  );
}

export default TrajectoryChart;
