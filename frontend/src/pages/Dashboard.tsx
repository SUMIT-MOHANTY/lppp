import { Typography, Grid, Paper } from '@mui/material'

export default function Dashboard() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>Dashboard</Typography>
      <Grid container spacing={3}>
        {['Total Users', 'Active Sessions', 'Recent Activity', 'System Status'].map((title, i) => (
          <Grid item xs={12} sm={6} md={3} key={i}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="subtitle2" color="text.secondary">{title}</Typography>
              <Typography variant="h4">{Math.floor(Math.random() * 100)}</Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  )
}

import { Box } from '@mui/material'
