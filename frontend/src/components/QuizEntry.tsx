import './QuizEntry.css'
import Button from './Button.tsx'

function QuizEntry(props : any) {

    return (
        <>
            <div className="quiz-entry-container">
                <div className="quiz-entry-name">{props.name}</div>
                <div className="quiz-entry-description">{props.description}</div>
                <div className="quiz-entry-author">Autor: {props.author}</div>
                <Button className="primary quiz-entry-button">Rozwiąż</Button>
                {props.children}
            </div>
        </>
     );
}

export default QuizEntry;