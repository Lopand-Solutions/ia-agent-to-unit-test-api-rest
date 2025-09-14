#!/usr/bin/env python3
"""
CLI de configuración para IA Agent
IA Agent para Generación de Pruebas Unitarias .NET
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from utils.logging import get_logger

console = Console()
logger = get_logger("config-cli")


class ConfigCLI:
    """CLI para configuración de API keys y proveedores"""
    
    def __init__(self):
        self.config_file = Path(".env")
        self.providers = {
            "1": {
                "name": "DeepSeek",
                "key": "DEEPSEEK_API_KEY",
                "model": "deepseek-coder",
                "description": "Especializado en programación, más económico",
                "url": "https://platform.deepseek.com/"
            },
            "2": {
                "name": "Gemini",
                "key": "GEMINI_API_KEY", 
                "model": "gemini-pro",
                "description": "Google AI, bueno para análisis general",
                "url": "https://makersuite.google.com/app/apikey"
            },
            "3": {
                "name": "OpenAI",
                "key": "OPENAI_API_KEY",
                "model": "gpt-4",
                "description": "Estándar de la industria, más caro",
                "url": "https://platform.openai.com/api-keys"
            }
        }
    
    def show_welcome(self):
        """Mostrar mensaje de bienvenida"""
        welcome_text = Text()
        welcome_text.append("🔧 ", style="bold blue")
        welcome_text.append("Configuración de IA Agent", style="bold")
        welcome_text.append("\n\nConfigura tu proveedor de IA y API key para comenzar a usar el sistema.")
        
        console.print(Panel(welcome_text, title="IA Agent - Configuración", border_style="blue"))
    
    def show_providers(self):
        """Mostrar proveedores disponibles"""
        table = Table(title="🤖 Proveedores de IA Disponibles")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Proveedor", style="magenta")
        table.add_column("Modelo", style="green")
        table.add_column("Descripción", style="white")
        
        for provider_id, provider in self.providers.items():
            table.add_row(
                provider_id,
                provider["name"],
                provider["model"],
                provider["description"]
            )
        
        console.print(table)
        console.print()
    
    def get_provider_choice(self) -> str:
        """Obtener elección del proveedor"""
        while True:
            choice = Prompt.ask(
                "Selecciona un proveedor (1-3)",
                choices=["1", "2", "3"],
                default="1"
            )
            
            if choice in self.providers:
                return choice
            
            console.print("❌ Opción inválida. Por favor selecciona 1, 2 o 3.", style="red")
    
    def get_api_key(self, provider_name: str) -> str:
        """Obtener API key del usuario"""
        console.print(f"\n🔑 Configuración de API Key para {provider_name}")
        console.print("💡 Tu API key se guardará localmente en el archivo .env")
        
        while True:
            api_key = Prompt.ask(
                f"Ingresa tu API key de {provider_name}",
                password=True
            )
            
            if api_key and len(api_key) > 10:
                return api_key
            
            console.print("❌ API key inválida. Debe tener al menos 10 caracteres.", style="red")
    
    def show_provider_info(self, provider_id: str):
        """Mostrar información del proveedor seleccionado"""
        provider = self.providers[provider_id]
        
        info_text = Text()
        info_text.append(f"Proveedor: ", style="bold")
        info_text.append(f"{provider['name']}\n", style="cyan")
        info_text.append(f"Modelo: ", style="bold")
        info_text.append(f"{provider['model']}\n", style="green")
        info_text.append(f"Descripción: ", style="bold")
        info_text.append(f"{provider['description']}\n\n", style="white")
        info_text.append("Para obtener tu API key, visita:\n", style="bold")
        info_text.append(f"{provider['url']}", style="blue underline")
        
        console.print(Panel(info_text, title=f"📋 Información de {provider['name']}", border_style="green"))
    
    def save_config(self, provider_id: str, api_key: str):
        """Guardar configuración en archivo .env"""
        provider = self.providers[provider_id]
        
        # Leer configuración existente
        existing_config = {}
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        existing_config[key] = value
        
        # Actualizar configuración
        existing_config[provider["key"]] = api_key
        existing_config["AI_PROVIDER"] = provider["name"].lower()
        existing_config["AI_MODEL"] = provider["model"]
        existing_config["AI_TEMPERATURE"] = "0.1"
        existing_config["AI_MAX_TOKENS"] = "4000"
        
        # Escribir archivo .env
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write("# Configuración de IA Agent\n")
            f.write("# Generado automáticamente por el CLI de configuración\n\n")
            
            f.write("# Configuración de IA\n")
            f.write(f"{provider['key']}={api_key}\n")
            f.write(f"AI_PROVIDER={provider['name'].lower()}\n")
            f.write(f"AI_MODEL={provider['model']}\n")
            f.write(f"AI_TEMPERATURE=0.1\n")
            f.write(f"AI_MAX_TOKENS=4000\n\n")
            
            f.write("# Configuración de logging\n")
            f.write("LOG_LEVEL=INFO\n")
            f.write("LOG_FILE=./logs/ia_agent.log\n\n")
            
            f.write("# Configuración de memoria\n")
            f.write("MEMORY_CACHE_SIZE=1000\n")
            f.write("CHROMADB_PERSIST_DIRECTORY=./memory/vector\n\n")
            
            f.write("# Configuración de agentes\n")
            f.write("MAX_CONCURRENT_AGENTS=3\n")
            f.write("AGENT_TIMEOUT=60\n\n")
            
            f.write("# Configuración de archivos\n")
            f.write("TEMP_DIRECTORY=./temp\n")
            f.write("OUTPUT_DIRECTORY=./output\n")
            f.write("ALLOWED_FILE_EXTENSIONS=.cs,.csproj,.sln\n\n")
            
            f.write("# Configuración de .NET\n")
            f.write("DOTNET_PATH=dotnet\n")
        
        console.print(f"✅ Configuración guardada en {self.config_file}", style="green")
    
    def test_configuration(self, provider_id: str, api_key: str) -> bool:
        """Probar la configuración"""
        provider = self.providers[provider_id]
        
        console.print(f"\n🧪 Probando configuración de {provider['name']}...")
        
        try:
            # Importar y probar el proveedor
            if provider_id == "1":  # DeepSeek
                from ai.llm_manager import DeepSeekLLM
                llm = DeepSeekLLM(api_key=api_key, model=provider["model"])
                response = llm.invoke("Hola, ¿puedes responder con 'OK'?")
                if "OK" in response.content or "ok" in response.content.lower():
                    return True
                    
            elif provider_id == "2":  # Gemini
                from ai.llm_manager import GeminiLLM
                llm = GeminiLLM(api_key=api_key, model=provider["model"])
                response = llm.invoke("Hola, ¿puedes responder con 'OK'?")
                if "OK" in response.content or "ok" in response.content.lower():
                    return True
                    
            elif provider_id == "3":  # OpenAI
                from langchain_openai import ChatOpenAI
                llm = ChatOpenAI(api_key=api_key, model=provider["model"])
                response = llm.invoke("Hola, ¿puedes responder con 'OK'?")
                if "OK" in response.content or "ok" in response.content.lower():
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error al probar configuración: {e}")
            return False
    
    def show_success(self, provider_name: str):
        """Mostrar mensaje de éxito"""
        success_text = Text()
        success_text.append("🎉 ", style="bold green")
        success_text.append("¡Configuración completada exitosamente!\n\n", style="bold green")
        success_text.append(f"Proveedor: ", style="bold")
        success_text.append(f"{provider_name}\n", style="cyan")
        success_text.append("Estado: ", style="bold")
        success_text.append("✅ Configurado y funcionando\n\n", style="green")
        success_text.append("Ahora puedes usar el sistema:\n", style="bold")
        success_text.append("• ia-agent --help\n", style="blue")
        success_text.append("• ia-agent analyze --project ./mi-proyecto\n", style="blue")
        success_text.append("• ia-agent generate --file ./Controllers/UserController.cs", style="blue")
        
        console.print(Panel(success_text, title="✅ Configuración Exitosa", border_style="green"))
    
    def run(self):
        """Ejecutar CLI de configuración"""
        try:
            self.show_welcome()
            self.show_providers()
            
            # Verificar si ya existe configuración
            if self.config_file.exists():
                if not Confirm.ask("Ya existe un archivo .env. ¿Deseas reconfigurar?"):
                    console.print("Configuración cancelada.", style="yellow")
                    return
            
            # Obtener elección del proveedor
            provider_id = self.get_provider_choice()
            provider = self.providers[provider_id]
            
            # Mostrar información del proveedor
            self.show_provider_info(provider_id)
            
            # Obtener API key
            api_key = self.get_api_key(provider["name"])
            
            # Probar configuración
            if Confirm.ask("¿Deseas probar la configuración antes de guardar?"):
                if self.test_configuration(provider_id, api_key):
                    console.print("✅ Configuración probada exitosamente!", style="green")
                else:
                    console.print("❌ Error en la configuración. Verifica tu API key.", style="red")
                    if not Confirm.ask("¿Deseas continuar de todos modos?"):
                        console.print("Configuración cancelada.", style="yellow")
                        return
            
            # Guardar configuración
            self.save_config(provider_id, api_key)
            
            # Mostrar éxito
            self.show_success(provider["name"])
            
        except KeyboardInterrupt:
            console.print("\n\nConfiguración cancelada por el usuario.", style="yellow")
        except Exception as e:
            logger.error(f"Error en configuración: {e}")
            console.print(f"❌ Error: {e}", style="red")


def main():
    """Función principal"""
    cli = ConfigCLI()
    cli.run()


if __name__ == "__main__":
    main()
