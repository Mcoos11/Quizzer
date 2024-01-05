import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { create_quiz } from '../actions/quiz_editor'

const CreateQuiz = ({ create_quiz, isAuthenticated }) => {
    const [formData, setFormData] = useState({
        name: '', 
        topic: '', 
        number_of_questions: '', 
        max_time: '', 
        score_to_pass: '', 
        difficulty: ''
    });

    const { name, topic, number_of_questions, max_time, score_to_pass, difficulty } = formData;
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });
    const onSubmit = e => {
        e.preventDefault();
        create_quiz(name, topic, number_of_questions, max_time, score_to_pass, difficulty);
    }

    if(isAuthenticated){
        return (
            <div className='container mt-5'>
                <h1>Logowanie</h1>
                <form onSubmit={e => onSubmit(e)}>
                    <div className='form-group'>
                        <input 
                            className='form-control mb-1'
                            type='text'
                            placeholder='Nazwa'
                            name='name'
                            value={name}
                            onChange={e => onChange(e)}
                            required
                        />
                        <input 
                            className='form-control mb-1'
                            type='text'
                            placeholder='Temat'
                            name='topic'
                            value={topic}
                            onChange={e => onChange(e)}
                            required
                        />
                        <input 
                            className='form-control mb-1'
                            type='number'
                            placeholder='Liczba pytań'
                            name='number_of_questions'
                            value={number_of_questions}
                            onChange={e => onChange(e)}
                            required
                        />
                        <input 
                            className='form-control mb-1'
                            type='number'
                            placeholder='Maksymalny czas'
                            name='max_time'
                            value={max_time}
                            onChange={e => onChange(e)}
                            required
                        />
                        <input 
                            className='form-control mb-1'
                            type='number'
                            placeholder='Punkty do zaliczenia'
                            name='score_to_pass'
                            value={score_to_pass}
                            onChange={e => onChange(e)}
                            required
                        />
                        <select 
                            className='form-control mb-1'
                            placeholder='Poziom trudności'
                            name='difficulty'
                            value={difficulty}
                            onChange={e => onChange(e)}
                            required
                        >
                            <option value="łatwy">łatwy</option>
                            <option value="normalny">normalny</option>
                            <option value="trudny">trudny</option>
                        </select>
                    </div>
                    <button className='btn btn-primary' type='submit'>Utwórz</button>
                </form>
            </div>
        );
    }
    else{
        return <Navigate to='/' />;
    }
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { create_quiz })(CreateQuiz);