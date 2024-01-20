import { useState } from 'react';
import './Quiz.css'

const q1 = {
    question: "Ile tydzień ma dni?",
    answers: ["4", "3", "7", "12", "365", "30"]
}

const q2 = {
    question: "Kiedy miała miejsce bitwa pod Grunwaldem?",
    answers: ["w 1410", "w 2017", "w 996"]
}

let questions = [q1, q2, q1, q2, q1, q2, q1];


function Quiz() {

    let [currentQuestion, setCurrent] = useState(0);

    const handleClick = (index : number) => {
        setCurrent(index);// = index;
        console.log("CLICK ", index);
    }
    const questionNavigationList = questions.map((item, index) => (
            (index > currentQuestion-3 && index < currentQuestion+3) ?
            (<li key={index} onClick={() => handleClick(index)} className={(index == currentQuestion) ? "active" : ""}>{index+1}</li>) : (<></>)
        
      ));

    const answers = questions[currentQuestion].answers.map((item, index) => (
        <li key={index}>{item}</li>
        ));

    return (
        <>
            <section className="quiz">
                <ul className="question-nav">
                    {questionNavigationList}
                </ul>
                <h1>{questions[currentQuestion].question}</h1>
                <ul className="answers">
                    {answers}
                </ul>
            </section>
        </>
    )
}

export default Quiz;