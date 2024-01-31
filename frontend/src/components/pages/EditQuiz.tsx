import Button from '../Button';
import QuizEntry from '../QuizEntry'
import TextInput from '../TextInput';
import './EditQuiz.css'
import { delete_question, get_question_set } from '../../actions/quiz_editor';
import React, { useEffect, useState } from 'react';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import { connect } from 'react-redux';
import store from '../../store'
import Select from 'react-select'

function EditQuiz( {isAuthenticated}: any) {
    const navigate = useNavigate();
    const { quiz_pk } = useParams();
    const quiz_pk_number = quiz_pk ? parseInt(quiz_pk, 10) : -1;
    const [questionList, setQuestionList] = useState({
        results: [{
            pk: 0,
            text: ""
        }]
    });

    useEffect(() => {
        const fetchData = async () => {
          try {
            // Assume fetchDataFunction is a predefined function that returns a promise
            const result = await get_question_set(quiz_pk_number);
            console.log(result);
            setQuestionList(result);
          } catch (error) {
            console.error("get_question_set() couldn't be fetched");
          }
        };
    
        // Call the fetchData function when the component mounts
        fetchData();
      }, []);

    const deleteAnswer = async (questionText: string, pk: number) => {
        if(confirm("Czy na pewno chcesz usunąć pytanie: " + questionText)) {
            try {
                await delete_question(pk);
                window.location.reload();
            } catch (error: any) {
                console.error(error.message);
            }
        } else {
            return;
        }
    }

    if(!isAuthenticated){
        return <Navigate to='/Login' />;
    }

    return (
        <>
        <form className="create-quiz-form">
            <span className="go-back" onClick={() => navigate('/Profile')}>{'<'} Profil</span>
            <h1>Edytuj Quiz {quiz_pk}</h1>
        </form>
        <div className="form-button-container">
            <Button className="secondary" onClick={() => {navigate('/Create-Question/' + quiz_pk)}} >Dodaj Pytanie</Button>
        </div>
            {questionList.results.map((item, id) => (
                <div key={id} className="question-entry">{id+1}. {item.text}
                    <Button className="secondary edit-button" onClick={() => {navigate('/Edit-Question/' + quiz_pk + '/' + item.pk);}}>Edytuj</Button>
                    <Button className="secondary delete-button" onClick={() => deleteAnswer(item.text, item.pk)} >Usuń</Button>
                </div>
            ))}
        </>
    )
}

const mapStateToProps = () => ({
    isAuthenticated: store.getState().auth.isAuthenticated,
});

export default connect(mapStateToProps)(EditQuiz);