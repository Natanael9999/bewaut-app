@@ -0,0 +1,59 @@
 from fastapi import FastAPI
 from fastapi.staticfiles import StaticFiles
 import serial
 import requests
 import threading
 import time
 
 # Configuração da porta serial
 SERIAL_PORT = "COM3"
 baud_rate = 9600
 ser = serial.Serial(SERIAL_PORT, baud_rate, timeout=1)
 
 # Variável global para armazenar o estado da torneira
 torneira_status = "Desconhecido"
 
 # Configuração da API do OpenWeatherMap
 WEATHER_API_KEY = "d4f1f3ab1b1d4840e939f8bbb02b8888"
 CITY = "Itapetinga"
 WEATHER_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
 
 app = FastAPI()
 
 # Servir arquivos estáticos (frontend)
 app.mount("/static", StaticFiles(directory="frontend"), name="static")
 
 def get_weather():
     """ Obtém a previsão do tempo da cidade especificada """
     try:
         response = requests.get(WEATHER_URL)
         data = response.json()
         rain = data.get("rain", {}).get("1h", 0)  # Probabilidade de chuva na última hora
         return rain
     except Exception as e:
         print(f"Erro ao obter clima: {e}")
         return None
 
 def read_serial():
     """ Lê os dados do serial e atualiza o estado da torneira """
     global torneira_status
     while True:
         if ser.in_waiting > 0:
             line = ser.readline().decode('utf-8').strip()
             torneira_status = "Aberta" if line == "1" else "Fechada"
         time.sleep(1)
 
 @app.get("/status")
 def read_status():
     """ Obtém o status do sensor e a previsão do tempo """
     rain_probability = get_weather()
     return {"torneira": torneira_status, "chuva": rain_probability}
 
 if __name__ == "__main__":
     # Inicia a thread para ler o serial
     serial_thread = threading.Thread(target=read_serial, daemon=True)
     serial_thread.start()
 
     # Inicia o servidor FastAPI
     import uvicorn
     uvicorn.run(app, host="0.0.0.0", port=8000)