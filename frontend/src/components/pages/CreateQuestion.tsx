import Button from '../Button';
import QuizEntry from '../QuizEntry'
import TextInput from '../TextInput';
import './CreateQuestion.css'
import { create_question, create_quiz } from '../../actions/quiz_editor';
import React, { useState } from 'react';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import { connect } from 'react-redux';
import store from '../../store'
import Select from 'react-select'

function CreateQuestion( {isAuthenticated}: any) {
    const navigate = useNavigate();
    const { quiz_pk } = useParams();
    const quiz_pk_number: number = quiz_pk ? parseInt(quiz_pk, 10) : -1;

    const [formData, setFormData] = useState({
        text: '',
        answer_type:'',
    });

    const { text, answer_type } = formData;
    const onChange = (e: any) => setFormData({ ...formData, [e.target.name]: e.target.value });
    const onSubmit = (e: any) => {
        e.preventDefault();
        const postQuery = async () => {
            try {
                let res = await create_question(formData.text, quiz_pk_number, store.getState()?.auth?.user?.id, formData.answer_type);
                console.log(res);
                navigate('/Edit-Quiz/' + quiz_pk);
            } catch (error) {
                console.error("Quiz couldn't be created");
            }
        }
        postQuery();
    }

    if(!isAuthenticated){
        return <Navigate to='/Login' />;
    }

    const question_type = [
        { value: 'jednokrotny', label: 'Jednokrotnego wyboru' },
        { value: 'wielokrotny', label: 'Wielokrotnego wyboru' }
    ]

    return (
        <>
        <form className="create-quiz-form" onSubmit={e => onSubmit(e)}>
            <h1>Stwórz Pytanie</h1>
            <TextInput
                        name='text'
                        value={text}
                        onChange={(e: any) => onChange(e)}>Treść pytania</TextInput>
            <Select     name='answer_type' 
                        options={question_type}
                        value={question_type.find(option => option.value === formData.answer_type)}
                        onChange={(e: any) => {setFormData({ ...formData, answer_type: e.value })}} /><br></br>
            <Button className="primary" type="submit">Stwórz</Button>
        </form>
        </>
    )
}

const mapStateToProps = () => ({
    isAuthenticated: store.getState().auth.isAuthenticated,
});

export default connect(mapStateToProps, { create_quiz })(CreateQuestion);