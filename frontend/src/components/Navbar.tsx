import './Navbar.css'
import Button from './Button.tsx'
import logo from '../../img/logo.png'

function Navbar() {
    return ( 
        <header className="navbar">
            <h3 className="logo">
                <img src={logo}></img>
            </h3>
            <nav className="main-nav">
                <ul>
                    <li><a href="/Home">O nas</a></li>
                    <li><a href="/Courses">Kursy</a></li>
                    <li><a href="/Quizzes">Quizy</a></li>
                </ul>
            </nav>
            <div className="login-container">
                <Button className="secondary" link="/Registration">Zarejestruj się</Button>
                <Button className="primary" link="/Login">Zaloguj</Button>
            </div>
        </header>
     );
}

export default Navbar;