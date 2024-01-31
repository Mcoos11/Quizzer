import Button from '../Button';
import QuizEntry from '../QuizEntry'
import TextInput from '../TextInput';
import './CreateAnswer.css'
import { create_answer } from '../../actions/quiz_editor';
import React, { useState } from 'react';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import { connect } from 'react-redux';
import store from '../../store'
import Select from 'react-select'

function CreateAnswer( {isAuthenticated}: any) {
    const navigate = useNavigate();
    const { quiz_pk, question_pk } = useParams();
    const question_pk_number: number = question_pk ? parseInt(question_pk, 10) : -1;

    const [formData, setFormData] = useState({
        text: '',
        answer_type: false,
    });

    const { text, answer_type } = formData;
    const onChange = (e: any) => setFormData({ ...formData, [e.target.name]: e.target.value });
    const onSubmit = (e: any) => {
        e.preventDefault();
        const postQuery = async () => {
            try {
                let res = await create_answer(formData.text, question_pk_number, formData.answer_type);
                console.log(res);
                navigate('/Edit-Question/' + quiz_pk + '/' + question_pk);
            } catch (error) {
                console.error("Quiz couldn't be created");
            }
        }
        postQuery();
    }

    if(!isAuthenticated){
        return <Navigate to='/Login' />;
    }

    const correct_type = [
        { value: true, label: 'Poprawna' },
        { value: false, label: 'Błędna' }
    ]

    return (
        <>
        <form className="create-quiz-form" onSubmit={e => onSubmit(e)}>
            <span className="go-back" onClick={() => navigate('/Edit-Question/' + quiz_pk + '/' + question_pk)}>{'<'} Edytuj Pytanie</span>
            <h1>Stwórz Odpowiedź</h1>
            <TextInput
                        name='text'
                        value={text}
                        onChange={(e: any) => onChange(e)}>Treść odpowiedzi</TextInput>
            <Select     name='correct_type' 
                        options={correct_type}
                        value={correct_type.find(option => option.value === formData.answer_type)}
                        onChange={(e: any) => {setFormData({ ...formData, answer_type: e.value })}} /><br></br>
            <Button className="primary" type="submit">Stwórz</Button>
        </form>
        </>
    )
}

const mapStateToProps = () => ({
    isAuthenticated: store.getState().auth.isAuthenticated,
});

export default connect(mapStateToProps)(CreateAnswer);