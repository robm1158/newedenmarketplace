import React from 'react';
import Plot from 'react-plotly.js';

function Graph({ data, itemName }) {
  
  const plotData = [
    {
      x: data.map(d => d.issued), 
      y: data.map(d => d.price), 
      type: 'scatter',
      mode: 'points',
      marker: { color: 'orange' },
      line: { shape: 'none' }
    }
  ];
  const titleText = itemName || "No Title";
  return (
    <Plot
      data={plotData}
      layout={{ 
        autosize: true,
        plot_bgcolor: "transparent",
        paper_bgcolor: "transparent",
        xaxis: {
          title: 'Date',
          color: 'white',
          tickcolor: 'white',
          gridcolor: 'gray',
          rangeslider: {           // This is the property for the range slider
            bgcolor: 'gray',       // You can adjust the slider's background color
            thickness: 0.15         // Adjust the slider's thickness relative to the plot
          }
        },
        yaxis: {
          title: 'Price [ISK]',
          color: 'white',
          tickcolor: 'white',
          gridcolor: 'gray',
          fixedrange: false  
        },
        title: {
          text: titleText,
          font: {
            color: 'white'
          }
        }
      }}
      style={{ width: "100%", height: "100%" }}
      useResizeHandler={true}
    />
);

}


export default Graph;
