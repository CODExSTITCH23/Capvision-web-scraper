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
} from "@mui/material";

export default function PdfSentimentHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/pdf-sentiment-history")
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
                  primary={`[${item.timestamp}] ${item.title}`}
                  secondary={
                    <Paper sx={{ p: 2, mt: 1, mb: 1, maxHeight: 300, overflow: 'auto', whiteSpace: 'pre-wrap' }}>
                      {typeof item.content === "string"
                        ? item.content.slice(0, 5000) + (item.content.length > 5000 ? "..." : "")
                        : "Error or malformed content"}
                    </Paper>
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