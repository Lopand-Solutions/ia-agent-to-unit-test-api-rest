# 🛠️ Guía de Solución de Problemas - IA Agent para Generación de Pruebas Unitarias .NET

## 🚨 Problemas Comunes

### 1. Error de API Key

#### Síntomas
```
OPENAI_API_KEY no configurado. Funcionalidad de IA limitada.
```

#### Solución
```bash
# Configurar variable de entorno
export OPENAI_API_KEY="tu_api_key_aqui"

# O en archivo .env
echo "OPENAI_API_KEY=tu_api_key_aqui" >> .env
```

#### Verificación
```bash
python -c "import os; print('API Key configurada:', bool(os.getenv('OPENAI_API_KEY')))"
```

### 2. Error de .NET

#### Síntomas
```
.NET no encontrado
Error: 'dotnet' no se reconoce como comando interno o externo
```

#### Solución
```bash
# Windows
# Descargar e instalar .NET 8.0 SDK desde https://dotnet.microsoft.com/download

# Linux
wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y dotnet-sdk-8.0

# macOS
brew install --cask dotnet
```

#### Verificación
```bash
dotnet --version
# Debe mostrar: 8.0.x
```

### 3. Error de ChromaDB

#### Síntomas
```
ChromaDB no disponible, usando modo sin persistencia
An instance of Chroma already exists for ephemeral with different settings
```

#### Solución
```bash
# Limpiar instancias existentes
python -c "
from src.utils.chromadb_singleton import chromadb_singleton
chromadb_singleton.reset()
print('ChromaDB reset completado')
"

# O reiniciar el sistema
python validate_production.py
```

#### Verificación
```bash
python -c "
import sys; sys.path.insert(0, 'src')
from memory.memory_manager import memory_manager
stats = memory_manager.get_memory_stats()
print('Memoria funcionando:', stats['shared_memory'])
"
```

### 4. Error de Memoria

#### Síntomas
```
MemoryError: Unable to allocate array
Out of memory
```

#### Solución
```bash
# Aumentar límite de memoria
export MEMORY_CACHE_SIZE=2000

# Limpiar cache
python -c "
import sys; sys.path.insert(0, 'src')
from memory.memory_manager import memory_manager
memory_manager.optimize_memory()
print('Memoria optimizada')
"
```

### 5. Error de Permisos

#### Síntomas
```
PermissionError: [Errno 13] Permission denied
```

#### Solución
```bash
# Linux/macOS
chmod -R 755 src/
chmod 600 .env

# Windows
# Ejecutar como administrador o cambiar permisos de carpeta
```

### 6. Error de Dependencias

#### Síntomas
```
ModuleNotFoundError: No module named 'chromadb'
ImportError: cannot import name 'BaseSettings'
```

#### Solución
```bash
# Reinstalar dependencias
pip install -r requirements.txt

# Instalar dependencias faltantes
pip install chromadb pydantic-settings psutil
```

## 🔍 Debugging Avanzado

### 1. Habilitar Logging Detallado

```bash
# Configurar logging
export LOG_LEVEL=DEBUG
export DEBUG_MODE=true

# Ejecutar con logging detallado
python validate_production.py
```

### 2. Verificar Estado del Sistema

```bash
# Verificar todos los componentes
python -c "
import sys; sys.path.insert(0, 'src')
from config.environment import environment_manager
from memory.memory_manager import memory_manager
from monitoring.performance_optimizer import performance_optimizer

print('=== ESTADO DEL SISTEMA ===')
print('Configuración:', environment_manager.get_environment_info())
print('Memoria:', memory_manager.get_memory_stats())
print('Rendimiento:', performance_optimizer.get_performance_report())
"
```

### 3. Verificar Agentes

```bash
# Verificar agentes individuales
python -c "
import sys; sys.path.insert(0, 'src')
from agents.analysis_agent import analysis_agent
print('Analysis Agent:', analysis_agent.name, analysis_agent.role)
"
```

### 4. Verificar Herramientas

```bash
# Verificar herramientas
python -c "
import sys; sys.path.insert(0, 'src')
from tools.file_tools import file_manager
from tools.dotnet_tools import dotnet_manager

print('File Manager:', file_manager is not None)
print('.NET Version:', dotnet_manager.get_dotnet_version())
"
```

## 🐳 Problemas con Docker

### 1. Error de Construcción

#### Síntomas
```
ERROR: failed to build: failed to solve
```

#### Solución
```bash
# Limpiar cache de Docker
docker system prune -a

# Reconstruir imagen
docker build --no-cache -t ia-agent .
```

### 2. Error de Conexión

#### Síntomas
```
Connection refused
Cannot connect to the Docker daemon
```

#### Solución
```bash
# Verificar que Docker esté ejecutándose
docker ps

# Reiniciar Docker
sudo systemctl restart docker  # Linux
# O reiniciar Docker Desktop en Windows/macOS
```

### 3. Error de Volúmenes

#### Síntomas
```
Permission denied
Volume mount failed
```

#### Solución
```bash
# Verificar permisos de directorios
ls -la ./memory ./logs ./output

# Corregir permisos
chmod -R 755 ./memory ./logs ./output
```

## 🔧 Problemas de Rendimiento

### 1. Sistema Lento

#### Diagnóstico
```bash
# Verificar recursos del sistema
python -c "
import sys; sys.path.insert(0, 'src')
from monitoring.performance_optimizer import performance_optimizer
report = performance_optimizer.get_performance_report()
print('CPU:', report['system_resources']['cpu_percent'])
print('Memoria:', report['system_resources']['memory_percent'])
"
```

#### Solución
```bash
# Optimizar sistema
python -c "
import sys; sys.path.insert(0, 'src')
from monitoring.performance_optimizer import performance_optimizer
result = performance_optimizer.optimize_now()
print('Optimización:', result['success'])
"
```

### 2. Alto Uso de Memoria

#### Solución
```bash
# Reducir cache de memoria
export MEMORY_CACHE_SIZE=500

# Limpiar memoria
python -c "
import sys; sys.path.insert(0, 'src')
from memory.memory_manager import memory_manager
memory_manager.cleanup_memory()
"
```

### 3. Timeouts de Agentes

#### Solución
```bash
# Aumentar timeout
export AGENT_TIMEOUT=120

# Reducir agentes concurrentes
export MAX_CONCURRENT_AGENTS=2
```

## 📊 Monitoreo y Métricas

### 1. Verificar Métricas

```bash
# Ver métricas en tiempo real
python -c "
import sys; sys.path.insert(0, 'src')
from monitoring.performance_optimizer import performance_optimizer
metrics = performance_optimizer.get_all_metrics()
for name, stats in metrics.items():
    if stats:
        print(f'{name}: {stats[\"avg\"]:.2f}ms')
"
```

### 2. Verificar Errores

```bash
# Ver errores del sistema
python -c "
import sys; sys.path.insert(0, 'src')
from utils.error_handler import error_handler
stats = error_handler.get_error_stats()
print('Errores totales:', stats['stats']['total_errors'])
print('Errores no resueltos:', stats['unresolved_errors'])
"
```

## 🔄 Recuperación de Desastres

### 1. Backup de Datos

```bash
# Crear backup
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  memory/ logs/ output/ .env

# Verificar backup
ls -la backup_*.tar.gz
```

### 2. Restaurar desde Backup

```bash
# Restaurar backup
tar -xzf backup_20250914_120000.tar.gz

# Verificar restauración
python validate_production.py
```

### 3. Reset Completo

```bash
# Limpiar todo
rm -rf memory/ logs/ output/ temp/
python -c "
import sys; sys.path.insert(0, 'src')
from utils.chromadb_singleton import chromadb_singleton
from memory.memory_manager import memory_manager
chromadb_singleton.reset()
memory_manager.optimize_memory()
print('Reset completo realizado')
"
```

## 📞 Soporte y Recursos

### 1. Logs del Sistema

```bash
# Ver logs en tiempo real
tail -f logs/ia_agent.log

# Ver logs de errores
tail -f logs/errors.log

# Ver logs de Docker
docker logs ia-agent
```

### 2. Información del Sistema

```bash
# Información completa
python -c "
import sys; sys.path.insert(0, 'src')
from config.environment import environment_manager
from memory.memory_manager import memory_manager
from monitoring.performance_optimizer import performance_optimizer
from utils.error_handler import error_handler

print('=== INFORMACIÓN DEL SISTEMA ===')
print('Entorno:', environment_manager.get_environment_info())
print('Memoria:', memory_manager.get_memory_stats())
print('Rendimiento:', performance_optimizer.get_performance_report())
print('Errores:', error_handler.get_error_stats())
"
```

### 3. Recursos de Ayuda

- **Documentación**: `docs/`
- **Ejemplos**: `examples/`
- **Tests**: `tests/`
- **Issues**: GitHub Issues
- **Logs**: `logs/`

### 4. Contacto

- **Email**: [tu-email@ejemplo.com]
- **GitHub**: [tu-usuario-github]
- **Slack**: [canal-de-soporte]

## 🎯 Checklist de Solución de Problemas

### Antes de Contactar Soporte

- [ ] Verificar que todas las dependencias estén instaladas
- [ ] Confirmar que las variables de entorno estén configuradas
- [ ] Revisar los logs del sistema
- [ ] Ejecutar `python validate_production.py`
- [ ] Verificar que .NET esté instalado y funcionando
- [ ] Confirmar que Docker esté ejecutándose (si se usa)
- [ ] Revisar el uso de recursos del sistema
- [ ] Intentar reiniciar el sistema

### Información para Soporte

Cuando contactes soporte, incluye:

1. **Versión del sistema**: `python -c "import sys; print(sys.version)"`
2. **Versión de .NET**: `dotnet --version`
3. **Logs de error**: Últimas 50 líneas de `logs/errors.log`
4. **Estado del sistema**: Resultado de `python validate_production.py`
5. **Configuración**: Variables de entorno (sin API keys)
6. **Pasos para reproducir**: Descripción detallada del problema

---

## 📝 Notas Adicionales

### Mejores Prácticas

1. **Mantener logs limpios**: Rotar logs regularmente
2. **Monitorear recursos**: Verificar CPU y memoria
3. **Hacer backups**: Backup regular de configuraciones
4. **Actualizar dependencias**: Mantener paquetes actualizados
5. **Usar variables de entorno**: No hardcodear configuraciones

### Prevención de Problemas

1. **Configuración adecuada**: Usar archivos `.env`
2. **Monitoreo continuo**: Verificar métricas regularmente
3. **Testing regular**: Ejecutar tests de validación
4. **Documentación**: Mantener documentación actualizada
5. **Versionado**: Usar control de versiones adecuadamente

---

*Última actualización: Septiembre 2025*
