
export const login = (state, action) => {

    switch (action.type) {

        case "LOGIN":
            localStorage.setItem("acces_token", JSON.stringify(action.payload.access_token))
            localStorage.setItem("user", JSON.stringify(action.payload.user))

            return {
                is_authenticated: true,
                token: action.payload.access_token,
                user: action.payload.user
            }

        case "LOGOUT":
            localStorage.clear()
            return {
                is_authenticated: false,
                token: null,
                user: null
            }
    
        default:
            return state
    }
} 