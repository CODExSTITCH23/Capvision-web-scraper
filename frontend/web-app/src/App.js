import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Navigation';
import { AppBar, Toolbar, Typography } from '@mui/material';
import './components/styles.css';
import PdfSentiment from './components/scrapers/PdfSentiment';
import Ism from './components/scrapers/ISM_Scraper';
import ScrapeRequest from './components/scrapers/ScrapeRequest';
import ScrapedHistory from "./components/ScrapedHistory";
import { useParams } from 'react-router-dom';
import ScraperScheduler from './components/scrapers/ScraperScheduler';
import PSEIndexHistory from './components/scrapers/PSEIndexHistory';
import BLSCPIHistory from './components/scrapers/BLSCPIHistory';
import PdfSentimentHistory from './components/scrapers/PdfSentimentHistory';
import ISMHistory from './components/scrapers/ISMHistory';
import BLSPPIHistory from './components/scrapers/BLSPPIHistory';
import JOLTSHistory from './components/scrapers/JOLTSHistory';
import ConferenceBoardHistory from './components/scrapers/ConferenceBoardHistory';

// Map of view names to components
const componentMap = {
  pdfsentiment: <PdfSentiment />,
  ism: <Ism />
};

// Wrapper component to dynamically load component based on name
const ViewRouter = () => {
  const { name } = useParams();
  const component = componentMap[name?.toLowerCase()];
  return component || <h2 style={{ padding: '1rem' }}>No view found for: {name}</h2>;
};

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <Router>
      <div className="app-container">
        <AppBar
          position="fixed"
          className={`app-bar ${sidebarOpen ? 'expanded' : 'collapsed'}`}
        >
          <Toolbar sx={{ backgroundColor: '#ffffff' }}>
            <Typography variant="h6" noWrap color='black'>
              Capvision Scraper
            </Typography>
          </Toolbar>
        </AppBar>

        <Dashboard open={sidebarOpen} setOpen={setSidebarOpen} />

        <main className={`main-content ${sidebarOpen ? 'shifted' : ''}`}>
          <Toolbar />
          <Routes>
            <Route path="/" element={<h1>Welcome to Capvision Scraper</h1>} />
            <Route path="/ScrapeRequest" element={<ScrapeRequest />} />
            <Route path="/labor" element={<PdfSentiment/>} />
            <Route path="/business" element={<Ism />} />
            <Route path="/scrape-history" element={<ScrapedHistory />} />
            <Route path="/scheduler" element={<ScraperScheduler />} />
            <Route path="/pse-index-history" element={<PSEIndexHistory />} />
            <Route path="/bls-cpi-history" element={<BLSCPIHistory />} />
            <Route path="/bls-ppi-history" element={<BLSPPIHistory />} />
            <Route path="/jolts-history" element={<JOLTSHistory />} />
            <Route path="/conference-board-history" element={<ConferenceBoardHistory />} />
            <Route path="/pdf-sentiment-history" element={<PdfSentimentHistory />} />
            <Route path="/ism-history" element={<ISMHistory />} />
            <Route path="/view/:name" element={<ViewRouter />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
