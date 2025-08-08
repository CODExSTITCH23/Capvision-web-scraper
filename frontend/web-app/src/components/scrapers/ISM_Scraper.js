import React, { useEffect, useState } from "react";
import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Typography, Box, CircularProgress
} from "@mui/material";

const ISMData = () => {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/ism-data")
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      });
  }, []);

  const renderTable = (title, dataset) => (
    <Box key={title} mb={4}>
      <Typography variant="h6" gutterBottom>{title}</Typography>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              {dataset.length > 0 &&
                Object.keys(dataset[0]).map((col, idx) => (
                  <TableCell key={idx}><strong>{col}</strong></TableCell>
                ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {dataset.map((row, i) => (
              <TableRow key={i}>
                {Object.values(row).map((value, j) => (
                  <TableCell key={j}>{value}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box p={4}>
      {Object.entries(data).map(([title, dataset]) =>
        Array.isArray(dataset) ? renderTable(title, dataset) : (
          <Typography key={title} color="error">
            {dataset.error}
          </Typography>
        )
      )}
    </Box>
  );
};

export default ISMData;
