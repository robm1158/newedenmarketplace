import React from 'react';
import Plot from 'react-plotly.js';

function BubbleGraph({ data, itemName }) {
    // Create an object where each key is an item_name and its value is an array of data points for that item_name
    const groupedData = {};
    data.forEach(entry => {
        if (!groupedData[entry.item_name]) {
            groupedData[entry.item_name] = [];
        }
        groupedData[entry.item_name].push(entry);
    });

    // Create a trace for each item_name
    const traces = Object.keys(groupedData).map(item_name => {
        return {
            x: groupedData[item_name].map(e => e.order_count),
            y: groupedData[item_name].map(e => e.percent_profit),
            text: groupedData[item_name].map(e => e.item_name),
            mode: 'markers',
            marker: {
                size: groupedData[item_name].map(e => e.adjusted_volume),
                colorscale: 'Viridis',
                sizemode: 'diameter',
            },
            name: item_name // Set the trace name to item_name for it to appear in the legend
        };
    });

    const layout = {
        autosize: true,
        plot_bgcolor: "transparent",
        paper_bgcolor: "transparent",
        legend: {
            font: {
                color: 'white' // Setting legend values color to white
            },
            title: {
                text: 'Group Types',
                font: {
                    color: 'white' // Setting legend title color to white
                }
            }
        },
        title: {
            text: `Percent Profit vs Total Order Count`,
            font: {
                color: 'white' // Setting main title color to white
            }
        },
        xaxis: {
            title: {
                text: "Total Order Count Per Day",
                font: {
                    color: 'white' // Setting legend title color to white
                }
            },
            tickfont: {
                color: 'white' // Setting x-axis tick values color to white
            },
            tickcolor: 'white',
            gridcolor: 'gray'
        },
        yaxis: {
            title: {
                text: "Relative Percent Profit",
                font: {
                    color: 'white' // Setting legend title color to white
                }
            },
            tickfont: {
                color: 'white' // Setting x-axis tick values color to white
            },
            tickcolor: 'white',
            gridcolor: 'gray',
            gridwidth: 2
        },
    };

    return <Plot data={traces} layout={layout} />;
}

export default BubbleGraph;
