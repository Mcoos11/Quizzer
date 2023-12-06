import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { logout } from '../actions/auth';

const Navbar = ({ logout, isAuthenticated }) => {
    const guestLinks = () => (
        <Fragment>
            <li className='nav-item'>
                <Link className='nav-link' to='/login'>Logowanie</Link>
            </li>
            <li className='nav-item'>
                <Link className='nav-link' to='/signup'>Rejestracja</Link>
            </li>
        </Fragment>
    );

    const authLinks = () => (
        <li className='nav-item'>
            <a className='nav-link' href='#!' onClick={logout}>Wyloguj</a>
        </li>
    );

    return (
        <nav className='navbar navbar-expand-lg bg-light mb-5'>
            <div className='container-fluid'>
                <Link className='navbar-brand' to='/'>HomePage</Link>
                <button className='navbar-toggler' type='button' data-bs-toggle='collapse' data-bs-target='#navbarNav' aria-controls='navbarNav' aria-expanded='false' aria-label='Toggle navigation'>
                <span className='navbar-toggler-icon'></span>
                </button>
                <div className='collapse navbar-collapse' id='navbarNav'>
                <ul className='navbar-nav'>
                    {isAuthenticated ? authLinks() : guestLinks()}
                </ul>
                </div>
            </div>
            </nav>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { logout })(Navbar);