import React from 'react';
import Plot from 'react-plotly.js';

function Graph({ data }) {
  const plotData = [
    {
      x: data.map(d => d.issued), // Assuming 'date' is a key in your data
      y: data.map(d => d.price), // Assuming 'value' is a key in your data
      type: 'scatter',
      mode: 'lines+points',
      marker: { color: 'red' },
    },
  ];

  return (
    <Plot
      data={plotData}
      layout={{ width: 720, height: 440, title: 'Plotly Graph' }}
    />
  );
}

export default Graph;
