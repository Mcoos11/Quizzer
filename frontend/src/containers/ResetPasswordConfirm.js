import React, { useState } from 'react';
import { Navigate, useParams } from 'react-router-dom';
import { connect } from 'react-redux';
import { reset_password_confirm } from '../actions/auth'

const ResetPasswordConfirm = ({ reset_password_confirm }) => {
    const routeParams = useParams();
    const [requestSent, setRequestSent] = useState(false);
    const [formData, setFormData] = useState({
        new_password: '',
        re_new_password: '',
    });

    const { new_password, re_new_password } = formData;
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });
    const onSubmit = e => {
        e.preventDefault();
        const uid = routeParams.uid;
        const token = routeParams.token;
        reset_password_confirm(uid, token, new_password, re_new_password);
        setRequestSent(true);
    }

    if(requestSent){
        return <Navigate to='/' />;
    }

    return (
        <div className='container mt-5'>
            <h1>Reset hasła</h1>
            <form onSubmit={e => onSubmit(e)}>
                <div className='form-group'>
                    <input
                        className='form-control mb-1'
                        type='password'
                        placeholder='Nowe hasło'
                        name='new_password'
                        value={new_password}
                        onChange={e => onChange(e)}
                        minLength='6'
                        required
                    />
                    <input
                        className='form-control mb-1'
                        type='password'
                        placeholder='Powtórz hasło'
                        name='re_new_password'
                        value={re_new_password}
                        onChange={e => onChange(e)}
                        minLength='6'
                        required
                    />
                </div>
                <button className='btn btn-primary' type='submit'>Wyślij</button>
            </form>
        </div>
    );
};

export default connect(null, { reset_password_confirm })(ResetPasswordConfirm);