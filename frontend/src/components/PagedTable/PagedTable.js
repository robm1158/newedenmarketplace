import React, { useState } from 'react';

function PagedTable({ data, headers, rowsPerPage = 10 }) {
    const [currentPage, setCurrentPage] = useState(0);
    
    const totalPages = Math.ceil(data.length / rowsPerPage);
    
    const currentData = data.slice(currentPage * rowsPerPage, (currentPage + 1) * rowsPerPage);

    return (
        <div>
            <table>
                <thead>
                    <tr>
                        {headers.map(header => <th key={header}>{header}</th>)}
                    </tr>
                </thead>
                <tbody>
                    {currentData.map((row, rowIndex) => (
                        <tr key={rowIndex}>
                            {headers.map(header => <td key={header}>{row[header]}</td>)}
                        </tr>
                    ))}
                </tbody>
            </table>
            <div>
                {currentPage > 0 && <button onClick={() => setCurrentPage(currentPage - 1)}>Previous</button>}
                {currentPage < totalPages - 1 && <button onClick={() => setCurrentPage(currentPage + 1)}>Next</button>}
            </div>
        </div>
    );
}

export default PagedTable;
