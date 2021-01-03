import React, { useReducer, useEffect } from 'react'
import { ThemeProvider } from '@material-ui/core/styles'
import CssBaseline from '@material-ui/core/CssBaseline'
import theme from './themes/default'

//Contexts
import { Auth } from './contexts/auth'

//Reducers
import { login } from './reducers/auth'

//Containers
import Home from './containers/Home'
import Login from './containers/Login'

function App() {

  const initialValues = {
    is_authenticated : false,
    user: null,
    token: null
  }

  const [state, dispatch] = useReducer(login, initialValues)

  useEffect (() => {

    const access_token = JSON.parse(localStorage.getItem('access_token') || null)
    const user = JSON.parse(localStorage.getItem('user') || null)

    if(user && access_token){
      dispatch({
        type: 'LOGIN',
        payload: {
          access_token,
          user          
        }
      })
    }

  }, [])

  return (
    <ThemeProvider theme = {theme}>
      <CssBaseline />
      <Auth.Provider value={{state, dispatch}}>
        {state.is_authenticated ?
          <Home /> : <Login />
        }
        
      </Auth.Provider>
    </ThemeProvider>
  )
}

export default App
