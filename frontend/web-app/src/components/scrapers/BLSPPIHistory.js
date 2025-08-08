import React, { useEffect, useState } from "react";
import {
  Typography,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";

export default function BLSPPIHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/bls-ppi-history")
      .then((res) => res.json())
      .then((data) => {
        setHistory(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <Container>
      {loading ? (
        <CircularProgress />
      ) : (
        <List>
          {history.map((item, idx) => (
            <React.Fragment key={idx}>
              <ListItem alignItems="flex-start">
                <ListItemText
                  primary={`[${item.timestamp}] ${item.label}`}
                  secondary={
                    <>
                      {item.data && item.data.map((table, tIdx) => (
                        <TableContainer component={Paper} sx={{ mt: 1, mb: 1 }} key={tIdx}>
                          <Table size="small">
                            <TableHead>
                              <TableRow>
                                {table.headers && table.headers.map((key) => (
                                  <TableCell key={key}>{key}</TableCell>
                                ))}
                              </TableRow>
                            </TableHead>
                            <TableBody>
                              {table.rows && table.rows.map((row, i) => (
                                <TableRow key={i}>
                                  {table.headers.map((header, j) => (
                                    <TableCell key={j}>{row[header]}</TableCell>
                                  ))}
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </TableContainer>
                      ))}
                    </>
                  }
                />
              </ListItem>
              <Divider />
            </React.Fragment>
          ))}
        </List>
      )}
    </Container>
  );
} 