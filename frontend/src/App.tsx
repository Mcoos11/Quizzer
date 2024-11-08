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
import CreateQuiz from './components/pages/CreateQuiz'
import Profile from './components/pages/Profile'
import EditQuiz from './components/pages/EditQuiz'
import CreateQuestion from './components/pages/CreateQuestion'
import EditQuestion from './components/pages/EditQuestion'
import CreateAnswer from './components/pages/CreateAnswer'
import Results from './components/pages/Results'

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
            <Route path="/Profile" element={<Profile />} />
            <Route path="/Registration" element={<Registration />} />
            <Route path="/Quizzes" element={<Quizzes />} />
            <Route path="/Create-Quiz" element={<CreateQuiz />} />
            <Route path="/Edit-Quiz/:quiz_pk" element={<EditQuiz />} />
            <Route path="/Create-Question/:quiz_pk" element={<CreateQuestion />} />
            <Route path="/Edit-Question/:quiz_pk/:question_pk" element={<EditQuestion />} />
            <Route path="/Create-Answer/:quiz_pk/:question_pk" element={<CreateAnswer />} />
            <Route path="/Quiz/:quiz_pk" element={<Quiz />} />
            <Route path="/Results/:quiz_pk" element={<Results />} />
            <Route path="/Courses" element={<Courses />} />
            <Route path="/QuestionGenerator" element={<QuestionGenerator />} />
          </Routes>
        </BrowserRouter>
      </Provider>
    </>
  );
}

export default App
