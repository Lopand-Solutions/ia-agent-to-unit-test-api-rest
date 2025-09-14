#!/usr/bin/env python3
"""
Script de despliegue para IA Agent
IA Agent para Generación de Pruebas Unitarias .NET
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s'
)
logger = logging.getLogger(__name__)


class DeploymentManager:
    """Manager de despliegue"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.deployment_configs = {
            "development": {
                "docker_compose_file": "docker-compose.yml",
                "profiles": [],
                "environment": "development"
            },
            "staging": {
                "docker_compose_file": "docker-compose.yml",
                "profiles": ["monitoring"],
                "environment": "staging"
            },
            "production": {
                "docker_compose_file": "docker-compose.yml",
                "profiles": ["monitoring", "chromadb"],
                "environment": "production"
            }
        }
    
    def check_prerequisites(self) -> bool:
        """Verificar prerrequisitos"""
        logger.info("Verificando prerrequisitos...")
        
        # Verificar Docker
        try:
            result = subprocess.run(["docker", "--version"], 
                                  capture_output=True, text=True, check=True)
            logger.info(f"Docker encontrado: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Docker no encontrado. Instalar Docker primero.")
            return False
        
        # Verificar Docker Compose
        try:
            result = subprocess.run(["docker-compose", "--version"], 
                                  capture_output=True, text=True, check=True)
            logger.info(f"Docker Compose encontrado: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Docker Compose no encontrado. Instalar Docker Compose primero.")
            return False
        
        # Verificar archivos necesarios
        required_files = ["Dockerfile", "docker-compose.yml", "requirements.txt"]
        for file in required_files:
            if not (self.project_root / file).exists():
                logger.error(f"Archivo requerido no encontrado: {file}")
                return False
        
        logger.info("✅ Todos los prerrequisitos cumplidos")
        return True
    
    def create_directories(self):
        """Crear directorios necesarios"""
        logger.info("Creando directorios necesarios...")
        
        directories = [
            "logs",
            "memory/vector",
            "temp",
            "output",
            "projects"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directorio creado/verificado: {directory}")
    
    def setup_environment(self, environment: str):
        """Configurar variables de entorno"""
        logger.info(f"Configurando entorno: {environment}")
        
        env_file = self.project_root / ".env"
        env_example = self.project_root / "env.example"
        
        if not env_file.exists() and env_example.exists():
            logger.info("Copiando archivo de configuración de ejemplo...")
            env_file.write_text(env_example.read_text())
            logger.warning("⚠️  Configurar variables de entorno en .env antes de continuar")
        
        # Configuraciones específicas por entorno
        if environment == "production":
            logger.info("Configurando para producción...")
            # Aquí se pueden agregar configuraciones específicas de producción
        
        elif environment == "staging":
            logger.info("Configurando para staging...")
            # Aquí se pueden agregar configuraciones específicas de staging
    
    def build_images(self, environment: str):
        """Construir imágenes Docker"""
        logger.info(f"Construyendo imágenes Docker para {environment}...")
        
        try:
            cmd = ["docker-compose", "-f", "docker-compose.yml", "build"]
            subprocess.run(cmd, check=True, cwd=self.project_root)
            logger.info("✅ Imágenes construidas exitosamente")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al construir imágenes: {e}")
            raise
    
    def deploy_services(self, environment: str):
        """Desplegar servicios"""
        logger.info(f"Desplegando servicios para {environment}...")
        
        config = self.deployment_configs[environment]
        cmd = ["docker-compose", "-f", config["docker_compose_file"]]
        
        # Agregar perfiles si existen
        if config["profiles"]:
            cmd.extend(["--profile"] + config["profiles"])
        
        cmd.extend(["up", "-d"])
        
        try:
            subprocess.run(cmd, check=True, cwd=self.project_root)
            logger.info("✅ Servicios desplegados exitosamente")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al desplegar servicios: {e}")
            raise
    
    def check_health(self):
        """Verificar salud de los servicios"""
        logger.info("Verificando salud de los servicios...")
        
        try:
            # Verificar contenedores
            result = subprocess.run(
                ["docker-compose", "ps"], 
                capture_output=True, text=True, check=True, cwd=self.project_root
            )
            logger.info("Estado de los contenedores:")
            print(result.stdout)
            
            # Verificar logs del servicio principal
            logger.info("Verificando logs del servicio principal...")
            result = subprocess.run(
                ["docker-compose", "logs", "--tail=10", "ia-agent"], 
                capture_output=True, text=True, check=True, cwd=self.project_root
            )
            print(result.stdout)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al verificar salud: {e}")
    
    def stop_services(self):
        """Detener servicios"""
        logger.info("Deteniendo servicios...")
        
        try:
            subprocess.run(
                ["docker-compose", "down"], 
                check=True, cwd=self.project_root
            )
            logger.info("✅ Servicios detenidos")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al detener servicios: {e}")
    
    def cleanup(self):
        """Limpiar recursos"""
        logger.info("Limpiando recursos...")
        
        try:
            # Detener y eliminar contenedores
            subprocess.run(
                ["docker-compose", "down", "--volumes", "--remove-orphans"], 
                check=True, cwd=self.project_root
            )
            
            # Eliminar imágenes no utilizadas
            subprocess.run(["docker", "image", "prune", "-f"], check=True)
            
            logger.info("✅ Limpieza completada")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error en limpieza: {e}")
    
    def deploy(self, environment: str, skip_build: bool = False):
        """Desplegar sistema completo"""
        logger.info(f"🚀 Iniciando despliegue para entorno: {environment}")
        
        try:
            # Verificar prerrequisitos
            if not self.check_prerequisites():
                return False
            
            # Crear directorios
            self.create_directories()
            
            # Configurar entorno
            self.setup_environment(environment)
            
            # Construir imágenes (si no se omite)
            if not skip_build:
                self.build_images(environment)
            
            # Desplegar servicios
            self.deploy_services(environment)
            
            # Verificar salud
            self.check_health()
            
            logger.info("🎉 Despliegue completado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en despliegue: {e}")
            return False


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Desplegar IA Agent")
    parser.add_argument(
        "environment", 
        choices=["development", "staging", "production"],
        help="Entorno de despliegue"
    )
    parser.add_argument(
        "--skip-build", 
        action="store_true",
        help="Omitir construcción de imágenes"
    )
    parser.add_argument(
        "--stop", 
        action="store_true",
        help="Detener servicios"
    )
    parser.add_argument(
        "--cleanup", 
        action="store_true",
        help="Limpiar recursos"
    )
    parser.add_argument(
        "--health", 
        action="store_true",
        help="Verificar salud de servicios"
    )
    
    args = parser.parse_args()
    
    deployment_manager = DeploymentManager()
    
    if args.stop:
        deployment_manager.stop_services()
    elif args.cleanup:
        deployment_manager.cleanup()
    elif args.health:
        deployment_manager.check_health()
    else:
        success = deployment_manager.deploy(args.environment, args.skip_build)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
