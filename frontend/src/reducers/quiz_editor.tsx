import {
    CREATE_SUCCESS,
    CREATE_FAIL,
    GET_USER_QUIZ_SET_SUCCESS,
    GET_USER_QUIZ_SET_FAIL,
} from '../actions/types';

const initialState = {
    loading: true,
    data: [],
    error: ''
};

let new_state: any;

export default function(state = initialState, action: any) {
    const { type, payload } = action;
    switch(type){
        case CREATE_SUCCESS:
        case CREATE_FAIL:
        case GET_USER_QUIZ_SET_SUCCESS:
            new_state = {
                ...state,
                loading: false,
                data: action.payload
            };
            return new_state;
        case GET_USER_QUIZ_SET_FAIL:
        default:
            new_state = {
                ...state,
            };
            return new_state;
    }
}