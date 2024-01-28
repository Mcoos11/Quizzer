import Button from '../Button';
import QuizEntry from '../QuizEntry'
import './Quizzes.css'

function Quizzes() {

    const desc = 'lorem ipsum, quia dolor sit, amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam. lorem ipsum, quia dolor sit, amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt, ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam. ';

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

            <QuizEntry name="Matematyka" description={desc} author="Jan Kowalski"></QuizEntry>
            <QuizEntry name="Fizyka" description={desc} author="Jan Kowalski"></QuizEntry>
            <QuizEntry name="Informatyka" description={desc} author="Jan Kowalski"></QuizEntry>
            <QuizEntry name="Biologia" description={desc} author="Jan Kowalski"></QuizEntry>
            <QuizEntry name="Geografia" description={desc} author="Jan Kowalski"></QuizEntry>
            <QuizEntry name="Chemia" description={desc} author="Jan Kowalski"></QuizEntry>

        </>
    )
}

export default Quizzes;