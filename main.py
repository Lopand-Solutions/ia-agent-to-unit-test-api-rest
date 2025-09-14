#!/usr/bin/env python3
"""
IA Agent para Generación de Pruebas Unitarias .NET
Sistema Multi-Agente con LangChain y AutoGen

Punto de entrada principal del sistema
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cli.multi_agent_cli import main

if __name__ == "__main__":
    main()
