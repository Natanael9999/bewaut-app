import React, { useEffect, useState } from "react";
import "./page.css";

export default function Home() {
  const [status, setStatus] = useState({ torneira: "Desconhecido", chuva: null });
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch("http://localhost:8000/status");
        if (!response.ok) {
          throw new Error(`Erro ao buscar dados: ${response.statusText}`);
        }
        const data = await response.json();
        setStatus(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchStatus();
  }, []);

  return (
    <div className="page">
      <h1 className="title">Status do Sistema</h1>
      {error ? (
        <p className="error">Erro: {error}</p>
      ) : (
        <div className="status">
          <p>Irrigação: {status.torneira}</p>
          <p>Probabilidade de Chuva: {status.chuva !== null ? `${status.chuva}%` : "Desconhecido"}</p>
        </div>
      )}
    </div>
  );
}
