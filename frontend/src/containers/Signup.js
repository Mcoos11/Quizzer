import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { signup } from '../actions/auth'

const Signup = ({ signup, isAuthenticated }) => {
    const [accountCreated, setAccountCreated] = useState(false);
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        re_password: '',
    });

    const { first_name, last_name, email, password, re_password } = formData;
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });
    const onSubmit = e => {
        e.preventDefault();
        if (password === re_password){
            signup(first_name, last_name, email, password, re_password);
            setAccountCreated(true);
        }
    }

    if(isAuthenticated){
        return <Navigate to='/' />;
    }
    if(accountCreated){
        return <Navigate to='/login' />;
    }

    return (
        <div className='container mt-5'>
            <h1>Rejestracja</h1>
            <form onSubmit={e => onSubmit(e)}>
                <div className='form-group'>
                    <input 
                        className='form-control mb-1'
                        type='text'
                        placeholder='Imię'
                        name='first_name'
                        value={first_name}
                        onChange={e => onChange(e)}
                        required
                    />
                    <input 
                        className='form-control mb-1'
                        type='text'
                        placeholder='Namzwisko'
                        name='last_name'
                        value={last_name}
                        onChange={e => onChange(e)}
                        required
                    />
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
                    <input
                        className='form-control mb-1'
                        type='password'
                        placeholder='Powtórz hasło'
                        name='re_password'
                        value={re_password}
                        onChange={e => onChange(e)}
                        minLength='6'
                        required
                    />
                </div>
                <button className='btn btn-primary' type='submit'>Zarejestruj</button>
            </form>
            <p className='mt-3'>
                Masz już konto? Zaloguj się <Link to='/login'>tutaj</Link>!
            </p>
        </div>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { signup })(Signup);