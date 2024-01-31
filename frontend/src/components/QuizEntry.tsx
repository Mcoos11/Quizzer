import './QuizEntry.css'
import Button from './Button.tsx'
import { useNavigate } from 'react-router-dom';

function QuizEntry(props : any) {
    const navigate = useNavigate();

    return (
        <>
            <div className="quiz-entry-container">
                <div className="quiz-entry-name">{props.name}</div>
                <div className="quiz-entry-description">{props.description}</div>
                <div className="quiz-entry-author">Autor: {props.author}</div>
                <Button className="primary quiz-entry-button" onClick={() => navigate('/Quiz/' + props.pk)} >Rozwiąż</Button>
                {props.children}
            </div>
        </>
     );
}

export default QuizEntry;