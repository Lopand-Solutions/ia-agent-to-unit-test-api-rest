#!/usr/bin/env python3
"""
Script para ejecutar el sistema multi-agente
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

def test_system_components():
    """Probar componentes del sistema"""
    print("🧪 Probando componentes del sistema...")
    
    try:
        # Probar configuración
        from utils.config import get_config
        config = get_config()
        print(f"✅ Configuración: {config.agent.name}")
        
        # Probar logging
        from utils.logging import get_logger, setup_logging
        setup_logging(level="INFO")
        logger = get_logger("test")
        logger.info("Sistema de logging funcionando")
        print("✅ Logging funcionando")
        
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
        
        # Probar memoria compartida
        from multi_agent.shared_memory import SharedMemory
        shared_memory = SharedMemory()
        shared_memory.set_project_context("test_project", "Proyecto de Prueba", "./", "xunit")
        context = shared_memory.get_project_context()
        print("✅ Memoria compartida funcionando")
        
        # Probar herramientas
        from tools.file_tools import file_manager
        test_file = "test_file.txt"
        content = "Archivo de prueba"
        file_manager.write_file(test_file, content)
        read_content = file_manager.read_file(test_file)
        if read_content == content:
            print("✅ Herramientas de archivos funcionando")
            os.remove(test_file)
        
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
        
        print("\n🎉 ¡Todos los componentes funcionando correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en componentes: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_cli():
    """Ejecutar CLI"""
    print("\n🚀 Iniciando CLI del sistema...")
    
    try:
        from cli.multi_agent_cli import MultiAgentCLI
        
        cli = MultiAgentCLI()
        
        # Inicializar sistema
        if cli.initialize():
            print("✅ Sistema inicializado correctamente")
            
            # Mostrar estado del sistema
            print("\n📊 Estado del Sistema:")
            print(f"   - Agentes disponibles: {len(cli.collaboration.autogen_agents)}")
            print(f"   - Memoria compartida: {'✅' if cli.shared_memory else '❌'}")
            print(f"   - Configuración: {cli.config.agent.name}")
            
            # Mostrar capacidades de agentes
            capabilities = cli.collaboration.get_agent_capabilities()
            print(f"\n🤖 Agentes Disponibles:")
            for agent_name, agent_capabilities in capabilities.items():
                print(f"   - {agent_name}: {len(agent_capabilities)} capacidades")
            
            print("\n✅ Sistema listo para usar!")
            print("💡 Para usar el CLI interactivo, ejecuta: python run_system.py --interactive")
            
        else:
            print("❌ Error al inicializar el sistema")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error al ejecutar CLI: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 IA Agent para Generación de Pruebas Unitarias .NET")
    print("=" * 60)
    
    # Verificar argumentos
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # Ejecutar CLI interactivo
        try:
            from cli.multi_agent_cli import MultiAgentCLI
            cli = MultiAgentCLI()
            if cli.initialize():
                cli.show_main_menu()
            else:
                print("❌ No se pudo inicializar el sistema")
        except Exception as e:
            print(f"❌ Error al ejecutar CLI interactivo: {e}")
    else:
        # Ejecutar pruebas
        print("Ejecutando pruebas del sistema...")
        
        # Probar componentes
        if test_system_components():
            # Ejecutar CLI básico
            run_cli()
        else:
            print("❌ Las pruebas fallaron, no se puede ejecutar el sistema")

if __name__ == "__main__":
    main()
