# Guía de Uso

## IA Agent para Generación de Pruebas Unitarias .NET

### Tabla de Contenidos

1. [Instalación](#instalación)
2. [Configuración Inicial](#configuración-inicial)
3. [Uso Básico](#uso-básico)
4. [Uso Avanzado](#uso-avanzado)
5. [Ejemplos Prácticos](#ejemplos-prácticos)
6. [Troubleshooting](#troubleshooting)

---

## Instalación

### Requisitos Previos

- Python 3.8+
- .NET SDK 6.0+
- Git

### Instalación de Dependencias

```bash
# Clonar repositorio
git clone <repository-url>
cd ia-agent-to-unit-tes-api-rest

# Instalar dependencias Python
pip install -r requirements.txt

# Verificar instalación
python -c "import sys; sys.path.insert(0, 'src'); from utils.config import get_config; print('✅ Instalación exitosa')"
```

### Configuración de Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar .env con tus configuraciones
nano .env
```

---

## Configuración Inicial

### 1. Configurar API Keys

Edita el archivo `.env`:

```env
# OpenAI
OPENAI_API_KEY=tu_api_key_aqui

# Azure OpenAI (alternativa)
AZURE_OPENAI_ENDPOINT=https://tu-recurso.openai.azure.com/
AZURE_OPENAI_API_KEY=tu_azure_api_key

# Anthropic (alternativa)
ANTHROPIC_API_KEY=tu_anthropic_api_key
```

### 2. Configurar Memoria

```env
# ChromaDB
CHROMA_PERSIST_DIRECTORY=./memory/vector_stores/chroma
CHROMA_COLLECTION_NAME=ia_agent_memory
```

### 3. Configurar Logging

```env
# Nivel de logging
LOG_LEVEL=INFO

# Archivo de log
LOG_FILE=./logs/agent.log
```

---

## Uso Básico

### 1. Análisis de Código

```python
import sys
from pathlib import Path
sys.path.insert(0, 'src')

from agents.analysis_agent import AnalysisAgent
from tools.file_tools import file_manager

# Crear agente de análisis
agent = AnalysisAgent()

# Leer código
code = file_manager.read_file("Calculator.cs")

# Analizar código
result = agent.analyze_code(code)
print(result)
```

### 2. Generación de Pruebas

```python
from agents.generation_agent import GenerationAgent

# Crear agente de generación
agent = GenerationAgent()

# Generar pruebas
tests = agent.generate_tests(code, framework="xunit")
print(tests)
```

### 3. Uso del CLI

```bash
# Ejecutar CLI
python -m src.cli.main

# O usar directamente
python src/cli/main.py
```

---

## Uso Avanzado

### 1. Multi-Agente

```python
from agents.coordinator_agent import CoordinatorAgent
from ai.context_manager import ContextManager

# Crear coordinador
coordinator = CoordinatorAgent()

# Crear context manager
context_manager = ContextManager()
session = context_manager.create_session("proyecto1")

# Coordinar tarea compleja
result = coordinator.coordinate_task(
    "Analizar proyecto completo y generar todas las pruebas unitarias"
)
```

### 2. Memoria Persistente

```python
from langchain_agents.memory.conversation_memory import ConversationMemory
from langchain_agents.memory.vector_memory import VectorMemory

# Memoria de conversación
conversation_memory = ConversationMemory(
    agent_name="analyst",
    storage_path="./memory"
)

# Memoria vectorial
vector_memory = VectorMemory(
    agent_name="analyst",
    storage_path="./memory"
)

# Agregar contexto
vector_memory.add_document(
    content="Código del proyecto",
    metadata={"tipo": "código", "proyecto": "Calculator"}
)

# Buscar contexto relevante
results = vector_memory.search("Calculator", limit=5)
```

### 3. Monitoreo y Métricas

```python
from monitoring.metrics_collector import MetricsCollector

# Crear collector
collector = MetricsCollector(storage_path="./metrics")

# Registrar métricas
collector.record_metric("response_time", 0.5)
collector.record_metric("success_count", 1)

# Obtener dashboard
dashboard_data = collector.get_dashboard_data()
print(dashboard_data)
```

---

## Ejemplos Prácticos

### Ejemplo 1: Análisis de Proyecto Completo

```python
import sys
from pathlib import Path
sys.path.insert(0, 'src')

from agents.analysis_agent import AnalysisAgent
from agents.generation_agent import GenerationAgent
from tools.file_tools import file_manager
from tools.dotnet_tools import dotnet_manager

def analyze_project(project_path):
    """Analizar proyecto completo"""
    
    # Crear agentes
    analysis_agent = AnalysisAgent()
    generation_agent = GenerationAgent()
    
    # Obtener información del proyecto
    project_info = dotnet_manager.get_project_info(project_path)
    print(f"Proyecto: {project_info}")
    
    # Buscar archivos C#
    cs_files = list(Path(project_path).glob("**/*.cs"))
    
    results = []
    for cs_file in cs_files:
        print(f"Analizando: {cs_file}")
        
        # Leer código
        code = file_manager.read_file(str(cs_file))
        
        # Analizar código
        analysis = analysis_agent.analyze_code(code)
        
        # Generar pruebas
        tests = generation_agent.generate_tests(code, analysis, "xunit")
        
        results.append({
            "file": str(cs_file),
            "analysis": analysis,
            "tests": tests
        })
    
    return results

# Usar función
project_results = analyze_project("./mi_proyecto")
```

### Ejemplo 2: Pipeline de Testing

```python
def testing_pipeline(project_path):
    """Pipeline completo de testing"""
    
    # 1. Análisis
    analysis_agent = AnalysisAgent()
    code = file_manager.read_file("Calculator.cs")
    analysis = analysis_agent.analyze_code(code)
    
    # 2. Generación
    generation_agent = GenerationAgent()
    tests = generation_agent.generate_tests(code, analysis, "xunit")
    
    # 3. Validación
    validation_agent = ValidationAgent()
    validation = validation_agent.validate_tests(code, tests)
    
    # 4. Optimización
    optimization_agent = OptimizationAgent()
    optimized_tests = optimization_agent.optimize_tests(tests)
    
    # 5. Guardar resultados
    file_manager.write_file("CalculatorTests.cs", optimized_tests)
    
    return {
        "analysis": analysis,
        "tests": optimized_tests,
        "validation": validation
    }

# Ejecutar pipeline
results = testing_pipeline("./proyecto")
```

### Ejemplo 3: Monitoreo en Tiempo Real

```python
import time
from monitoring.metrics_collector import MetricsCollector

def monitor_system():
    """Monitorear sistema en tiempo real"""
    
    collector = MetricsCollector()
    
    while True:
        # Simular operación
        start_time = time.time()
        
        # ... realizar operación ...
        
        # Registrar métricas
        response_time = time.time() - start_time
        collector.record_metric("response_time", response_time)
        
        # Mostrar dashboard
        dashboard = collector.get_dashboard_data()
        print(f"Tiempo de respuesta: {dashboard['performance']['avg_response_time']:.2f}s")
        
        time.sleep(60)  # Esperar 1 minuto

# Ejecutar monitoreo
monitor_system()
```

---

## Troubleshooting

### Problemas Comunes

#### 1. Error de Importación

```
ModuleNotFoundError: No module named 'langchain'
```

**Solución:**
```bash
pip install langchain langchain-openai langchain-community
```

#### 2. Error de ChromaDB

```
ValueError: An instance of Chroma already exists
```

**Solución:**
```bash
# Limpiar instancias existentes
rm -rf ./memory/vector_stores/chroma
```

#### 3. Error de API Key

```
AuthenticationError: Invalid API key
```

**Solución:**
- Verificar que el archivo `.env` existe
- Verificar que la API key es correcta
- Verificar que la API key tiene permisos suficientes

#### 4. Error de Memoria

```
MemoryError: Unable to allocate memory
```

**Solución:**
- Reducir el tamaño de los documentos
- Usar procesamiento en lotes
- Aumentar la memoria disponible

### Logs y Debugging

#### Habilitar Logs Detallados

```env
LOG_LEVEL=DEBUG
```

#### Ver Logs en Tiempo Real

```bash
tail -f logs/agent.log
```

#### Debug de Agentes

```python
from utils.logging import get_logger

logger = get_logger("debug")
logger.debug("Información de debug")
```

### Performance

#### Optimizar Rendimiento

1. **Usar LLM más rápido:**
```python
from ai.llm_manager import LLMManager

manager = LLMManager()
manager.switch_llm("fast")  # Usar GPT-3.5-turbo
```

2. **Procesamiento en lotes:**
```python
responses = manager.generate_batch(prompts)
```

3. **Caché de resultados:**
```python
from ai.context_manager import ContextManager

context_manager = ContextManager()
# El context manager mantiene caché automáticamente
```

### Soporte

Para problemas adicionales:

1. Revisar logs en `./logs/`
2. Verificar configuración en `.env`
3. Ejecutar tests: `python run_tests.py`
4. Consultar documentación en `./docs/`
