from abc import ABC, abstractmethod
from typing import List, Union, Dict, Optional
from string import Formatter
from .log import Log

logger = Log(__name__)

class Content(ABC):
    """
    Clase base abstracta para tipos de contenido.
    """

    @abstractmethod
    def to_dict(self) -> Dict:
        """
        Convierte el contenido a una representación de diccionario.

        Returns:
            Dict: Representación en diccionario del contenido.
        """
        pass

class TextContent(Content):
    """Representa contenido de texto en un mensaje."""

    def __init__(self, text: str):
        """
        Inicializa TextContent.

        Args:
            text (str): El contenido de texto.
        """
        self.text = text
        logger.info(f"TextContent creado: {text[:50]}...")

    def to_dict(self) -> Dict:
        """
        Convierte TextContent a diccionario.

        Returns:
            Dict: Una representación en diccionario del contenido de texto.
        """
        return {"type": "text", "text": self.text}

class ImageUrlContent(Content):
    """Representa contenido de URL de imagen en un mensaje."""

    def __init__(self, url: str):
        """
        Inicializa ImageUrlContent.

        Args:
            url (str): La URL de la imagen.
        """
        self.url = url
        logger.info(f"ImageUrlContent creado: {url}")

    def to_dict(self) -> Dict:
        """
        Convierte ImageUrlContent a diccionario.

        Returns:
            Dict: Una representación en diccionario del contenido de URL de imagen.
        """
        return {"type": "image_url", "image_url": {"url": self.url}}

class BaseMessage(ABC):
    """Clase base abstracta para todos los tipos de mensajes."""

    def __init__(self, *args, **kwargs):
        """
        Inicializa BaseMessage.

        Args:
            *args: Lista de argumentos de longitud variable.
            **kwargs: Argumentos de palabras clave arbitrarios.

        Raises:
            ValueError: Si se proporcionan argumentos inválidos.
        """
        if len(args) == 1 and isinstance(args[0], str):
            self.content = [TextContent(args[0])]
        elif len(args) == 2 and all(isinstance(arg, str) for arg in args):
            self.content = [TextContent(args[0]), ImageUrlContent(args[1])]
        elif kwargs:
            self.content = []
            for key, value in kwargs.items():
                if key.startswith('text'):
                    self.content.append(TextContent(value))
                elif key.startswith('url'):
                    self.content.append(ImageUrlContent(value))
        else:
            logger.error("Se proporcionaron argumentos inválidos a BaseMessage")
            raise ValueError("Argumentos inválidos")

        logger.info(f"{self.__class__.__name__} creado con {len(self.content)} elemento(s) de contenido")

    @abstractmethod
    def role(self) -> str:
        """
        Retorna el rol del mensaje.

        Returns:
            str: El rol del mensaje.
        """
        pass

    def __repr__(self):
        """
        Retorna una representación en string del mensaje.

        Returns:
            str: Representación en string del mensaje.
        """
        return f"{self.__class__.__name__}(content={self.content})"

    def __str__(self):
        """
        Retorna una representación en string de la forma de diccionario del mensaje.

        Returns:
            str: Representación en string del diccionario del mensaje.
        """
        return str(self.to_dict())

    def to_dict(self) -> Dict:
        """
        Convierte el mensaje a una representación de diccionario.

        Returns:
            Dict: Una representación en diccionario del mensaje.
        """
        if len(self.content) == 1 and isinstance(self.content[0], TextContent):
            return {
                "role": self.role(),
                "content": self.content[0].text
            }
        else:
            return {
                "role": self.role(),
                "content": [item.to_dict() for item in self.content]
            }

class SystemMessage(BaseMessage):
    """Representa un mensaje del sistema."""

    def role(self) -> str:
        """
        Retorna el rol del mensaje del sistema.

        Returns:
            str: El rol 'system'.
        """
        return "system"

class UserMessage(BaseMessage):
    """Representa un mensaje del usuario."""

    def role(self) -> str:
        """
        Retorna el rol del mensaje del usuario.

        Returns:
            str: El rol 'user'.
        """
        return "user"

class AssistantMessage(BaseMessage):
    """Representa un mensaje del asistente."""

    def role(self) -> str:
        """
        Retorna el rol del mensaje del asistente.

        Returns:
            str: El rol 'assistant'.
        """
        return "assistant"

class PromptTemplate:
    """Clase base para crear plantillas de mensajes."""

    def __init__(self, template: str):
        """
        Inicializa PromptTemplate.

        Args:
            template (str): La cadena de plantilla con marcadores de posición.
        """
        self.template = template
        self.field_names = [fname for _, fname, _, _ in Formatter().parse(template) if fname is not None]
        logger.info(f"PromptTemplate creado con campos: {', '.join(self.field_names)}")

    def __call__(self, *args, **kwargs):
        """
        Rellena la plantilla con los argumentos proporcionados.

        Args:
            *args: Argumentos posicionales para rellenar la plantilla.
            **kwargs: Argumentos de palabras clave para rellenar la plantilla.

        Returns:
            str: La cadena de plantilla rellenada.

        Raises:
            ValueError: Si faltan argumentos requeridos, si se proporcionan argumentos de más,
                        o si se mezclan argumentos posicionales y de palabras clave.
        """
        if args and kwargs:
            logger.error("Se mezclaron argumentos posicionales y de palabras clave")
            raise ValueError("No se pueden mezclar argumentos posicionales y de palabras clave")

        if args:
            if len(args) > len(self.field_names):
                extra_args = len(args) - len(self.field_names)
                logger.error(f"Se proporcionaron {extra_args} argumentos de más")
                raise ValueError(f"Se proporcionaron {extra_args} argumentos de más")
            elif len(args) < len(self.field_names):
                missing_args = ', '.join(self.field_names[len(args):])
                logger.error(f"Faltan los siguientes argumentos: {missing_args}")
                raise ValueError(f"Faltan los siguientes argumentos: {missing_args}")
            return self.template.format(**dict(zip(self.field_names, args)))
        elif kwargs:
            missing_args = [field for field in self.field_names if field not in kwargs]
            if missing_args:
                missing_args_str = ', '.join(missing_args)
                logger.error(f"Faltan los siguientes argumentos: {missing_args_str}")
                raise ValueError(f"Faltan los siguientes argumentos: {missing_args_str}")
            extra_args = [key for key in kwargs if key not in self.field_names]
            if extra_args:
                extra_args_str = ', '.join(extra_args)
                logger.error(f"Se proporcionaron argumentos adicionales que no serán utilizados: {extra_args_str}")
                raise ValueError(f"Sobran los siguientes argumentos: {extra_args_str}")
            return self.template.format(**kwargs)
        else:
            logger.error(f"No se proporcionaron argumentos. Se requieren: {', '.join(self.field_names)}")
            raise ValueError(f"No se proporcionaron argumentos. Se requieren: {', '.join(self.field_names)}")

class SystemTemplate(PromptTemplate):
    """Plantilla para crear mensajes del sistema."""

    def __call__(self, *args, **kwargs):
        """
        Crea un SystemMessage a partir de la plantilla.

        Args:
            *args: Argumentos posicionales para rellenar la plantilla.
            **kwargs: Argumentos de palabras clave para rellenar la plantilla.

        Returns:
            SystemMessage: Un mensaje del sistema con la plantilla rellenada.
        """
        return SystemMessage(super().__call__(*args, **kwargs))

class UserTemplate(PromptTemplate):
    """Plantilla para crear mensajes del usuario."""

    def __call__(self, *args, **kwargs):
        """
        Crea un UserMessage a partir de la plantilla.

        Args:
            *args: Argumentos posicionales para rellenar la plantilla.
            **kwargs: Argumentos de palabras clave para rellenar la plantilla.

        Returns:
            UserMessage: Un mensaje del usuario con la plantilla rellenada.
        """
        return UserMessage(super().__call__(*args, **kwargs))

class AssistantTemplate(PromptTemplate):
    """Plantilla para crear mensajes del asistente."""

    def __call__(self, *args, **kwargs):
        """
        Crea un AssistantMessage a partir de la plantilla.

        Args:
            *args: Argumentos posicionales para rellenar la plantilla.
            **kwargs: Argumentos de palabras clave para rellenar la plantilla.

        Returns:
            AssistantMessage: Un mensaje del asistente con la plantilla rellenada.
        """
        return AssistantMessage(super().__call__(*args, **kwargs))

class History:
    """Clase para manejar el historial de conversación."""

    def __init__(self, conversation: List[Dict], limit: Optional[int] = None):
        """
        Inicializa History.

        Args:
            conversation (List[Dict]): Lista de mensajes de la conversación.
            limit (Optional[int]): Límite opcional de mensajes a mantener.
        """
        self.limit = limit
        self.history = self._filter_and_limit_conversation(conversation)
        self._update_interactions()

    def _filter_and_limit_conversation(self, conversation: List[Dict]) -> List[Dict]:
        """
        Filtra y limita la conversación.

        Args:
            conversation (List[Dict]): Lista de mensajes de la conversación.

        Returns:
            List[Dict]: Lista filtrada y limitada de mensajes.
        """
        # Filtrar mensajes del sistema
        filtered = [msg for msg in conversation if msg['role'] != 'system']
        
        # Aplicar límite si está especificado
        if self.limit is not None:
            # Asegurarse de que mantenemos pares completos de usuario-asistente
            num_pairs_to_keep = min(self.limit, len(filtered) // 2)
            return filtered[-2 * num_pairs_to_keep:]
        
        return filtered

    def _update_interactions(self):
        """Actualiza el número de interacciones en el historial."""
        self.interactions = len(self.history) // 2

    def add_message(self, message: Dict):
        """
        Añade un mensaje al historial.

        Args:
            message (Dict): Mensaje a añadir.
        """
        if message['role'] != 'system':
            self.history.append(message)
            self._update_interactions()

    def get_history(self) -> List[Dict]:
        """
        Obtiene el historial de mensajes.

        Returns:
            List[Dict]: Lista de mensajes en el historial.
        """
        return self.history

    def clear_history(self):
        """Limpia el historial de mensajes."""
        self.history = []
        self.interactions = 0

    def __len__(self):
        """
        Retorna el número de mensajes en el historial.

        Returns:
            int: Número de mensajes en el historial.
        """
        return len(self.history)

    def __iter__(self):
        """
        Permite iterar sobre los mensajes del historial.

        Returns:
            iterator: Iterador sobre los mensajes del historial.
        """
        return iter(self.history)

    def __str__(self):
        """
        Retorna una representación en string del historial.

        Returns:
            str: Representación en string del historial.
        """
        return "\n".join(str(msg) for msg in self.history)

    def __repr__(self):
        """
        Retorna una representación detallada del objeto History.

        Returns:
            str: Representación detallada del objeto History.
        """
        return f"History(messages: {len(self.history)}, interactions: {self.interactions}, initial_limit: {self.limit})"

    def __getitem__(self, index):
        """
        Permite la indexación directa del objeto History.

        Args:
            index: Índice del mensaje a obtener.

        Returns:
            Dict: Mensaje en el índice especificado.
        """
        return self.history[index]

class Message:
    """Clase principal para manejar mensajes y conversaciones."""

    def __init__(self, system_message: Union[SystemMessage, str, History], *args, history_limit: Optional[int] = None):
        """
        Inicializa Message.

        Args:
            system_message (Union[SystemMessage, str, History]): Mensaje del sistema inicial o un objeto History.
            *args: Argumentos adicionales (pueden ser History, List[Dict], o mensajes individuales).
            history_limit (Optional[int]): Límite opcional para el historial de mensajes.
        """
        if isinstance(system_message, History):
            self.system_message = None
            self.history = system_message
        else:
            if isinstance(system_message, str):
                self.system_message = SystemMessage(system_message)
            else:
                self.system_message = system_message

            self.history = History([], limit=history_limit)

            for arg in args:
                if isinstance(arg, History):
                    self.history = History(arg.get_history(), limit=history_limit)
                elif isinstance(arg, list) and all(isinstance(item, dict) for item in arg):
                    self.history = History(arg, limit=history_limit)
                else:
                    self.add_message(arg)

    def add_message(self, message: Union[str, Dict, UserMessage, AssistantMessage]):
        """
        Añade un mensaje a la conversación.

        Args:
            message (Union[str, Dict, UserMessage, AssistantMessage]): Mensaje a añadir.

        Raises:
            ValueError: Si el tipo de mensaje no es soportado.
        """
        if isinstance(message, (UserMessage, AssistantMessage)):
            self.history.add_message(message.to_dict())
        elif isinstance(message, str):
            self.history.add_message(UserMessage(message).to_dict())
        elif isinstance(message, dict):
            self.history.add_message(message)
        else:
            raise ValueError(f"Tipo de mensaje no soportado: {type(message)}")

    def __iter__(self):
        if self.system_message:
            yield self.system_message.to_dict()
        yield from self.history.get_history()


    def __call__(self) -> List[Dict]:
        """
        Retorna la conversación completa.

        Returns:
            List[Dict]: Lista de todos los mensajes en la conversación.
        """
        return self.get_full_conversation()
    
    def __len__(self):
        return len(self.history) + 1 

    def get_full_conversation(self) -> List[Dict]:
        """
        Obtiene la conversación completa, incluyendo el mensaje del sistema si existe.

        Returns:
            List[Dict]: Lista de todos los mensajes en la conversación.
        """
        conversation = []
        if self.system_message:
            conversation.append(self.system_message.to_dict())
        conversation.extend(self.history.get_history())
        return conversation

    def __str__(self):
        """
        Retorna una representación en string de la conversación completa.

        Returns:
            str: Representación en string de la conversación completa.
        """
        return str(self.get_full_conversation())

    def __repr__(self):
        """
        Retorna una representación detallada del objeto Message.

        Returns:
            str: Representación detallada del objeto Message.
        """
        return f"Message(system: {self.system_message}, history: {repr(self.history)})"