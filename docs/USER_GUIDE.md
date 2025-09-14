# 📖 Guía de Usuario - IA Agent para Generación de Pruebas Unitarias .NET

## 🎯 Introducción

El **IA Agent** es un sistema inteligente que automatiza la generación de pruebas unitarias para proyectos .NET. Utiliza múltiples agentes de IA especializados para analizar código, generar pruebas, validar resultados y optimizar el proceso.

## 🚀 Inicio Rápido

### Prerrequisitos

- **Python 3.11+**
- **.NET 8.0+**
- **Docker** (opcional, para despliegue)
- **API Key de DeepSeek** (recomendado) o **OpenAI** (alternativa)

### Instalación

1. **Instalar desde PyPI (RECOMENDADO):**
```bash
pip install ia-agent-dotnet
```

2. **Configurar API key (una sola vez):**
```bash
ia-agent-config
```

3. **¡Listo para usar!**
```bash
ia-agent
```

### Instalación para Desarrollo

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Lopand-Solutions/ia-agent-to-unit-test-api-rest.git
cd ia-agent-to-unit-test-api-rest
```

2. **Instalar en modo desarrollo:**
```bash
pip install -e .
```

## 🖥️ Uso del Sistema

### Interfaz de Línea de Comandos (CLI)

#### Iniciar el CLI
```bash
# Descubrir y analizar proyectos automáticamente (NUEVO)
ia-agent

# O especificar un proyecto específico
ia-agent --project-path ./mi-proyecto
```

#### Comandos Disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `help` | Mostrar ayuda | `help` |
| `status` | Estado del sistema | `status` |
| `project <ruta>` | Establecer proyecto | `project ./mi_proyecto` |
| `analyze <archivo>` | Analizar archivo | `analyze Calculator.cs` |
| `generate <archivo>` | Generar pruebas | `generate Calculator.cs` |
| `validate <archivo>` | Validar código | `validate Calculator.cs` |
| `optimize <archivo>` | Optimizar código | `optimize Calculator.cs` |
| `exit` | Salir del sistema | `exit` |

### 🔍 Descubrimiento Automático de Proyectos (NUEVO)

El agente ahora detecta automáticamente todos los proyectos .NET en el directorio actual:

```bash
# Navega a tu directorio de proyecto
cd ./mi-proyecto-dotnet

# Ejecuta el agente (descubre automáticamente)
ia-agent
```

**El agente mostrará una tabla como esta:**
```
📁 Proyectos .NET Encontrados
┌────┬─────────────────┬─────────────┬──────────┬─────────────────────┐
│ ID │ Nombre          │ Tipo        │ Framework│ Ruta                │
├────┼─────────────────┼─────────────┼──────────┼─────────────────────┤
│ 1  │ 🌐 MyWebApi     │ web-api     │ net8.0   │ ./src/MyWebApi      │
│ 2  │ 📚 MyLibrary    │ class-lib   │ net8.0   │ ./src/MyLibrary     │
│ 3  │ 🧪 MyTests      │ test        │ net8.0   │ ./tests/MyTests     │
└────┴─────────────────┴─────────────┴──────────┴─────────────────────┘

🎯 Selecciona un proyecto (1-3) o 'q' para salir: 1
✅ Proyecto seleccionado: MyWebApi
```

### Ejemplo de Uso Completo

```bash
# 1. Descubrir y seleccionar proyecto automáticamente
ia-agent

# 2. Analizar archivo
analyze src/Calculator.cs

# 3. Generar pruebas
generate src/Calculator.cs

# 4. Validar resultados
validate tests/CalculatorTests.cs
```

## 🤖 Agentes del Sistema

### 1. **Analysis Agent** (Agente Analista)
- **Función**: Analiza código .NET y extrae información
- **Capacidades**:
  - Detección de clases y métodos
  - Análisis de dependencias
  - Identificación de patrones de código
  - Extracción de metadatos

### 2. **Generation Agent** (Agente Generador)
- **Función**: Genera pruebas unitarias
- **Capacidades**:
  - Creación de pruebas xUnit/NUnit/MSTest
  - Generación de casos de prueba
  - Configuración de mocks
  - Documentación de pruebas

### 3. **Validation Agent** (Agente Validador)
- **Función**: Valida código y pruebas
- **Capacidades**:
  - Verificación de sintaxis
  - Validación de cobertura
  - Detección de errores
  - Análisis de calidad

### 4. **Optimization Agent** (Agente Optimizador)
- **Función**: Optimiza código y pruebas
- **Capacidades**:
  - Refactoring automático
  - Optimización de rendimiento
  - Mejora de legibilidad
  - Eliminación de código muerto

### 5. **Coordinator Agent** (Agente Coordinador)
- **Función**: Coordina el trabajo entre agentes
- **Capacidades**:
  - Orquestación de tareas
  - Gestión de flujo de trabajo
  - Resolución de conflictos
  - Monitoreo de progreso

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `OPENAI_API_KEY` | Clave API de OpenAI | Requerido para OpenAI |
| `DEEPSEEK_API_KEY` | Clave API de DeepSeek | Requerido para DeepSeek |
| `AI_PROVIDER` | Proveedor de IA | `openai` |
| `AI_MODEL` | Modelo de IA | `gpt-4` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |
| `DEBUG_MODE` | Modo debug | `false` |
| `MAX_CONCURRENT_AGENTS` | Agentes concurrentes | `3` |
| `AGENT_TIMEOUT` | Timeout de agentes | `60` |

### Configuración de Archivos

El sistema busca archivos de configuración en este orden:
1. Variables de entorno
2. Archivo `.env`
3. Valores por defecto

### Configuración por Defecto (DeepSeek)

El sistema está configurado para usar **DeepSeek** por defecto:

```bash
# Configuración automática (ya incluida)
AI_PROVIDER=deepseek
AI_MODEL=deepseek-coder
AI_TEMPERATURE=0.1
AI_MAX_TOKENS=4000

# Solo necesitas configurar tu API key
DEEPSEEK_API_KEY=tu_api_key_aqui
```

**Ventajas de DeepSeek (Proveedor por Defecto):**
- ✅ Más económico que OpenAI GPT-4
- ✅ Especializado en programación
- ✅ Respuestas rápidas
- ✅ API compatible con OpenAI
- ✅ Optimizado para generación de código

**Modelos disponibles:**
- `deepseek-chat`: Modelo general de chat
- `deepseek-coder`: Especializado en programación (por defecto)
- `deepseek-math`: Especializado en matemáticas

### Configuración Alternativa (Gemini)

Para usar Gemini (Google AI):

```bash
# Configurar variables de entorno
export GEMINI_API_KEY="tu_api_key_aqui"
export AI_PROVIDER="gemini"
export AI_MODEL="gemini-pro"

# O usar archivo .env
GEMINI_API_KEY=tu_api_key_aqui
AI_PROVIDER=gemini
AI_MODEL=gemini-pro
```

**Ventajas de Gemini:**
- ✅ Gratuito hasta cierto límite
- ✅ Bueno para análisis general
- ✅ Integración con Google AI
- ✅ Respuestas rápidas

### Configuración Alternativa (OpenAI)

Para usar OpenAI:

```bash
# Configurar variables de entorno
export OPENAI_API_KEY="tu_api_key_aqui"
export AI_PROVIDER="openai"
export AI_MODEL="gpt-4"

# O usar archivo .env
OPENAI_API_KEY=tu_api_key_aqui
AI_PROVIDER=openai
AI_MODEL=gpt-4
```

## 📁 Estructura de Proyectos

### Proyecto .NET Típico
```
mi_proyecto/
├── src/
│   ├── Calculator.cs
│   ├── MathService.cs
│   └── Models/
├── tests/
│   ├── CalculatorTests.cs
│   └── MathServiceTests.cs
└── mi_proyecto.csproj
```

### Archivos Generados
```
output/
├── tests/
│   ├── CalculatorTests.cs
│   └── MathServiceTests.cs
├── reports/
│   ├── coverage_report.html
│   └── analysis_report.json
└── logs/
    └── generation.log
```

## 🔧 Herramientas Integradas

### File Manager
- Lectura/escritura de archivos
- Validación de extensiones
- Gestión de directorios
- Backup automático

### .NET Tools
- Análisis de proyectos
- Compilación automática
- Ejecución de pruebas
- Generación de reportes

### Memory System
- Cache inteligente
- Persistencia de datos
- Búsqueda semántica
- Optimización automática

## 📊 Monitoreo y Métricas

### Métricas Disponibles
- **Rendimiento**: Tiempo de respuesta, uso de CPU/memoria
- **Calidad**: Cobertura de pruebas, complejidad ciclomática
- **Uso**: Comandos ejecutados, archivos procesados
- **Errores**: Tipos de errores, frecuencia, resolución

### Acceso a Métricas
```bash
# Ver métricas en tiempo real
python -c "import sys; sys.path.insert(0, 'src'); from monitoring.performance_optimizer import performance_optimizer; print(performance_optimizer.get_performance_report())"
```

## 🐳 Despliegue con Docker

### Desarrollo
```bash
docker-compose up --build
```

### Producción
```bash
python deploy.py production
```

### Verificar Estado
```bash
docker-compose ps
docker-compose logs ia-agent
```

## 🛠️ Solución de Problemas

### Problemas Comunes

#### 1. Error de API Key
```
OPENAI_API_KEY no configurado
```
**Solución**: Configurar la variable de entorno o archivo `.env`

#### 2. Error de .NET
```
.NET no encontrado
```
**Solución**: Instalar .NET 8.0+ y verificar PATH

#### 3. Error de ChromaDB
```
ChromaDB no disponible
```
**Solución**: El sistema funciona en modo sin persistencia

#### 4. Error de Memoria
```
Memoria insuficiente
```
**Solución**: Aumentar `MEMORY_CACHE_SIZE` o reiniciar sistema

### Logs y Debugging

#### Ver Logs
```bash
tail -f logs/ia_agent.log
```

#### Modo Debug
```bash
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG
python validate_production.py
```

## 📈 Mejores Prácticas

### 1. **Organización de Proyectos**
- Mantener estructura clara
- Usar nombres descriptivos
- Separar lógica de negocio

### 2. **Configuración**
- Usar variables de entorno
- Mantener archivos `.env` seguros
- Documentar configuraciones personalizadas

### 3. **Monitoreo**
- Revisar métricas regularmente
- Configurar alertas
- Mantener logs limpios

### 4. **Mantenimiento**
- Actualizar dependencias
- Limpiar archivos temporales
- Hacer backup de configuraciones

## 🔒 Seguridad

### Recomendaciones
- No commitear archivos `.env`
- Usar API keys seguras
- Validar archivos de entrada
- Mantener dependencias actualizadas

### Configuración Segura
```bash
# Permisos de archivos
chmod 600 .env
chmod 755 src/
```

## 📞 Soporte

### Recursos
- **Documentación**: `docs/`
- **Ejemplos**: `examples/`
- **Tests**: `tests/`
- **Issues**: GitHub Issues

### Contacto
- **Email**: [tu-email@ejemplo.com]
- **GitHub**: [tu-usuario-github]
- **Documentación**: [enlace-a-docs]

---

## 📝 Notas de Versión

### v0.4.0 (Actual)
- Sistema de configuración robusto
- Manager de memoria optimizado
- Optimizador de rendimiento
- Manejador de errores avanzado
- Configuración Docker completa
- Scripts de despliegue automatizado

### Próximas Versiones
- Interfaz web
- Integración con CI/CD
- Soporte para más frameworks de pruebas
- Análisis de código más avanzado

---

*Última actualización: Septiembre 2025*
