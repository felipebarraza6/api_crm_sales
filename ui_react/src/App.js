import React from 'react'

import { ThemeProvider } from '@material-ui/core/styles'
import CssBaseline from '@material-ui/core/CssBaseline'
import theme from './themes/default'


function App() {
  return (
    <ThemeProvider theme = {theme}>
      <CssBaseline />

    </ThemeProvider>
  )
}

export default App
