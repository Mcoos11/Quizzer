import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOAD_USER_SUCCESS,
    LOAD_USER_FAIL,
    AUTHENTICATED_SUCCESS,
    AUTHENTICATED_FAIL,
    LOGOUT,
    PASSWORD_RESET_CONFIRM_FAIL,
    PASSWORD_RESET_CONFIRM_SUCCESS,
    PASSWORD_RESET_FAIL,
    PASSWORD_RESET_SUCCESS,
    SIGNUP_FAIL, 
    SIGNUP_SUCCESS,
    ACTIVATION_FAIL,
    ACTIVATION_SUCCESS
} from '../actions/types';

const initialState = localStorage.getItem("auth") != null ? JSON.parse(localStorage.getItem("auth")): {};
let new_state: any;

export default function(state = initialState, action: any) {
    const { type, payload } = action;
    switch(type){
        case LOGIN_SUCCESS:
            localStorage.setItem('access', payload.access);

            new_state = {
                ...state,
                isAuthenticated: true,
                access: payload.access,
                refresh: payload.refresh
            };
            localStorage.setItem("auth", JSON.stringify(new_state));
            return new_state;
        case SIGNUP_FAIL:
        case LOGIN_FAIL:
        case LOGOUT:
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            new_state = {
                ...state,
                isAuthenticated: false,
                access: null,
                refresh: null,
                user: null
            };
            localStorage.setItem("auth", JSON.stringify(new_state));
            return new_state;
        case LOAD_USER_SUCCESS:
            new_state = {
                ...state,
                user: payload
            }
            localStorage.setItem("auth", JSON.stringify(new_state));
            return new_state;
        case LOAD_USER_FAIL:
            new_state = {
                ...state,
                user: null
            };
            localStorage.setItem("auth", JSON.stringify(new_state));
            return new_state;
        case AUTHENTICATED_SUCCESS:
            new_state = {
                ...state,
                isAuthenticated: true,
            };
            localStorage.setItem("auth", JSON.stringify(new_state));
            return new_state;
        case AUTHENTICATED_FAIL:
            new_state = {
                ...state,
                isAuthenticated: false,
            };
            localStorage.setItem("auth", JSON.stringify(new_state));
            return new_state
        case SIGNUP_SUCCESS:
            new_state = {
                ...state,
                isAuthenticated: false
            };
            localStorage.setItem("auth", JSON.stringify(new_state));
            return new_state
        case PASSWORD_RESET_CONFIRM_FAIL:
        case PASSWORD_RESET_CONFIRM_SUCCESS:
        case PASSWORD_RESET_FAIL:
        case PASSWORD_RESET_SUCCESS:
        case ACTIVATION_FAIL:
        case ACTIVATION_SUCCESS:
            new_state = {
                ...state,
            };
            localStorage.setItem("auth", JSON.stringify(new_state));
            return new_state;
        default:
            new_state = {
                ...state,
            };
            localStorage.setItem("auth", JSON.stringify(new_state));
            return new_state;
    }
};