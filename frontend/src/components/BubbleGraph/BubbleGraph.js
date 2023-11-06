import React from 'react';
import Plot from 'react-plotly.js';

function BubbleGraph({ data, itemName }) {
    // Create an object where each key is an item_name and its value is an array of data points for that item_name
    const groupedData = {};

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

    data.forEach(entry => {
        if (!groupedData[entry.item_name]) {
            groupedData[entry.item_name] = [];
        }
        groupedData[entry.item_name].push(entry);
    });

    // Create a trace for each item_name
    const traces = Object.keys(groupedData).map(item_name => {
        const formattedItemName = item_name ? formatItemName(item_name) : '';
        return {
            x: groupedData[item_name].map(e => e.order_count),
            y: groupedData[item_name].map(e => e.percent_profit),
            mode: 'markers',
            marker: {
                size: groupedData[item_name].map(e => e.adjusted_volume),
                colorscale: 'Viridis',
                sizemode: 'diameter',
            },
            hoverinfo: 'text', // Only show the 'text' property on hover
            text: groupedData[item_name].map(e => 
            `Item: ${e.item_name}<br>Daily Orders: ${e.order_count}<br>Percent Profit: ${e.percent_profit}`
            ),
            name: formattedItemName // Set the trace name to item_name for it to appear in the legend
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
            text: `Percent Profit vs Total Order Count vs Market Volume`,
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
