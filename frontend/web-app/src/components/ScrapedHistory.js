import React from "react";
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';

export default function ScrapedHistory() {
  // Helper to open a route in a new tab
  const openInNewTab = (route) => {
    window.open(route, '_blank', 'noopener');
  };

  return (
    <Container>
      <Button
        variant="contained"
        color="primary"
        sx={{ mt: 2, mb: 2, textTransform: 'none', maxWidth: 350, width: '100%', display: 'block', mx: 'auto' }}
        onClick={() => openInNewTab('/pdf-sentiment-history')}
      >
        PDF Sentiment History
      </Button>
      <Button
        variant="contained"
        color="primary"
        sx={{ mt: 2, mb: 2, textTransform: 'none', maxWidth: 350, width: '100%', display: 'block', mx: 'auto' }}
        onClick={() => openInNewTab('/ism-history')}
      >
        ISM PMI History
      </Button>
      <Button
        variant="contained"
        color="primary"
        sx={{ mt: 2, mb: 2, textTransform: 'none', maxWidth: 350, width: '100%', display: 'block', mx: 'auto' }}
        onClick={() => openInNewTab('/pse-index-history')}
      >
        PSE Index History
      </Button>
      <Button
        variant="contained"
        color="primary"
        sx={{ mt: 2, mb: 2, textTransform: 'none', maxWidth: 350, width: '100%', display: 'block', mx: 'auto' }}
        onClick={() => openInNewTab('/bls-cpi-history')}
      >
        BLS CPI Table A History
      </Button>
    </Container>
  );
}
