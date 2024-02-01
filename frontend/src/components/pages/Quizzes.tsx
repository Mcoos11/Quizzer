import { useEffect, useState } from 'react';
import Button from '../Button';
import QuizEntry from '../QuizEntry'
import './Quizzes.css'
import { get_quiz_set } from '../../actions/quiz_editor';

function Quizzes() {

    const desc = 'lorem ipsum, quia dolor sit, amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam. lorem ipsum, quia dolor sit, amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam. ';

    const [quizzesList, setQuizzesList] = useState({
        results: [{
            name: "",
            topic: "",
            author: 0,
            pk: 0
        }],
        users_names: []
    });
    
    // setQuizzesList(get_user_quiz_set());

    useEffect(() => {
        const fetchData = async () => {
          try {
            // Assume fetchDataFunction is a predefined function that returns a promise
            const result = await get_quiz_set();
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

    return (
        <>
            <div className="container-header-quizzes">
                <div className="header-title">Quizy</div>
            </div>
            <div className="filter-bar">
                <form>
                    <div className="dropdown" tabIndex={0}>
                        <div className="dropdown-trigger" tabIndex={0}>Kategorie</div>
                        <div className="dropdown-content">
                            <label>
                                <input type="checkbox"></input>Matematyka
                            </label>
                            <label>
                                <input type="checkbox"></input>Fizyka
                            </label>
                        </div>
                    </div>
                    <div className="search-bar">
                        {/* <TextInput></TextInput> */}
                    </div>
                </form>
                <div className="button-panel">
                    <Button className="primary" link="/Create-Quiz">Stwórz Quiz</Button>
                </div>
            </div>
{/* 
            <QuizEntry name="Matematyka" description={desc} author="Jan Kowalski"></QuizEntry>
            <QuizEntry name="Fizyka" description={desc} author="Jan Kowalski"></QuizEntry>
            <QuizEntry name="Informatyka" description={desc} author="Jan Kowalski"></QuizEntry>
            <QuizEntry name="Biologia" description={desc} author="Jan Kowalski"></QuizEntry>
            <QuizEntry name="Geografia" description={desc} author="Jan Kowalski"></QuizEntry>
            <QuizEntry name="Chemia" description={desc} author="Jan Kowalski"></QuizEntry> */}
            {quizzesList.results.map((item, id) => (
                <QuizEntry key={id} pk={item.pk} name={item.name} description={item.topic} author={quizzesList.users_names[item.author]}></QuizEntry>
            ))}

        </>
    )
}

export default Quizzes;