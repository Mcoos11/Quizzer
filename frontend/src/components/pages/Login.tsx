import './Login.css'
import Button from '../Button.tsx'
import TextInput from '../TextInput.tsx';
import { FormEvent } from 'react';

import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { login } from '../../actions/auth';


function Login({ login, isAuthenticated}: any) {
    
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });

    const { email, password } = formData;
    const onChange = (e: any) => setFormData({ ...formData, [e.target.name]: e.target.value });
    const onSubmit = (e: any) => {
        e.preventDefault();
        login(email, password);
    }

    if(isAuthenticated){
        return <Navigate to='/' />;
    }

    return (
        <>
            <form className="login-form" onSubmit={e => onSubmit(e)}>
                <h1>Zaloguj się</h1>
                <TextInput
                        name='email'
                        value={email}
                        onChange={(e: any) => onChange(e)}>E-mail</TextInput>
                <TextInput 
                        type="password"
                        name='password'
                        value={password}
                        onChange={(e: any) => onChange(e)}>Hasło</TextInput>
                <Button className="primary" type="submit">Zaloguj</Button>
            </form>
        </>
    )
}


const mapStateToProps = (state: any) => ({
    isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { login })(Login);
//export default Login;