FROM python:3.10-slim

WORKDIR /app

# Kopiowanie zależności
COPY requirements.txt .

# Instalacja pakietów
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie reszty kodu
COPY . .

# Konfiguracja strefy czasowej (przydatne dla giełdy)
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Uruchomienie głównego procesu demona
CMD ["python", "-u", "run_server.py"]
