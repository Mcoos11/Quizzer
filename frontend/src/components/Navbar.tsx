import './Navbar.css'
import Button from './Button.tsx'
import logo from '../../img/logo.png'

import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import { logout } from '../actions/auth';
import store from '../store'

function Navbar({ logout, isAuthenticated }: any) {
    const guestLinks = () => (
        <Fragment>
            <Button className="secondary" link="/Registration">Zarejestruj się</Button>
            <Button className="primary" link="/Login">Zaloguj</Button>
        </Fragment>
    );

    const authLinks = () => (
        <Fragment>
            <Button className="primary" onClick={logout}>Wyloguj</Button>
        </Fragment>
    );
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
                {isAuthenticated ? authLinks() : guestLinks()}
            </div>
        </header>
     );
}

const mapStateToProps = () => ({
    isAuthenticated: store.getState().auth.isAuthenticated,
});

export default connect(mapStateToProps, { logout })(Navbar);