import React from 'react';

const DataTable = ({ data }) => {
  return (
    <div>
      <h2>Item Data:</h2>
      <table border="1">
        <thead>
          <tr>
            <th>Issued</th>
            <th>Price</th>
            <th>Is Buy Order</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.issued}</td>
              <td>{item.price}</td>
              <td>{item.is_buy_order ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;