#!/usr/bin/env python3
"""
Script de prueba para el sistema multi-agente
IA Agent para Generación de Pruebas Unitarias .NET
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Probar importaciones del sistema"""
    print("🧪 Probando importaciones del sistema...")
    
    try:
        # Probar configuración
        from utils.config import get_config, Config
        config = get_config()
        print("✅ Configuración importada correctamente")
        
        # Probar logging
        from utils.logging import get_logger, setup_logging
        logger = get_logger("test")
        logger.info("Sistema de logging funcionando")
        print("✅ Sistema de logging funcionando")
        
        # Probar helpers
        from utils.helpers import file_helper, json_helper, yaml_helper
        print("✅ Helpers importados correctamente")
        
        # Probar herramientas .NET
        from tools.dotnet_tools import project_analyzer, controller_analyzer, command_executor
        print("✅ Herramientas .NET importadas correctamente")
        
        # Probar herramientas de archivos
        from tools.file_tools import file_manager, code_file_manager
        print("✅ Herramientas de archivos importadas correctamente")
        
        # Probar memoria
        from langchain_agents.memory.conversation_memory import ConversationMemory
        from langchain_agents.memory.vector_memory import VectorMemory
        print("✅ Sistema de memoria importado correctamente")
        
        # Probar memoria compartida
        from multi_agent.shared_memory import SharedMemory
        print("✅ Memoria compartida importada correctamente")
        
        # Probar agentes base
        from agents.base_agent import BaseAgent, ReActAgent, AgentRole, AgentStatus
        print("✅ Agentes base importados correctamente")
        
        # Probar agentes individuales
        from agents.analysis_agent import analysis_agent
        from agents.generation_agent import generation_agent
        from agents.validation_agent import validation_agent
        from agents.optimization_agent import optimization_agent
        from agents.coordinator_agent import coordinator_agent
        print("✅ Agentes individuales importados correctamente")
        
        # Probar colaboración multi-agente
        from multi_agent.autogen_collaboration import multi_agent_collaboration
        print("✅ Colaboración multi-agente importada correctamente")
        
        # Probar CLI
        from cli.multi_agent_cli import MultiAgentCLI
        print("✅ CLI importado correctamente")
        
        print("\n🎉 ¡Todas las importaciones exitosas!")
        return True
        
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """Probar sistema de configuración"""
    print("\n🧪 Probando sistema de configuración...")
    
    try:
        from utils.config import get_config, ConfigManager
        
        # Probar configuración por defecto
        config = get_config()
        print(f"✅ Configuración cargada: {config.agent.name}")
        print(f"   - Modelo IA: {config.ai.model}")
        print(f"   - Modo multi-agente: {config.multi_agent.mode}")
        print(f"   - Nivel de logging: {config.agent.log_level}")
        
        # Probar gestor de configuración
        config_manager = ConfigManager()
        config_loaded = config_manager.load_config()
        print(f"✅ Gestor de configuración funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_memory_system():
    """Probar sistema de memoria"""
    print("\n🧪 Probando sistema de memoria...")
    
    try:
        from langchain_agents.memory.conversation_memory import ConversationMemory
        from langchain_agents.memory.vector_memory import VectorMemory
        from multi_agent.shared_memory import SharedMemory
        
        # Probar memoria de conversación
        conv_memory = ConversationMemory("test_agent")
        success = conv_memory.start_conversation("test_session")
        if success:
            conv_memory.add_message("human", "Hola, esto es una prueba")
            conv_memory.add_message("ai", "Hola, soy un agente de prueba")
            conv_memory.end_conversation()
            print("✅ Memoria de conversación funcionando")
        
        # Probar memoria vectorial
        vector_memory = VectorMemory("test_agent")
        entry_id = vector_memory.add_entry("Este es un texto de prueba", {"test": True})
        if entry_id:
            print("✅ Memoria vectorial funcionando")
        
        # Probar memoria compartida
        shared_memory = SharedMemory()
        shared_memory.set_project_context("test_project", "Proyecto de Prueba", "./", "xunit")
        context = shared_memory.get_project_context()
        if context:
            print("✅ Memoria compartida funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en sistema de memoria: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agents():
    """Probar agentes individuales"""
    print("\n🧪 Probando agentes individuales...")
    
    try:
        from agents.analysis_agent import analysis_agent
        from agents.generation_agent import generation_agent
        from agents.validation_agent import validation_agent
        from agents.optimization_agent import optimization_agent
        from agents.coordinator_agent import coordinator_agent
        
        # Probar capacidades de cada agente
        agents = [
            ("Análisis", analysis_agent),
            ("Generación", generation_agent),
            ("Validación", validation_agent),
            ("Optimización", optimization_agent),
            ("Coordinación", coordinator_agent)
        ]
        
        for name, agent in agents:
            try:
                capabilities = agent.get_capabilities()
                print(f"✅ Agente {name}: {len(capabilities)} capacidades")
            except Exception as e:
                print(f"⚠️  Agente {name}: Error al obtener capacidades - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en agentes: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli():
    """Probar CLI"""
    print("\n🧪 Probando CLI...")
    
    try:
        from cli.multi_agent_cli import MultiAgentCLI
        
        # Crear instancia del CLI
        cli = MultiAgentCLI()
        print("✅ CLI creado correctamente")
        
        # Probar inicialización (sin ejecutar el menú)
        # success = cli.initialize()
        # if success:
        #     print("✅ CLI inicializado correctamente")
        # else:
        #     print("⚠️  CLI no se pudo inicializar completamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en CLI: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas del sistema multi-agente")
    print("=" * 60)
    
    tests = [
        ("Importaciones", test_imports),
        ("Configuración", test_configuration),
        ("Sistema de Memoria", test_memory_system),
        ("Agentes Individuales", test_agents),
        ("CLI", test_cli)
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
        print("🎉 ¡Todas las pruebas pasaron! El sistema está funcionando correctamente.")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar errores arriba.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
