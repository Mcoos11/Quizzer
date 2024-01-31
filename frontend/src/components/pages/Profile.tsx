import Button from '../Button';
import QuizEntry from '../QuizEntry';
import TextInput from '../TextInput';
import './Profile.css';
import React, { useEffect, useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { delete_quiz, get_user_quiz_set } from '../../actions/quiz_editor';
import { connect, useDispatch, useSelector } from 'react-redux';
import store from '../../store';
import default_avatar from '../../../img/default_avatar.png';

function Profile( {isAuthenticated}: any) {

    const navigate = useNavigate();

    if(!isAuthenticated){
        return <Navigate to='/Login' />;
    }

    // const dispatch = useDispatch();
    // const data = useSelector((state: any) => state.data);
  
    // useEffect(() => {
    //     dispatch(get_user_quiz_set());
    //     userQuizSet();
    // }, []);

    const [quizzesList, setQuizzesList] = useState({
        results: [{
            name: "",
            topic: "",
            pk: 0
        }]
    });
    
    // setQuizzesList(get_user_quiz_set());

    useEffect(() => {
        const fetchData = async () => {
          try {
            // Assume fetchDataFunction is a predefined function that returns a promise
            const result = await get_user_quiz_set();
            console.log(result);
            // Set the state when the data is loaded
            setQuizzesList(result);
          } catch (error) {
            console.error("get_user_quiz_set() couldn't be fetched");
          }
        };
    
        // Call the fetchData function when the component mounts
        fetchData();
      }, []);

    const deleteQuiz = async (quizName: string, pk: number) => {
        if(confirm("Czy na pewno chcesz usunąć quiz: " + quizName)) {
            try {
                await delete_quiz(pk);
                window.location.reload();
            } catch (error) {
                console.error("quiz couldn't be deleted");
            }
        } else {
            return;
        }
    }


    const userName = String(store.getState()?.auth?.user?.first_name) + " " + String(store.getState()?.auth?.user?.last_name);

    return (
        <>
        <section className="profile">
            <img className="profile-picture" src={default_avatar}></img>
            <span className="user-name">{userName}</span>
            <span className="user-email">{String(store.getState()?.auth?.user?.email)}</span>
        </section>
        <section className="user-quizzes">
            <h1>Twoje quizy</h1>
            {quizzesList.results.map((item, id) => (
                <QuizEntry key={id} name={item.name} description={item.topic} author={userName}>
                    <Button className="secondary delete-button" onClick={() => deleteQuiz(item.name, item.pk)}>Usuń</Button>
                    <Button className="secondary edit-button" onClick={() => {navigate('/Edit-Quiz/' + item.pk);}}>Edytuj</Button>
                </QuizEntry>
            ))}
        </section>
        </>
    )
}

const mapStateToProps = () => ({
    isAuthenticated: store.getState().auth.isAuthenticated,
});

// const mapDispatchtoprops = (dispatch: any) => ({
//     userQuizSet: ()=>dispatch(get_user_quiz_set())
// });

export default connect(mapStateToProps)(Profile);