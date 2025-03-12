"use client";
import React, { useEffect, useState } from "react";
import "./style.css";

export default function Home() {
  const [status, setStatus] = useState({ torneira: "Desconhecido" });
  const [error, setError] = useState(null);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    if (isClient) {
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
      const interval = setInterval(fetchStatus, 5000); // Atualiza a cada 5s
      return () => clearInterval(interval);
    }
  }, [isClient]);

  if (!isClient) {
    return null;
  }

  return (
    <div className="page">
      <h1 className="title">Sistema de Irrigação</h1>
      {error ? (
        <p className="error">Erro: {error}</p>
      ) : (
        <div className="status">
          <p>Irrigação: {status.torneira}</p>
        </div>
      )}
    </div>
  );
}
