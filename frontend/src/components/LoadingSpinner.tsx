import { CircularProgress, Box } from '@mui/material'

interface Props {
  fullScreen?: boolean
  message?: string
}

export function LoadingSpinner({ fullScreen, message }: Props) {
  const containerStyle = fullScreen
    ? { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(255,255,255,0.8)' }
    : { display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }

  return (
    <Box sx={containerStyle}>
      <CircularProgress />
      {message && <Box sx={{ ml: 2 }}>{message}</Box>}
    </Box>
  )
}
