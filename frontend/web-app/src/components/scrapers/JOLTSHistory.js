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
  Box,
  Chip,
  Grid,
  Card,
  CardContent
} from "@mui/material";

export default function JOLTSHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/jlt-history")
      .then((res) => res.json())
      .then((data) => {
        setHistory(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        JOLTS - Job Openings and Labor Turnover Survey
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Latest Numbers from Bureau of Labor Statistics
      </Typography>
      
      {loading ? (
        <Box display="flex" justifyContent="center" mt={4}>
          <CircularProgress />
        </Box>
      ) : (
        <List>
          {history.map((item, idx) => (
            <React.Fragment key={idx}>
              <ListItem alignItems="flex-start">
                <Paper sx={{ width: '100%', p: 2 }}>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h6" color="primary">
                      {item.label}
                    </Typography>
                    <Chip 
                      label={new Date(item.timestamp).toLocaleDateString()} 
                      variant="outlined" 
                      size="small"
                    />
                  </Box>
                  
                  {item.data && item.data.length > 0 ? (
                    <Grid container spacing={2}>
                      {item.data.map((dataPoint, dataIdx) => (
                        <Grid item xs={12} sm={6} md={4} key={dataIdx}>
                          <Card variant="outlined" sx={{ height: '100%' }}>
                            <CardContent>
                              <Typography variant="h6" color="secondary" gutterBottom>
                                {dataPoint.data_value}
                              </Typography>
                              <Typography variant="body2" color="text.primary" gutterBottom>
                                {dataPoint.title}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                {dataPoint.period} {dataPoint.year}
                              </Typography>
                            </CardContent>
                          </Card>
                        </Grid>
                      ))}
                    </Grid>
                  ) : item.value ? (
                    // Backward compatibility for old single-value format
                    <Typography variant="h6" color="primary">
                      {item.value}
                    </Typography>
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No data available
                    </Typography>
                  )}
                  
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
                    Last updated: {new Date(item.timestamp).toLocaleString()}
                  </Typography>
                </Paper>
              </ListItem>
              {idx < history.length - 1 && <Divider />}
            </React.Fragment>
          ))}
          {history.length === 0 && (
            <ListItem>
              <ListItemText primary="No JOLTS data available." />
            </ListItem>
          )}
        </List>
      )}
    </Container>
  );
} 