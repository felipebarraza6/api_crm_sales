
export const login = (state, action) => {

    switch (action.type) {

        case "LOGIN": 
            
            localStorage.setItem("access_token", JSON.stringify(action.payload.access_token)||null)
            localStorage.setItem("user", JSON.stringify(action.payload.user)||null)
                        
            return {
                is_authenticated: true,
                token: action.payload.access_token,
                user: action.payload.user,
                errors: null,
                is_loading: false
            }

        case "LOGOUT":
            localStorage.clear()
            return {
                ...state,
                is_authenticated: false,
                token: null,
                user: null,
                is_loading: false,
                errors: null
            }
        
        case "ERRORS":
            return {
                ...state,
                errors: action.errors,
                is_loading: false
            }

        case "LOADING":
            return {
                ...state,
                is_loading:true
            }
    
        default:
            return state
    }
} 