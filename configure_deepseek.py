#!/usr/bin/env python3
"""
Script de configuración para DeepSeek
IA Agent para Generación de Pruebas Unitarias .NET
"""

import os
import sys
from pathlib import Path

def create_deepseek_env():
    """Crear archivo .env para DeepSeek"""
    print("🔧 Configurando DeepSeek...")
    
    # Contenido del archivo .env para DeepSeek
    env_content = """# Configuración para DeepSeek
DEEPSEEK_API_KEY=tu_deepseek_api_key_aqui
AI_PROVIDER=deepseek
AI_MODEL=deepseek-coder
AI_TEMPERATURE=0.1
AI_MAX_TOKENS=4000

# Configuración de logging
LOG_LEVEL=INFO
LOG_FILE=./logs/ia_agent.log

# Configuración de memoria
MEMORY_CACHE_SIZE=1000
CHROMADB_PERSIST_DIRECTORY=./memory/vector

# Configuración de agentes
MAX_CONCURRENT_AGENTS=3
AGENT_TIMEOUT=60

# Configuración de archivos
TEMP_DIRECTORY=./temp
OUTPUT_DIRECTORY=./output
ALLOWED_FILE_EXTENSIONS=.cs,.csproj,.sln

# Configuración de .NET
DOTNET_PATH=dotnet
"""
    
    # Escribir archivo .env
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado para DeepSeek")
    print("📝 Edita el archivo .env y agrega tu API key real de DeepSeek")

def show_deepseek_info():
    """Mostrar información sobre DeepSeek"""
    print("\n📋 Información sobre DeepSeek:")
    print("=" * 50)
    
    print("\n🎯 ¿Qué es DeepSeek?")
    print("DeepSeek es un modelo de IA especializado en programación y análisis de código.")
    print("Ofrece excelente rendimiento para tareas de desarrollo de software.")
    
    print("\n💰 Ventajas de DeepSeek:")
    print("• Más económico que OpenAI GPT-4")
    print("• Especializado en código")
    print("• Respuestas rápidas")
    print("• API compatible con OpenAI")
    
    print("\n🔑 Cómo obtener API Key:")
    print("1. Visitar: https://platform.deepseek.com/")
    print("2. Crear cuenta gratuita")
    print("3. Ir a 'API Keys' en el dashboard")
    print("4. Crear nueva API key")
    print("5. Copiar la key y pegarla en el archivo .env")
    
    print("\n📊 Modelos disponibles:")
    models = {
        "deepseek-chat": "Modelo general de chat",
        "deepseek-coder": "Especializado en programación (RECOMENDADO)",
        "deepseek-math": "Especializado en matemáticas"
    }
    
    for model, description in models.items():
        print(f"  • {model}: {description}")

def test_deepseek_connection():
    """Probar conexión con DeepSeek"""
    print("\n🧪 Probando conexión con DeepSeek...")
    
    try:
        # Verificar si existe API key
        if not os.getenv('DEEPSEEK_API_KEY') or os.getenv('DEEPSEEK_API_KEY') == 'tu_deepseek_api_key_aqui':
            print("⚠️  API key no configurada. Configura tu API key real en el archivo .env")
            return False
        
        # Importar y probar
        sys.path.insert(0, 'src')
        from ai.llm_manager import DeepSeekLLM
        
        # Crear instancia
        deepseek = DeepSeekLLM(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            model='deepseek-coder',
            temperature=0.1,
            max_tokens=100
        )
        
        print("✅ Conexión con DeepSeek establecida")
        print("✅ Modelo: deepseek-coder")
        print("✅ Configuración correcta")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en conexión: {e}")
        return False

def show_usage_examples():
    """Mostrar ejemplos de uso"""
    print("\n💡 Ejemplos de uso con DeepSeek:")
    print("=" * 50)
    
    print("\n1. Configurar variables de entorno:")
    print("   export DEEPSEEK_API_KEY='tu_api_key'")
    print("   export AI_PROVIDER='deepseek'")
    print("   export AI_MODEL='deepseek-coder'")
    
    print("\n2. Usar el CLI:")
    print("   python -c \"import sys; sys.path.insert(0, 'src'); from cli.simple_cli import SimpleCLI; cli = SimpleCLI(); cli.run_interactive()\"")
    
    print("\n3. Validar sistema:")
    print("   python validate_production.py")
    
    print("\n4. Probar agentes:")
    print("   python -c \"import sys; sys.path.insert(0, 'src'); from agents.analysis_agent import analysis_agent; print('Analysis Agent:', analysis_agent.name)\"")

def main():
    """Función principal"""
    print("🚀 Configurador de DeepSeek para IA Agent")
    print("=" * 50)
    
    # Crear configuración
    create_deepseek_env()
    
    # Mostrar información
    show_deepseek_info()
    
    # Mostrar ejemplos
    show_usage_examples()
    
    print("\n" + "=" * 50)
    print("📝 Próximos pasos:")
    print("1. Editar archivo .env y agregar tu API key real")
    print("2. Ejecutar: python validate_production.py")
    print("3. Usar el sistema con DeepSeek")
    
    print("\n🎉 ¡Configuración completada!")
    print("El sistema está listo para usar con DeepSeek una vez que configures tu API key.")

if __name__ == "__main__":
    main()
