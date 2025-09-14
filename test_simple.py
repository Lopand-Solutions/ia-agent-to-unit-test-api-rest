#!/usr/bin/env python3
"""
Script de prueba simplificado para el sistema multi-agente
IA Agent para Generación de Pruebas Unitarias .NET
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_imports():
    """Probar importaciones básicas"""
    print("🧪 Probando importaciones básicas...")
    
    try:
        # Probar configuración
        from utils.config import get_config, Config
        print("✅ Configuración importada")
        
        # Probar logging
        from utils.logging import get_logger
        logger = get_logger("test")
        logger.info("Logging funcionando")
        print("✅ Logging funcionando")
        
        # Probar helpers
        from utils.helpers import file_helper, json_helper
        print("✅ Helpers importados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en importaciones básicas: {e}")
        return False

def test_configuration():
    """Probar configuración"""
    print("\n🧪 Probando configuración...")
    
    try:
        from utils.config import get_config
        
        config = get_config()
        print(f"✅ Configuración cargada: {config.agent.name}")
        print(f"   - Modelo: {config.ai.model}")
        print(f"   - Logging: {config.agent.log_level}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_system():
    """Probar sistema de memoria básico"""
    print("\n🧪 Probando sistema de memoria...")
    
    try:
        from langchain_agents.memory.conversation_memory import ConversationMemory
        
        # Probar memoria de conversación
        conv_memory = ConversationMemory("test_agent")
        success = conv_memory.start_conversation("test_session")
        if success:
            conv_memory.add_message("human", "Hola")
            conv_memory.add_message("ai", "Hola, soy un agente")
            conv_memory.end_conversation()
            print("✅ Memoria de conversación funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en memoria: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tools():
    """Probar herramientas básicas"""
    print("\n🧪 Probando herramientas...")
    
    try:
        from tools.file_tools import file_manager
        
        # Probar gestor de archivos
        test_file = "test_file.txt"
        content = "Este es un archivo de prueba"
        
        success = file_manager.write_file(test_file, content)
        if success:
            read_content = file_manager.read_file(test_file)
            if read_content == content:
                print("✅ Herramientas de archivos funcionando")
                # Limpiar archivo de prueba
                os.remove(test_file)
            else:
                print("❌ Error al leer archivo")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en herramientas: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas básicas del sistema")
    print("=" * 50)
    
    tests = [
        ("Importaciones Básicas", test_basic_imports),
        ("Configuración", test_configuration),
        ("Sistema de Memoria", test_memory_system),
        ("Herramientas", test_tools)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS BÁSICAS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:.<25} {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas básicas pasaron!")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
