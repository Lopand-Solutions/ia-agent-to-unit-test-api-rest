"""
Agente Generador - Especializado en generación de código de pruebas
IA Agent para Generación de Pruebas Unitarias .NET
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from agents.base_agent import ReActAgent, AgentRole, AgentTask
from tools.file_tools import code_file_manager
from langchain_agents.memory.conversation_memory import ConversationMemory
from langchain_agents.memory.vector_memory import VectorMemory
from utils.config import Config
from utils.logging import get_logger

logger = get_logger("generation-agent")


class GenerationAgent(ReActAgent):
    """Agente especializado en generación de código de pruebas"""
    
    def __init__(self, config: Optional[Config] = None):
        super().__init__("generation_agent", AgentRole.GENERATOR, config)
        
        self.logger = logger
        self.llm = None
        self.agent_executor = None
        
        # Memoria del agente
        self.conversation_memory = ConversationMemory("generation_agent")
        self.vector_memory = VectorMemory("generation_agent")
        
        # Templates de pruebas
        self.test_templates = {
            "xunit": self._get_xunit_template(),
            "nunit": self._get_nunit_template(),
            "mstest": self._get_mstest_template()
        }
        
        # Herramientas específicas del generador
        self.tools = {
            "generate_test_file": self._generate_test_file,
            "create_test_method": self._create_test_method,
            "generate_mock_data": self._generate_mock_data,
            "validate_generated_code": self._validate_generated_code,
            "apply_test_template": self._apply_test_template
        }
        
        self.logger.info("Agente Generador inicializado")
    
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
            
            self.logger.info("Agente Generador configurado exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al inicializar Agente Generador: {e}")
            return False
    
    def get_capabilities(self) -> List[str]:
        """Obtener capacidades del agente"""
        return [
            "Generar archivos de pruebas completos",
            "Crear métodos de prueba individuales",
            "Generar datos de prueba (mocks y stubs)",
            "Aplicar templates de diferentes frameworks",
            "Validar código generado",
            "Generar pruebas para controladores API",
            "Generar pruebas para servicios y repositorios",
            "Crear casos de prueba para happy path, edge cases y error handling"
        ]
    
    def process_task(self, task: AgentTask) -> Any:
        """Procesar tarea de generación"""
        try:
            self.logger.info(f"Procesando tarea: {task.task_id}")
            self.set_status(self.status.THINKING)
            
            # Ejecutar generación usando LangChain
            result = self.agent_executor.invoke({
                "input": task.description,
                "chat_history": self.conversation_memory.get_conversation_history()
            })
            
            # Guardar resultado en memoria
            self._save_generation_result(task.task_id, result)
            
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
                "context_type": "test_generation",
                "target_component": context.get("target_component"),
                "framework": context.get("framework", "xunit"),
                "test_type": context.get("test_type", "unit"),
                "analysis_data": context.get("analysis_data"),
                "timestamp": datetime.now().isoformat()
            }
            
            # Buscar en memoria vectorial para patrones similares
            if context.get("target_component"):
                similar_generations = self.vector_memory.search(
                    f"test generation {context['target_component']}", 
                    limit=3
                )
                analysis["similar_generations"] = [
                    {
                        "content": result.entry.content,
                        "similarity": result.similarity,
                        "metadata": result.entry.metadata
                    }
                    for result in similar_generations
                ]
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error al analizar contexto: {e}")
            return {"error": str(e)}
    
    def _identify_actions(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identificar acciones necesarias para generación"""
        try:
            actions = []
            
            target_component = analysis.get("target_component")
            framework = analysis.get("framework", "xunit")
            analysis_data = analysis.get("analysis_data")
            
            if not target_component or not analysis_data:
                return [{"action": "error", "priority": 1, "message": "Datos insuficientes para generación"}]
            
            # Acciones básicas de generación
            actions.append({
                "action": "generate_test_file",
                "priority": 1,
                "parameters": {
                    "target_component": target_component,
                    "framework": framework,
                    "analysis_data": analysis_data
                }
            })
            
            # Generar métodos de prueba específicos
            if "methods" in analysis_data:
                for method in analysis_data["methods"]:
                    actions.append({
                        "action": "create_test_method",
                        "priority": 2,
                        "parameters": {
                            "method_info": method,
                            "framework": framework
                        }
                    })
            
            # Generar datos de prueba
            actions.append({
                "action": "generate_mock_data",
                "priority": 3,
                "parameters": {
                    "target_component": target_component,
                    "analysis_data": analysis_data
                }
            })
            
            return actions
            
        except Exception as e:
            self.logger.error(f"Error al identificar acciones: {e}")
            return [{"action": "error", "priority": 1, "message": str(e)}]
    
    def _execute_action(self, action: Dict[str, Any]) -> Any:
        """Ejecutar acción específica de generación"""
        try:
            action_name = action["action"]
            parameters = action.get("parameters", {})
            
            self.logger.info(f"Ejecutando acción: {action_name}")
            
            if action_name == "generate_test_file":
                return self._generate_test_file(**parameters)
            elif action_name == "create_test_method":
                return self._create_test_method(**parameters)
            elif action_name == "generate_mock_data":
                return self._generate_mock_data(**parameters)
            elif action_name == "validate_generated_code":
                return self._validate_generated_code(**parameters)
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
            "generate_test_file": "Genera un archivo completo de pruebas unitarias para un componente específico",
            "create_test_method": "Crea un método de prueba individual con casos de prueba específicos",
            "generate_mock_data": "Genera datos de prueba y mocks para las pruebas unitarias",
            "validate_generated_code": "Valida que el código generado compile correctamente y siga las mejores prácticas",
            "apply_test_template": "Aplica un template específico de framework de testing al código generado"
        }
        return descriptions.get(tool_name, f"Herramienta: {tool_name}")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Crear template de prompt para el agente"""
        template = """
Eres un agente especializado en generación de pruebas unitarias para código .NET. Tu tarea es crear pruebas unitarias completas, bien estructuradas y que sigan las mejores prácticas.

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
    def _generate_test_file(self, target_component: str, framework: str, 
                           analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generar archivo completo de pruebas"""
        try:
            # Obtener template del framework
            template = self.test_templates.get(framework, self.test_templates["xunit"])
            
            # Generar código de prueba usando LLM
            prompt = f"""
Genera un archivo completo de pruebas unitarias para el siguiente componente:

Componente: {target_component}
Framework: {framework}
Datos de análisis: {analysis_data}

El archivo debe incluir:
1. Using statements necesarios
2. Namespace apropiado
3. Clase de prueba con [TestClass] o [Test] según el framework
4. Métodos de prueba para cada método público
5. Casos de prueba para happy path, edge cases y error handling
6. Mocks y stubs apropiados
7. Comentarios explicativos

Usa el siguiente template como base:
{template}
"""
            
            response = self.llm.invoke(prompt)
            test_code = response.content
            
            # Guardar en memoria vectorial
            self.vector_memory.add_entry(
                content=f"Archivo de pruebas generado para {target_component}",
                metadata={
                    "target_component": target_component,
                    "framework": framework,
                    "code_length": len(test_code)
                }
            )
            
            return {
                "success": True,
                "test_code": test_code,
                "framework": framework,
                "target_component": target_component
            }
            
        except Exception as e:
            self.logger.error(f"Error al generar archivo de pruebas: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_test_method(self, method_info: Dict[str, Any], framework: str) -> Dict[str, Any]:
        """Crear método de prueba individual"""
        try:
            method_name = method_info.get("name", "UnknownMethod")
            return_type = method_info.get("return_type", "void")
            parameters = method_info.get("parameters", [])
            
            # Generar método de prueba usando LLM
            prompt = f"""
Genera un método de prueba para el siguiente método:

Método: {method_name}
Tipo de retorno: {return_type}
Parámetros: {parameters}
Framework: {framework}

El método de prueba debe incluir:
1. Atributo de prueba apropiado ([Test] o [TestMethod])
2. Nombre descriptivo del método
3. Casos de prueba para diferentes escenarios
4. Assertions apropiadas
5. Manejo de excepciones si es necesario

Usa el patrón Arrange-Act-Assert.
"""
            
            response = self.llm.invoke(prompt)
            test_method_code = response.content
            
            return {
                "success": True,
                "test_method_code": test_method_code,
                "method_name": method_name,
                "framework": framework
            }
            
        except Exception as e:
            self.logger.error(f"Error al crear método de prueba: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_mock_data(self, target_component: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generar datos de prueba y mocks"""
        try:
            # Generar datos de prueba usando LLM
            prompt = f"""
Genera datos de prueba y mocks para el siguiente componente:

Componente: {target_component}
Datos de análisis: {analysis_data}

Genera:
1. Datos de prueba para modelos/DTOs
2. Mocks para dependencias
3. Datos de prueba para diferentes escenarios
4. Configuración de mocks

Usa Moq como framework de mocking.
"""
            
            response = self.llm.invoke(prompt)
            mock_data_code = response.content
            
            return {
                "success": True,
                "mock_data_code": mock_data_code,
                "target_component": target_component
            }
            
        except Exception as e:
            self.logger.error(f"Error al generar datos de prueba: {e}")
            return {"success": False, "error": str(e)}
    
    def _validate_generated_code(self, code: str) -> Dict[str, Any]:
        """Validar código generado"""
        try:
            # Validaciones básicas
            validations = {
                "has_using_statements": "using " in code,
                "has_namespace": "namespace " in code,
                "has_test_class": any(attr in code for attr in ["[TestClass]", "[Test]", "class"]),
                "has_test_methods": any(attr in code for attr in ["[Test]", "[TestMethod]"]),
                "has_assertions": "Assert." in code or "Assert." in code,
                "code_length": len(code) > 100
            }
            
            all_valid = all(validations.values())
            
            return {
                "success": all_valid,
                "validations": validations,
                "issues": [k for k, v in validations.items() if not v]
            }
            
        except Exception as e:
            self.logger.error(f"Error al validar código: {e}")
            return {"success": False, "error": str(e)}
    
    def _apply_test_template(self, code: str, framework: str) -> Dict[str, Any]:
        """Aplicar template específico de framework"""
        try:
            template = self.test_templates.get(framework, self.test_templates["xunit"])
            
            # Aplicar template usando LLM
            prompt = f"""
Aplica el template de {framework} al siguiente código de prueba:

Código original:
{code}

Template de {framework}:
{template}

Asegúrate de que el código resultante:
1. Use los atributos correctos del framework
2. Siga las convenciones de naming
3. Use las assertions apropiadas
4. Tenga la estructura correcta
"""
            
            response = self.llm.invoke(prompt)
            templated_code = response.content
            
            return {
                "success": True,
                "templated_code": templated_code,
                "framework": framework
            }
            
        except Exception as e:
            self.logger.error(f"Error al aplicar template: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_xunit_template(self) -> str:
        """Obtener template de xUnit"""
        return """
using Xunit;
using Moq;
using Microsoft.Extensions.Logging;

namespace {namespace}
{{
    public class {class_name}Tests
    {{
        private readonly Mock<ILogger<{class_name}>> _mockLogger;
        private readonly {class_name} _sut;

        public {class_name}Tests()
        {{
            _mockLogger = new Mock<ILogger<{class_name}>>();
            _sut = new {class_name}(_mockLogger.Object);
        }}

        [Fact]
        public void {method_name}_Should_ReturnExpectedResult_When_ValidInput()
        {{
            // Arrange
            var input = "test";

            // Act
            var result = _sut.{method_name}(input);

            // Assert
            Assert.NotNull(result);
        }}
    }}
}}
"""
    
    def _get_nunit_template(self) -> str:
        """Obtener template de NUnit"""
        return """
using NUnit.Framework;
using Moq;
using Microsoft.Extensions.Logging;

namespace {namespace}
{{
    [TestFixture]
    public class {class_name}Tests
    {{
        private Mock<ILogger<{class_name}>> _mockLogger;
        private {class_name} _sut;

        [SetUp]
        public void Setup()
        {{
            _mockLogger = new Mock<ILogger<{class_name}>>();
            _sut = new {class_name}(_mockLogger.Object);
        }}

        [Test]
        public void {method_name}_Should_ReturnExpectedResult_When_ValidInput()
        {{
            // Arrange
            var input = "test";

            // Act
            var result = _sut.{method_name}(input);

            // Assert
            Assert.That(result, Is.Not.Null);
        }}
    }}
}}
"""
    
    def _get_mstest_template(self) -> str:
        """Obtener template de MSTest"""
        return """
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using Microsoft.Extensions.Logging;

namespace {namespace}
{{
    [TestClass]
    public class {class_name}Tests
    {{
        private Mock<ILogger<{class_name}>> _mockLogger;
        private {class_name} _sut;

        [TestInitialize]
        public void TestInitialize()
        {{
            _mockLogger = new Mock<ILogger<{class_name}>>();
            _sut = new {class_name}(_mockLogger.Object);
        }}

        [TestMethod]
        public void {method_name}_Should_ReturnExpectedResult_When_ValidInput()
        {{
            // Arrange
            var input = "test";

            // Act
            var result = _sut.{method_name}(input);

            // Assert
            Assert.IsNotNull(result);
        }}
    }}
}}
"""
    
    def _save_generation_result(self, task_id: str, result: Any):
        """Guardar resultado de generación en memoria"""
        try:
            self.vector_memory.add_entry(
                content=f"Resultado de generación para tarea {task_id}",
                metadata={
                    "task_id": task_id,
                    "result_type": type(result).__name__,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error al guardar resultado de generación: {e}")


# Instancia global del agente generador
generation_agent = GenerationAgent()
