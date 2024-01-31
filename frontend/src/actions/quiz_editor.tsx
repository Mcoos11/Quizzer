import axios from 'axios'
import {
    CREATE_SUCCESS,
    CREATE_FAIL,
    GET_USER_QUIZ_SET_SUCCESS,
    GET_USER_QUIZ_SET_FAIL,
} from './types';

// export const create_quiz = (name: string, topic: string, number_of_questions: string, max_time: string, score_to_pass: string, difficulty: string) => async (dispatch: any) => {
//     const body = JSON.stringify({ "name": name, "topic": topic, "number_of_questions": parseInt(number_of_questions), "max_time": parseInt(max_time), "score_to_pass": parseInt(score_to_pass), difficulty });

//     const config = {
//         headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `JWT ${localStorage.getItem('access')}`,
//             'Accept': '*/*'
//         }
//     };

//     try {
//         const res = await axios.post(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/create_quiz/`, body, config);

//         dispatch({
//             type: CREATE_SUCCESS,
//             payload: res.data
//         });

//     } catch(err) {
//         dispatch({
//             type: CREATE_FAIL
//         });
//     }
// };

export const create_quiz = async (name: string, topic: string, number_of_questions: number, max_time: number, score_to_pass: number, difficulty: string) => {
    const body = JSON.stringify({ "name": name, "topic": topic, "number_of_questions": number_of_questions, "max_time": max_time, "score_to_pass": score_to_pass, difficulty });

    const config = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        console.log("quiz post");
        const res = await axios.post(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/quiz/`, body, config);

        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
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

        // Access the response data
        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};


export const get_quiz_set = async () => {
 
    const config = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            // 'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.get(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/quiz_set/`, config)

        // Access the response data
        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};

export const delete_quiz = async (pk: number) => {
 
    const config = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.delete(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/quiz/${pk}/`, config);

        // Access the response data
        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};

export const get_question_set = async (pk: number) => {
 
    const config = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.get(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/question_set/${pk}/`, config);

        // Access the response data
        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};

export const create_question = async (text: string, quiz: number, author: number, answer_type: string) => {
    const body = JSON.stringify({ "text": text, "quiz": [quiz], "author": author, "answer_type": answer_type });

    const config = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.post(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/question/`, body, config);

        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};

export const delete_question = async (pk: number) => {
 
    const config = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.delete(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/question/${pk}/`, config);

        // Access the response data
        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};

export const get_answer_set = async (pk: number) => {
 
    const config = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.get(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/answer_set/${pk}/`, config);

        // Access the response data
        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};

export const create_answer = async (text: string, question: number, correct: boolean) => {
    const body = JSON.stringify({ "text": text, "question": question, "correct": correct });

    const config = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.post(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/answer/`, body, config);

        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};

export const delete_answer = async (pk: number) => {
 
    const config = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.delete(`${import.meta.env.VITE_APP_API_URL}/quiz_editor/answer/${pk}/`, config);

        // Access the response data
        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};