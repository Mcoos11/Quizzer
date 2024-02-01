import { useNavigate, useParams } from 'react-router-dom';
import { get_quiz, get_user_results } from '../../actions/quiz_solve';
import './Results.css'
import { useEffect, useState } from 'react';
import store from '../../store';

function Results() {
    const navigate = useNavigate();
    const { quiz_pk } = useParams();
    const quiz_pk_number = quiz_pk ? parseInt(quiz_pk, 10) : -1;
    // const [loading, setLoading] = useState(true);

    const [userResult, setUserResult] = useState({
        date: "2024-01-01",
        quiz_pass: false,
        score: 0,
    });

    const [quiz, setQuiz] = useState({
        number_of_questions: 0,
    });

    interface resInter {
        quiz: number;
    }

    useEffect(() => {
        const fetchData = async () => {
          try {
            const res = await get_user_results(store.getState()?.auth?.user?.id);
            console.log(res[0].quiz)
            let result = res.filter((item: resInter) => item.quiz === quiz_pk_number);
            result = result[result.length-1];
            const result_quiz = await get_quiz(result.quiz);
            setUserResult(result);
            setQuiz(result_quiz);
          } catch (error: any) {
            console.error(error.message);
          }
        };
        fetchData();
    }, []);



    return (
        <>
        <section className="results">
            <h1>Wyniki</h1>
            <h2 className={userResult.quiz_pass ? "active" : ""}>{userResult.quiz_pass ? "Zaliczony": "Nie Zaliczony"}</h2>
            <h3>Szczegóły</h3>
            <div className="result-details">
                <label>Wynik punktowy<div>{userResult.score}/{quiz.number_of_questions}</div></label>
                <label>Wynik procentowy<div>{(100 * userResult.score / quiz.number_of_questions).toFixed(2)}%</div></label>
            </div>
            <div className="result-date">Data wykonania<div>{userResult.date}</div></div>
        </section>
        </>
    )
}

export default Results;