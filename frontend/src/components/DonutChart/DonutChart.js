import React from 'react';
import Plot from 'react-plotly.js';

const DonutChart = ({ data }) => {
  // Function to process the wallet journal data for incoming and outgoing separately
  const processData = (data) => {
    const summary = { incoming: {}, outgoing: {} };

    data.forEach(curr => {
      const refType = curr.ref_type;
      const amount = curr.amount;

      if (amount > 0) {
        summary.incoming[refType] = (summary.incoming[refType] || 0) + amount;
      } else {
        summary.outgoing[refType] = (summary.outgoing[refType] || 0) + Math.abs(amount);
      }
    });

    return summary;
  };

  const chartData = processData(data);

  const incomingData = {
    labels: Object.keys(chartData.incoming),
    values: Object.values(chartData.incoming),
  };

  const outgoingData = {
    labels: Object.keys(chartData.outgoing),
    values: Object.values(chartData.outgoing),
  };

  return (
    <div className="donut-charts-container">
      <Plot
        data={[{
          values: incomingData.values,
          labels: incomingData.labels,
          textfont: { color: 'white' },
          type: 'pie',
          hole: 0.4,
          name: 'Incoming',
        }]}
        layout={{ title:{
            text: 'Incoming Funds',
            font: {
                color: 'white' // set main title color
            }
        },
        legend: {
            font: {
                color: 'white' // This sets the legend text color to white
            }
        },
        height: 400, 
        width: 500,
        plot_bgcolor: "transparent",
        paper_bgcolor: "transparent" }}
      />
      <Plot
        data={[{
          values: outgoingData.values,
          labels: outgoingData.labels,
          textfont: { color: 'white' },
          type: 'pie',
          hole: 0.4,
          name: 'Outgoing',
        }]}
        layout={{ title:{
            text: 'Outgoing Funds',
            font: {
                color: 'white' // set main title color
            }
        },
        legend: {
            font: {
                color: 'white' // This sets the legend text color to white
            }
        }, 
        textfont: { color: 'white' },
        height: 400, 
        width: 500,
        plot_bgcolor: "transparent",
        paper_bgcolor: "transparent" }}
      />
    </div>
  );
};

export default DonutChart;
