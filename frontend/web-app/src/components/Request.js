import React, { useState } from 'react';
import { 
  Button, 
  TextField, 
  Box, 
  Paper, 
  Typography,
  Container
} from '@mui/material';
import Swal from 'sweetalert2';
import axios from 'axios';

const RequestForm = () => {
  const [showForm, setShowForm] = useState(false);
  const [url, setUrl] = useState('');
  const [name, setName] = useState('');

  const handleSubmit = async () => {
    try {
      // Send request to our backend server
      const response = await axios.post('https://capvision-web-scraper.onrender.com', {
        url,
        name
      });

      console.log('Server Response:', response.data);

      // Show success message to user
      await Swal.fire({
        title: 'Request Sent!',
        text: 'This request is sent to the admin, Please wait for it to be approved.',
        icon: 'success',
        confirmButtonColor: '#4CAF50'
      });

      // Reset form
      setUrl('');
      setName('');
      setShowForm(false);
    } catch (error) {
      console.error('Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
      
      Swal.fire({
        title: 'Error!',
        text: error.response?.data?.error || 'Failed to send request. Please try again.',
        icon: 'error',
        confirmButtonColor: '#f44336'
      });
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 4 }}>
        {!showForm ? (
          <Button 
            variant="contained" 
            color="primary" 
            onClick={() => setShowForm(true)}
            fullWidth
          >
            Request New Scraping
          </Button>
        ) : (
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Submit Scraping Request
            </Typography>
            <Box component="form" sx={{ mt: 2 }}>
              <TextField
                fullWidth
                label="URL"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                margin="normal"
                required
              />
              <TextField
                fullWidth
                label="Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                margin="normal"
                required
              />
              <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSubmit}
                  disabled={!url || !name}
                >
                  Add
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => setShowForm(false)}
                >
                  Cancel
                </Button>
              </Box>
            </Box>
          </Paper>
        )}
      </Box>
    </Container>
  );
};

export default RequestForm; 