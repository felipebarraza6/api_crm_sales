// METHODS FOR API DJANGO
import { POST_LOGIN } from '../config'


const LOGIN = async (data) => {    
    const request = await POST_LOGIN('users/login/', {
        email: data.email,
        password: data.password
    })

    return request
}

export const auth_endpoints = {
    login: LOGIN
}