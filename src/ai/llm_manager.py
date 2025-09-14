"""
Gestor avanzado de LLMs
IA Agent para Generación de Pruebas Unitarias .NET
"""

from typing import Dict, List, Any, Optional, Union
from enum import Enum
import asyncio
from dataclasses import dataclass

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import AzureOpenAI

from utils.logging import get_logger
from utils.config import get_config

logger = get_logger("llm-manager")


class LLMProvider(Enum):
    """Proveedores de LLM soportados"""
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC = "anthropic"


@dataclass
class LLMConfig:
    """Configuración de LLM"""
    provider: LLMProvider
    model: str
    temperature: float = 0.1
    max_tokens: int = 4000
    timeout: int = 30
    api_key: Optional[str] = None
    endpoint: Optional[str] = None


class LLMManager:
    """Gestor avanzado de LLMs con múltiples proveedores"""
    
    def __init__(self):
        self.logger = logger
        self.config = get_config()
        self.llms: Dict[str, Any] = {}
        self.current_llm: Optional[Any] = None
        self._setup_default_llms()
    
    def _setup_default_llms(self):
        """Configurar LLMs por defecto"""
        try:
            # LLM principal (OpenAI)
            if self.config.ai.provider == "openai":
                self.llms["primary"] = ChatOpenAI(
                    model=self.config.ai.model,
                    temperature=self.config.ai.temperature,
                    max_tokens=self.config.ai.max_tokens,
                    timeout=self.config.ai.timeout
                )
                self.current_llm = self.llms["primary"]
            
            # LLM de respaldo (más rápido)
            self.llms["fast"] = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.1,
                max_tokens=2000,
                timeout=15
            )
            
            # LLM especializado en código
            self.llms["code"] = ChatOpenAI(
                model="gpt-4",
                temperature=0.05,
                max_tokens=6000,
                timeout=45
            )
            
            self.logger.info("LLMs configurados correctamente")
            
        except Exception as e:
            self.logger.error(f"Error al configurar LLMs: {e}")
            raise
    
    def get_llm(self, llm_type: str = "primary") -> Any:
        """Obtener LLM por tipo"""
        if llm_type not in self.llms:
            self.logger.warning(f"LLM tipo '{llm_type}' no encontrado, usando primary")
            llm_type = "primary"
        
        return self.llms[llm_type]
    
    def switch_llm(self, llm_type: str):
        """Cambiar LLM actual"""
        if llm_type in self.llms:
            self.current_llm = self.llms[llm_type]
            self.logger.info(f"LLM cambiado a: {llm_type}")
        else:
            self.logger.warning(f"LLM tipo '{llm_type}' no encontrado")
    
    async def generate_async(self, prompt: str, llm_type: str = "primary") -> str:
        """Generar respuesta de forma asíncrona"""
        try:
            llm = self.get_llm(llm_type)
            response = await llm.ainvoke(prompt)
            return response.content
            
        except Exception as e:
            self.logger.error(f"Error en generación asíncrona: {e}")
            raise
    
    def generate_batch(self, prompts: List[str], llm_type: str = "primary") -> List[str]:
        """Generar respuestas en lote"""
        try:
            llm = self.get_llm(llm_type)
            responses = []
            
            for prompt in prompts:
                response = llm.invoke(prompt)
                responses.append(response.content)
            
            self.logger.info(f"Generadas {len(responses)} respuestas en lote")
            return responses
            
        except Exception as e:
            self.logger.error(f"Error en generación en lote: {e}")
            raise
    
    def get_available_llms(self) -> List[str]:
        """Obtener LLMs disponibles"""
        return list(self.llms.keys())
    
    def get_llm_info(self, llm_type: str) -> Dict[str, Any]:
        """Obtener información del LLM"""
        if llm_type not in self.llms:
            return {}
        
        llm = self.llms[llm_type]
        return {
            "type": llm_type,
            "model": getattr(llm, 'model_name', 'unknown'),
            "temperature": getattr(llm, 'temperature', 0.1),
            "max_tokens": getattr(llm, 'max_tokens', 4000),
            "timeout": getattr(llm, 'timeout', 30)
        }
