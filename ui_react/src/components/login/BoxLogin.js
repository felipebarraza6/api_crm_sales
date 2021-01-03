// React
import React from 'react'

// Maaterial UI
import { makeStyles } from '@material-ui/styles'
import { Grid, Paper, Typography } from '@material-ui/core'
import { AccountCircleOutlined ,InfoTwoTone } from '@material-ui/icons'

// Components
import FormLogin from './FormLogin'


const BoxLogin = () => {

    const classes = useStyles()

    return(
        <div className={classes.root}>
            <Grid container>            
                <Paper className={classes.paper} elevation={24} variant={'elevation'}>  
                <Grid container direction="column" alignItems="center">
                        <Grid item xs={12} >
                            <AccountCircleOutlined className={classes.icon} />
                        </Grid>
                        <Grid item>
                            <FormLogin />
                        </Grid>  
                        <Grid item xs={12} >
                            <Typography 
                                variant={'subtitle1'}                                 
                                className={classes.textHelp}
                            >
                                <InfoTwoTone className={classes.info}  />
                                 Ingresa tu usuario y contraseña, en caso de olvidarla comunicate con el administrador
                                 
                            </Typography>
                        </Grid>
                                                                                                                      
                    </Grid>                                          
                </Paper>
            </Grid>
        </div>                
    )
}

const useStyles = makeStyles((theme)=>({
    root: {
        flexGrow: 1                
    },
    paper: {
        padding: theme.spacing(5),
        margin: 'auto',
        maxWidth: 700,
        marginTop:'40px',
        boxShadow:'10'
    },
    icon:{
        fontSize:'150px',
        color:theme.palette.primary.dark

    },
    textHelp: {
        fontSize:'15px'
    },
    info: {
        color: theme.palette.warning.dark,        
        fontSize:'30px'
    }
}))

export default BoxLogin