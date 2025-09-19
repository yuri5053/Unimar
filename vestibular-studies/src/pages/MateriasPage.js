// src/pages/MateriasPage.jsx
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

export default function MateriasPage() {
  const [materias, setMaterias] = useState([]);
  const [erro, setErro] = useState('');

  useEffect(() => {
    api.get('Materia')
      .then((res) => setMaterias(res.data))
      .catch(() => setErro('Erro ao buscar matérias. Faça login novamente.'));
  }, []);

  return (
  <div className="container">
    <h1>Matérias</h1>

    {erro && <p style={{ color: 'red' }}>{erro}</p>}

    {materias.map((m) => (
      <div key={m.id} className="card">
        <a href={`/materias/${m.id}/questoes`}>{m.nome}</a>
      </div>
    ))}
  </div>
);

}
