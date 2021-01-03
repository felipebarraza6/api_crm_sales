import React from 'react'
import { Container } from '@material-ui/core'
import { makeStyles } from '@material-ui/styles'
import BoxLogin from '../components/login/BoxLogin'



const Login = () => {
    
    const classes = useStyles()

    return(
        <Container className={classes.container} maxWidth={'xl'}>           
            <BoxLogin />
        </Container>
        
    )
}

const useStyles = makeStyles((theme)=>({
    container:{
        paddingTop:'30px',
        margin:0,
        backgroundColor: theme.palette.primary.dark,
        height:'100vh',
        overflow:'hidden'
    }
}))



export default Login