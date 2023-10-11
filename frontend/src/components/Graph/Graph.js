import React from 'react';
import Plot from 'react-plotly.js';

function Graph({ data }) {
  const plotData = [
    {
      x: data.map(d => d.issued), 
      y: data.map(d => d.price), 
      type: 'scatter',
      mode: 'lines+points',
      marker: { color: 'red' },
      title: data.map(d => d.name)
    },
    
  ];

  return (
    <Plot
      data={plotData}
      layout={{ width: 720, height: 440}}
    />
  );
}

export default Graph;
