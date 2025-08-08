import React, { useState } from 'react';
import {
  Box, TextField, Button, Card, CardContent, Typography,
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, IconButton, Paper
} from '@mui/material';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';

export default function WebsiteList() {
  const [nameInput, setNameInput] = useState('');
  const [urlInput, setUrlInput] = useState('');
  const [websites, setWebsites] = useState([]);
  const [showInput, setShowInput] = useState(false);

  const notifySlackAdmin = async (name, url) => {
    try {
      await fetch('/api/notify-slack', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, url }),
      });
    } catch (error) {
      console.error('Failed to notify Slack:', error);
    }
  };

  const handleAddWebsite = async () => {
    if (nameInput.trim() && urlInput.trim()) {
      const newEntry = {
        name: nameInput.trim(),
        url: urlInput.trim(),
        status: 'pending', // Set initial status
      };
      setWebsites([...websites, newEntry]);
      await notifySlackAdmin(newEntry.name, newEntry.url);
      setNameInput('');
      setUrlInput('');
      setShowInput(false); // hide input after adding
    }
  };

  const handleVisit = (url) => {
    const formattedUrl = url.startsWith('http') ? url : `https://${url}`;
    window.open(formattedUrl, '_blank');
  };

  const handleViewContent = (url) => {
    alert(`Display or fetch content from: ${url}`);
  };

  const handleDelete = (index) => {
    const updated = [...websites];
    updated.splice(index, 1);
    setWebsites(updated);
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 5 }}>
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5">Labor URL Manager</Typography>
            <Button variant="outlined" onClick={() => setShowInput(!showInput)}>
              {showInput ? 'Cancel' : 'Add New'}
            </Button>
          </Box>

          {showInput && (
            <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
              <TextField
                fullWidth
                label="Enter name"
                variant="outlined"
                value={nameInput}
                onChange={(e) => setNameInput(e.target.value)}
              />
              <TextField
                fullWidth
                label="Enter website URL"
                variant="outlined"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
              />
              <Button variant="contained" onClick={handleAddWebsite}>
                Add
              </Button>
            </Box>
          )}

          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell><strong>Website Name</strong></TableCell>
                  <TableCell><strong>Status</strong></TableCell>
                  <TableCell align="center"><strong>Visit</strong></TableCell>
                  <TableCell align="center"><strong>View</strong></TableCell>
                  <TableCell align="center"><strong>Delete</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {websites.map((site, index) => (
                  <TableRow key={index}>
                    <TableCell>{site.name}</TableCell>
                    <TableCell>
                      {site.status === 'pending' ? (
                        <Typography color="orange">Waiting for admin to approve the URL / Website</Typography>
                      ) : (
                        site.status
                      )}
                    </TableCell>
                    <TableCell align="center">
                      <IconButton onClick={() => handleVisit(site.url)} aria-label="visit">
                        <OpenInNewIcon />
                      </IconButton>
                    </TableCell>
                    <TableCell align="center">
                      <IconButton onClick={() => handleViewContent(site.url)} aria-label="view">
                        <VisibilityIcon />
                      </IconButton>
                    </TableCell>
                    <TableCell align="center">
                      <IconButton onClick={() => handleDelete(index)} aria-label="delete">
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
}
