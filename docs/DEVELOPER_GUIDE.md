# 👨‍💻 Guía de Desarrollador - IA Agent para Generación de Pruebas Unitarias .NET

## 🏗️ Arquitectura del Sistema

### Visión General

El sistema está construido con una arquitectura modular basada en agentes de IA, utilizando patrones de diseño como Singleton, Factory, y Observer para garantizar escalabilidad y mantenibilidad.

```
┌─────────────────────────────────────────────────────────────┐
│                    IA Agent System                         │
├─────────────────────────────────────────────────────────────┤
│  CLI Layer (src/cli/)                                      │
│  ├── simple_cli.py                                         │
│  ├── multi_agent_cli.py                                    │
│  └── main.py                                               │
├─────────────────────────────────────────────────────────────┤
│  Agent Layer (src/agents/)                                 │
│  ├── analysis_agent.py                                     │
│  ├── generation_agent.py                                   │
│  ├── validation_agent.py                                   │
│  ├── optimization_agent.py                                 │
│  └── coordinator_agent.py                                  │
├─────────────────────────────────────────────────────────────┤
│  AI Layer (src/ai/)                                        │
│  ├── llm_manager.py                                        │
│  ├── prompt_engineer.py                                    │
│  ├── context_manager.py                                    │
│  └── ai_optimizer.py                                       │
├─────────────────────────────────────────────────────────────┤
│  Memory Layer (src/memory/)                                │
│  ├── memory_manager.py                                     │
│  └── vector_memory.py                                      │
├─────────────────────────────────────────────────────────────┤
│  Tools Layer (src/tools/)                                  │
│  ├── file_tools.py                                         │
│  └── dotnet_tools.py                                       │
├─────────────────────────────────────────────────────────────┤
│  Utils Layer (src/utils/)                                  │
│  ├── logging.py                                            │
│  ├── error_handler.py                                      │
│  └── chromadb_singleton.py                                 │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Configuración del Entorno de Desarrollo

### Prerrequisitos

```bash
# Python 3.11+
python --version

# .NET 8.0+
dotnet --version

# Git
git --version

# Docker (opcional)
docker --version
```

### Configuración Inicial

1. **Clonar y configurar:**
```bash
git clone <repository-url>
cd ia-agent-to-unit-tes-api-rest
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Si existe
```

3. **Configurar pre-commit hooks:**
```bash
pre-commit install
```

4. **Configurar IDE:**
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true
}
```

## 🧩 Componentes Principales

### 1. Sistema de Agentes

#### Base Agent
```python
# src/agents/base_agent.py
class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.memory = VectorMemory(name)
        self.tools = []
    
    async def process(self, input_data: Dict) -> Dict:
        # Implementación base
        pass
```

#### Analysis Agent
```python
# src/agents/analysis_agent.py
class AnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("analysis_agent", "analyst")
        self.code_analyzer = CodeAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
    
    async def analyze_code(self, file_path: str) -> AnalysisResult:
        # Análisis de código
        pass
```

### 2. Sistema de Memoria

#### Memory Manager
```python
# src/memory/memory_manager.py
class MemoryManager:
    def __init__(self):
        self.cache = MemoryCache()
        self.agent_memories = {}
        self.shared_memory = SharedMemory()
    
    def get_agent_memory(self, agent_name: str) -> VectorMemory:
        # Lazy loading de memorias
        pass
```

#### Vector Memory
```python
# src/langchain_agents/memory/vector_memory.py
class VectorMemory:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.chroma_client = chromadb_singleton.get_client(agent_name)
        self.collection = None
    
    def add_entry(self, content: str, metadata: Dict) -> str:
        # Agregar entrada a la memoria vectorial
        pass
```

### 3. Sistema de Herramientas

#### File Tools
```python
# src/tools/file_tools.py
class FileManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.allowed_extensions = ['.cs', '.csproj', '.sln']
    
    def read_file(self, file_path: str) -> str:
        # Lectura segura de archivos
        pass
    
    def write_file(self, file_path: str, content: str) -> bool:
        # Escritura segura de archivos
        pass
```

#### .NET Tools
```python
# src/tools/dotnet_tools.py
class DotNetManager:
    def __init__(self):
        self.project_analyzer = ProjectAnalyzer()
        self.command_executor = DotNetCommandExecutor()
    
    def build_project(self, project_path: str) -> Dict:
        # Compilación de proyectos .NET
        pass
```

## 🧪 Testing

### Estructura de Tests

```
tests/
├── __init__.py
├── test_agents.py          # Tests de agentes
├── test_ai.py              # Tests de IA
├── test_memory.py          # Tests de memoria
├── test_tools.py           # Tests de herramientas
├── test_monitoring.py      # Tests de monitoreo
└── test_integration.py     # Tests de integración
```

### Ejecutar Tests

```bash
# Todos los tests
python run_tests.py

# Tests específicos
python -m pytest tests/test_agents.py -v

# Tests con cobertura
python -m pytest --cov=src tests/

# Tests de integración
python -m pytest tests/test_integration.py -v
```

### Escribir Tests

```python
# tests/test_agents.py
import unittest
from unittest.mock import Mock, patch
from src.agents.analysis_agent import AnalysisAgent

class TestAnalysisAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AnalysisAgent()
    
    def test_agent_initialization(self):
        self.assertEqual(self.agent.name, "analysis_agent")
        self.assertEqual(self.agent.role, "analyst")
    
    @patch('src.tools.file_tools.file_manager')
    def test_analyze_code(self, mock_file_manager):
        mock_file_manager.read_file.return_value = "public class Test {}"
        result = self.agent.analyze_code("test.cs")
        self.assertIsNotNone(result)
```

## 🔍 Debugging

### Logging

```python
# Configuración de logging
import logging
from src.utils.logging import setup_logging

setup_logging("DEBUG")

# En tu código
logger = logging.getLogger(__name__)
logger.info("Mensaje informativo")
logger.error("Error ocurrido", exc_info=True)
```

### Debugging de Agentes

```python
# src/agents/analysis_agent.py
class AnalysisAgent(BaseAgent):
    async def analyze_code(self, file_path: str) -> AnalysisResult:
        logger.debug(f"Iniciando análisis de: {file_path}")
        
        try:
            # Tu código aquí
            result = await self._perform_analysis(file_path)
            logger.debug(f"Análisis completado: {result}")
            return result
        except Exception as e:
            logger.error(f"Error en análisis: {e}", exc_info=True)
            raise
```

### Profiling

```python
# Profiling de rendimiento
import cProfile
import pstats

def profile_function():
    # Tu función aquí
    pass

# Ejecutar profiling
cProfile.run('profile_function()', 'profile_output.prof')

# Analizar resultados
stats = pstats.Stats('profile_output.prof')
stats.sort_stats('cumulative').print_stats(10)
```

## 🚀 Despliegue

### Desarrollo Local

```bash
# Modo desarrollo
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG
python validate_production.py
```

### Docker

```bash
# Construir imagen
docker build -t ia-agent .

# Ejecutar contenedor
docker run -p 8000:8000 ia-agent

# Con docker-compose
docker-compose up --build
```

### Producción

```bash
# Despliegue automatizado
python deploy.py production

# Verificar estado
python validate_production.py
```

## 📊 Monitoreo y Métricas

### Métricas Personalizadas

```python
# src/monitoring/performance_optimizer.py
from src.monitoring.performance_optimizer import performance_optimizer

# Agregar métrica personalizada
performance_optimizer.add_metric(
    name="custom_operation",
    value=execution_time,
    unit="ms",
    metadata={"operation": "code_analysis"}
)

# Obtener estadísticas
stats = performance_optimizer.get_metric_stats("custom_operation")
print(f"Tiempo promedio: {stats['avg']}ms")
```

### Health Checks

```python
# src/monitoring/health_check.py
class HealthChecker:
    def check_system_health(self) -> Dict:
        health_status = {
            "status": "healthy",
            "checks": {
                "database": self._check_database(),
                "memory": self._check_memory(),
                "agents": self._check_agents()
            }
        }
        return health_status
```

## 🔧 Extensibilidad

### Agregar Nuevo Agente

```python
# src/agents/custom_agent.py
from src.agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__("custom_agent", "custom_role")
        self.custom_tools = []
    
    async def process(self, input_data: Dict) -> Dict:
        # Implementar lógica del agente
        result = await self._custom_processing(input_data)
        return result
    
    async def _custom_processing(self, data: Dict) -> Dict:
        # Lógica específica
        pass
```

### Agregar Nueva Herramienta

```python
# src/tools/custom_tools.py
from src.tools.base_tool import BaseTool

class CustomTool(BaseTool):
    def __init__(self):
        super().__init__("custom_tool")
    
    def execute(self, params: Dict) -> Dict:
        # Implementar funcionalidad
        return {"result": "success"}
```

### Configuración Personalizada

```python
# src/config/custom_config.py
from src.config.environment import EnvironmentConfig

class CustomConfig(EnvironmentConfig):
    custom_setting: str = Field("default_value", env="CUSTOM_SETTING")
    
    def get_custom_config(self) -> Dict:
        return {
            "custom_setting": self.custom_setting,
            "other_config": "value"
        }
```

## 🐛 Solución de Problemas

### Problemas Comunes

#### 1. Import Errors
```python
# Error: ModuleNotFoundError
# Solución: Verificar PYTHONPATH
import sys
sys.path.insert(0, 'src')
```

#### 2. ChromaDB Errors
```python
# Error: ChromaDB instance conflict
# Solución: Usar singleton
from src.utils.chromadb_singleton import chromadb_singleton
client = chromadb_singleton.get_client("agent_name")
```

#### 3. Memory Issues
```python
# Error: Memory overflow
# Solución: Limpiar cache
from src.memory.memory_manager import memory_manager
memory_manager.optimize_memory()
```

### Debugging Avanzado

```python
# Habilitar debugging detallado
import logging
logging.basicConfig(level=logging.DEBUG)

# Debugging de memoria
from src.memory.memory_manager import memory_manager
stats = memory_manager.get_memory_stats()
print(f"Cache stats: {stats}")

# Debugging de rendimiento
from src.monitoring.performance_optimizer import performance_optimizer
report = performance_optimizer.get_performance_report()
print(f"Performance: {report}")
```

## 📚 Recursos Adicionales

### Documentación
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Rich Documentation](https://rich.readthedocs.io/)

### Herramientas Recomendadas
- **IDE**: VS Code con extensiones Python
- **Testing**: pytest, coverage
- **Linting**: pylint, black, isort
- **Profiling**: cProfile, memory_profiler
- **Documentation**: Sphinx, mkdocs

### Patrones de Código

#### Singleton Pattern
```python
class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

#### Factory Pattern
```python
class AgentFactory:
    @staticmethod
    def create_agent(agent_type: str) -> BaseAgent:
        agents = {
            "analysis": AnalysisAgent,
            "generation": GenerationAgent,
            "validation": ValidationAgent
        }
        return agents[agent_type]()
```

#### Observer Pattern
```python
class EventObserver:
    def __init__(self):
        self.observers = []
    
    def subscribe(self, observer):
        self.observers.append(observer)
    
    def notify(self, event):
        for observer in self.observers:
            observer.update(event)
```

---

## 📝 Contribución

### Flujo de Trabajo

1. **Fork** del repositorio
2. **Crear branch** para feature: `git checkout -b feature/nueva-funcionalidad`
3. **Commit** cambios: `git commit -m "feat: agregar nueva funcionalidad"`
4. **Push** al branch: `git push origin feature/nueva-funcionalidad`
5. **Crear Pull Request**

### Estándares de Código

- **PEP 8** para estilo de código
- **Type hints** para todas las funciones
- **Docstrings** para todas las clases y métodos
- **Tests** para nueva funcionalidad
- **Logging** apropiado

### Code Review

- Revisar funcionalidad
- Verificar tests
- Comprobar documentación
- Validar rendimiento
- Confirmar seguridad

---

*Última actualización: Septiembre 2025*
