import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './components/pages/Home'
import Login from './components/pages/Login'
import Quizzes from './components/pages/Quizzes'
import Registration from './components/pages/Registration'
import Courses from './components/pages/Courses'
import Quiz from './components/pages/Quiz'
import QuestionGenerator from './components/pages/QuestionGenerator'

import { Provider } from 'react-redux';
import store from './store';

function App() {
  

  return (
    <>
      <Provider store={store}>
        <Navbar/>
        <BrowserRouter>
          <Routes>
            <Route index element={<Home />} />
            <Route path="/Home" element={<Home />} />
            <Route path="/Login" element={<Login />} />
            <Route path="/Registration" element={<Registration />} />
            <Route path="/Quizzes" element={<Quizzes />} />
            <Route path="/Quiz" element={<Quiz />} />
            <Route path="/Courses" element={<Courses />} />
            <Route path="/QuestionGenerator" element={<QuestionGenerator />} />
          </Routes>
        </BrowserRouter>
      </Provider>
    </>
  );
}

export default App
