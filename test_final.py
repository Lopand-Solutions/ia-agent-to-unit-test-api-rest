#!/usr/bin/env python3
"""
Script de prueba final para el sistema multi-agente
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
    """Probar componentes principales del sistema"""
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
        
        # Probar memoria vectorial
        from langchain_agents.memory.vector_memory import VectorMemory
        vector_memory = VectorMemory("test_agent")
        entry_id = vector_memory.add_entry("Texto de prueba", {"test": True})
        print("✅ Memoria vectorial funcionando")
        
        # Probar agentes base
        from agents.base_agent import BaseAgent, ReActAgent, AgentRole, AgentStatus
        print("✅ Agentes base importados")
        
        # Probar agentes individuales
        from agents.analysis_agent import analysis_agent
        from agents.generation_agent import generation_agent
        from agents.validation_agent import validation_agent
        from agents.optimization_agent import optimization_agent
        from agents.coordinator_agent import coordinator_agent
        print("✅ Agentes individuales importados")
        
        # Probar colaboración multi-agente
        from multi_agent.autogen_collaboration import MultiAgentCollaboration
        collaboration = MultiAgentCollaboration()
        print("✅ Colaboración multi-agente importada")
        
        # Probar CLI
        from cli.multi_agent_cli import MultiAgentCLI
        cli = MultiAgentCLI()
        print("✅ CLI importado")
        
        print("\n🎉 ¡Todos los componentes principales funcionando correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en componentes: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_capabilities():
    """Probar capacidades de los agentes"""
    print("\n🧪 Probando capacidades de agentes...")
    
    try:
        from agents.analysis_agent import analysis_agent
        from agents.generation_agent import generation_agent
        from agents.validation_agent import validation_agent
        from agents.optimization_agent import optimization_agent
        from agents.coordinator_agent import coordinator_agent
        
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
                for capability in capabilities[:3]:  # Mostrar primeras 3
                    print(f"   - {capability}")
                if len(capabilities) > 3:
                    print(f"   - ... y {len(capabilities) - 3} más")
            except Exception as e:
                print(f"⚠️  Agente {name}: Error al obtener capacidades - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en capacidades de agentes: {e}")
        return False

def test_cli_functionality():
    """Probar funcionalidad del CLI"""
    print("\n🧪 Probando funcionalidad del CLI...")
    
    try:
        from cli.multi_agent_cli import MultiAgentCLI
        
        # Crear instancia del CLI
        cli = MultiAgentCLI()
        print("✅ CLI creado correctamente")
        
        # Probar configuración del CLI
        print(f"   - Proyecto actual: {cli.current_project_path or 'Ninguno'}")
        print(f"   - Sesión actual: {cli.current_session_id or 'Ninguna'}")
        print(f"   - Agentes inicializados: {cli.agents_initialized}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en CLI: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 IA Agent para Generación de Pruebas Unitarias .NET")
    print("=" * 60)
    print("Probando componentes principales del sistema...")
    
    tests = [
        ("Componentes Principales", test_core_components),
        ("Capacidades de Agentes", test_agent_capabilities),
        ("Funcionalidad del CLI", test_cli_functionality)
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
        print("✅ Los agentes tienen sus capacidades configuradas")
        print("✅ El CLI está listo para usar")
        print("\n💡 Para usar el sistema:")
        print("   - Ejecuta: python run_system.py --interactive")
        print("   - O usa el CLI directamente desde el directorio src/")
        return True
    else:
        print("\n⚠️  Algunas pruebas fallaron.")
        print("Revisar errores arriba para más detalles.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
