import Button from '../Button';
import QuizEntry from '../QuizEntry'
import TextInput from '../TextInput';
import './CreateQuiz.css'
import { create_quiz } from '../../actions/quiz_editor';
import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import store from '../../store'
import Select from 'react-select'

function CreateQuiz( {isAuthenticated}: any) {

    const [formData, setFormData] = useState({
        title: '',
        description: '',
        difficulty: '',
    });

    const { title, description, difficulty } = formData;
    const onChange = (e: any) => setFormData({ ...formData, [e.target.name]: e.target.value });
    const onSubmit = (e: any) => {
        e.preventDefault();
        const postQuery = async () => {
            try {
                await create_quiz(formData.title, formData.description, 0, 0, 0, formData.difficulty);
                return <Navigate to='/Quizzes' />
            } catch (error) {
                console.error("Quiz couldn't be created");
            }
        }
        postQuery();
    }

    if(!isAuthenticated){
        return <Navigate to='/Login' />;
    }

    const difficulty_levels = [
        { value: 'łatwy', label: 'Łatwy' },
        { value: 'normalny', label: 'Normalny' },
        { value: 'trudny', label: 'Trudny' }
    ]

    return (
        <>
        <form className="create-quiz-form" onSubmit={e => onSubmit(e)}>
            <h1>Stwórz Quiz</h1>
            <TextInput
                        name='title'
                        value={title}
                        onChange={(e: any) => onChange(e)}>Tytuł</TextInput>
            <label className="input-label">
                <div>Opis</div>
                <textarea className="text-input" rows={4}
                        name='description'
                        value={description}
                        onChange={(e: any) => onChange(e)} ></textarea>
            </label>
            <Select     name='difficulty' 
                        options={difficulty_levels}
                        value={difficulty_levels.find(option => option.value === formData.difficulty)}
                        onChange={(e: any) => {setFormData({ ...formData, difficulty: e.value })}} /><br></br>
            <Button className="primary" type="submit">Stwórz</Button>
        </form>
        </>
    )
}

const mapStateToProps = () => ({
    isAuthenticated: store.getState().auth.isAuthenticated,
});

export default connect(mapStateToProps, { create_quiz })(CreateQuiz);