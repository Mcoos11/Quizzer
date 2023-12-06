import React from 'react';
import { Link } from 'react-router-dom'

const Home = () => {
    return (
        <div className='container'>
            <div className='p-5 mb-4 bg-light rounded-3'>
                <h1 className='display-4'>Witamy!</h1>
                <p className='lead'>Tutaj może być jakiś opis...</p>
                <hr className='my-4' />
                <p>Tutaj też. LoginBtn -</p>
                <Link className='btn btn-primary btn-log' to='/login' role='button'>Logowanie</Link>
            </div>
        </div>
    );
};

export default Home;