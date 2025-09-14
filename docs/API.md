# API Reference

## IA Agent para Generación de Pruebas Unitarias .NET

### Tabla de Contenidos

1. [Agentes](#agentes)
2. [Herramientas](#herramientas)
3. [Memoria](#memoria)
4. [IA Avanzada](#ia-avanzada)
5. [Monitoreo](#monitoreo)
6. [Configuración](#configuración)

---

## Agentes

### BaseAgent

Clase base para todos los agentes del sistema.

```python
from agents.base_agent import BaseAgent, AgentRole, AgentStatus

# Crear agente
agent = BaseAgent(
    name="mi_agente",
    role=AgentRole.ANALYST,
    system_message="Eres un analista de código experto"
)

# Propiedades
agent.name          # Nombre del agente
agent.role          # Rol del agente
agent.status        # Estado actual
agent.capabilities  # Lista de capacidades
agent.created_at    # Fecha de creación
```

### ReActAgent

Agente con capacidades de razonamiento y acción.

```python
from agents.base_agent import ReActAgent

# Crear agente ReAct
agent = ReActAgent(
    name="react_agent",
    role=AgentRole.ANALYST,
    system_message="Eres un agente de razonamiento"
)

# Agregar herramientas
agent.add_tool(tool)

# Ejecutar tarea
result = agent.run("Analiza este código: public class Test { }")
```

### AnalysisAgent

Agente especializado en análisis de código.

```python
from agents.analysis_agent import AnalysisAgent

# Crear agente de análisis
agent = AnalysisAgent()

# Obtener capacidades
capabilities = agent.get_capabilities()

# Analizar código
result = agent.analyze_code("public class Calculator { }")
```

### GenerationAgent

Agente especializado en generación de código y pruebas.

```python
from agents.generation_agent import GenerationAgent

# Crear agente de generación
agent = GenerationAgent()

# Generar pruebas
tests = agent.generate_tests(code, framework="xunit")
```

### ValidationAgent

Agente especializado en validación de código.

```python
from agents.validation_agent import ValidationAgent

# Crear agente de validación
agent = ValidationAgent()

# Validar código
result = agent.validate_code(code)
```

### OptimizationAgent

Agente especializado en optimización de código.

```python
from agents.optimization_agent import OptimizationAgent

# Crear agente de optimización
agent = OptimizationAgent()

# Optimizar código
optimized = agent.optimize_code(code)
```

### CoordinatorAgent

Agente coordinador para tareas complejas.

```python
from agents.coordinator_agent import CoordinatorAgent

# Crear agente coordinador
agent = CoordinatorAgent()

# Coordinar tarea
result = agent.coordinate_task("Generar pruebas para el proyecto")
```

---

## Herramientas

### FileManager

Gestor de operaciones de archivos.

```python
from tools.file_tools import file_manager

# Escribir archivo
file_manager.write_file("ruta/archivo.txt", "contenido")

# Leer archivo
content = file_manager.read_file("ruta/archivo.txt")

# Verificar existencia
exists = file_manager.file_exists("ruta/archivo.txt")

# Eliminar archivo
file_manager.delete_file("ruta/archivo.txt")

# Crear directorio
file_manager.create_directory("ruta/directorio")

# Listar archivos
files = file_manager.list_files("ruta/directorio")
```

### DotNetManager

Gestor de operaciones .NET.

```python
from tools.dotnet_tools import dotnet_manager

# Obtener versión de .NET
version = dotnet_manager.get_dotnet_version()

# Obtener información del proyecto
info = dotnet_manager.get_project_info("ruta/proyecto.csproj")

# Compilar proyecto
result = dotnet_manager.build_project("ruta/proyecto.csproj")

# Ejecutar pruebas
result = dotnet_manager.run_tests("ruta/proyecto.csproj")
```

---

## Memoria

### ConversationMemory

Memoria de conversación para agentes.

```python
from langchain_agents.memory.conversation_memory import ConversationMemory

# Crear memoria
memory = ConversationMemory(
    agent_name="mi_agente",
    storage_path="./memory"
)

# Agregar mensaje
memory.add_message("human", "Hola")

# Obtener historial
history = memory.get_conversation_history()

# Limpiar memoria
memory.clear_memory()
```

### VectorMemory

Memoria vectorial para búsqueda semántica.

```python
from langchain_agents.memory.vector_memory import VectorMemory

# Crear memoria vectorial
memory = VectorMemory(
    agent_name="mi_agente",
    storage_path="./memory"
)

# Agregar documento
memory.add_document(
    content="Contenido del documento",
    metadata={"tipo": "código"}
)

# Buscar documentos
results = memory.search("consulta", limit=5)
```

### SharedMemory

Memoria compartida entre agentes.

```python
from multi_agent.shared_memory import SharedMemory

# Crear memoria compartida
memory = SharedMemory(storage_path="./memory")

# Agregar entrada
memory.add_entry(
    agent_name="agente1",
    content="Contenido compartido",
    metadata={"tipo": "análisis"}
)

# Buscar entradas
results = memory.search("consulta", limit=5)
```

---

## IA Avanzada

### LLMManager

Gestor de modelos de lenguaje.

```python
from ai.llm_manager import LLMManager

# Crear manager
manager = LLMManager()

# Obtener LLM
llm = manager.get_llm("primary")

# Cambiar LLM
manager.switch_llm("fast")

# Generar respuesta asíncrona
response = await manager.generate_async("prompt")

# Generar en lote
responses = manager.generate_batch(["prompt1", "prompt2"])
```

### PromptEngineer

Ingeniero de prompts.

```python
from ai.prompt_engineer import PromptEngineer

# Crear engineer
engineer = PromptEngineer()

# Generar prompt
prompt = engineer.generate_prompt(
    "code_analysis",
    {"code": "public class Test { }", "context": "contexto"}
)

# Obtener templates disponibles
templates = engineer.get_available_templates()
```

### ContextManager

Gestor de contexto.

```python
from ai.context_manager import ContextManager

# Crear manager
manager = ContextManager()

# Crear sesión
session = manager.create_session("sesion1")

# Agregar contexto de código
manager.add_code_context("archivo.cs", "contenido")

# Establecer contexto de proyecto
manager.set_project_context("ruta", "nombre", "net8.0")

# Obtener contexto relevante
context = manager.get_relevant_context("consulta")
```

### AIOptimizer

Optimizador de IA.

```python
from ai.ai_optimizer import AIOptimizer

# Crear optimizer
optimizer = AIOptimizer()

# Optimizar prompt
optimized = await optimizer.optimize_prompt("prompt", context)

# Optimizar respuesta
result = await optimizer.optimize_response("respuesta", "prompt")

# Obtener métricas
metrics = optimizer.get_performance_metrics()
```

---

## Monitoreo

### MetricsCollector

Recolector de métricas.

```python
from monitoring.metrics_collector import MetricsCollector

# Crear collector
collector = MetricsCollector(storage_path="./metrics")

# Registrar métrica
collector.record_metric("nombre", 42.0, tags={"tipo": "test"})

# Registrar métricas del sistema
system_metrics = SystemMetrics(
    timestamp=datetime.now(),
    cpu_usage=75.5,
    memory_usage=60.2,
    disk_usage=45.8,
    active_sessions=5,
    requests_per_minute=120.0,
    average_response_time=0.5,
    error_rate=0.02
)
collector.record_system_metrics(system_metrics)

# Obtener métricas
metrics = collector.get_metrics(name="nombre")

# Obtener resumen
summary = collector.get_metric_summary("nombre", period_hours=24)

# Obtener datos del dashboard
dashboard_data = collector.get_dashboard_data()
```

---

## Configuración

### Config

Configuración del sistema.

```python
from utils.config import get_config

# Obtener configuración
config = get_config()

# Propiedades
config.agent          # Configuración de agentes
config.ai            # Configuración de IA
config.memory        # Configuración de memoria
config.testing       # Configuración de testing
config.generation    # Configuración de generación
config.multi_agent   # Configuración multi-agente
```

### Logging

Sistema de logging.

```python
from utils.logging import get_logger

# Obtener logger
logger = get_logger("mi_modulo")

# Usar logger
logger.info("Mensaje informativo")
logger.warning("Mensaje de advertencia")
logger.error("Mensaje de error")
logger.debug("Mensaje de debug")
```

---

## Ejemplos de Uso

### Análisis de Código

```python
from agents.analysis_agent import AnalysisAgent
from tools.file_tools import file_manager

# Crear agente
agent = AnalysisAgent()

# Leer código
code = file_manager.read_file("Calculator.cs")

# Analizar código
result = agent.analyze_code(code)
print(result)
```

### Generación de Pruebas

```python
from agents.generation_agent import GenerationAgent
from agents.analysis_agent import AnalysisAgent

# Crear agentes
analysis_agent = AnalysisAgent()
generation_agent = GenerationAgent()

# Analizar código
analysis = analysis_agent.analyze_code(code)

# Generar pruebas
tests = generation_agent.generate_tests(code, analysis, "xunit")
print(tests)
```

### Flujo Completo

```python
from agents.coordinator_agent import CoordinatorAgent
from ai.context_manager import ContextManager

# Crear coordinador
coordinator = CoordinatorAgent()

# Crear context manager
context_manager = ContextManager()
session = context_manager.create_session("proyecto1")

# Coordinar tarea completa
result = coordinator.coordinate_task(
    "Analizar y generar pruebas para el proyecto Calculator"
)
```

---

## Notas

- Todos los agentes requieren configuración adecuada de API keys
- La memoria vectorial requiere ChromaDB
- El sistema de monitoreo es opcional pero recomendado
- Los tests requieren dependencias adicionales
