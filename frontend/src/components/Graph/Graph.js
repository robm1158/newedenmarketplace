import React from 'react';
import Plot from 'react-plotly.js';

function Graph({ data, itemName }) {

  const isRomanNumeral = (word) => {
    // Regex to match a Roman numeral
    const romanRegex = /^(?=[MDCLXVI])(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))$/i;
    return romanRegex.test(word);
  };

  // Function to capitalize each segment of the itemName properly, including Roman numerals
  const formatItemName = (itemName) => {
      if (!itemName) return '';

      // Split the itemName into words, then map through each word
      return itemName.toLowerCase().split('_').map(word => {
          // If the word is a Roman numeral, capitalize all letters, otherwise just capitalize the first letter
          return isRomanNumeral(word) ? word.toUpperCase() : word.charAt(0).toUpperCase() + word.slice(1);
      }).join(' ');
  };
  const formattedItemName = itemName ? formatItemName(itemName) : '';
  const lineTrace = {
    x: data.map(d => d.date),
    y: data.map(d => d.average),
    type: 'scatter',
    mode: 'lines',
    name: 'Average Price',
    line: { color: 'orange' }
  };

  const barTrace = {
    x: data.map(d => d.date),
    y: data.map(d => d.volume),
    type: 'bar',
    name: 'Volume',
    yaxis: 'y2',
    marker: { color: '#00daff' },
    // visible: false
  };


  return (
    <Plot
      data={[lineTrace, barTrace]}
      layout={{
        autosize: true,
        plot_bgcolor: "transparent",
        paper_bgcolor: "transparent",
        legend: {
          font: {
            color: 'white' // This sets the legend text color to white
        }
      },
        title: {
          text: formattedItemName,
          font: {
            color: 'white' // set main title color
          }
        },
        xaxis: {
          title: 'Date',
          color: 'white',
          tickcolor: 'white',
          gridcolor: 'gray',
          rangeslider: { bgcolor: 'gray', thickness: 0.15 },
          rangeselector: {
            buttons: [
              { count: 1, label: '1m', step: 'month', stepmode: 'backward' },
              { count: 6, label: '6m', step: 'month', stepmode: 'backward' },
              { count: 1, label: '1y', step: 'year', stepmode: 'backward' },
              { step: 'all' }
            ]
          }
        },
        yaxis: {
          title: 'Price [ISK]',
          color: 'white',
          tickcolor: 'white',
          gridcolor: 'gray'
        },
        yaxis2: {
          title: 'Volume',
          color: 'white',
          overlaying: 'y',
          side: 'right'
        },
        // updatemenus: updatemenus
      }}
      style={{ width: "100%", height: "100%" }}
      useResizeHandler={true}
    />
  );
}

export default Graph;
