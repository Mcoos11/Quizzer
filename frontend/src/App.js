// import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import Home from './containers/Home';
import Signup from './containers/Signup';
import Login from './containers/Login';
import ResetPassword from './containers/ResetPassword';
import ResetPasswordConfirm from './containers/ResetPasswordConfirm';
import Activate from './containers/Activate'
import NoPage from './containers/NoPage';

import { Provider } from 'react-redux';
import store from './store';

import Layout from './hocs/Layout';

export default function App() {
  return (
    <Provider store={store}>
      <Router>
        <Layout>
          <Routes>
            <Route index path="/" element={<Home />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/login" element={<Login />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path="/password/reset/confirm/:uid/:token" element={<ResetPasswordConfirm />} />
            <Route path="/activate/:uid/:token" element={<Activate />} />
            <Route path="*" element={<NoPage />} />
          </Routes>
        </Layout>
      </Router>
    </Provider>
  );
};