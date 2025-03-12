from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import serial
import threading
import time

# Configuração da porta serial
SERIAL_PORT = "COM9"
baud_rate = 9600

try:
    ser = serial.Serial(SERIAL_PORT, baud_rate, timeout=1)
except Exception as e:
    print(f"Erro ao conectar à porta serial: {e}")
    ser = None  # Evita falha caso a serial não esteja disponível

# Variável global para armazenar o estado da torneira
torneira_status = "Desconhecido"

app = FastAPI()

# Configuração do CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modifique para o domínio do seu frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def read_serial():
    """Lê os dados da serial e atualiza o estado da torneira"""
    global torneira_status
    if ser:
        while True:
            try:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    torneira_status = "Aberta" if line == "1" else "Fechada"
            except Exception as e:
                print(f"Erro na leitura serial: {e}")
            time.sleep(1)

@app.get("/status")
def read_status():
    return {"torneira": torneira_status}

if __name__ == "__main__":
    if ser:
        serial_thread = threading.Thread(target=read_serial, daemon=True)
        serial_thread.start()

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
