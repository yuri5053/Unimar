// src/pages/QuestoesPage.jsx
import React, { useEffect, useState, useRef } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import api from '../services/api';
import './QuestoesPage.css'; // cria este CSS (exemplo abaixo)

function shuffleArray(a) {
  // Fisher-Yates
  const arr = [...a];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

export default function QuestoesPage() {
  const { id } = useParams(); // ex: "1,2,3"
  const materiaIds = (id || '').split(',').map((s) => Number(s)).filter(Boolean);
  const location = useLocation();
  const navigate = useNavigate();

  // tentativa de recuperar config (primeiro do location.state, depois do sessionStorage)
  const configFromState = location.state;
  const stored = sessionStorage.getItem('studyConfig');
  const config = configFromState || (stored ? JSON.parse(stored) : null);

  const [loading, setLoading] = useState(true);
  const [questoes, setQuestoes] = useState([]); // array final de questões
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({}); // { [questaoId]: { resposta, timeTakenSec } }
  const [error, setError] = useState('');
  const [timeLeft, setTimeLeft] = useState(null); // segundos, null = infinito
  const totalTimeRef = useRef(null); // total em segundos, para barra

  const intervalRef = useRef(null);
  const startTimeRef = useRef(null); // tempo quando abriu a questão atual

  // função para extrair opções da questão — ajuste conforme seu payload
  const getOptions = (q) => {
    // várias formas comuns:
    if (Array.isArray(q.opcoes) && q.opcoes.length) return q.opcoes; // [{id, texto}]
    if (Array.isArray(q.alternativas) && q.alternativas.length) return q.alternativas;
    // se seu backend retorna alternativaA/B/C/D:
    const opts = [];
    if (q.alternativaA) opts.push({ id: 'A', texto: q.alternativaA });
    if (q.alternativaB) opts.push({ id: 'B', texto: q.alternativaB });
    if (q.alternativaC) opts.push({ id: 'C', texto: q.alternativaC });
    if (q.alternativaD) opts.push({ id: 'D', texto: q.alternativaD });
    if (opts.length) return opts;
    return null; // resposta aberta
  };

  useEffect(() => {
    const init = async () => {
      if (!config || !materiaIds.length) {
        setError('Configuração de estudo não encontrada. Volte para a página de seleção.');
        setLoading(false);
        return;
      }

      try {
        // buscar questões por cada matéria (paralelo)
        const fetches = materiaIds.map((mid) => api.get(`Materia/${mid}/questoes`));
        const responses = await Promise.all(fetches);

        // responses[i].data -> array de questões dessa matéria
        let final = [];

        for (const resp of responses) {
          const arr = Array.isArray(resp.data) ? resp.data : [];
          // determina a matériaId (assume que cada questao tem materiaId ou we can get from arr[0].materiaId)
          const mid = arr.length
            ? (arr[0].materiaId || arr[0].materia_id || Number(resp.config.url.match(/Materia\/(\d+)/)?.[1]))
            : null;
          // find requested count:
          const requestedCount = config.numQuestoesPorMateria?.[mid] ?? 10;
          const take = Math.min(requestedCount, arr.length);
          const picked = shuffleArray(arr).slice(0, take);
          // anexa materia id em cada questao se não existir (para referência)
          const withMateria = picked.map((q) => ({ ...q, materiaId: Number(mid) }));
          final = final.concat(withMateria);
        }

        // embaralha o conjunto final (opcional)
        final = shuffleArray(final);

        setQuestoes(final);
        setLoading(false);

        // configurar timer
        if (config.tempo == null) {
          setTimeLeft(null); // infinito
          totalTimeRef.current = null;
        } else {
          const totalSec = Number(config.tempo) * 60;
          totalTimeRef.current = totalSec;
          setTimeLeft(totalSec);
        }

        // registro de início
        startTimeRef.current = Date.now();
      } catch (err) {
        console.error(err);
        setError('Erro ao carregar questões.');
        setLoading(false);
      }
    };

    init();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  // timer
  useEffect(() => {
    // se timeLeft === null => infinito => não inicia interval
    if (timeLeft === null) return;

    intervalRef.current = setInterval(() => {
      setTimeLeft((t) => {
        if (t === null) return null;
        if (t <= 1) {
          clearInterval(intervalRef.current);
          handleFinish(); // tempo acabou
          return 0;
        }
        return t - 1;
      });
    }, 1000);

    return () => clearInterval(intervalRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeLeft === null]); // reinicia apenas quando mudar entre infinito e não

  // marcar resposta local e (opcional) salvar imediatamente
  const handleAnswer = (questaoId, resposta) => {
    const now = Date.now();
    const timeTakenSec = Math.round((now - (startTimeRef.current || now)) / 1000);
    setAnswers((prev) => ({ ...prev, [questaoId]: { resposta, timeTakenSec, answeredAt: now } }));
    // reinicia o timer de questão
    startTimeRef.current = Date.now();
  };

  const handleNext = () => {
    if (currentIndex < questoes.length - 1) {
      setCurrentIndex(currentIndex + 1);
      startTimeRef.current = Date.now();
    }
  };
  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      startTimeRef.current = Date.now();
    }
  };

  // função para enviar respostas (batch)
  const submitAnswers = async (finalizar = true) => {
    // montar payload
    const payload = {
      respostas: Object.keys(answers).map((qid) => ({
        questaoId: qid,
        resposta: answers[qid].resposta,
        tempoSegundos: answers[qid].timeTakenSec,
      })),
      // se seu backend precisa do id do usuário, ele pode ler do token do request
      // ou você pode enviar userId aqui: userId: ...
      metadata: {
        materias: materiaIds,
        config,
      },
    };

    try {
      // tente enviar em batch — ajuste o endpoint conforme seu backend
      await api.post('/respostas/batch', payload);
      if (finalizar) {
        // limpa config
        sessionStorage.removeItem('studyConfig');
        // redireciona pra dashboard ou página de resultado
        navigate('/dashboard');
      }
    } catch (err) {
      console.error('Erro ao enviar respostas:', err);
      // Se endpoint diferente, implemente conforme seu backend (ex.: salvar por questão)
    }
  };

  // quando o tempo acabar
  const handleFinish = () => {
    // pode mostrar modal, etc. — por enquanto, submete automaticamente
    submitAnswers(true);
  };

  const formatTime = (sec) => {
    if (sec == null) return '--:--';
    const m = Math.floor(sec / 60)
      .toString()
      .padStart(2, '0');
    const s = (sec % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  if (loading) return <div className="questoes-loading">Carregando questões...</div>;
  if (error) return <div className="questoes-error">{error}</div>;
  if (!questoes.length) return <div className="questoes-empty">Nenhuma questão disponível.</div>;

  const q = questoes[currentIndex];
  const options = getOptions(q);

  const percentLeft =
    totalTimeRef.current && timeLeft != null
      ? Math.max(0, Math.round((timeLeft / totalTimeRef.current) * 100))
      : null;

  return (
    <div className="questoes-page">
      <div className="questoes-topbar">
        <div className="progress-info">
          <strong>
            {currentIndex + 1}/{questoes.length}
          </strong>
          <span className="questao-materia">Matéria: {q.materiaNome || q.materia || q.materiaId}</span>
        </div>

        <div className="timer-box">
          <div className="timer">{timeLeft === null ? 'Ilimitado' : formatTime(timeLeft)}</div>
          {percentLeft != null && (
            <div className="timer-bar">
              <div className="timer-bar-fill" style={{ width: `${percentLeft}%` }} />
            </div>
          )}
        </div>
      </div>

      <div className="questao-card">
        <h3 className="enunciado">{q.enunciado || q.titulo || 'Sem enunciado'}</h3>

        {options ? (
          <div className="opcoes-list">
            {options.map((opt, idx) => {
              // cria um id seguro para cada opção
              const optId = opt && (opt.id ?? opt.codigo ?? opt.letra ?? `opt-${idx}`);
              const selected = answers[q.id]?.resposta === optId;
              // texto da opção (vários formatos suportados)
              const labelText = (opt && (opt.texto ?? opt.text ?? opt.label)) ?? String(opt);
              return (
                <button
                  key={optId ?? idx}
                  className={`opcao ${selected ? 'selected' : ''}`}
                  onClick={() => handleAnswer(q.id, optId)}
                >
                  {labelText}
                </button>
              );
            })}
          </div>
        ) : (
          <div className="resposta-aberta">
            <textarea
              placeholder="Digite sua resposta..."
              value={answers[q.id]?.resposta || ''}
              onChange={(e) => handleAnswer(q.id, e.target.value)}
            />
          </div>
        )}

        <div className="nav-buttons">
          <button onClick={handlePrev} disabled={currentIndex === 0} className="nav-btn">
            Anterior
          </button>
          {currentIndex < questoes.length - 1 ? (
            <button onClick={handleNext} className="nav-btn primary">
              Próxima
            </button>
          ) : (
            <button onClick={() => submitAnswers(true)} className="nav-btn primary">
              Enviar e Finalizar
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
