import React, { useState } from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  TableSortLabel,
} from '@mui/material';

function PagedTable({ data, headers, rowsPerPageOptions = [5, 10, 15] }) {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(rowsPerPageOptions[0]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });



    // Function to format the date
  function formatDate(dateString) {
    // Create a new Date object using the date string
    const date = new Date(dateString);

    // Format the date and time as 'YYYY-MM-DD HH:MM:SS'
    // You can adjust the formatting as needed
    return date.toISOString().replace('T', ' ').replace(/\..+/, '');
  }

  // Function to format the price
  function formatPrice(price) {
    // Format the price as a string with commas and add ' ISK' at the end
    const numberPrice = parseFloat(price).toFixed(2);
    // This will handle integer prices; if you have decimal prices, you might need to adjust
    return Number(numberPrice).toLocaleString() + ' ISK';
  }

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = event => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedData = React.useMemo(() => {
    const sortableItems = [...data];
    if (sortConfig.key !== null) {
      sortableItems.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [data, sortConfig]);

  const pagedData = sortedData.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

  return (
    <Paper>
      <TableContainer>
        <Table stickyHeader size='small'>
          <TableHead>
            <TableRow>
              {headers.map(header => (
                <TableCell key={header.dataKey}>
                  <TableSortLabel
                    active={sortConfig.key === header.dataKey}
                    direction={sortConfig.key === header.dataKey ? sortConfig.direction : 'asc'}
                    onClick={() => handleSort(header.dataKey)}
                  >
                    {header.displayName}
                  </TableSortLabel>
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {pagedData.map((row, rowIndex) => (
              <TableRow hover key={rowIndex}>
                {headers.map(header => (
                  <TableCell key={`${rowIndex}-${header.dataKey}`}>
                    {header.dataKey === 'issued'
                      ? formatDate(row[header.dataKey])
                      : header.dataKey === 'price'
                      ? formatPrice(row[header.dataKey])
                      : row[header.dataKey]}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={rowsPerPageOptions}
        component="div"
        count={data.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
}

export default PagedTable;