// src/pages/LoginPage.jsx
import React, { useState } from 'react';
import api from '../services/api';
import { useNavigate, useLocation } from 'react-router-dom';
import './LoginPage.css'; // CSS separado para deixar o código limpo

export default function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [cadastro, setCadastro] = useState(location.state?.cadastro || false);
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erro, setErro] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setErro('');
    try {
      const response = await api.post('Usuario/login', { email, senha });
      const { token } = response.data;
      localStorage.setItem('token', token);
      navigate('/study');
    } catch {
      setErro('Login falhou. Verifique seus dados.');
    }
  };

  const handleCadastro = async (e) => {
    e.preventDefault();
    setErro('');
    try {
      await api.post('Usuario/cadastro', { nome, email, senha });
      setCadastro(false);
      setNome('');
      setEmail('');
      setSenha('');
      alert('Cadastro realizado com sucesso! Faça login.');
    } catch {
      setErro('Cadastro falhou. Tente outro email.');
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>{cadastro ? 'Cadastro' : 'Login'}</h1>
        {erro && <p className="error">{erro}</p>}
        <form onSubmit={cadastro ? handleCadastro : handleLogin}>
          {cadastro && (
            <input
              className="input-field"
              type="text"
              placeholder="Nome"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              required
            />
          )}
          <input
            className="input-field"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            className="input-field"
            type="password"
            placeholder="Senha"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            required
          />
          <button className="btn-submit" type="submit">
            {cadastro ? 'Cadastrar' : 'Entrar'}
          </button>
        </form>
        <div className="switch-mode">
          {cadastro ? (
            <span>
              Já tem conta?{' '}
              <button className="btn-switch" onClick={() => setCadastro(false)}>
                Login
              </button>
            </span>
          ) : (
            <span>
              Não tem conta?{' '}
              <button className="btn-switch" onClick={() => setCadastro(true)}>
                Cadastrar
              </button>
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
