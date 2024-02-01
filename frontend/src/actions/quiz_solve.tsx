import axios from 'axios'


export const get_quiz = async (pk: number) => {
 
    const config = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.get(`${import.meta.env.VITE_APP_API_URL}/quiz_solver/solve/${pk}/`, config)

        // Access the response data
        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};

export const send_results = async (pk: number, body: object) => {
 
    const config = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `JWT ${localStorage.getItem('access')}`,
            'Accept': '*/*'
        }
    };

    try {
        const res = await axios.post(`${import.meta.env.VITE_APP_API_URL}/quiz_solver/results/${pk}/`, body, config)

        // Access the response data
        const data = res.data;
        return data;
    } catch (error: any) {
        console.error('Error fetching data:', error.message);
    }
};