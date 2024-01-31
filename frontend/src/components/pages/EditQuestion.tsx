import Button from '../Button';
import QuizEntry from '../QuizEntry'
import TextInput from '../TextInput';
import './EditQuestion.css'
import { delete_answer, get_answer_set } from '../../actions/quiz_editor';
import React, { useEffect, useState } from 'react';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import { connect } from 'react-redux';
import store from '../../store'
import Select from 'react-select'

function EditQuestion( {isAuthenticated}: any) {
    const navigate = useNavigate();
    const { quiz_pk, question_pk } = useParams();
    const question_pk_number = question_pk ? parseInt(question_pk, 10) : -1;
    const [questionList, setQuestionList] = useState({
        results: [{
            pk: 0,
            text: "",
            correct: false
        }]
    });

    useEffect(() => {
        const fetchData = async () => {
          try {
            // Assume fetchDataFunction is a predefined function that returns a promise
            const result = await get_answer_set(question_pk_number);
            console.log(result);
            setQuestionList(result);
          } catch (error: any) {
            console.error(error.message);
          }
        };
    
        // Call the fetchData function when the component mounts
        fetchData();
      }, []);

    const deleteAnswer = async (answerText: string, pk: number) => {
        if(confirm("Czy na pewno chcesz usunąć odpowiedź: " + answerText)) {
            try {
                await delete_answer(pk);
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
            <span className="go-back" onClick={() => navigate('/Edit-Quiz/'+quiz_pk)}>{'<'} Edytuj Quiz</span>
            <h1>Edytuj Pytanie {question_pk}</h1>
        </form>
        <div className="form-button-container">
            <Button className="secondary" onClick={() => {navigate('/Create-Answer/'+quiz_pk+'/'+question_pk)}} >Dodaj Odpowiedź</Button>
        </div>
            {questionList.results.map((item, id) => (
                <div key={id} className={"question-entry " + (item.correct ? "active" : "")}> {item.text}
                    {/* <Button className="secondary edit-button" onClick={() => {navigate('/Edit-Question/' + item.pk);}}>Edytuj</Button> */}
                    <Button className="secondary delete-button" onClick={() => deleteAnswer(item.text, item.pk)} >Usuń</Button>
                </div>
            ))}
        </>
    )
}

const mapStateToProps = () => ({
    isAuthenticated: store.getState().auth.isAuthenticated,
});

export default connect(mapStateToProps)(EditQuestion);