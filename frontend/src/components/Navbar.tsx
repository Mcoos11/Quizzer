import './Navbar.css'
import Button from './Button.tsx'
import logo from '../../img/logo.png'

import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { logout } from '../actions/auth';
import { load_user } from '../actions/auth';
import store from '../store'

function Navbar({ load_user, logout, isAuthenticated }: any) {

    load_user();
    const guestLinks = () => {return (
        <Fragment>
            <Button className="secondary" link="/Registration">Zarejestruj się</Button>
            <Button className="primary" link="/Login">Zaloguj</Button>
        </Fragment>
    )};

    const authLinks = () => { return (
        <div className="profile-container">
            <Button className="primary" onClick={logout}>Wyloguj</Button>
            <a href="/Profile" className="user-name">{String(store.getState()?.auth?.user?.first_name) + " " + String(store.getState()?.auth?.user?.last_name)}</a>
        </div>
    )};


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
                    <li><a href="/QuestionGenerator">Generowanie pytań</a></li>
                </ul>
            </nav>
            <div className="login-container">
                {isAuthenticated ? authLinks() : guestLinks()}
            </div>
        </header>
     );
}

const mapStateToProps = () => ({
    isAuthenticated: store.getState().auth.isAuthenticated,
});

export default connect(mapStateToProps, { load_user, logout })(Navbar);