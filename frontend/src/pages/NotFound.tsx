import { useNavigate } from 'react-router-dom'
import { Typography, Button, Box } from '@mui/material'

export default function NotFound() {
  const navigate = useNavigate()

  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', p: 2 }}>
      <Typography variant="h1" sx={{ fontSize: '6rem', fontWeight: 'bold' }}>404</Typography>
      <Typography variant="h5" gutterBottom>Page Not Found</Typography>
      <Typography color="text.secondary" sx={{ mb: 3 }}>The page you're looking for doesn't exist.</Typography>
      <Button variant="contained" onClick={() => navigate('/dashboard')}>Go to Dashboard</Button>
    </Box>
  )
}
