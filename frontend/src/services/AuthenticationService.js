import net from './NetworkService'

const session = null;

export const login = (username, password) => {
    // TODO: implement login logic

    //on success, to be scheduled as per expiration
    session = setInterval(isAuthenticated, 300000)
}


export const logout = () => {
    // TODO: implement logout logic

    //on success
    clearInterval(session)

    // TODO: navigate to the logout url
}


export const signup = (username, password) => {
    // TODO: implement user registration logic

}


export const isAuthenticated = () => {
    // TODO: get token and ping the server to validate, if invalid clear session
    // if expired refresh else logout
    logout()

}


export const currentUser = () => {
    // TODO: implement ping server to get the owner of the token
    // if not found logout
    logout()

}
