"""
Singleton para ChromaDB para evitar conflictos de múltiples instancias
IA Agent para Generación de Pruebas Unitarias .NET
"""

import os
import threading
from typing import Optional, Dict, Any
from pathlib import Path

import chromadb
from chromadb.config import Settings

from utils.logging import get_logger

logger = get_logger("chromadb-singleton")


class ChromaDBSingleton:
    """Singleton para ChromaDB"""
    
    _instance: Optional['ChromaDBSingleton'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'ChromaDBSingleton':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._client: Optional[chromadb.Client] = None
            self._settings: Optional[Settings] = None
            self._base_path: Optional[Path] = None
            self._initialized = True
    
    def get_client(self, agent_name: str, base_path: Optional[Path] = None) -> chromadb.Client:
        """Obtener cliente ChromaDB para un agente específico"""
        if base_path is None:
            base_path = Path("./memory/vector")
        
        # Crear path único para el agente
        agent_path = base_path / f"agent_{agent_name}"
        agent_path.mkdir(parents=True, exist_ok=True)
        
        # Si ya tenemos un cliente con la misma configuración, reutilizarlo
        if self._client is not None and self._base_path == agent_path:
            return self._client
        
        try:
            # Configuración única para el agente
            settings = Settings(
                persist_directory=str(agent_path),
                anonymized_telemetry=False
            )
            
            # Crear nuevo cliente
            self._client = chromadb.Client(settings)
            self._settings = settings
            self._base_path = agent_path
            
            logger.info(f"Cliente ChromaDB creado para agente: {agent_name}")
            return self._client
            
        except Exception as e:
            logger.error(f"Error al crear cliente ChromaDB para {agent_name}: {e}")
            raise
    
    def reset(self):
        """Resetear el singleton (para pruebas)"""
        with self._lock:
            self._client = None
            self._settings = None
            self._base_path = None


# Instancia global
chromadb_singleton = ChromaDBSingleton()
