import React, { useState } from 'react';
import { Navigate, useParams } from 'react-router-dom';
import { connect } from 'react-redux';
import { verify } from '../actions/auth'

const Activate = ({ verify }) => {
    const routeParams = useParams();
    const [verified, setVerified] = useState(false);
    const verify_account = e => {
        const uid = routeParams.uid;
        const token = routeParams.token;
        verify(uid, token);
        setVerified(true);
    }

    if(verified){
        return <Navigate to='/login' />;
    }

    return (
        <div className='container'>
            <div className='d-flex flex-column justify-content-center align-items-center mt-5'>
                <h1>Zweryfikuj knto</h1>
                <button className='btn btn-primary mt-5' onClick={verify_account} type='button'>
                    Zweryfikuj
                </button>
            </div>
        </div>
    );
};

export default connect(null, { verify })(Activate);