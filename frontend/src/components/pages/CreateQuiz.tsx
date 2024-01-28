import Button from '../Button';
import QuizEntry from '../QuizEntry'
import TextInput from '../TextInput';
import './CreateQuiz.css'
import { create_quiz } from '../../actions/quiz_editor';
import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import store from '../../store'

function CreateQuiz( {isAuthenticated}: any) {

    if(!isAuthenticated){
        return <Navigate to='/Login' />;
    }

    return (
        <>
        <form className="create-quiz-form">
            <h1>Stwórz Quiz</h1>
            <TextInput>Tytuł</TextInput>
            <label className="input-label">
                <div>Opis</div>
                <textarea className="text-input" rows={4}></textarea>
            </label>
            <Button className="primary">Stwórz</Button>
        </form>
        </>
    )
}

const mapStateToProps = () => ({
    isAuthenticated: store.getState().auth.isAuthenticated,
});

export default connect(mapStateToProps, { create_quiz })(CreateQuiz);