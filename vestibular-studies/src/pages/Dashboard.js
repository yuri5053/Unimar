// src/pages/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Link } from 'react-router-dom';
import Header from '../components/Header';

export default function Dashboard() {
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    api.get('/questoes')
      .then((response) => setQuestions(response.data))
      .catch((err) => console.error(err));
  }, []);

  return (
  <div className="container">
    <h1>Questões de Vestibular</h1>

    {questions.map((q) => (
      <div key={q.id} className="card">
        <a href={`/materias/${q.materiaId}/questoes`}>{q.titulo}</a>
      </div>
    ))}
  </div>
);
}
