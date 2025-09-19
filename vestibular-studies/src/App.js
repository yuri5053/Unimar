// src/App.js
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import MateriasPage from './pages/MateriasPage';
import QuestoesPage from './pages/QuestoesPage';
import StudyPage from './pages/StudyPage'; 
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/study" element={<StudyPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/materias" element={<MateriasPage />} />
        <Route path="/materias/:id/questoes" element={<QuestoesPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
