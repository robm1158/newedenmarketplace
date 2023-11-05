// Dashboard.js
import React from 'react';
import Graph from '../Graph/Graph';
import BubbleGraph from '../BubbleGraph/BubbleGraph';
import PagedTable from '../PagedTable/PagedTable';

function Dashboard({ graphData, selectedItemName, nonBuyOrders, bubbleGraphData, buyOrders, transformDataWithLocation }) {
    return (
        <div>
            <div style={{ display: "flex" }}>
                {graphData && <Graph data={graphData} itemName={selectedItemName} />}
            </div>
            <div className="flex-container" style={{ display: 'flex', justifyContent: 'space-between' }}>
                {nonBuyOrders && nonBuyOrders.length > 0 && (
                    <div style={{ flex: 1 }}>
                        <h2>Sell Orders</h2>
                        <PagedTable data={transformDataWithLocation(nonBuyOrders)} headers={[
                            { displayName: 'Date', dataKey: 'issued' },
                            { displayName: 'Order ID', dataKey: 'order_id' },
                            { displayName: 'Location', dataKey: 'location_id' },
                            { displayName: 'Price', dataKey: 'price' },
                            { displayName: 'Volume', dataKey: 'volume_remain' }
                        ]} />
                    </div>
                )}
                <div style={{ flex: 1 }}>
                    {bubbleGraphData && <BubbleGraph data={bubbleGraphData} itemName={selectedItemName} />}
                </div>
            </div>
            <div className="flex-container" style={{ display: 'flex', justifyContent: 'left', marginTop: '-110px' }}>
                {buyOrders && buyOrders.length > 0 && (
                    <div>
                        <h2>Buy Orders</h2>
                        <PagedTable data={transformDataWithLocation(buyOrders)} headers={[
                            { displayName: 'Date', dataKey: 'issued' },
                            { displayName: 'Order ID', dataKey: 'order_id' },
                            { displayName: 'Location', dataKey: 'location_id' },
                            { displayName: 'Price', dataKey: 'price' },
                            { displayName: 'Volume', dataKey: 'volume_remain' }
                        ]} />
                    </div>
                )}
            </div>
        </div>
    );
}

export default Dashboard;
