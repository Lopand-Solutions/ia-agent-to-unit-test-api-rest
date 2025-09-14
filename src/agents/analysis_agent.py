"""
Agente Analista - Especializado en análisis de código .NET
IA Agent para Generación de Pruebas Unitarias .NET
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

from agents.base_agent import ReActAgent, AgentRole, AgentTask
from tools.dotnet_tools import project_analyzer, controller_analyzer, command_executor
from tools.file_tools import code_file_manager
from langchain_agents.memory.conversation_memory import ConversationMemory
from langchain_agents.memory.vector_memory import VectorMemory
from utils.config import Config
from utils.logging import get_logger

logger = get_logger("analysis-agent")


class AnalysisAgent(ReActAgent):
    """Agente especializado en análisis de código .NET"""
    
    def __init__(self, config: Optional[Config] = None):
        super().__init__("analysis_agent", AgentRole.ANALYST, config)
        
        self.logger = logger
        self.llm = None
        self.agent_executor = None
        
        # Memoria del agente
        self.conversation_memory = ConversationMemory("analysis_agent")
        self.vector_memory = VectorMemory("analysis_agent")
        
        # Herramientas específicas del analista
        self.tools = {
            "analyze_dotnet_project": self._analyze_dotnet_project,
            "parse_controller": self._parse_controller,
            "identify_dependencies": self._identify_dependencies,
            "extract_models": self._extract_models,
            "find_source_files": self._find_source_files,
            "get_project_info": self._get_project_info
        }
        
        self.logger.info("Agente Analista inicializado")
    
    def initialize(self) -> bool:
        """Inicializar el agente"""
        try:
            # Configurar LLM
            self.llm = ChatOpenAI(
                model=self.config.ai.model,
                temperature=self.config.ai.temperature,
                openai_api_key=self.config.ai.openai_api_key
            )
            
            # Configurar herramientas de LangChain
            langchain_tools = self._create_langchain_tools()
            
            # Crear prompt template
            prompt = self._create_prompt_template()
            
            # Crear agente ReAct
            agent = create_react_agent(
                llm=self.llm,
                tools=langchain_tools,
                prompt=prompt
            )
            
            # Crear ejecutor del agente
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=langchain_tools,
                verbose=True,
                max_iterations=5,
                early_stopping_method="generate"
            )
            
            self.logger.info("Agente Analista configurado exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al inicializar Agente Analista: {e}")
            return False
    
    def get_capabilities(self) -> List[str]:
        """Obtener capacidades del agente"""
        return [
            "Analizar proyectos .NET completos",
            "Extraer información de controladores API",
            "Identificar dependencias e inyección de servicios",
            "Detectar patrones de arquitectura",
            "Analizar modelos de datos (DTOs, Entities)",
            "Generar metadatos del proyecto",
            "Buscar archivos fuente",
            "Obtener información de configuración"
        ]
    
    def process_task(self, task: AgentTask) -> Any:
        """Procesar tarea de análisis"""
        try:
            self.logger.info(f"Procesando tarea: {task.task_id}")
            self.set_status(self.status.THINKING)
            
            # Ejecutar análisis usando LangChain
            result = self.agent_executor.invoke({
                "input": task.description,
                "chat_history": self.conversation_memory.get_conversation_history()
            })
            
            # Guardar resultado en memoria
            self._save_analysis_result(task.task_id, result)
            
            # Actualizar métricas
            self.tasks_completed += 1
            
            self.logger.info(f"Tarea completada: {task.task_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error al procesar tarea {task.task_id}: {e}")
            self.tasks_failed += 1
            raise
    
    def _analyze_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analizar contexto específico del agente"""
        try:
            analysis = {
                "context_type": "dotnet_analysis",
                "project_path": context.get("project_path"),
                "analysis_type": context.get("analysis_type", "full"),
                "target_components": context.get("target_components", []),
                "timestamp": datetime.now().isoformat()
            }
            
            # Buscar en memoria vectorial para contexto similar
            if context.get("project_path"):
                similar_analyses = self.vector_memory.search(
                    f"project analysis {context['project_path']}", 
                    limit=3
                )
                analysis["similar_analyses"] = [
                    {
                        "content": result.entry.content,
                        "similarity": result.similarity,
                        "metadata": result.entry.metadata
                    }
                    for result in similar_analyses
                ]
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error al analizar contexto: {e}")
            return {"error": str(e)}
    
    def _identify_actions(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identificar acciones necesarias para análisis"""
        try:
            actions = []
            
            project_path = analysis.get("project_path")
            analysis_type = analysis.get("analysis_type", "full")
            
            if not project_path:
                return [{"action": "error", "priority": 1, "message": "No se proporcionó ruta del proyecto"}]
            
            # Acciones básicas de análisis
            actions.append({
                "action": "analyze_dotnet_project",
                "priority": 1,
                "parameters": {"project_path": project_path}
            })
            
            if analysis_type in ["full", "controllers"]:
                actions.append({
                    "action": "find_controllers",
                    "priority": 2,
                    "parameters": {"project_path": project_path}
                })
            
            if analysis_type in ["full", "dependencies"]:
                actions.append({
                    "action": "identify_dependencies",
                    "priority": 3,
                    "parameters": {"project_path": project_path}
                })
            
            if analysis_type in ["full", "models"]:
                actions.append({
                    "action": "extract_models",
                    "priority": 4,
                    "parameters": {"project_path": project_path}
                })
            
            return actions
            
        except Exception as e:
            self.logger.error(f"Error al identificar acciones: {e}")
            return [{"action": "error", "priority": 1, "message": str(e)}]
    
    def _execute_action(self, action: Dict[str, Any]) -> Any:
        """Ejecutar acción específica de análisis"""
        try:
            action_name = action["action"]
            parameters = action.get("parameters", {})
            
            self.logger.info(f"Ejecutando acción: {action_name}")
            
            if action_name == "analyze_dotnet_project":
                return self._analyze_dotnet_project(**parameters)
            elif action_name == "find_controllers":
                return self._find_controllers(**parameters)
            elif action_name == "identify_dependencies":
                return self._identify_dependencies(**parameters)
            elif action_name == "extract_models":
                return self._extract_models(**parameters)
            else:
                raise ValueError(f"Acción no reconocida: {action_name}")
                
        except Exception as e:
            self.logger.error(f"Error al ejecutar acción {action['action']}: {e}")
            raise
    
    def _create_langchain_tools(self) -> List[Tool]:
        """Crear herramientas de LangChain"""
        tools = []
        
        for tool_name, tool_func in self.tools.items():
            tool = Tool(
                name=tool_name,
                description=self._get_tool_description(tool_name),
                func=tool_func
            )
            tools.append(tool)
        
        return tools
    
    def _get_tool_description(self, tool_name: str) -> str:
        """Obtener descripción de herramienta"""
        descriptions = {
            "analyze_dotnet_project": "Analiza un proyecto .NET completo y extrae información sobre su estructura, dependencias y configuración",
            "parse_controller": "Analiza un controlador API específico y extrae información sobre sus métodos, rutas y parámetros",
            "identify_dependencies": "Identifica las dependencias del proyecto, incluyendo paquetes NuGet y referencias de proyecto",
            "extract_models": "Extrae información sobre modelos de datos (DTOs, Entities, ViewModels) del proyecto",
            "find_source_files": "Busca archivos fuente .cs en el proyecto",
            "get_project_info": "Obtiene información básica del proyecto desde el archivo .csproj"
        }
        return descriptions.get(tool_name, f"Herramienta: {tool_name}")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Crear template de prompt para el agente"""
        template = """
Eres un agente especializado en análisis de código .NET. Tu tarea es analizar proyectos .NET y extraer información relevante para la generación de pruebas unitarias.

Tienes acceso a las siguientes herramientas:
{tools}

Usa el siguiente formato:

Question: la pregunta de entrada que debes responder
Thought: siempre debes pensar en qué hacer
Action: la acción a tomar, debe ser una de [{tool_names}]
Action Input: la entrada para la acción
Observation: el resultado de la acción
... (este Thought/Action/Action Input/Observation puede repetirse N veces)
Thought: ahora sé la respuesta final
Final Answer: la respuesta final a la pregunta original

Historial de conversación:
{chat_history}

Question: {input}
Thought: {agent_scratchpad}
"""
        
        return PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad", "tools", "tool_names", "chat_history"]
        )
    
    # Métodos de herramientas específicas
    def _analyze_dotnet_project(self, project_path: str) -> Dict[str, Any]:
        """Analizar proyecto .NET"""
        try:
            result = project_analyzer.analyze_project(project_path)
            
            # Guardar en memoria vectorial
            self.vector_memory.add_entry(
                content=f"Análisis de proyecto: {result.name} en {project_path}",
                metadata={
                    "project_name": result.name,
                    "project_path": project_path,
                    "target_framework": result.target_framework,
                    "project_type": result.project_type.value,
                    "test_framework": result.test_framework
                }
            )
            
            return {
                "success": True,
                "project_info": {
                    "name": result.name,
                    "path": result.path,
                    "target_framework": result.target_framework,
                    "project_type": result.project_type.value,
                    "packages": result.packages,
                    "references": result.references,
                    "source_files": result.source_files,
                    "test_framework": result.test_framework
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error al analizar proyecto {project_path}: {e}")
            return {"success": False, "error": str(e)}
    
    def _parse_controller(self, controller_file: str) -> Dict[str, Any]:
        """Analizar controlador específico"""
        try:
            result = controller_analyzer.analyze_controller(controller_file)
            
            # Guardar en memoria vectorial
            self.vector_memory.add_entry(
                content=f"Análisis de controlador: {result.name} en {controller_file}",
                metadata={
                    "controller_name": result.name,
                    "file_path": controller_file,
                    "namespace": result.namespace,
                    "base_class": result.base_class,
                    "methods_count": len(result.methods),
                    "dependencies": result.dependencies
                }
            )
            
            return {
                "success": True,
                "controller_info": {
                    "name": result.name,
                    "file_path": result.file_path,
                    "namespace": result.namespace,
                    "base_class": result.base_class,
                    "methods": result.methods,
                    "attributes": result.attributes,
                    "dependencies": result.dependencies
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error al analizar controlador {controller_file}: {e}")
            return {"success": False, "error": str(e)}
    
    def _identify_dependencies(self, project_path: str) -> Dict[str, Any]:
        """Identificar dependencias del proyecto"""
        try:
            project_info = project_analyzer.analyze_project(project_path)
            
            return {
                "success": True,
                "dependencies": {
                    "packages": project_info.packages,
                    "references": project_info.references,
                    "target_framework": project_info.target_framework
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error al identificar dependencias: {e}")
            return {"success": False, "error": str(e)}
    
    def _extract_models(self, project_path: str) -> Dict[str, Any]:
        """Extraer modelos de datos del proyecto"""
        try:
            source_files = code_file_manager.find_csharp_files(project_path)
            models = []
            
            for file_path in source_files:
                try:
                    content = code_file_manager.read_code_file(file_path)
                    
                    # Buscar clases que podrían ser modelos
                    import re
                    class_matches = re.findall(r'public\s+class\s+(\w+)', content)
                    
                    for class_name in class_matches:
                        models.append({
                            "name": class_name,
                            "file_path": str(file_path),
                            "type": "class"
                        })
                
                except Exception as e:
                    self.logger.warning(f"Error al procesar archivo {file_path}: {e}")
                    continue
            
            return {
                "success": True,
                "models": models
            }
            
        except Exception as e:
            self.logger.error(f"Error al extraer modelos: {e}")
            return {"success": False, "error": str(e)}
    
    def _find_source_files(self, project_path: str) -> Dict[str, Any]:
        """Buscar archivos fuente en el proyecto"""
        try:
            source_files = code_file_manager.find_csharp_files(project_path)
            
            return {
                "success": True,
                "source_files": [str(f) for f in source_files]
            }
            
        except Exception as e:
            self.logger.error(f"Error al buscar archivos fuente: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_project_info(self, project_path: str) -> Dict[str, Any]:
        """Obtener información básica del proyecto"""
        try:
            project_info = project_analyzer.analyze_project(project_path)
            
            return {
                "success": True,
                "project_info": {
                    "name": project_info.name,
                    "path": project_info.path,
                    "target_framework": project_info.target_framework,
                    "project_type": project_info.project_type.value
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error al obtener información del proyecto: {e}")
            return {"success": False, "error": str(e)}
    
    def _find_controllers(self, project_path: str) -> Dict[str, Any]:
        """Buscar controladores en el proyecto"""
        try:
            source_files = code_file_manager.find_csharp_files(project_path)
            controllers = []
            
            for file_path in source_files:
                try:
                    content = code_file_manager.read_code_file(file_path)
                    
                    # Buscar clases que heredan de ControllerBase o Controller
                    import re
                    if re.search(r':\s*(ControllerBase|Controller)', content):
                        class_match = re.search(r'public\s+class\s+(\w+)', content)
                        if class_match:
                            controllers.append({
                                "name": class_match.group(1),
                                "file_path": str(file_path)
                            })
                
                except Exception as e:
                    self.logger.warning(f"Error al procesar archivo {file_path}: {e}")
                    continue
            
            return {
                "success": True,
                "controllers": controllers
            }
            
        except Exception as e:
            self.logger.error(f"Error al buscar controladores: {e}")
            return {"success": False, "error": str(e)}
    
    def _save_analysis_result(self, task_id: str, result: Any):
        """Guardar resultado de análisis en memoria"""
        try:
            self.vector_memory.add_entry(
                content=f"Resultado de análisis para tarea {task_id}",
                metadata={
                    "task_id": task_id,
                    "result_type": type(result).__name__,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error al guardar resultado de análisis: {e}")


# Instancia global del agente analista
analysis_agent = AnalysisAgent()
