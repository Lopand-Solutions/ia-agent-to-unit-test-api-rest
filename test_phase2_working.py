#!/usr/bin/env python3
"""
Script de prueba funcional para la Fase 2
IA Agent para Generación de Pruebas Unitarias .NET
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Cambiar al directorio src para que las importaciones relativas funcionen
os.chdir(src_path)

def test_core_components():
    """Probar componentes principales"""
    print("🧪 Probando componentes principales...")
    
    try:
        # Probar configuración
        from utils.config import get_config
        config = get_config()
        print(f"✅ Configuración: {config.agent.name}")
        print(f"   - Modelo: {config.ai.model}")
        print(f"   - Logging: {config.agent.log_level}")
        
        # Probar logging
        from utils.logging import get_logger, setup_logging
        setup_logging(level="INFO")
        logger = get_logger("test")
        logger.info("Sistema de logging funcionando")
        print("✅ Logging funcionando")
        
        # Probar helpers
        from utils.helpers import file_helper, json_helper, yaml_helper
        print("✅ Helpers importados")
        
        # Probar JSON Helper
        test_data = {"test": "data", "number": 42}
        json_str = json_helper.dumps(test_data)
        parsed_data = json_helper.loads(json_str)
        assert parsed_data == test_data
        print("✅ JSON Helper funcionando")
        
        # Probar herramientas
        from tools.file_tools import file_manager
        from tools.dotnet_tools import project_analyzer, controller_analyzer
        print("✅ Herramientas importadas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en componentes principales: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_conversation():
    """Probar memoria de conversación"""
    print("\n🧪 Probando memoria de conversación...")
    
    try:
        from langchain_agents.memory.conversation_memory import ConversationMemory
        
        # Probar memoria de conversación
        conv_memory = ConversationMemory("test_agent")
        conv_memory.start_conversation("test_session")
        conv_memory.add_message("human", "Hola")
        conv_memory.add_message("ai", "Hola, soy un agente")
        conv_memory.end_conversation()
        
        # Verificar que la conversación se guardó
        history = conv_memory.get_conversation_history()
        print(f"✅ Memoria de conversación funcionando ({len(history)} mensajes)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en memoria de conversación: {e}")
        return False

def test_agents_base():
    """Probar agentes base"""
    print("\n🧪 Probando agentes base...")
    
    try:
        from agents.base_agent import BaseAgent, ReActAgent, AgentRole, AgentStatus
        print("✅ Agentes base importados")
        
        # Probar enums
        assert AgentRole.ANALYST == "analyst"
        assert AgentStatus.IDLE == "idle"
        print("✅ Enums de agentes funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en agentes base: {e}")
        return False

def test_file_operations():
    """Probar operaciones de archivos"""
    print("\n🧪 Probando operaciones de archivos...")
    
    try:
        from tools.file_tools import file_manager
        
        # Probar escritura y lectura de archivos
        test_file = "test_file.txt"
        content = "Archivo de prueba para validación"
        success = file_manager.write_file(test_file, content)
        assert success
        
        read_content = file_manager.read_file(test_file)
        assert read_content == content
        
        # Limpiar archivo de prueba
        os.remove(test_file)
        print("✅ Operaciones de archivos funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en operaciones de archivos: {e}")
        return False

def test_dotnet_tools():
    """Probar herramientas .NET"""
    print("\n🧪 Probando herramientas .NET...")
    
    try:
        from tools.dotnet_tools import project_analyzer, controller_analyzer, command_executor
        
        # Verificar que las herramientas están disponibles
        assert hasattr(project_analyzer, 'analyze_project')
        assert hasattr(controller_analyzer, 'analyze_controller')
        assert hasattr(command_executor, 'execute_command')
        print("✅ Herramientas .NET importadas y disponibles")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en herramientas .NET: {e}")
        return False

def test_cli_import():
    """Probar importación del CLI"""
    print("\n🧪 Probando importación del CLI...")
    
    try:
        # Solo probar la importación, no la inicialización completa
        from cli.multi_agent_cli import MultiAgentCLI
        print("✅ CLI importado correctamente")
        
        # Verificar que la clase existe
        assert hasattr(MultiAgentCLI, '__init__')
        print("✅ Clase CLI disponible")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en importación del CLI: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 IA Agent para Generación de Pruebas Unitarias .NET")
    print("=" * 60)
    print("VALIDACIÓN FUNCIONAL DE LA FASE 2")
    print("=" * 60)
    
    tests = [
        ("Componentes Principales", test_core_components),
        ("Memoria de Conversación", test_memory_conversation),
        ("Agentes Base", test_agents_base),
        ("Operaciones de Archivos", test_file_operations),
        ("Herramientas .NET", test_dotnet_tools),
        ("Importación del CLI", test_cli_import)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VALIDACIÓN FASE 2")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("\n🎉 ¡FASE 2 VALIDADA EXITOSAMENTE!")
        print("✅ Todos los componentes principales funcionando")
        print("✅ Sistema de configuración operativo")
        print("✅ Logging avanzado funcionando")
        print("✅ Helpers y herramientas disponibles")
        print("✅ Memoria de conversación operativa")
        print("✅ Agentes base implementados")
        print("✅ Herramientas .NET disponibles")
        print("✅ CLI importado correctamente")
        print("\n🚀 El sistema está listo para uso!")
        return True
    else:
        print(f"\n⚠️  {total - passed} pruebas fallaron.")
        print("Revisar errores arriba para más detalles.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
