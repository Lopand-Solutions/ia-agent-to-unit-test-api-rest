#!/usr/bin/env python3
"""
Script principal para ejecutar tests
IA Agent para Generación de Pruebas Unitarias .NET
"""

import sys
import unittest
import argparse
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tests.test_agents import TestAgents
from tests.test_memory import TestMemory
from tests.test_tools import TestTools
from tests.test_ai import TestAI
from tests.test_monitoring import TestMonitoring
from tests.test_integration import TestIntegration

from utils.logging import get_logger

logger = get_logger("test-runner")


def create_test_suite(test_modules=None):
    """Crear suite de tests"""
    suite = unittest.TestSuite()
    
    if test_modules is None:
        test_modules = [
            TestAgents,
            TestMemory,
            TestTools,
            TestAI,
            TestMonitoring,
            TestIntegration
        ]
    
    for test_module in test_modules:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_module)
        suite.addTests(tests)
    
    return suite


def run_tests(test_modules=None, verbosity=2):
    """Ejecutar tests"""
    try:
        logger.info("Iniciando ejecución de tests...")
        
        # Crear suite de tests
        suite = create_test_suite(test_modules)
        
        # Ejecutar tests
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        
        # Mostrar resumen
        logger.info(f"Tests ejecutados: {result.testsRun}")
        logger.info(f"Fallos: {len(result.failures)}")
        logger.info(f"Errores: {len(result.errors)}")
        logger.info(f"Omitidos: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
        
        if result.failures:
            logger.error("Tests fallidos:")
            for test, traceback in result.failures:
                logger.error(f"  - {test}: {traceback}")
        
        if result.errors:
            logger.error("Tests con errores:")
            for test, traceback in result.errors:
                logger.error(f"  - {test}: {traceback}")
        
        # Retornar código de salida
        return 0 if result.wasSuccessful() else 1
        
    except Exception as e:
        logger.error(f"Error al ejecutar tests: {e}")
        return 1


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Ejecutar tests del sistema")
    parser.add_argument("--module", "-m", action="append", 
                       choices=["agents", "memory", "tools", "ai", "monitoring", "integration"],
                       help="Módulos específicos a probar")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Salida verbose")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Salida silenciosa")
    
    args = parser.parse_args()
    
    # Determinar verbosidad
    if args.quiet:
        verbosity = 0
    elif args.verbose:
        verbosity = 2
    else:
        verbosity = 1
    
    # Determinar módulos a probar
    test_modules = None
    if args.module:
        module_map = {
            "agents": TestAgents,
            "memory": TestMemory,
            "tools": TestTools,
            "ai": TestAI,
            "monitoring": TestMonitoring,
            "integration": TestIntegration
        }
        test_modules = [module_map[module] for module in args.module]
    
    # Ejecutar tests
    exit_code = run_tests(test_modules, verbosity)
    
    if exit_code == 0:
        logger.info("✅ Todos los tests pasaron exitosamente!")
    else:
        logger.error("❌ Algunos tests fallaron")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
