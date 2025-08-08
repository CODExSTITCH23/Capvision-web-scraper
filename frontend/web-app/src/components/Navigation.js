import React, { useState } from 'react';
import {
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Collapse,
} from '@mui/material';
import {
  ChevronLeft as ChevronLeftIcon,
  Home as HomeIcon,
  Handyman as HandymanIcon,
  ExpandLess,
  ExpandMore,
  Work as BusinessIcon,
  Gavel as LaborIcon,
  LocationCity as RegionalIcon,
  FileOpen as Request,
  History as HistoryIcon,
  Schedule as ScheduleIcon,
  ShowChart as ShowChartIcon,
  TableChart as TableChartIcon
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

import logoExpanded from './images/Capvision_logo_expanded.png';
import logoCollapsed from './images/Collapsed.png';

export default function Sidebar({ open, setOpen }) {
  const [scraperOpen, setScraperOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const toggleDrawer = () => setOpen(!open);
  const defaultColor = '#ffffff';
  const activeColor = '#3769a0';

  const isActive = (path) => location.pathname === path;
  const getColor = (path) => (isActive(path) ? activeColor : defaultColor);

  return (
    <Drawer
      variant="permanent"
      className={`drawer ${open ? 'open' : 'collapsed'}`}
      classes={{
        paper: `drawer-paper ${open ? 'open' : 'collapsed'}`,
      }}
    >
      <Toolbar className="toolbar">
        <IconButton onClick={toggleDrawer}>
          <div className="logo-container">
            <img
              src={open ? logoExpanded : logoCollapsed}
              alt="Logo"
              className="logo-image"
            />
          </div>
          {open && <ChevronLeftIcon sx={{ color: defaultColor }} />}
        </IconButton>
      </Toolbar>

      <List>
        <ListItem button onClick={() => navigate("/")}>
          <ListItemIcon>
            <HomeIcon sx={{ color: getColor("/") }} />
          </ListItemIcon>
          {open && (
            <ListItemText
              primary="Home"
              primaryTypographyProps={{ sx: { color: getColor("/") } }}
            />
          )}
        </ListItem>

        <ListItem button onClick={() => navigate("/ScrapeRequest")}>
          <ListItemIcon>
            <Request sx={{ color: getColor("/ScrapeRequest") }} />
          </ListItemIcon>
          {open && (
            <ListItemText
              primary="Scrape Request"
              primaryTypographyProps={{ sx: { color: getColor("/ScrapeRequest") } }}
            />
          )}
        </ListItem>

        <ListItem
            button
            onClick={() => navigate("/scrape-history")}
            >
            <ListItemIcon>
              <HistoryIcon sx={{ color: getColor("/scrape-history") }} />
            </ListItemIcon>
             {open && (
            <ListItemText
              primary="Scrape History"
              primaryTypographyProps={{ sx: { color: getColor("/scrape-history") } }}
            />
            )}
            </ListItem>

              <ListItem
              button
              onClick={() => navigate("/scheduler")}
            >
              <ListItemIcon>
                <ScheduleIcon sx={{ color: getColor("/scheduler") }} />
              </ListItemIcon>
              {open && (
              <ListItemText
                primary="Scraper Scheduler"
                primaryTypographyProps={{ sx: { color: getColor("/scheduler") } }}
              />
              )}
            </ListItem>

        <ListItem button onClick={() => setScraperOpen(!scraperOpen)}>
          <ListItemIcon>
            <HandymanIcon sx={{ color: defaultColor }} />
          </ListItemIcon>
          {open && (
            <ListItemText
              primary="Scraper"
              primaryTypographyProps={{ sx: { color: defaultColor } }}
            />
          )}
          {open &&
            (scraperOpen ? (
              <ExpandLess sx={{ color: defaultColor }} />
            ) : (
              <ExpandMore sx={{ color: defaultColor }} />
            ))}
        </ListItem>

        <Collapse in={scraperOpen} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <ListItem button sx={{ pl: 4 }} onClick={() => navigate("/labor")}>
              <ListItemIcon>
                <LaborIcon sx={{ color: getColor("/labor") }} />
              </ListItemIcon>
              <ListItemText
                primary="Labor"
                primaryTypographyProps={{ sx: { color: getColor("/labor") } }}
              />
            </ListItem>

            <ListItem
              button
              sx={{ pl: 4 }}
              onClick={() => navigate("/business")}
            >
              <ListItemIcon>
                <BusinessIcon sx={{ color: getColor("/business") }} />
              </ListItemIcon>
              <ListItemText
                primary="Business"
                primaryTypographyProps={{ sx: { color: getColor("/business") } }}
              />
            </ListItem>

            <ListItem
              button
              sx={{ pl: 4 }}
              onClick={() => navigate("/regional")}
            >
              <ListItemIcon>
                <RegionalIcon sx={{ color: getColor("/regional") }} />
              </ListItemIcon>
              <ListItemText
                primary="Regional Feds"
                primaryTypographyProps={{ sx: { color: getColor("/regional") } }}
              />
            </ListItem>

              <ListItem
              button
              sx={{ pl: 4 }}
              onClick={() => navigate("/pse-index-history")}
            >
              <ListItemIcon>
                <ShowChartIcon sx={{ color: getColor("/pse-index-history") }} />
              </ListItemIcon>
              <ListItemText
                primary="PSE Index History"
                primaryTypographyProps={{ sx: { color: getColor("/pse-index-history") } }}
              />
            </ListItem>

            <ListItem
              button
              sx={{ pl: 4 }}
              onClick={() => navigate("/bls-cpi-history")}
            >
              <ListItemIcon>
                <TableChartIcon sx={{ color: getColor("/bls-cpi-history") }} />
              </ListItemIcon>
              <ListItemText
                primary="BLS CPI "
                primaryTypographyProps={{ sx: { color: getColor("/bls-cpi-history") } }}
              />
            </ListItem>
            <ListItem
              button
              sx={{ pl: 4 }}
              onClick={() => navigate("/bls-ppi-history")}
            >
              <ListItemIcon>
                <TableChartIcon sx={{ color: getColor("/bls-ppi-history") }} />
              </ListItemIcon>
              <ListItemText
                primary="BLS PPI "
                primaryTypographyProps={{ sx: { color: getColor("/bls-ppi-history") } }}
              />
            </ListItem>

            <ListItem
              button
              sx={{ pl: 4 }}
              onClick={() => navigate("/jolts-history")}
            >
              <ListItemIcon>
                <BusinessIcon sx={{ color: getColor("/jolts-history") }} />
              </ListItemIcon>
              <ListItemText
                primary="JOLTS "
                primaryTypographyProps={{ sx: { color: getColor("/jolts-history") } }}
              />
            </ListItem>

            <ListItem
              button
              sx={{ pl: 4 }}
              onClick={() => navigate("/conference-board-history")}
            >
              <ListItemIcon>
                <ShowChartIcon sx={{ color: getColor("/conference-board-history") }} />
              </ListItemIcon>
              <ListItemText
                primary="Conference Board "
                primaryTypographyProps={{ sx: { color: getColor("/conference-board-history") } }}
              />
            </ListItem>
          </List>
        </Collapse>
      </List>
    </Drawer>
  );
}
