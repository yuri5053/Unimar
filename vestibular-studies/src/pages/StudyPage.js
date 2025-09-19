// src/pages/StudyPage.jsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './StudyPage.css';

export default function StudyPage() {
  const navigate = useNavigate();
  const [materias, setMaterias] = useState([]);
  const [selectedMaterias, setSelectedMaterias] = useState([]);
  const [numQuestoesPorMateria, setNumQuestoesPorMateria] = useState({});
  const [tempo, setTempo] = useState(30);
  const [tempoInfinito, setTempoInfinito] = useState(false);
  const [erro, setErro] = useState('');

  useEffect(() => {
    const fetchMaterias = async () => {
      try {
        const response = await api.get('Materia');
        // garante que ids são números
        const data = Array.isArray(response.data)
          ? response.data.map((m) => ({ ...m, id: Number(m.id) }))
          : [];
        setMaterias(data);
      } catch {
        setErro('Erro ao buscar matérias. Faça login novamente.');
      }
    };
    fetchMaterias();
  }, []);

  const handleCheckbox = (id) => {
    const numId = Number(id);
    if (selectedMaterias.includes(numId)) {
      setSelectedMaterias(selectedMaterias.filter((mid) => mid !== numId));
      const newNums = { ...numQuestoesPorMateria };
      delete newNums[numId];
      setNumQuestoesPorMateria(newNums);
    } else {
      setSelectedMaterias([...selectedMaterias, numId]);
      setNumQuestoesPorMateria({ ...numQuestoesPorMateria, [numId]: 10 });
    }
  };

  const handleNumQuestoesChange = (id, value) => {
    const num = Math.max(1, Math.min(50, Number(value) || 1)); // garante 1..50 e número
    setNumQuestoesPorMateria({ ...numQuestoesPorMateria, [Number(id)]: num });
  };

  const handleStart = () => {
    setErro('');

    if (selectedMaterias.length === 0) {
      setErro('Selecione pelo menos uma matéria.');
      return;
    }

    // garante que cada matéria selecionada tenha uma quantidade válida
    const finalNums = { ...numQuestoesPorMateria };
    selectedMaterias.forEach((mid) => {
      if (!finalNums[mid]) finalNums[mid] = 10;
      finalNums[mid] = Math.max(1, Math.min(50, Number(finalNums[mid] || 10)));
    });

    // garante que tempo é number e dentro de 1..300 (quando não infinito)
    const finalTempo = tempoInfinito ? null : Math.max(1, Math.min(300, Number(tempo || 1)));

    const studyConfig = {
      selectedMaterias,
      numQuestoesPorMateria: finalNums,
      tempo: finalTempo, // minutos or null
      startedAt: Date.now(),
    };

    // salva em sessionStorage para persistir recarregamentos
    try {
      sessionStorage.setItem('studyConfig', JSON.stringify(studyConfig));
    } catch (err) {
      console.warn('Não foi possível salvar studyConfig no sessionStorage:', err);
    }

    navigate(`/materias/${selectedMaterias.join(',')}/questoes`, { state: studyConfig });
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <div className="study-page">
      <div className="study-card">
        <h1 className="study-title">Preparar Sessão de Estudo</h1>
        {erro && <p className="error">{erro}</p>}

        {/* Seção de Matérias */}
        <div className="section">
          <h2 className="section-title">Matérias</h2>
          <p className="section-subtitle">
            Selecione uma ou mais matérias e defina a quantidade de questões para cada uma (1 a 50).
          </p>

          <div className="materias-container">
            {materias.map((m) => (
              <div
                key={m.id}
                className={`materia-card ${selectedMaterias.includes(m.id) ? 'selected' : ''}`}
              >
                <label className="custom-checkbox" htmlFor={`materia-${m.id}`}>
                  <input
                    id={`materia-${m.id}`}
                    type="checkbox"
                    checked={selectedMaterias.includes(m.id)}
                    onChange={() => handleCheckbox(m.id)}
                  />
                  <span className="checkmark" aria-hidden="true"></span>
                  <span style={{ marginLeft: 6 }}>{m.nome}</span>
                </label>

                {selectedMaterias.includes(m.id) && (
                  <div className="num-questoes-wrapper">
                    <label htmlFor={`num-questoes-${m.id}`} className="num-questoes-label">
                      Quantidade de questões:
                    </label>
                    <input
                      id={`num-questoes-${m.id}`}
                      type="number"
                      min="1"
                      max="50"
                      value={numQuestoesPorMateria[m.id] ?? 10}
                      onChange={(e) => handleNumQuestoesChange(m.id, e.target.value)}
                      className="input-field small-input"
                      disabled={tempoInfinito}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Seção de Tempo */}
        <div className="section">
          <h2 className="section-title">Tempo de estudo</h2>
          <div className="tempo-card">
            <label className="custom-checkbox" htmlFor="tempo-ilimitado">
              <input
                id="tempo-ilimitado"
                type="checkbox"
                checked={tempoInfinito}
                onChange={(e) => setTempoInfinito(e.target.checked)}
              />
              <span className="checkmark" aria-hidden="true"></span>
              <span style={{ marginLeft: 6 }}>Tempo ilimitado</span>
            </label>

            {!tempoInfinito && (
              <div className="form-group">
                <label htmlFor="tempo-minutos">Tempo (minutos, 1 a 300):</label>
                <input
                  id="tempo-minutos"
                  type="number"
                  min="1"
                  max="300"
                  value={tempo}
                  onChange={(e) => setTempo(Math.max(1, Math.min(300, Number(e.target.value || 1))))}
                  className="input-field"
                />
              </div>
            )}
          </div>
        </div>

        <div className="buttons-container">
          <button className="btn-submit" onClick={handleStart}>
            Começar
          </button>
          <button className="btn-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}
