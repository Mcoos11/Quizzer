import axios from 'axios';

import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOAD_USER_SUCCESS,
    LOAD_USER_FAIL,
    AUTHENTICATED_FAIL,
    AUTHENTICATED_SUCCESS,
    LOGOUT,
    PASSWORD_RESET_CONFIRM_FAIL,
    PASSWORD_RESET_CONFIRM_SUCCESS,
    PASSWORD_RESET_FAIL,
    PASSWORD_RESET_SUCCESS,
    SIGNUP_FAIL, 
    SIGNUP_SUCCESS,
    ACTIVATION_FAIL,
    ACTIVATION_SUCCESS
} from './types';

export const checkAuthenticated = () => async (dispatch: any) => {
    if (localStorage.getItem('access')) {
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        }; 

        const body = JSON.stringify({ token: localStorage.getItem('access') });

        try {
            const res = await axios.post(`${import.meta.env.VITE_APP_API_URL}/auth/jwt/verify/`, body, config)

            if (res.data.code !== 'token_not_valid') {
                dispatch({
                    type: AUTHENTICATED_SUCCESS
                });
            } else {
                dispatch({
                    type: AUTHENTICATED_FAIL
                });
            }
        } catch (err) {
            dispatch({
                type: AUTHENTICATED_FAIL
            });
        }

    } else {
        dispatch({
            type: AUTHENTICATED_FAIL
        });
    }
};

export const load_user = () => async (dispatch: any) => {
    if(localStorage.getItem('access')){
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `JWT ${localStorage.getItem('access')}`,
                'Accept': 'application/json'
            }
        };

        try {
            const res = await axios.get(`${import.meta.env.VITE_APP_API_URL}/auth/users/me/`, config);
    
            dispatch({
                type: LOAD_USER_SUCCESS,
                payload: res.data
            });
        } catch(err) {
            dispatch({
                type: LOAD_USER_FAIL
            });
        }
    }else {
        dispatch({
            type: LOAD_USER_FAIL
        });
    }
};

export const login = (email: string, password: string): any => async (dispatch: any) => {
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const body = JSON.stringify({ email, password });

    try {
        const res = await axios.post(`${import.meta.env.VITE_APP_API_URL}/auth/jwt/create/`, body, config);
        console.log(res.data);
        dispatch({
            type: LOGIN_SUCCESS,
            payload: res.data
        });

        dispatch(load_user());
    } catch(err) {
        console.log("Fail");
        dispatch({
            type: LOGIN_FAIL
        });
    }
};

export const logout = () => (dispatch: any) => {
    console.log("Logout")
    dispatch({
        type: LOGOUT
    });
};