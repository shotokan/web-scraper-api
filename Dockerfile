FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxrandr2 \
    libxcomposite1 \
    libxdamage1 \
    libxkbcommon0 \
    libwayland-egl1 \
    libwayland-server0 \
    libgbm1 \
    libasound2 \
    libxshmfence1 \
    xdg-utils \
    fonts-liberation \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*


# Copiar dependencias y archivos del proyecto

RUN pip install --no-cache-dir playwright
RUN playwright install-deps
RUN playwright install
WORKDIR /app
COPY . /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar la aplicación
# Exponer el puerto de la aplicación
EXPOSE 8000

# Ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]