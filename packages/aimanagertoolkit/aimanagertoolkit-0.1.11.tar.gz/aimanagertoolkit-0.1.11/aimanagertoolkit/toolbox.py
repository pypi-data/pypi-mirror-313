import os
import importlib
from pydantic import BaseModel
from typing import List, Dict, Any
from .log import Log

logger = Log(__name__)  


class Tool(BaseModel):
    """
    Clase base que representa una herramienta (tool) que puede ser utilizada por la API de OpenAI.

    Atributos:
        name (str): Nombre de la herramienta.
        description (str): Descripción de la herramienta y su funcionalidad.
        parameters (Dict[str, Any]): Esquema JSON de los parámetros que acepta la herramienta.
        type (str): Tipo de herramienta (por defecto es 'function').
        strict (bool): Indica si la herramienta debe usar Structured Outputs.
    """

    name: str
    description: str
    parameters: Dict[str, Any]
    type: str = "function"
    strict: bool = False

    def __init__(self, **data: Any):
        """
        Inicializa una instancia de Tool y la registra automáticamente en el Toolbox global.

        Parámetros:
            **data (Any): Datos que se pasan para inicializar la herramienta.
        """
        super().__init__(**data)
        try:
            Toolbox.register_tool(self)  # Registro automático en el Toolbox global
        except Exception as e:
            logger.error(f"Error al registrar la herramienta {self.name}: {e}")

class Toolbox:
    """
    Clase para gestionar y registrar herramientas (tools) de manera automática en la aplicación.

    Atributos:
        _global_tools (List[Tool]): Lista global que almacena todas las herramientas registradas.
    """

    _global_tools: List[Tool] = []  # Lista global para almacenar herramientas registradas

    @classmethod
    def register_tool(cls, tool: Tool):
        """
        Registra una nueva herramienta en el gestor global.

        Parámetros:
            tool (Tool): Instancia de la herramienta a registrar.
        """
        try:
            logger.info(f"Registrando herramienta globalmente: {tool.name}")
            cls._global_tools.append(tool)
        except Exception as e:
            logger.error(f"Error al registrar la herramienta {tool.name}: {e}")

    @classmethod
    def get_tools(cls) -> List[dict]:
        """
        Devuelve la lista de herramientas registradas en formato diccionario.

        Retorno:
            List[dict]: Lista de herramientas en formato diccionario.
        """
        try:
            logger.info(f"Obteniendo lista de herramientas registradas. Total: {len(cls._global_tools)} herramientas.")
            return [tool.dict() for tool in cls._global_tools]
        except Exception as e:
            logger.error(f"Error al obtener la lista de herramientas: {e}")
            return []

    @classmethod
    def __call__(cls) -> List[dict]:
        """
        Permite que la clase Toolbox sea llamada como una función para obtener las herramientas registradas.

        Retorno:
            List[dict]: Lista de herramientas en formato diccionario.
        """
        return cls.get_tools()

    @classmethod
    def __str__(cls):
        """
        Retorna la representación en cadena del Toolbox, mostrando la lista de herramientas registradas.
        """
        return str(cls.get_tools())

    @classmethod
    def __repr__(cls):
        """
        Retorna la representación en cadena del Toolbox, mostrando la lista de herramientas registradas.
        """
        return str(cls.get_tools())