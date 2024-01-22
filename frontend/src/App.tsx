import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './components/pages/Home'
import Login from './components/pages/Login'
import Quizzes from './components/pages/Quizzes'
import Registration from './components/pages/Registration'
import Courses from './components/pages/Courses'
import Quiz from './components/pages/Quiz'

function App() {
  

  return (
    <>
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
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App