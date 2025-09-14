"""
Punto de entrada principal para el CLI
IA Agent para Generación de Pruebas Unitarias .NET
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.multi_agent_cli import main

if __name__ == "__main__":
    main()
