import { createContext, useContext, useState, useMemo, ReactNode } from 'react'
import { ThemeProvider as MuiThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'

interface ThemeContextType {
  mode: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [mode, setMode] = useState<'light' | 'dark'>(() => {
    const saved = localStorage.getItem('themeMode')
    return (saved as 'light' | 'dark') || 'light'
  })

  const toggleTheme = () => {
    setMode(prev => {
      const newMode = prev === 'light' ? 'dark' : 'light'
      localStorage.setItem('themeMode', newMode)
      return newMode
    })
  }

  const theme = useMemo(() => createTheme({
    palette: {
      mode,
      primary: { main: '#1976d2' },
      secondary: { main: '#dc004e' },
      background: { default: mode === 'light' ? '#f5f5f5' : '#121212' }
    },
    typography: {
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    },
    components: {
      MuiButton: { styleOverrides: { root: { textTransform: 'none' } } }
    }
  }), [mode])

  return (
    <ThemeContext.Provider value={{ mode, toggleTheme }}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  )
}

export function useThemeMode() {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useThemeMode must be used within ThemeProvider')
  return context
}
