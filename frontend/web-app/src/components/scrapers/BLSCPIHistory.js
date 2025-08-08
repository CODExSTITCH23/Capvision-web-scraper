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

export default function BLSCPIHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/bls-cpi-history")
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
                    <TableContainer component={Paper} sx={{ mt: 1, mb: 1 }}>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            {item.data && item.data[0] &&
                              Object.keys(item.data[0]).map((key) => (
                                <TableCell key={key}>{key}</TableCell>
                              ))}
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {item.data && item.data.map((row, i) => (
                            <TableRow key={i}>
                              {Object.values(row).map((val, j) => (
                                <TableCell key={j}>{val}</TableCell>
                              ))}
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
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