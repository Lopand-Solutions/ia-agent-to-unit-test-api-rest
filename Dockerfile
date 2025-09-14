# Dockerfile para IA Agent - Generación de Pruebas Unitarias .NET
FROM python:3.11-slim

# Metadatos
LABEL maintainer="IA Agent Team"
LABEL description="IA Agent para Generación de Pruebas Unitarias .NET"
LABEL version="0.3.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar .NET SDK
RUN wget https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb -O packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install -y dotnet-sdk-8.0 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN groupadd -r iaagent && useradd -r -g iaagent iaagent

# Crear directorios de trabajo
WORKDIR /app
RUN mkdir -p /app/logs /app/memory /app/temp /app/output \
    && chown -R iaagent:iaagent /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/
COPY run_tests.py .
COPY README.md .

# Cambiar permisos
RUN chown -R iaagent:iaagent /app

# Cambiar a usuario no-root
USER iaagent

# Exponer puerto (si se necesita para API futura)
EXPOSE 8000

# Variables de entorno por defecto
ENV LOG_LEVEL=INFO
ENV DEBUG_MODE=false
ENV CHROMADB_PERSIST_DIRECTORY=/app/memory/vector
ENV TEMP_DIRECTORY=/app/temp
ENV OUTPUT_DIRECTORY=/app/output

# Comando por defecto
CMD ["python", "run_tests.py"]
