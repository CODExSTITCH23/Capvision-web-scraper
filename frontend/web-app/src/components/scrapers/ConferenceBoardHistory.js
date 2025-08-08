import React, { useEffect, useState } from "react";
import {
  Typography,
  CircularProgress,
  List,
  ListItem,
  Divider,
  Container,
  Paper,
  Box,
  Chip,
  Grid,
  Card,
  CardContent
} from "@mui/material";
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat';

export default function ConferenceBoardHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/conference-board-history")
      .then((res) => res.json())
      .then((data) => {
        setHistory(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const getTrendIcon = (percentage) => {
    if (percentage.includes('+')) {
      return <TrendingUpIcon sx={{ color: 'green', mr: 1 }} />;
    } else if (percentage.includes('-')) {
      return <TrendingDownIcon sx={{ color: 'red', mr: 1 }} />;
    } else {
      return <TrendingFlatIcon sx={{ color: 'gray', mr: 1 }} />;
    }
  };

  const getTrendColor = (percentage) => {
    if (percentage.includes('+')) {
      return 'success';
    } else if (percentage.includes('-')) {
      return 'error';
    } else {
      return 'default';
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Conference Board - Leading Economic Indicators
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Global Economic Performance Indicators (LEI)
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
                      {item.data.map((indicator, dataIdx) => (
                        <Grid item xs={12} sm={6} md={4} lg={3} key={dataIdx}>
                          <Card variant="outlined" sx={{ height: '100%' }}>
                            <CardContent>
                              <Box display="flex" alignItems="center" mb={1}>
                                {getTrendIcon(indicator.percentage)}
                                <Chip 
                                  label={indicator.percentage} 
                                  color={getTrendColor(indicator.percentage)}
                                  size="small"
                                />
                              </Box>
                              <Typography variant="h6" gutterBottom>
                                {indicator.region}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                {indicator.indicator}
                              </Typography>
                            </CardContent>
                          </Card>
                        </Grid>
                      ))}
                    </Grid>
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No indicator data available
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
              <Typography variant="body1" color="text.secondary">
                No Conference Board data available.
              </Typography>
            </ListItem>
          )}
        </List>
      )}
    </Container>
  );
} 