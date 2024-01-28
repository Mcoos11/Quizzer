import axios from 'axios'
import {
    CREATE_SUCCESS,
    CREATE_FAIL,
    GET_USER_QUIZ_SET_SUCCESS,
    GET_USER_QUIZ_SET_FAIL,
} from './types';

export const create_quiz = (name: string, topic: string, number_of_questions: string, max_time: string, score_to_pass: string, difficulty: string) => async (dispatch: any) => {
    const body = JSON.stringify({ "name": name, "topic": topic, "number_of_questions": parseInt(number_of_questions), "max_time": parseInt(max_time), "score_to_pass": parseInt(score_to_pass), difficulty });

    const config = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.post(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/create_quiz/`, body, config);

        dispatch({
            type: CREATE_SUCCESS,
            payload: res.data
        });

    } catch(err) {
        dispatch({
            type: CREATE_FAIL
        });
    }
};

// export const get_user_quiz_set = () => async (dispatch: any) => {
 
//     const config = {
//         headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `JWT ${localStorage.getItem('access')}`,
//             'Accept': '*/*'
//         }
//     };

//     try {
//         const res = await axios.get(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/user_quiz_set/`, config);

//         dispatch({
//             type: GET_USER_QUIZ_SET_SUCCESS,
//             payload: res.data
//         });

//     } catch(err) {
//         dispatch({
//             type: GET_USER_QUIZ_SET_FAIL
//         });
//     }
// };


export const get_user_quiz_set = async () => {
 
    const config = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.get(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/user_quiz_set/`, config)
        // .then(function (response) {
        //   console.log(response);
        // });
    
        // console.log('res data:', res);
        // Access the response data
        const data = res.data;
        // console.log('Fetched data:', data);
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};