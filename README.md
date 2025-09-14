# IA Agent para Generación de Pruebas Unitarias .NET

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![.NET 8.0+](https://img.shields.io/badge/.NET-8.0+-purple.svg)](https://dotnet.microsoft.com/download)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0+-green.svg)](https://langchain.com/)
[![AutoGen](https://img.shields.io/badge/AutoGen-0.2.0+-orange.svg)](https://microsoft.github.io/autogen/)

Un sistema multi-agente de IA avanzado con capacidades de memoria y herramientas externas (ReAct) especializado en la generación automática de pruebas unitarias para APIs REST desarrolladas en .NET.

## 🚀 Características Principales

- **🤖 Sistema Multi-Agente**: Colaboración inteligente entre agentes especializados
- **🧠 Memoria Persistente**: Recuerda conversaciones y contexto entre sesiones
- **🛠️ Herramientas Externas**: Ejecuta código y busca documentación automáticamente
- **🔄 Patrón ReAct**: Razonamiento y actuación iterativa para decisiones autónomas
- **🎯 Especialización**: Agentes especializados en análisis, generación, validación y optimización
- **📊 Soporte Multi-Framework**: xUnit, NUnit, MSTest
- **⚡ Ejecución Windows**: CLI optimizada para terminal de comandos

## 🏗️ Arquitectura

El sistema utiliza **LangChain** para capacidades ReAct individuales y **AutoGen** para colaboración entre agentes especializados:

- **Agente Analista**: Analiza código .NET y extrae información
- **Agente Generador**: Genera código de pruebas y templates
- **Agente Validador**: Valida código y ejecuta pruebas
- **Agente Optimizador**: Optimiza pruebas y sugiere mejoras
- **Agente Coordinador**: Coordina tareas y gestiona flujos de trabajo

## 📦 Instalación Rápida

```bash
# Crear entorno virtual
python -m venv ia-agent-env
ia-agent-env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar API keys
ia-agent config --setup
```

## 🎯 Uso Básico

### Modo Interactivo (Recomendado)
```bash
ia-agent interactive
```

### Comandos Directos
```bash
# Generar pruebas para un controlador
ia-agent generate --controller "UserController" --output "./Tests"

# Analizar cobertura de pruebas
ia-agent analyze --coverage --report-format html

# Optimizar pruebas existentes
ia-agent optimize --tests "./Tests" --framework xunit
```

### Modo Multi-Agente
```bash
# Activar colaboración entre agentes
ia-agent multi-agent --mode collaborative

# Ver colaboración en tiempo real
ia-agent multi-agent --monitor
```

## 📋 Requisitos del Sistema

- **Sistema Operativo**: Windows 10/11 (64-bit)
- **Python**: 3.11 o superior
- **.NET SDK**: 8.0 o superior
- **Memoria RAM**: 8GB mínimo, 16GB recomendado
- **Conexión a Internet**: Para APIs de IA

## 🔧 Configuración

### Variables de Entorno
```bash
# Copiar archivo de ejemplo
copy env.example .env

# Configurar API key de DeepSeek (recomendado)
DEEPSEEK_API_KEY=tu_api_key_aqui

# O configurar OpenAI como alternativa
OPENAI_API_KEY=tu_api_key_aqui
AI_PROVIDER=openai
```

### Archivo de Configuración
```yaml
# config/agent_configs/default.yaml
agent:
  mode: "multi-agent"
  memory:
    type: "persistent"
    storage_path: "./memory"

ai:
  provider: "deepseek"
  model: "deepseek-coder"
  temperature: 0.1
```

## 📚 Documentación

- [📋 Requisitos Funcionales y Técnicos](docs/requirements.md)
- [🏗️ Arquitectura del Sistema](docs/architecture.md)
- [📖 Guía de Instalación y Uso](plan.MD#guía-de-instalación-y-uso-para-desarrolladores)
- [🎯 Plan de Desarrollo Completo](plan.MD)

## 🛠️ Desarrollo

### Estructura del Proyecto
```
ia-agent-unit-tests/
├── src/
│   ├── agents/                 # Agentes especializados
│   ├── multi_agent/            # Sistema multi-agente
│   ├── langchain_agents/       # Agentes individuales
│   ├── tools/                  # Herramientas del agente
│   └── cli/                    # Interfaz CLI
├── templates/                  # Templates de pruebas
├── memory/                     # Almacenamiento de memoria
├── config/                     # Configuraciones
└── docs/                       # Documentación
```

### Contribuir
1. Fork el repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📊 Estado del Proyecto

### ✅ Fases Completadas

#### Fase 1: Análisis y Diseño ✅
- [x] Estructura del proyecto creada
- [x] Dependencias configuradas
- [x] Repositorio Git inicializado
- [x] Archivos de configuración creados
- [x] Requisitos documentados
- [x] Arquitectura diseñada

#### Fase 2: Desarrollo del Sistema Multi-Agente ✅
- [x] Agentes especializados implementados
- [x] Sistema de memoria vectorial
- [x] Herramientas .NET integradas
- [x] CLI básico funcional
- [x] Sistema de logging implementado

#### Fase 3: Funcionalidades Avanzadas ✅
- [x] Suite de testing completa
- [x] Mejoras de IA implementadas
- [x] Sistema de monitoreo
- [x] Documentación de API
- [x] Optimizaciones de rendimiento

#### Fase 4: Optimización y Despliegue ✅
- [x] Sistema de configuración robusto
- [x] Manager de memoria optimizado
- [x] Optimizador de rendimiento
- [x] Manejador de errores avanzado
- [x] Configuración Docker completa
- [x] Scripts de despliegue automatizado
- [x] Validador de producción

#### Fase 5: Documentación Final y Entrega ✅
- [x] Guía de usuario completa
- [x] Guía de desarrollador
- [x] Guía de despliegue
- [x] Documentación de API
- [x] Guía de solución de problemas
- [x] Changelog del proyecto
- [x] Licencia MIT

### 🎯 Versión Actual: v0.4.0
- **Estado**: ✅ **COMPLETADO Y LISTO PARA PRODUCCIÓN**
- **Funcionalidades**: 25+ características principales
- **Tests**: 100% de componentes cubiertos
- **Documentación**: 5 guías completas
- **Despliegue**: Docker y scripts automatizados

## 🤝 Soporte

- **GitHub Issues**: Para reportar bugs y solicitar features
- **Documentación**: Wiki completa con ejemplos
- **Email**: soporte@ia-agent.com

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- [LangChain](https://langchain.com/) - Framework para agentes con capacidades ReAct
- [AutoGen](https://microsoft.github.io/autogen/) - Framework para colaboración multi-agente
- [OpenAI](https://openai.com/) - APIs de IA para generación de código
- Comunidad .NET por las mejores prácticas de testing

---

**Desarrollado con ❤️ para la comunidad .NET**