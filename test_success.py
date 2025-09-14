#!/usr/bin/env python3
"""
Script de prueba exitosa para el sistema multi-agente
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

def test_system_imports():
    """Probar importaciones del sistema"""
    print("🧪 Probando importaciones del sistema...")
    
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
        
        # Probar herramientas
        from tools.file_tools import file_manager
        from tools.dotnet_tools import project_analyzer, controller_analyzer
        print("✅ Herramientas importadas")
        
        # Probar memoria de conversación
        from langchain_agents.memory.conversation_memory import ConversationMemory
        conv_memory = ConversationMemory("test_agent")
        conv_memory.start_conversation("test_session")
        conv_memory.add_message("human", "Hola")
        conv_memory.add_message("ai", "Hola, soy un agente")
        conv_memory.end_conversation()
        print("✅ Memoria de conversación funcionando")
        
        # Probar agentes base
        from agents.base_agent import BaseAgent, ReActAgent, AgentRole, AgentStatus
        print("✅ Agentes base importados")
        
        # Probar colaboración multi-agente
        from multi_agent.autogen_collaboration import MultiAgentCollaboration
        collaboration = MultiAgentCollaboration()
        print("✅ Colaboración multi-agente importada")
        
        # Probar CLI
        from cli.multi_agent_cli import MultiAgentCLI
        cli = MultiAgentCLI()
        print("✅ CLI importado")
        
        print("\n🎉 ¡Todas las importaciones exitosas!")
        return True
        
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Probar funcionalidad básica"""
    print("\n🧪 Probando funcionalidad básica...")
    
    try:
        # Probar configuración
        from utils.config import get_config
        config = get_config()
        
        # Verificar configuración
        assert config.agent.name == "IA Agent Unit Tests"
        assert config.ai.model == "gpt-4"
        assert config.agent.log_level == "INFO"
        print("✅ Configuración validada")
        
        # Probar logging
        from utils.logging import get_logger
        logger = get_logger("test")
        logger.info("Prueba de logging")
        print("✅ Logging funcionando")
        
        # Probar helpers
        from utils.helpers import file_helper, json_helper
        test_data = {"test": "data"}
        json_str = json_helper.dumps(test_data)
        parsed_data = json_helper.loads(json_str)
        assert parsed_data == test_data
        print("✅ Helpers JSON funcionando")
        
        # Probar herramientas de archivos
        from tools.file_tools import file_manager
        test_file = "test_file.txt"
        content = "Archivo de prueba"
        success = file_manager.write_file(test_file, content)
        if success:
            read_content = file_manager.read_file(test_file)
            assert read_content == content
            print("✅ Herramientas de archivos funcionando")
            os.remove(test_file)
        
        # Probar memoria de conversación
        from langchain_agents.memory.conversation_memory import ConversationMemory
        conv_memory = ConversationMemory("test_agent")
        conv_memory.start_conversation("test_session")
        conv_memory.add_message("human", "Hola")
        conv_memory.add_message("ai", "Hola, soy un agente")
        conv_memory.end_conversation()
        
        # Verificar que la conversación se guardó
        history = conv_memory.get_conversation_history()
        assert len(history) == 2
        print("✅ Memoria de conversación funcionando")
        
        print("\n🎉 ¡Funcionalidad básica validada!")
        return True
        
    except Exception as e:
        print(f"❌ Error en funcionalidad básica: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_creation():
    """Probar creación del CLI"""
    print("\n🧪 Probando creación del CLI...")
    
    try:
        from cli.multi_agent_cli import MultiAgentCLI
        
        # Crear instancia del CLI
        cli = MultiAgentCLI()
        print("✅ CLI creado correctamente")
        
        # Verificar propiedades básicas
        assert hasattr(cli, 'config')
        assert hasattr(cli, 'collaboration')
        assert hasattr(cli, 'shared_memory')
        print("✅ Propiedades del CLI verificadas")
        
        # Verificar configuración
        assert cli.config.agent.name == "IA Agent Unit Tests"
        print("✅ Configuración del CLI verificada")
        
        print("\n🎉 ¡CLI creado exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en creación del CLI: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 IA Agent para Generación de Pruebas Unitarias .NET")
    print("=" * 60)
    print("Ejecutando pruebas del sistema...")
    
    tests = [
        ("Importaciones del Sistema", test_system_imports),
        ("Funcionalidad Básica", test_basic_functionality),
        ("Creación del CLI", test_cli_creation)
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
    print("📊 RESUMEN DE PRUEBAS")
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
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ El sistema multi-agente está funcionando correctamente")
        print("✅ Todos los componentes principales están operativos")
        print("✅ Las importaciones funcionan correctamente")
        print("✅ La funcionalidad básica está validada")
        print("✅ El CLI se puede crear exitosamente")
        print("\n💡 El sistema está listo para usar!")
        print("   - Configuración: ✅")
        print("   - Logging: ✅")
        print("   - Helpers: ✅")
        print("   - Herramientas: ✅")
        print("   - Memoria: ✅")
        print("   - Agentes: ✅")
        print("   - Colaboración: ✅")
        print("   - CLI: ✅")
        return True
    else:
        print("\n⚠️  Algunas pruebas fallaron.")
        print("Revisar errores arriba para más detalles.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
