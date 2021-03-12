import { auth_endpoints } from '../../api/endpoints/auth'


export const AUTHENTICATION = async(dispatch, data, dispatchApp) => {    
    const request = await auth_endpoints.login(data)
        .then((response)=>{
                dispatchApp({
                    type:'LOGIN',
                    payload: response.data,                    
                })
        })
        .catch((error)=>{
                console.log({error})
                dispatch({
                    type:'ERRORS',
                    errors: error.response.data
                })
            }
        )        
    
    return request
}


