import React, { useEffect, useState } from "react";
import {
  Card,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Box,
  Divider,
  IconButton
} from '@mui/material';
import ScheduleIcon from '@mui/icons-material/Schedule';
import DescriptionIcon from '@mui/icons-material/Description';
import AssessmentIcon from '@mui/icons-material/Assessment';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import TableChartIcon from '@mui/icons-material/TableChart';

const MODULES = [
  { value: "pdf_sentiment", label: "PDF Sentiment", icon: <DescriptionIcon /> },
  { value: "ism_data", label: "ISM Data", icon: <AssessmentIcon /> },
  { value: "pse_index", label: "PSE Index", icon: <ShowChartIcon /> },
  { value: "bls_cpi", label: "BLS CPI Table A", icon: <TableChartIcon /> },
  { value: "bls_ppi", label: "BLS PPI Latest Numbers", icon: <TableChartIcon /> },
  { value: "conference_board", label: "Conference Board LEI", icon: <ShowChartIcon /> },
  { value: "jlt_scraper", label: "JOLTS Latest Numbers", icon: <AssessmentIcon /> },
  { value: "pmi_spglobal", label: "PMI S&P Global", icon: <ShowChartIcon /> },
  // Add more as needed
];

export default function ScraperScheduler() {
  const [schedules, setSchedules] = useState({});
  const [selectedModule, setSelectedModule] = useState(""); // No default selected
  const [time, setTime] = useState("00:00");
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/api/scraper-schedules")
      .then(res => res.json())
      .then(setSchedules);
  }, []);

  const handleSave = () => {
    const newSchedules = { ...schedules, [selectedModule]: time };
    fetch("http://localhost:8000/api/scraper-schedules", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newSchedules),
    })
      .then(res => res.json())
      .then(() => {
        fetch("http://localhost:8000/api/scraper-schedules")
          .then(res => res.json())
          .then(setSchedules);
        // Reset form after update
        setIsEditing(false);
        setSelectedModule("");
        setTime("00:00");
      });
  };

  const handleEdit = (mod, t) => {
    setSelectedModule(mod);
    setTime(t);
    setIsEditing(true);
  };

  const handleDelete = (mod) => {
    const newSchedules = { ...schedules };
    delete newSchedules[mod];
    fetch("http://localhost:8000/api/scraper-schedules", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newSchedules),
    })
      .then(res => res.json())
      .then(() => {
        fetch("http://localhost:8000/api/scraper-schedules")
          .then(res => res.json())
          .then(setSchedules);
        // Reset form if deleting the one being edited
        if (isEditing && selectedModule === mod) {
          setIsEditing(false);
          setSelectedModule("");
          setTime("00:00");
        }
      });
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="flex-start" mt={4}>
      <Card sx={{ minWidth: 400, maxWidth: 500 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            <ScheduleIcon sx={{ verticalAlign: 'middle', mr: 1 }} /> Scraper Scheduler
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <Box display="flex" gap={2} alignItems="center" mb={2}>
            <FormControl sx={{ minWidth: 150 }} size="small">
              <InputLabel id="module-label">Module</InputLabel>
              <Select
                labelId="module-label"
                value={selectedModule}
                label="Module"
                onChange={e => setSelectedModule(e.target.value)}
                disabled={isEditing}
              >
                <MenuItem value="" disabled>
                  Select One
                </MenuItem>
                {MODULES.map(m => (
                  <MenuItem key={m.value} value={m.value}>
                    <Box display="flex" alignItems="center" gap={1}>
                      {m.icon} {m.label}
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              label="Time"
              type="time"
              size="small"
              value={time}
              onChange={e => setTime(e.target.value)}
              InputLabelProps={{ shrink: true }}
              inputProps={{ step: 60 }}
            />
            <Button variant="contained" color="primary" onClick={handleSave}>
              {isEditing ? "Update" : "Save"}
            </Button>
          </Box>
          <Typography variant="h6" gutterBottom>
            Current Schedules
          </Typography>
          <List>
            {Object.entries(schedules).length === 0 && (
              <ListItem>
                <ListItemText primary="No schedules set." />
              </ListItem>
            )}
            {Object.entries(schedules).map(([mod, t]) => {
              const module = MODULES.find(m => m.value === mod);
              return (
                <ListItem key={mod} secondaryAction={
                  <Box>
                    <IconButton edge="end" aria-label="edit" onClick={() => handleEdit(mod, t)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(mod)}>
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                }>
                  <ListItemIcon>
                    {module?.icon || <ScheduleIcon />}
                  </ListItemIcon>
                  <ListItemText
                    primary={module?.label || mod}
                    secondary={`Time: ${t}`}
                  />
                </ListItem>
              );
            })}
          </List>
        </CardContent>
      </Card>
    </Box>
  );
} 