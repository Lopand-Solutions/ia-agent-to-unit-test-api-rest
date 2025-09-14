#!/usr/bin/env python3
"""
Script de validación de producción
IA Agent para Generación de Pruebas Unitarias .NET
"""

import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Any

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config.environment import environment_manager
from memory.memory_manager import memory_manager
from monitoring.performance_optimizer import performance_optimizer
from utils.error_handler import error_handler
from agents.analysis_agent import analysis_agent
from tools.file_tools import file_manager
from tools.dotnet_tools import dotnet_manager


class ProductionValidator:
    """Validador de producción"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = environment_manager.get_config()
        self.validation_results = {}
        self.start_time = time.time()
    
    def validate_environment(self) -> Dict[str, Any]:
        """Validar configuración de entorno"""
        self.logger.info("🔍 Validando configuración de entorno...")
        
        results = {
            "environment_info": environment_manager.get_environment_info(),
            "is_production": environment_manager.is_production(),
            "is_development": environment_manager.is_development(),
            "config_valid": True,
            "issues": []
        }
        
        # Verificar API key
        if not self.config.openai_api_key:
            results["issues"].append("OPENAI_API_KEY no configurado")
            results["config_valid"] = False
        
        # Verificar directorios
        required_dirs = [
            self.config.chromadb_persist_directory,
            self.config.temp_directory,
            self.config.output_directory
        ]
        
        for directory in required_dirs:
            if not Path(directory).exists():
                results["issues"].append(f"Directorio no existe: {directory}")
                results["config_valid"] = False
        
        self.logger.info(f"✅ Configuración de entorno: {'OK' if results['config_valid'] else 'ISSUES'}")
        return results
    
    def validate_agents(self) -> Dict[str, Any]:
        """Validar agentes de IA"""
        self.logger.info("🤖 Validando agentes de IA...")
        
        results = {
            "agents_available": {},
            "agents_functional": {},
            "total_agents": 0,
            "functional_agents": 0
        }
        
        agents = {
            "analysis_agent": analysis_agent,
            # Agregar otros agentes cuando estén disponibles
        }
        
        for agent_name, agent in agents.items():
            try:
                # Verificar que el agente existe
                results["agents_available"][agent_name] = agent is not None
                results["total_agents"] += 1
                
                # Verificar funcionalidad básica
                if agent and hasattr(agent, 'name'):
                    results["agents_functional"][agent_name] = True
                    results["functional_agents"] += 1
                else:
                    results["agents_functional"][agent_name] = False
                
            except Exception as e:
                self.logger.error(f"Error validando agente {agent_name}: {e}")
                results["agents_functional"][agent_name] = False
        
        success_rate = (results["functional_agents"] / results["total_agents"] * 100) if results["total_agents"] > 0 else 0
        self.logger.info(f"✅ Agentes: {results['functional_agents']}/{results['total_agents']} ({success_rate:.1f}%)")
        
        return results
    
    def validate_tools(self) -> Dict[str, Any]:
        """Validar herramientas"""
        self.logger.info("🔧 Validando herramientas...")
        
        results = {
            "file_manager": False,
            "dotnet_manager": False,
            "dotnet_version": None,
            "tools_functional": 0,
            "total_tools": 2
        }
        
        # Validar file manager
        try:
            test_file = "test_validation.tmp"
            file_manager.write_file(test_file, "test content")
            content = file_manager.read_file(test_file)
            file_manager.delete_file(test_file)
            
            if content == "test content":
                results["file_manager"] = True
                results["tools_functional"] += 1
        except Exception as e:
            self.logger.error(f"Error validando file manager: {e}")
        
        # Validar dotnet manager
        try:
            version = dotnet_manager.get_dotnet_version()
            if version and "Error" not in version:
                results["dotnet_manager"] = True
                results["dotnet_version"] = version
                results["tools_functional"] += 1
        except Exception as e:
            self.logger.error(f"Error validando dotnet manager: {e}")
        
        success_rate = (results["tools_functional"] / results["total_tools"] * 100)
        self.logger.info(f"✅ Herramientas: {results['tools_functional']}/{results['total_tools']} ({success_rate:.1f}%)")
        
        return results
    
    def validate_memory_system(self) -> Dict[str, Any]:
        """Validar sistema de memoria"""
        self.logger.info("🧠 Validando sistema de memoria...")
        
        results = {
            "memory_manager": False,
            "cache_functional": False,
            "shared_memory": False,
            "memory_stats": {}
        }
        
        try:
            # Verificar memory manager
            if memory_manager:
                results["memory_manager"] = True
                
                # Verificar cache
                test_key = "validation_test"
                test_value = "test_data"
                memory_manager.add_to_cache(test_key, test_value)
                retrieved_value = memory_manager.get_from_cache(test_key)
                
                if retrieved_value == test_value:
                    results["cache_functional"] = True
                
                # Verificar memoria compartida
                shared_memory = memory_manager.get_shared_memory()
                results["shared_memory"] = shared_memory is not None
                
                # Obtener estadísticas
                results["memory_stats"] = memory_manager.get_memory_stats()
                
        except Exception as e:
            self.logger.error(f"Error validando sistema de memoria: {e}")
        
        functional_components = sum([
            results["memory_manager"],
            results["cache_functional"],
            results["shared_memory"]
        ])
        
        self.logger.info(f"✅ Sistema de memoria: {functional_components}/3 componentes funcionales")
        
        return results
    
    def validate_performance(self) -> Dict[str, Any]:
        """Validar rendimiento del sistema"""
        self.logger.info("⚡ Validando rendimiento del sistema...")
        
        results = {
            "performance_optimizer": False,
            "system_resources": {},
            "metrics_collection": False,
            "optimization_available": False
        }
        
        try:
            # Verificar performance optimizer
            if performance_optimizer:
                results["performance_optimizer"] = True
                
                # Obtener recursos del sistema
                resources = performance_optimizer.get_system_resources()
                if resources:
                    results["system_resources"] = resources.__dict__
                
                # Verificar recolección de métricas
                performance_optimizer.add_metric("validation_test", 100.0)
                metrics = performance_optimizer.get_all_metrics()
                if "validation_test" in metrics:
                    results["metrics_collection"] = True
                
                # Verificar optimización
                results["optimization_available"] = len(performance_optimizer.optimization_callbacks) > 0
                
        except Exception as e:
            self.logger.error(f"Error validando rendimiento: {e}")
        
        self.logger.info(f"✅ Rendimiento: {'OK' if results['performance_optimizer'] else 'ISSUES'}")
        
        return results
    
    def validate_error_handling(self) -> Dict[str, Any]:
        """Validar manejo de errores"""
        self.logger.info("🛡️ Validando manejo de errores...")
        
        results = {
            "error_handler": False,
            "error_categories": 0,
            "error_callbacks": 0,
            "error_stats": {}
        }
        
        try:
            # Verificar error handler
            if error_handler:
                results["error_handler"] = True
                
                # Contar categorías de error
                results["error_categories"] = len(error_handler.error_callbacks)
                
                # Contar callbacks
                total_callbacks = sum(len(callbacks) for callbacks in error_handler.error_callbacks.values())
                results["error_callbacks"] = total_callbacks
                
                # Obtener estadísticas
                results["error_stats"] = error_handler.get_error_stats()
                
        except Exception as e:
            self.logger.error(f"Error validando manejo de errores: {e}")
        
        self.logger.info(f"✅ Manejo de errores: {'OK' if results['error_handler'] else 'ISSUES'}")
        
        return results
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Ejecutar validación completa"""
        self.logger.info("🚀 Iniciando validación completa de producción...")
        
        validation_results = {
            "timestamp": time.time(),
            "duration": 0,
            "overall_status": "PENDING",
            "validations": {}
        }
        
        try:
            # Ejecutar todas las validaciones
            validation_results["validations"]["environment"] = self.validate_environment()
            validation_results["validations"]["agents"] = self.validate_agents()
            validation_results["validations"]["tools"] = self.validate_tools()
            validation_results["validations"]["memory"] = self.validate_memory_system()
            validation_results["validations"]["performance"] = self.validate_performance()
            validation_results["validations"]["error_handling"] = self.validate_error_handling()
            
            # Calcular estado general
            validation_results["duration"] = time.time() - self.start_time
            
            # Determinar estado general
            all_validations = validation_results["validations"]
            critical_issues = 0
            
            # Verificar problemas críticos
            if not all_validations["environment"]["config_valid"]:
                critical_issues += 1
            
            if all_validations["agents"]["functional_agents"] == 0:
                critical_issues += 1
            
            if all_validations["tools"]["tools_functional"] == 0:
                critical_issues += 1
            
            # Determinar estado
            if critical_issues == 0:
                validation_results["overall_status"] = "PASS"
            elif critical_issues <= 2:
                validation_results["overall_status"] = "WARNING"
            else:
                validation_results["overall_status"] = "FAIL"
            
            self.logger.info(f"🎯 Validación completada: {validation_results['overall_status']}")
            self.logger.info(f"⏱️ Duración: {validation_results['duration']:.2f} segundos")
            
        except Exception as e:
            self.logger.error(f"Error en validación completa: {e}")
            validation_results["overall_status"] = "ERROR"
            validation_results["error"] = str(e)
        
        return validation_results
    
    def print_summary(self, results: Dict[str, Any]):
        """Imprimir resumen de validación"""
        print("\n" + "="*80)
        print("📊 RESUMEN DE VALIDACIÓN DE PRODUCCIÓN")
        print("="*80)
        
        print(f"Estado General: {results['overall_status']}")
        print(f"Duración: {results['duration']:.2f} segundos")
        print(f"Timestamp: {time.ctime(results['timestamp'])}")
        
        print("\n📋 DETALLES POR COMPONENTE:")
        print("-" * 40)
        
        for component, validation in results["validations"].items():
            status = "✅" if validation.get("config_valid", True) else "❌"
            print(f"{status} {component.upper()}")
            
            if component == "environment":
                print(f"   - Producción: {validation['is_production']}")
                print(f"   - Configuración válida: {validation['config_valid']}")
                if validation["issues"]:
                    print(f"   - Problemas: {len(validation['issues'])}")
            
            elif component == "agents":
                print(f"   - Agentes funcionales: {validation['functional_agents']}/{validation['total_agents']}")
            
            elif component == "tools":
                print(f"   - Herramientas funcionales: {validation['tools_functional']}/{validation['total_tools']}")
                if validation.get("dotnet_version"):
                    print(f"   - Versión .NET: {validation['dotnet_version']}")
            
            elif component == "memory":
                functional = sum([
                    validation["memory_manager"],
                    validation["cache_functional"],
                    validation["shared_memory"]
                ])
                print(f"   - Componentes funcionales: {functional}/3")
            
            elif component == "performance":
                print(f"   - Optimizador activo: {validation['performance_optimizer']}")
                print(f"   - Métricas recolectadas: {validation['metrics_collection']}")
            
            elif component == "error_handling":
                print(f"   - Manejador activo: {validation['error_handler']}")
                print(f"   - Categorías de error: {validation['error_categories']}")
        
        print("\n" + "="*80)


def main():
    """Función principal"""
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s'
    )
    
    validator = ProductionValidator()
    results = validator.run_full_validation()
    validator.print_summary(results)
    
    # Exit code basado en el resultado
    if results["overall_status"] == "PASS":
        sys.exit(0)
    elif results["overall_status"] == "WARNING":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
