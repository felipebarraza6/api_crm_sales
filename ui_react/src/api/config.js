import axios from 'axios'

const token = JSON.parse(localStorage.getItem('access_token') || null)

const instance_token = axios.create({
    baseURL: 'http://localhost:8000/api/',
    timeout: 1000,
    headers: {
        'Autorization': `Token ${token}`
    }
  })

const instance = axios.create({
    baseURL: 'http://localhost:8000/api/',
    timeout: 1000
})

export const POST_LOGIN = async(endpoint, data) => {
    const request = instance.post(endpoint, data)
    return request

}

export const GET = async(endpoint) => {
    const request = instance_token.get(endpoint).cath((error)=>console.log(error))
    return request

}