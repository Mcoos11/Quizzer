import { useEffect, useState } from 'react';
import './Quiz.css'
import { get_quiz, send_results } from '../../actions/quiz_solve';
import { useParams } from 'react-router-dom';
import Button from '../Button';

// const q1 = {
//     question: "Ile tydzień ma dni?",
//     answers: ["4", "3", "7", "12", "365", "30"]
// }

// const q2 = {
//     question: "Kiedy miała miejsce bitwa pod Grunwaldem?",
//     answers: ["w 1410", "w 2017", "w 996"]
// }

// let questions = [q1, q2, q1, q2, q1, q2, q1];

// let quiz = {
//     "number_of_questions": 11,
//     "max_time": 12,
//     "score_to_pass": 7,
//     "questions": [
//         {
//             "pk": 20,
//             "text": "Pytanie z obrazem",
//             "quiz": [
//                 17
//             ],
//             "author": 1,
//             "answers_type": "jednokrotny",
//             "media": "/quiz_editor/mediafiles/question_media/rainforest-3119822_VH03teF.jpg",
//             "media_url": null,
//             "answers": []
//         },
//         {
//             "pk": 21,
//             "text": "Pytanie z linkiem",
//             "quiz": [
//                 17
//             ],
//             "author": 1,
//             "answers_type": "jednokrotny",
//             "media": null,
//             "media_url": "https://ipla.pluscdn.pl/dituel/cp/7t/7tnkxp31x4mbz1g975ws7mxpuj2wci8q.jpg",
//             "answers": [
//                 {
//                     "pk": 1,
//                     "text": "Pytanie1",
//                     "correct": true,
//                     "question": 21
//                 },
//                 {
//                     "pk": 2,
//                     "text": "Pytanie2",
//                     "correct": false,
//                     "question": 21
//                 }
//             ]
//         }
//     ]
// }

function Quiz() {
    const { quiz_pk } = useParams();
    const quiz_pk_number = quiz_pk ? parseInt(quiz_pk, 10) : -1;

    let [currentQuestion, setCurrent] = useState(0);
    let [quiz, setQuiz] = useState(
        {"questions": [
            {
                "pk": 0,
                "text": "0",
                "quiz": [
                    17
                ],
                "author": 1,
                "answers_type": "jednokrotny",
                "media": "/quiz_editor/mediafiles/question_media/rainforest-3119822_VH03teF.jpg",
                "media_url": null,
                "answers": [{
                    text: "",
                    pk: 0,
                    question: 0
                }]
            }
            ]}
    );
    let [userAnswers, setUserAnswers] = useState(
        [{
            "question": 0,
            "answers": [0],
        }]
    );

    const getQuiz = async (pk: number) => {
        try {
            const res = await get_quiz(pk);
            console.log("RES: ", res.questions);
            return res;
        } catch (error: any) {
            console.error(error.message);
        }
    }

    // useEffect(() => {
    //     const fetchData = async () => {
    //       try {
    //         // Assume fetchDataFunction is a predefined function that returns a promise
    //         const result = await getQuiz(quiz_pk_number);
    //         setQuiz(result);
    //         setUserAnswers(
    //             Array.from({ length: quiz.questions.length }, (_, index) => ({
    //                 "question": quiz.questions[index].pk,
    //                 "answers": [],
    //               }));
    //         );
    //       } catch (error) {
    //         console.error("get_user_quiz_set() couldn't be fetched");
    //       }
    //     };
    //     fetchData();
    //   }, []);

    useEffect(() => {
        const fetchData = async () => {
          try {
            // Assume fetchDataFunction is a predefined function that returns a promise
            const result = await getQuiz(quiz_pk_number);
            setQuiz(result);
            setUserAnswers(
              Array.from({ length: result.questions.length }, (_, index) => ({
                question: result.questions[index].pk,
                answers: [],
              }))
            );
          } catch (error) {
            console.error("get_user_quiz_set() couldn't be fetched");
          }
        };
        fetchData();
      }, []);



    const handleClick = (index : number) => {
        setCurrent(index);
        // console.log("CLICK ", index);
    }
    const questionNavigationList = quiz.questions.map((item, index) => (
            (index > currentQuestion-3 && index < currentQuestion+3) ?
            (<li key={index} onClick={() => handleClick(index)} className={(index == currentQuestion) ? "active" : ""}>{index+1}</li>) : (<></>)
      ));

    const isAnswerActive = (question: number, answer: number) => {
        if(userAnswers.find(item => item.question === question)?.answers.includes(answer)) {
            return true;
        } else {
            return false;
        }
    }
    function toggleValue(array: Array<any>, value: any) {
        const index = array.indexOf(value);
      
        if (index !== -1) {
          array.splice(index, 1);
        } else {
          array.push(value);
        }
    }

    const answerOnClick = (question: number, answer: number) => {
        // console.log("clicked ", question, answer);
        // toggleValue(userAnswers.find(item => item.question === question)?.answers ?? [], answer);
        // setUserAnswers
        // console.log(userAnswers);
        const answerIndex = userAnswers.findIndex(item => item.question === question);
        let newAnswers = userAnswers[answerIndex].answers;
        toggleValue(newAnswers, answer);

        setUserAnswers(prevState => 
            prevState.map(obj =>
              obj.question === question ? { ...obj, answers: newAnswers } : obj
            )
          );
    }
    const answers = quiz.questions[currentQuestion].answers.map((item, index) => (
        <li key={index} onClick={() => answerOnClick(item.question, item.pk)} className={isAnswerActive(item.question, item.pk) ? 'active' : ''}  >{item.text}</li>
        ));

    const insertMedia = () => {
        if(quiz.questions[currentQuestion].media != null) {
            return (<iframe className="question-media" src={quiz.questions[currentQuestion].media ?? undefined} width="100%"></iframe>)
        }else if(quiz.questions[currentQuestion].media_url != null) {
            return (<iframe className="question-media" src={quiz.questions[currentQuestion].media_url ?? undefined} width="100%"></iframe>)

        } else {
            return <></>
        }
    }
    
    const finishQuiz = () => {
        if(confirm("Czy na pewno chcesz zakończyć rozwiązywanie quizu?")) {
            const body = { results: userAnswers };
            send_results(quiz_pk_number, body);
            const postQuery = async () => {
                try {
                    let res = await send_results(quiz_pk_number, body);
                    console.log(res);
                    // navigate('/Edit-Quiz/' + quiz_pk);
                } catch (error) {
                    console.error("Quiz couldn't be created");
                }
            }
            postQuery();
        }
    }

    return (
        <>
            <section className="quiz">
                <div className="quiz-control-panel">
                    <Button className="primary" onClick={() => finishQuiz()} >Zakończ</Button>
                </div>
                <ul className="question-nav">
                    {questionNavigationList}
                </ul>
                <h1>{quiz.questions[currentQuestion].text}</h1>
                {insertMedia()}
                <ul className="answers">
                    {answers}
                </ul>
            </section>
        </>
    )
}

export default Quiz;