"""
CLI simplificado para el sistema de agentes
IA Agent para Generación de Pruebas Unitarias .NET
"""

import os
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

from agents.analysis_agent import analysis_agent
from agents.generation_agent import generation_agent
from agents.validation_agent import validation_agent
from agents.optimization_agent import optimization_agent
from agents.coordinator_agent import coordinator_agent
from tools.file_tools import file_manager
from tools.dotnet_tools import dotnet_manager
from utils.config import get_config
from utils.logging import get_logger, setup_logging

logger = get_logger("simple-cli")
console = Console()


class SimpleCLI:
    """CLI simplificado para el sistema de agentes"""
    
    def __init__(self):
        self.config = get_config()
        self.console = console
        self.logger = logger
        
        # Agentes disponibles
        self.agents = {
            'analysis': analysis_agent,
            'generation': generation_agent,
            'validation': validation_agent,
            'optimization': optimization_agent,
            'coordinator': coordinator_agent
        }
        
        # Estado de la sesión
        self.current_project_path = None
        self.current_session_id = None
    
    def show_welcome(self):
        """Mostrar mensaje de bienvenida"""
        welcome_text = """
🚀 IA Agent para Generación de Pruebas Unitarias .NET
Sistema Multi-Agente con LangChain

Comandos disponibles:
- analyze: Analizar código .NET
- generate: Generar pruebas unitarias
- validate: Validar código
- optimize: Optimizar código
- help: Mostrar ayuda
- exit: Salir del sistema
        """
        
        self.console.print(Panel(welcome_text, title="Bienvenido", border_style="blue"))
    
    def show_help(self):
        """Mostrar ayuda"""
        help_text = """
📖 Comandos disponibles:

1. analyze <archivo> - Analizar archivo de código .NET
2. generate <archivo> - Generar pruebas unitarias para un archivo
3. validate <archivo> - Validar código y pruebas
4. optimize <archivo> - Optimizar código
5. project <ruta> - Establecer proyecto actual
6. status - Mostrar estado del sistema
7. help - Mostrar esta ayuda
8. exit - Salir del sistema

Ejemplos:
- analyze Calculator.cs
- generate Calculator.cs
- project ./mi_proyecto
- status
        """
        
        self.console.print(Panel(help_text, title="Ayuda", border_style="green"))
    
    def show_status(self):
        """Mostrar estado del sistema"""
        status_text = f"""
📊 Estado del Sistema:

Proyecto actual: {self.current_project_path or 'No establecido'}
Sesión: {self.current_session_id or 'No iniciada'}

Agentes disponibles:
- Analysis Agent: ✅ Disponible
- Generation Agent: ✅ Disponible  
- Validation Agent: ✅ Disponible
- Optimization Agent: ✅ Disponible
- Coordinator Agent: ✅ Disponible

Configuración:
- Log Level: {getattr(self.config.logging, 'level', 'INFO') if hasattr(self.config, 'logging') else 'INFO'}
- AI Provider: {getattr(self.config.ai, 'provider', 'openai') if hasattr(self.config, 'ai') else 'openai'}
- Model: {getattr(self.config.ai, 'model', 'gpt-4') if hasattr(self.config, 'ai') else 'gpt-4'}
        """
        
        self.console.print(Panel(status_text, title="Estado del Sistema", border_style="yellow"))
    
    def set_project(self, project_path: str):
        """Establecer proyecto actual"""
        try:
            path = Path(project_path)
            if not path.exists():
                self.console.print(f"❌ Error: El proyecto '{project_path}' no existe")
                return False
            
            self.current_project_path = str(path.absolute())
            self.console.print(f"✅ Proyecto establecido: {self.current_project_path}")
            return True
            
        except Exception as e:
            self.console.print(f"❌ Error al establecer proyecto: {e}")
            return False
    
    def analyze_file(self, file_path: str):
        """Analizar archivo de código"""
        try:
            if not self.current_project_path:
                self.console.print("❌ Error: No hay proyecto establecido. Use 'project <ruta>' primero")
                return
            
            full_path = Path(self.current_project_path) / file_path
            if not full_path.exists():
                self.console.print(f"❌ Error: El archivo '{file_path}' no existe")
                return
            
            self.console.print(f"🔍 Analizando archivo: {file_path}")
            
            # Leer código
            code = file_manager.read_file(str(full_path))
            
            # Analizar con el agente
            result = analysis_agent.analyze_code(code)
            
            # Mostrar resultado
            self.console.print(Panel(result, title="Resultado del Análisis", border_style="blue"))
            
        except Exception as e:
            self.console.print(f"❌ Error al analizar archivo: {e}")
    
    def generate_tests(self, file_path: str):
        """Generar pruebas unitarias"""
        try:
            if not self.current_project_path:
                self.console.print("❌ Error: No hay proyecto establecido. Use 'project <ruta>' primero")
                return
            
            full_path = Path(self.current_project_path) / file_path
            if not full_path.exists():
                self.console.print(f"❌ Error: El archivo '{file_path}' no existe")
                return
            
            self.console.print(f"🧪 Generando pruebas para: {file_path}")
            
            # Leer código
            code = file_manager.read_file(str(full_path))
            
            # Analizar primero
            analysis = analysis_agent.analyze_code(code)
            
            # Generar pruebas
            tests = generation_agent.generate_tests(code, analysis, "xunit")
            
            # Mostrar resultado
            syntax = Syntax(tests, "csharp", theme="monokai", line_numbers=True)
            self.console.print(Panel(syntax, title="Pruebas Generadas", border_style="green"))
            
        except Exception as e:
            self.console.print(f"❌ Error al generar pruebas: {e}")
    
    def validate_code(self, file_path: str):
        """Validar código"""
        try:
            if not self.current_project_path:
                self.console.print("❌ Error: No hay proyecto establecido. Use 'project <ruta>' primero")
                return
            
            full_path = Path(self.current_project_path) / file_path
            if not full_path.exists():
                self.console.print(f"❌ Error: El archivo '{file_path}' no existe")
                return
            
            self.console.print(f"✅ Validando código: {file_path}")
            
            # Leer código
            code = file_manager.read_file(str(full_path))
            
            # Validar con el agente
            result = validation_agent.validate_code(code)
            
            # Mostrar resultado
            self.console.print(Panel(result, title="Resultado de Validación", border_style="yellow"))
            
        except Exception as e:
            self.console.print(f"❌ Error al validar código: {e}")
    
    def optimize_code(self, file_path: str):
        """Optimizar código"""
        try:
            if not self.current_project_path:
                self.console.print("❌ Error: No hay proyecto establecido. Use 'project <ruta>' primero")
                return
            
            full_path = Path(self.current_project_path) / file_path
            if not full_path.exists():
                self.console.print(f"❌ Error: El archivo '{file_path}' no existe")
                return
            
            self.console.print(f"⚡ Optimizando código: {file_path}")
            
            # Leer código
            code = file_manager.read_file(str(full_path))
            
            # Optimizar con el agente
            result = optimization_agent.optimize_code(code)
            
            # Mostrar resultado
            syntax = Syntax(result, "csharp", theme="monokai", line_numbers=True)
            self.console.print(Panel(syntax, title="Código Optimizado", border_style="magenta"))
            
        except Exception as e:
            self.console.print(f"❌ Error al optimizar código: {e}")
    
    def run_interactive(self):
        """Ejecutar CLI interactivo"""
        self.show_welcome()
        
        while True:
            try:
                command = Prompt.ask("\n💻 Ingrese comando", default="help")
                
                if command.lower() in ['exit', 'quit', 'salir']:
                    self.console.print("👋 ¡Hasta luego!")
                    break
                
                elif command.lower() == 'help':
                    self.show_help()
                
                elif command.lower() == 'status':
                    self.show_status()
                
                elif command.startswith('project '):
                    project_path = command[8:].strip()
                    self.set_project(project_path)
                
                elif command.startswith('analyze '):
                    file_path = command[8:].strip()
                    self.analyze_file(file_path)
                
                elif command.startswith('generate '):
                    file_path = command[9:].strip()
                    self.generate_tests(file_path)
                
                elif command.startswith('validate '):
                    file_path = command[9:].strip()
                    self.validate_code(file_path)
                
                elif command.startswith('optimize '):
                    file_path = command[9:].strip()
                    self.optimize_code(file_path)
                
                else:
                    self.console.print("❌ Comando no reconocido. Use 'help' para ver comandos disponibles")
                    
            except KeyboardInterrupt:
                self.console.print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                self.console.print(f"❌ Error: {e}")


@click.command()
@click.option('--project-path', '-p', help='Ruta del proyecto .NET')
@click.option('--log-level', '-l', default='INFO', help='Nivel de logging')
def main(project_path: Optional[str], log_level: str):
    """IA Agent para Generación de Pruebas Unitarias .NET - CLI Simplificado"""
    
    # Configurar logging
    setup_logging(log_level)
    
    # Crear CLI
    cli = SimpleCLI()
    
    # Establecer proyecto si se proporciona
    if project_path:
        cli.set_project(project_path)
    
    # Ejecutar CLI interactivo
    cli.run_interactive()


if __name__ == "__main__":
    main()
