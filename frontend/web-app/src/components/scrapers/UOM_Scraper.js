import React, { useState } from 'react';
import {
  Box, TextField, Button, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow, Paper,
  IconButton, Typography
} from '@mui/material';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';
import { useNavigate } from 'react-router-dom';

export default function WebsiteList() {
  const [inputName, setInputName] = useState('');
  const [inputURL, setInputURL] = useState('');
  const [websites, setWebsites] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const navigate = useNavigate();

  const handleAddWebsite = () => {
    if (inputName.trim() && inputURL.trim()) {
      setWebsites([...websites, { name: inputName.trim(), url: inputURL.trim() }]);
      setInputName('');
      setInputURL('');
      setShowForm(false);
    }
  };

  const handleVisit = (url) => {
    const formattedUrl = url.startsWith('http') ? url : `https://${url}`;
    window.open(formattedUrl, '_blank');
  };

  const handleDelete = (index) => {
    const updated = [...websites];
    updated.splice(index, 1);
    setWebsites(updated);
  };

  const handleViewContent = (name) => {
    // Navigate to a component using a name-based path
    navigate(`/view/${encodeURIComponent(name)}`);
  };

  return (
    <Box sx={{ maxWidth: 900, mx: 'auto', mt: 5, p: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">Labor URL Manager</Typography>
        <Button variant="contained" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Add New'}
        </Button>
      </Box>

      {showForm && (
        <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
          <TextField
            label="Name"
            value={inputName}
            onChange={(e) => setInputName(e.target.value)}
            fullWidth
          />
          <TextField
            label="URL"
            value={inputURL}
            onChange={(e) => setInputURL(e.target.value)}
            fullWidth
          />
          <Button variant="contained" onClick={handleAddWebsite}>
            Add
          </Button>
        </Box>
      )}

      <Paper elevation={3}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>Name</strong></TableCell>
                <TableCell><strong>Actions</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {websites.map((site, index) => (
                <TableRow key={index}>
                  <TableCell>{site.name}</TableCell>
                  <TableCell>
                    <IconButton onClick={() => handleVisit(site.url)}><OpenInNewIcon /></IconButton>
                    <IconButton onClick={() => handleViewContent(site.name)}><VisibilityIcon /></IconButton>
                    <IconButton onClick={() => handleDelete(index)}><DeleteIcon /></IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
}
