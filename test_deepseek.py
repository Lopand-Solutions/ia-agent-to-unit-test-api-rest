#!/usr/bin/env python3
"""
Script de prueba para DeepSeek
IA Agent para Generación de Pruebas Unitarias .NET
"""

import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_deepseek_configuration():
    """Probar configuración de DeepSeek"""
    print("🔍 Probando configuración de DeepSeek...")
    
    try:
        from config.environment import environment_manager
        
        # Configurar para DeepSeek
        os.environ["AI_PROVIDER"] = "deepseek"
        os.environ["AI_MODEL"] = "deepseek-coder"
        os.environ["DEEPSEEK_API_KEY"] = "test_key"  # Clave de prueba
        
        config = environment_manager.get_config()
        print(f"✅ Proveedor configurado: {config.ai_provider}")
        print(f"✅ Modelo configurado: {config.ai_model}")
        print(f"✅ API Key configurada: {bool(config.deepseek_api_key)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_deepseek_llm():
    """Probar LLM de DeepSeek"""
    print("\n🤖 Probando LLM de DeepSeek...")
    
    try:
        from ai.llm_manager import DeepSeekLLM
        
        # Crear instancia de DeepSeek (sin API key real para prueba)
        deepseek = DeepSeekLLM(
            api_key="test_key",
            model="deepseek-coder",
            temperature=0.1,
            max_tokens=1000
        )
        
        print(f"✅ DeepSeek LLM creado")
        print(f"✅ Modelo: {deepseek.model}")
        print(f"✅ Temperature: {deepseek.temperature}")
        print(f"✅ Max tokens: {deepseek.max_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en LLM: {e}")
        return False

def test_llm_manager():
    """Probar LLM Manager con DeepSeek"""
    print("\n🔧 Probando LLM Manager...")
    
    try:
        from ai.llm_manager import LLMManager
        
        # Configurar variables de entorno
        os.environ["AI_PROVIDER"] = "deepseek"
        os.environ["AI_MODEL"] = "deepseek-coder"
        os.environ["DEEPSEEK_API_KEY"] = "test_key"
        
        manager = LLMManager()
        
        print(f"✅ LLM Manager creado")
        print(f"✅ LLMs disponibles: {manager.get_available_llms()}")
        
        # Obtener información del LLM principal
        info = manager.get_llm_info("primary")
        print(f"✅ Info del LLM principal: {info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en LLM Manager: {e}")
        return False

def show_deepseek_models():
    """Mostrar modelos disponibles de DeepSeek"""
    print("\n📋 Modelos disponibles de DeepSeek:")
    
    models = {
        "deepseek-chat": "Modelo de chat general",
        "deepseek-coder": "Modelo especializado en código",
        "deepseek-math": "Modelo especializado en matemáticas"
    }
    
    for model, description in models.items():
        print(f"  - {model}: {description}")
    
    print("\n💡 Recomendaciones:")
    print("  - Para generación de código: deepseek-coder")
    print("  - Para análisis general: deepseek-chat")
    print("  - Para cálculos matemáticos: deepseek-math")

def show_configuration_guide():
    """Mostrar guía de configuración"""
    print("\n📖 Guía de configuración para DeepSeek:")
    print("\n1. Obtener API Key:")
    print("   - Visitar: https://platform.deepseek.com/")
    print("   - Crear cuenta y obtener API key")
    
    print("\n2. Configurar variables de entorno:")
    print("   export DEEPSEEK_API_KEY='tu_api_key_aqui'")
    print("   export AI_PROVIDER='deepseek'")
    print("   export AI_MODEL='deepseek-coder'")
    
    print("\n3. O usar archivo .env:")
    print("   DEEPSEEK_API_KEY=tu_api_key_aqui")
    print("   AI_PROVIDER=deepseek")
    print("   AI_MODEL=deepseek-coder")
    
    print("\n4. Verificar configuración:")
    print("   python validate_production.py")

def main():
    """Función principal"""
    print("🚀 Prueba de integración con DeepSeek")
    print("=" * 50)
    
    # Ejecutar pruebas
    tests = [
        test_deepseek_configuration,
        test_deepseek_llm,
        test_llm_manager
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Error en {test.__name__}: {e}")
            results.append(False)
    
    # Mostrar información adicional
    show_deepseek_models()
    show_configuration_guide()
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 Resumen de pruebas:")
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Pruebas pasadas: {passed}/{total}")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! DeepSeek está listo para usar.")
        print("\n📝 Próximos pasos:")
        print("1. Configurar tu API key real de DeepSeek")
        print("2. Ejecutar: python validate_production.py")
        print("3. Usar el sistema con DeepSeek")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar configuración.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
