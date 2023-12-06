import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { login } from '../actions/auth'

const Login = ({ login, isAuthenticated }) => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });

    const { email, password } = formData;
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });
    const onSubmit = e => {
        e.preventDefault();
        login(email, password);
    }

    if(isAuthenticated){
        return <Navigate to='/' />;
    }

    return (
        <div className='container mt-5'>
            <h1>Logowanie</h1>
            <form onSubmit={e => onSubmit(e)}>
                <div className='form-group'>
                    <input 
                        className='form-control mb-1'
                        type='email'
                        placeholder='Email'
                        name='email'
                        value={email}
                        onChange={e => onChange(e)}
                        required
                    />
                    <input
                        className='form-control mb-1'
                        type='password'
                        placeholder='Hasło'
                        name='password'
                        value={password}
                        onChange={e => onChange(e)}
                        minLength='6'
                        required
                    />
                </div>
                <button className='btn btn-primary' type='submit'>Zaloguj</button>
            </form>
            <p className='mt-3'>
                Nie masz konta? Załóż je <Link to='/signup'>tutaj</Link>!
            </p>
            <p className='mt-3'>
                <Link to='/reset-password'>Odzyskaj hasło</Link>
            </p>
        </div>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { login })(Login);