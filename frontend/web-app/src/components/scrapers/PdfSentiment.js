import React, { useEffect, useState } from "react";
import {
  Container,
  Typography,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";

function PdfSentimentTable() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/pdf-sentiment")
      .then((res) => res.json())
      .then((json) => {
        const extractedRows = [];

        Object.entries(json).forEach(([title, content]) => {
          const lines = content.split("\n").filter(line => line.trim() !== "");

          lines.forEach((line) => {
            // Try to extract month-year + rest using regex
            const match = line.match(/^([A-Za-z]{3,9} \d{4}):?\s+(.*)/);
            if (match) {
              extractedRows.push({
                report: title,
                date: match[1],       // e.g., Apr 2025
                content: match[2],    // e.g., Consumer sentiment rose to 78.5
              });
            } 
          });
        });

        setRows(extractedRows);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load sentiment data", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <Container>
        <CircularProgress />
        <Typography>Loading PDF sentiment data...</Typography>
      </Container>
    );
  }

  return (
  <Container maxWidth="lg" sx={{ mt: 4 }}>
    <Typography variant="h5" gutterBottom>
      PDF Sentiment Report 
    </Typography>

    {Object.entries(
      rows.reduce((acc, row) => {
        acc[row.report] = acc[row.report] || [];
        acc[row.report].push(row);
        return acc;
      }, {})
    ).map(([reportTitle, reportRows]) => (
      <div key={reportTitle} style={{ marginBottom: "2rem" }}>
        <Typography variant="h6" gutterBottom>
          {reportTitle}
        </Typography>
        <TableContainer component={Paper} elevation={3}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: "bold" }}>Month</TableCell>
                <TableCell sx={{ fontWeight: "bold" }}>Content</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {reportRows.map((row, idx) => (
                <TableRow key={`${row.date}-${idx}`}>
                  <TableCell>{row.date}</TableCell>
                  <TableCell sx={{ whiteSpace: "pre-wrap" }}>{row.content}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    ))}
  </Container>
);

}

export default PdfSentimentTable;
