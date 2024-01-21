import axios from 'axios'
import {
    CREATE_SUCCESS,
    CREATE_FAIL,
} from './types';

export const create_quiz = (name, topic, number_of_questions, max_time, score_to_pass, difficulty) => async dispatch => {
    const body = JSON.stringify({ "name": name, "topic": topic, "number_of_questions": parseInt(number_of_questions), "max_time": parseInt(max_time), "score_to_pass": parseInt(score_to_pass), difficulty });

    const config = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.post(`${process.env.REACT_APP_API_URL}/quiz_editor/create_quiz/`, body, config);

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