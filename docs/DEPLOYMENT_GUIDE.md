# 🚀 Guía de Despliegue - IA Agent para Generación de Pruebas Unitarias .NET

## 📋 Prerrequisitos

### Sistema
- **OS**: Linux (Ubuntu 20.04+), Windows 10+, macOS 10.15+
- **RAM**: Mínimo 4GB, Recomendado 8GB+
- **CPU**: Mínimo 2 cores, Recomendado 4+ cores
- **Disco**: Mínimo 10GB libres

### Software
- **Python**: 3.11+
- **.NET**: 8.0+
- **Docker**: 20.10+ (opcional)
- **Docker Compose**: 2.0+ (opcional)
- **Git**: 2.30+

## 🏗️ Opciones de Despliegue

### 1. Despliegue Local (Desarrollo)

#### Instalación Manual

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd ia-agent-to-unit-tes-api-rest

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp env.example .env
# Editar .env con tu configuración

# 5. Verificar instalación
python validate_production.py

# 6. Ejecutar sistema
python run_tests.py
```

#### Configuración de Variables

```bash
# .env
OPENAI_API_KEY=tu_api_key_aqui
AI_PROVIDER=openai
AI_MODEL=gpt-4
LOG_LEVEL=INFO
DEBUG_MODE=false
CHROMADB_PERSIST_DIRECTORY=./memory/vector
TEMP_DIRECTORY=./temp
OUTPUT_DIRECTORY=./output
MAX_CONCURRENT_AGENTS=3
AGENT_TIMEOUT=60
```

### 2. Despliegue con Docker

#### Construcción de Imagen

```bash
# Construir imagen
docker build -t ia-agent:latest .

# Verificar imagen
docker images ia-agent
```

#### Ejecución con Docker

```bash
# Ejecutar contenedor
docker run -d \
  --name ia-agent \
  -p 8000:8000 \
  -e OPENAI_API_KEY=tu_api_key \
  -e LOG_LEVEL=INFO \
  -v $(pwd)/projects:/app/projects:ro \
  -v $(pwd)/output:/app/output \
  ia-agent:latest

# Verificar estado
docker ps
docker logs ia-agent
```

#### Docker Compose

```bash
# Desarrollo
docker-compose up --build

# Producción
docker-compose -f docker-compose.yml --profile production up -d

# Con monitoreo
docker-compose -f docker-compose.yml --profile monitoring up -d
```

### 3. Despliegue en Producción

#### Script Automatizado

```bash
# Despliegue completo
python deploy.py production

# Solo construcción
python deploy.py production --skip-build

# Verificar salud
python deploy.py production --health
```

#### Configuración de Producción

```bash
# Variables de entorno para producción
export ENVIRONMENT=production
export LOG_LEVEL=WARNING
export DEBUG_MODE=false
export MAX_CONCURRENT_AGENTS=5
export AGENT_TIMEOUT=120
export MEMORY_CACHE_SIZE=2000
export ENABLE_TELEMETRY=true
```

## 🐳 Configuración Docker

### Dockerfile Optimizado

```dockerfile
# Dockerfile.production
FROM python:3.11-slim

# Metadatos
LABEL maintainer="IA Agent Team"
LABEL version="0.4.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar .NET SDK
RUN wget https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install -y dotnet-sdk-8.0 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN groupadd -r iaagent && useradd -r -g iaagent iaagent

# Crear directorios
WORKDIR /app
RUN mkdir -p /app/logs /app/memory /app/temp /app/output \
    && chown -R iaagent:iaagent /app

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY src/ ./src/
COPY run_tests.py .
COPY validate_production.py .

# Cambiar permisos
RUN chown -R iaagent:iaagent /app
USER iaagent

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python validate_production.py || exit 1

# Comando por defecto
CMD ["python", "validate_production.py"]
```

### Docker Compose para Producción

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  ia-agent:
    build:
      context: .
      dockerfile: Dockerfile.production
    container_name: ia-agent-prod
    restart: unless-stopped
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=WARNING
      - DEBUG_MODE=false
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MAX_CONCURRENT_AGENTS=5
      - AGENT_TIMEOUT=120
    volumes:
      - ./logs:/app/logs
      - ./memory:/app/memory
      - ./output:/app/output
      - ./projects:/app/projects:ro
    networks:
      - ia-agent-network
    healthcheck:
      test: ["CMD", "python", "validate_production.py"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  monitoring:
    build: .
    container_name: ia-agent-monitoring
    restart: unless-stopped
    command: ["python", "-c", "import time; time.sleep(3600)"]
    environment:
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    networks:
      - ia-agent-network
    depends_on:
      - ia-agent

volumes:
  ia-agent-data:
    driver: local

networks:
  ia-agent-network:
    driver: bridge
```

## ☁️ Despliegue en la Nube

### AWS

#### EC2

```bash
# 1. Crear instancia EC2
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.medium \
  --key-name tu-key \
  --security-groups ia-agent-sg

# 2. Conectar a instancia
ssh -i tu-key.pem ubuntu@tu-instancia-ip

# 3. Instalar dependencias
sudo apt update
sudo apt install python3.11 python3.11-venv git docker.io docker-compose

# 4. Clonar y desplegar
git clone <repository-url>
cd ia-agent-to-unit-tes-api-rest
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Configurar y ejecutar
cp env.example .env
# Editar .env
python deploy.py production
```

#### ECS

```json
{
  "family": "ia-agent",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "ia-agent",
      "image": "tu-account.dkr.ecr.region.amazonaws.com/ia-agent:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        },
        {
          "name": "LOG_LEVEL",
          "value": "WARNING"
        }
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:ia-agent/openai-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ia-agent",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Azure

#### Container Instances

```bash
# 1. Crear resource group
az group create --name ia-agent-rg --location eastus

# 2. Crear container instance
az container create \
  --resource-group ia-agent-rg \
  --name ia-agent \
  --image tu-registry.azurecr.io/ia-agent:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8000 \
  --environment-variables \
    ENVIRONMENT=production \
    LOG_LEVEL=WARNING \
  --secure-environment-variables \
    OPENAI_API_KEY=tu_api_key
```

#### App Service

```bash
# 1. Crear App Service
az webapp create \
  --resource-group ia-agent-rg \
  --plan ia-agent-plan \
  --name ia-agent-app \
  --deployment-container-image-name tu-registry.azurecr.io/ia-agent:latest

# 2. Configurar variables de entorno
az webapp config appsettings set \
  --resource-group ia-agent-rg \
  --name ia-agent-app \
  --settings \
    ENVIRONMENT=production \
    LOG_LEVEL=WARNING \
    OPENAI_API_KEY=tu_api_key
```

### Google Cloud

#### Cloud Run

```bash
# 1. Construir y subir imagen
gcloud builds submit --tag gcr.io/tu-project/ia-agent

# 2. Desplegar en Cloud Run
gcloud run deploy ia-agent \
  --image gcr.io/tu-project/ia-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production,LOG_LEVEL=WARNING \
  --set-secrets OPENAI_API_KEY=openai-key:latest
```

## 🔧 Configuración de Producción

### Variables de Entorno

```bash
# Configuración de producción
ENVIRONMENT=production
LOG_LEVEL=WARNING
DEBUG_MODE=false
AI_PROVIDER=openai
AI_MODEL=gpt-4
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2000
MAX_CONCURRENT_AGENTS=5
AGENT_TIMEOUT=120
MEMORY_CACHE_SIZE=2000
CHROMADB_PERSIST_DIRECTORY=/app/memory/vector
TEMP_DIRECTORY=/app/temp
OUTPUT_DIRECTORY=/app/output
ENABLE_TELEMETRY=true
ENABLE_HEALTH_CHECKS=true
```

### Configuración de Logging

```python
# logging.conf
[loggers]
keys=root,ia_agent

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=WARNING
handlers=consoleHandler

[logger_ia_agent]
level=INFO
handlers=consoleHandler,fileHandler
qualname=ia_agent
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=simpleFormatter
args=('/app/logs/ia_agent.log',)

[formatter_simpleFormatter]
format=%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

### Configuración de Monitoreo

```yaml
# monitoring.yml
monitoring:
  enabled: true
  metrics:
    enabled: true
    port: 8080
    path: /metrics
  health_checks:
    enabled: true
    interval: 60
    timeout: 10
  alerts:
    enabled: true
    webhook_url: "https://hooks.slack.com/services/..."
    thresholds:
      cpu_percent: 80
      memory_percent: 85
      response_time_ms: 5000
```

## 🔒 Seguridad

### Configuración de Seguridad

```bash
# Variables de seguridad
ENABLE_FILE_VALIDATION=true
ALLOWED_FILE_EXTENSIONS=.cs,.csproj,.sln
MAX_FILE_SIZE=10485760
ENCRYPT_MEMORY=false
API_RATE_LIMIT=100
API_RATE_WINDOW=3600
```

### Secrets Management

```bash
# Usar secrets manager
# AWS
aws secretsmanager create-secret \
  --name "ia-agent/openai-key" \
  --description "OpenAI API Key" \
  --secret-string "tu_api_key_aqui"

# Azure
az keyvault secret set \
  --vault-name ia-agent-vault \
  --name openai-key \
  --value "tu_api_key_aqui"

# Google Cloud
gcloud secrets create openai-key --data-file=- <<< "tu_api_key_aqui"
```

### Network Security

```yaml
# docker-compose.security.yml
version: '3.8'

services:
  ia-agent:
    # ... configuración existente
    networks:
      - ia-agent-internal
    # No exponer puertos innecesarios

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    networks:
      - ia-agent-internal
      - ia-agent-external
    depends_on:
      - ia-agent

networks:
  ia-agent-internal:
    driver: bridge
    internal: true
  ia-agent-external:
    driver: bridge
```

## 📊 Monitoreo y Observabilidad

### Métricas

```python
# Configuración de métricas
METRICS_ENABLED=true
METRICS_PORT=8080
METRICS_PATH=/metrics
METRICS_INTERVAL=30
```

### Logging Centralizado

```yaml
# docker-compose.logging.yml
version: '3.8'

services:
  ia-agent:
    # ... configuración existente
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  fluentd:
    image: fluent/fluentd:latest
    volumes:
      - ./fluentd.conf:/fluentd/etc/fluent.conf
      - /var/log:/var/log
    ports:
      - "24224:24224"
    depends_on:
      - ia-agent
```

### Health Checks

```python
# health_check.py
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/health')
def health_check():
    try:
        # Verificar servicios
        response = requests.get('http://ia-agent:8000/health', timeout=5)
        if response.status_code == 200:
            return jsonify({"status": "healthy"}), 200
        else:
            return jsonify({"status": "unhealthy"}), 503
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

## 🔄 CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: python run_tests.py
    
    - name: Build Docker image
      run: docker build -t ia-agent:${{ github.sha }} .
    
    - name: Deploy to production
      run: |
        # Comandos de despliegue
        python deploy.py production
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - python -m pip install --upgrade pip
    - pip install -r requirements.txt
    - python run_tests.py

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - python deploy.py production
  only:
    - main
```

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. Error de Memoria
```bash
# Verificar uso de memoria
docker stats ia-agent

# Aumentar límite de memoria
docker run -m 4g ia-agent
```

#### 2. Error de Red
```bash
# Verificar conectividad
docker exec ia-agent ping google.com

# Verificar DNS
docker exec ia-agent nslookup google.com
```

#### 3. Error de Permisos
```bash
# Verificar permisos
ls -la /app

# Corregir permisos
chown -R iaagent:iaagent /app
```

### Logs de Debugging

```bash
# Ver logs del contenedor
docker logs ia-agent

# Ver logs en tiempo real
docker logs -f ia-agent

# Ver logs específicos
docker exec ia-agent tail -f /app/logs/ia_agent.log
```

### Recuperación de Desastres

```bash
# Backup de datos
docker exec ia-agent tar -czf /app/backup.tar.gz /app/memory /app/output

# Restaurar datos
docker exec ia-agent tar -xzf /app/backup.tar.gz -C /app/

# Restaurar desde backup
docker-compose down
docker-compose up -d
```

---

## 📞 Soporte

### Recursos de Ayuda
- **Documentación**: `docs/`
- **Issues**: GitHub Issues
- **Logs**: `/app/logs/`
- **Métricas**: `http://localhost:8080/metrics`

### Contacto
- **Email**: [tu-email@ejemplo.com]
- **Slack**: [canal-de-soporte]
- **GitHub**: [tu-usuario-github]

---

*Última actualización: Septiembre 2025*
