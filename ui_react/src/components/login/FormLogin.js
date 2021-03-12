// React
import React from 'react'
import { useState, useReducer } from 'react'

// Material
import {  Typography, Button, Grid, TextField } from '@material-ui/core'
import { makeStyles } from '@material-ui/styles'
import { FormControl, CircularProgress } from '@material-ui/core'
import { Alert } from '@material-ui/lab'

// Reducers
import { login } from '../../reducers/auth'

// Actions
import { AUTHENTICATION } from '../../actions/auth/authentication'

// Context
import { Auth } from '../../contexts/auth'


const FormLogin = () => {        

    const classes = useStyles()

    const { dispatch: dispatchApp } = React.useContext(Auth)

    const [state, dispatch] = useReducer(login, {
        errors: null,       
        error_email:false,
        error_password:false,
        is_loading: false
    })
    const [valuesForm, setValues] = useState({})    
    const [status, setStatus] = useState({
        email_disabled: false,
        password_disabled: true,                
    })

    function onChange (values) { 
        
        const {name, value: new_value} = values.target        
        
        if (!valuesForm.email){
            setStatus({...status, password_disabled: true})
        } else{
            setStatus({...status, password_disabled: false})
        }
            
        setValues({...valuesForm, [name]: new_value})
                
    }

    function onSubmit (e) {
        e.preventDefault()
        dispatch({
            type:'LOADING'
        })        
        AUTHENTICATION(dispatch, valuesForm, dispatchApp)              
    }


    return(
        <form onSubmit={onSubmit} autoComplete="off">            
            <Grid className={classes.grid} container direction="column" alignItems="center" >    
                <Typography className={classes.title} variant='h5' children='CRM y Gestión de Ventas' />
                <Grid item>
                    <FormControl className={classes.formControl}>                
                        <TextField 
                            label='Email'
                            type='email'
                            name='email'                                                           
                            variant="outlined"
                            disabled={status.email_disabled}
                            error = {state.error_email}
                            onChange={onChange} 
                            required 
                        />
                    </FormControl>
                </Grid>    
                <Grid item>
                    <FormControl className={classes.formControl}>
                        <TextField 
                            label='Contraseña' 
                            name='password' 
                            type='password'                             
                            variant='outlined'
                            disabled={status.password_disabled}                              
                            error={state.error_password}
                            onChange={onChange} 
                            required 
                        />
                    </FormControl>                          
                </Grid>                    
                <Grid item className={classes.gridErrors}>                
                {state.errors &&                                                
                        Object.keys(state.errors).map((key, index)=>{
                            let field = key
                            let message = state.errors[key]
                            if(key==='non_field_errors'){
                                field='Error'
                            }
                            return(                                 
                                 <Alert elevation={6} variant="filled" severity='error' children={`${field}: ${message}`} />
                                )                            
                        })
                    } 
                </Grid>
                <Grid item>                                                              
                    <Button className={classes.button} variant="contained" color="primary" children='Ingresar' type='submit' />
                    
                </Grid>  
                <Grid item>
                {state.is_loading &&
                        <CircularProgress size={25} className={classes.progress} />                 
                    }                    
                </Grid>      
            </Grid>
        </form>
        
    )
}


const useStyles = makeStyles((theme)=>({
    grid: {
        marginBottom:'60px'
    },
    title: {
        marginBottom:'30px'
    },
    formControl: {
        marginTop:'10px',
        marginBottom:'10px',
    },
    button: {
        marginTop:'15px',        
    }, 
    errors: {
        color: theme.palette.warning.dark,
        textTransform: 'lowercase'
    },
    gridErrors: {
        marginTop:'10px',
        marginBottom: '10px'
    },
    progress: {
        marginTop:'30px',        
    }
    
}))


export default FormLogin
