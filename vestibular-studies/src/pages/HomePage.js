import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="container" style={{ textAlign: 'center', marginTop: '100px' }}>
      <h1>Bem-vindo ao VestibularApp</h1>
      <div style={{ marginTop: '40px' }}>
        <button
          className="button"
          style={{ marginRight: '20px' }}
          onClick={() => navigate('/login')}
        >
          Entrar
        </button>
        <button
          className="button"
          onClick={() => navigate('/login', { state: { cadastro: true } })}
        >
          Cadastrar
        </button>
      </div>
    </div>
  );
}
