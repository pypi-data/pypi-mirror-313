####################################################
# Importaciones y configuraciones centralizadas
####################################################

import os
from openai import OpenAI as OpenAIClient
from openai import AsyncOpenAI as AsyncOpenAIClient
from pydantic import BaseModel
from aimanagertoolkit import Log
from dotenv import load_dotenv
import numpy as np
import aiofiles

logger = Log(__name__)

# Carga las variables de entorno desde un archivo .env
load_dotenv(override=True)

####################################################
# Clase OpenAI Toolkit (Versión Síncrona)
####################################################

class OpenAI:
    def __init__(self, 
                 model=None, 
                 embeddings_model=None,
                 api_key=None, 
                 temperature=None, 
                 max_tokens=None,
                 response_format=None,
                 tools=None,
                 tool_choice=None,
                 ):
        """
        Inicializa una instancia de OpenAiToolkit para manejar interacciones con OpenAI.

        Parámetros:
        - model (str): El modelo de OpenAI a utilizar. Si no se especifica, se obtiene de la variable de entorno 'OPENAI_MODEL'.
        - api_key (str): La clave API para autenticar las solicitudes a OpenAI. Si no se especifica, se obtiene de la variable de entorno 'OPENAI_API_KEY'.
        - temperature (float): Parámetro que controla la aleatoriedad de las respuestas. Valores más bajos dan respuestas más conservadoras.
        - max_tokens (int): El número máximo de tokens a generar en la respuesta.
        - response_format (str): Formato de la respuesta (puede ser 'json', 'json_schema', 'text', etc.).
        - tools (list): Herramientas adicionales que se pueden usar en el proceso.
        - tool_choice (str): La herramienta seleccionada para esta solicitud específica.
        """
        self.model = model or os.getenv("OPENAI_MODEL")
        self.embeddings_model = embeddings_model or os.getenv("OPENAI_EMBEDDINGS_MODEL") or "text-embedding-3-small"
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAIClient(
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        self.async_client = AsyncOpenAIClient(
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        self.response_format = response_format
        self.tools = tools
        self.tool_choice = tool_choice

    ####################################################
    # Chat Sincrónico (Respuesta Completa)
    ####################################################
    
    def chat(self,
             messages,
             temperature=None,
             tools=None,
             response_format=None):
        """
        Crea completaciones de chat utilizando la API de OpenAI con parámetros opcionales especificados durante la inicialización.

        Args:
            messages (list of dict): Una lista de diccionarios que representan el historial de conversación.
            temperature (float, opcional): Controla la aleatoriedad de las respuestas. Si no se especifica, se utiliza la temperatura definida en la inicialización.
            tools (list, opcional): Una lista de herramientas a utilizar en la llamada a la API. Si no se especifica, se utilizan las herramientas definidas en la inicialización.
            response_format (dict, opcional): El formato de la respuesta. Si se proporciona, este formato será utilizado. Si no se especifica, se utiliza el formato definido en la inicialización. Puede ser None.

        Returns:
            dict: La respuesta de la API de OpenAI que contiene la completación del chat. Devuelve None en caso de error.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens,
                response_format=response_format or self.response_format,
                stream=False,
                tools=tools or self.tools,
                tool_choice=self.tool_choice if (tools or self.tools) else None,
            )
            return response
        except Exception as e:
            logger.error(f"Ocurrió un error: {e}")
            return None

    ####################################################
    # Chat Sincrónico (Streaming)
    ####################################################

    def stream(self,
                messages,
                temperature=None,
                tools=None,
                response_format=None):
        """
        Crea completaciones de chat utilizando la API de OpenAI con respuesta por streaming.

        Args:
            messages (list of dict): Una lista de diccionarios que representan el historial de conversación.
            temperature (float, opcional): Controla la aleatoriedad de las respuestas. Si no se especifica, se utiliza la temperatura definida en la inicialización.
            tools (list, opcional): Una lista de herramientas a utilizar en la llamada a la API. Si no se especifica, se utilizan las herramientas definidas en la inicialización.
            response_format (dict, opcional): El formato de la respuesta. Si se proporciona, este formato será utilizado. Si no se especifica, se utiliza el formato definido en la inicialización. Puede ser None.

        Returns:
            None: Imprime las respuestas de la API de OpenAI a medida que se reciben.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens,
                response_format=response_format or self.response_format,
                stream=True,
                tools=tools or self.tools,
                tool_choice=self.tool_choice if (tools or self.tools) else None,
            )

            for chunk in response:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="")

        except Exception as e:
            logger.error(f"Ocurrió un error: {e}")
            return None

    ####################################################
    # Chat Sincrónico (Formato Estructurado)
    ####################################################
    
    def str_output(self, 
                   messages, 
                   response_format, 
                   temperature=None,
                   tools=None
            ):
        """
        Crea completaciones de chat utilizando la API de OpenAI con salida estructurada según un JSON Schema.

        Args:
            messages (list of dict): Una lista de diccionarios que representan el historial de conversación.
            response_format (BaseModel): Un esquema de Pydantic que define la estructura esperada de la respuesta.
            temperature (float, opcional): Controla la aleatoriedad de las respuestas. Si no se especifica, se utiliza la temperatura definida en la inicialización.

        Returns:
            dict: La respuesta de la API de OpenAI que contiene la completación del chat estructurada según el esquema proporcionado.
        """
        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                response_format=response_format,
            )
            return completion
        except Exception as e:
            logger.error(f"Ocurrió un error al generar una salida estructurada: {e}")
            return None

    ####################################################
    # Embeddings
    ####################################################

    def embeddings(self,
                   input: str,
                   model: str = None,
                   ):
        """
        Genera representaciones vectoriales (embeddings) de texto utilizando la API de OpenAI.

        Args:
            input (str): El texto de entrada para el cual se quieren generar los embeddings.
            model (str, opcional): El modelo de embeddings a utilizar. Puede ser uno de los siguientes:
                - 'text-embedding-3-small' (por defecto)
                - 'text-embedding-ada-002' 
                - 'text-embedding-3-large'

        Returns:
            dict: La respuesta de la API de OpenAI que contiene los embeddings generados para el texto de entrada.
                Devuelve None en caso de error.
        """
        try:
            input = input.replace("\n", " ") # Elimina saltos de línea del texto de entrada para evitar errores
            response = self.client.embeddings.create(
                input=input,
                model=model or self.embeddings_model,
            )
            return response
        except Exception as e:
            logger.error(f"Ocurrió un error al generar los embeddings: {e}")
            return None

    def cosine_similarity(self, 
                          a: list, 
                          b: list,
                          ):
        """
        Calcula la similitud coseno entre dos vectores.

        La similitud coseno es una métrica utilizada para medir cuán similares son dos vectores en un espacio de alta dimensionalidad. 
        Se utiliza comúnmente en tareas de procesamiento de lenguaje natural (NLP) y aprendizaje automático, especialmente para comparar embeddings de texto.

        La fórmula para la similitud coseno es:
        
            similitud_coseno = (a · b) / (||a|| * ||b||)

        donde "a · b" es el producto punto entre los dos vectores, y ||a|| y ||b|| son las magnitudes (normas) de los vectores.

        Args:
            a (np.ndarray): El primer vector (como array de numpy).
            b (np.ndarray): El segundo vector (como array de numpy).

        Returns:
            float: Un valor entre -1 y 1 que representa la similitud coseno entre los dos vectores. Un valor cercano a 1 indica alta similitud, 
            mientras que un valor cercano a -1 indica alta disimilitud.

        Ejemplo:
            >>> vector_a = np.array([1, 2, 3])
            >>> vector_b = np.array([4, 5, 6])
            >>> cosine_similarity(vector_a, vector_b)
            0.9746318461970762
        """
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    ####################################################
    # Speech to Text - STT
    ####################################################

    def transcribe(self,
                   file_path,
                   model="whisper-1", 
                   response_format="text", 
                   language=None, 
                   temperature=None,
                   timestamp_granularities=None,
                   ):
        """
        Transcribe un archivo de audio utilizando la API de OpenAI.

        Args:
            file_path (str): Ruta al archivo de audio a transcribir.
            model (str, opcional): Modelo a utilizar para la transcripción. Por defecto es "whisper-1".
            response_format (str, opcional): Formato de la respuesta ("json", "text", "srt", "verbose_json", "vtt"). Por defecto es "json".
            language (str, opcional): Código de idioma ISO-639-1 del idioma de entrada. Si no se especifica, se detectará automáticamente ("sp" - Spanish). 
            temperature (float, opcional): Temperatura de muestreo para la generación de tokens. Valores más altos aumentan la creatividad.
            timestamp_granularities (list, opcional): Lista de granularidades de marca de tiempo ("segment", "word").

        Returns:
            dict or str: La transcripción del audio en el formato especificado.
        """
        try:
            with open(file_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                    response_format=response_format,
                    language=language,
                    temperature=temperature or self.temperature,
                    timestamp_granularities=timestamp_granularities
                )
            return transcription
        except Exception as e:
            logger.error(f"Ocurrió un error durante la transcripción: {e}")
            return None

    def translate(self,
                  file_path, 
                  model="whisper-1", 
                  response_format="json", 
                  temperature=None,
                  timestamp_granularities=None,
                  ):
        """
        Traduce y transcribe un archivo de audio a inglés utilizando la API de OpenAI.

        Args:
            file_path (str): Ruta al archivo de audio a traducir.
            model (str, opcional): Modelo a utilizar para la traducción. Por defecto es "whisper-1".
            response_format (str, opcional): Formato de la respuesta ("json", "text", "srt", "verbose_json", "vtt"). Por defecto es "json".
            temperature (float, opcional): Temperatura de muestreo para la generación de tokens. Valores más altos aumentan la creatividad.
            timestamp_granularities (list, opcional): Lista de granularidades de marca de tiempo ("segment", "word").

        Returns:
            dict or str: La traducción del audio a texto en inglés en el formato especificado.
        """
        try:
            with open(file_path, "rb") as audio_file:
                translation = self.client.audio.translations.create(
                    model=model,
                    file=audio_file,
                    response_format=response_format,
                    temperature=temperature or self.temperature,
                    timestamp_granularities=timestamp_granularities
                )
            return translation
        except Exception as e:
            logger.error(f"Ocurrió un error durante la traducción: {e}")
            return None
        
    ####################################################
    # Text to Speech - TTS
    ####################################################

    def speech(self, 
                       text, 
                       output_file_path="output.mp3", 
                       model="tts-1", 
                       voice="alloy", 
                       response_format="mp3",
                       speed=1.0):
        """
        Genera audio hablado a partir de texto utilizando la API de OpenAI.

        Args:
            text (str): El texto que se convertirá en audio.
            output_file_path (str): Ruta del archivo donde se guardará el audio generado.
            model (str, opcional): Modelo a utilizar para la generación de voz. Opciones: "tts-1" (estándar) o "tts-1-hd" (alta definición). Por defecto es "tts-1".
            voice (str, opcional): Voz a utilizar. Opciones: "alloy", "echo", "fable", "onyx", "nova", "shimmer". Por defecto es "alloy".
            response_format (str, opcional): Formato del archivo de audio de salida. Opciones: "mp3", "opus", "aac", "flac", "pcm". Por defecto es "mp3".
            speed (float, opcional): Velocidad de la voz. Rango de 0.25 a 4.0. Por defecto es 1.0.

        Returns:
            bool: True si la generación y guardado del audio fue exitosa, False en caso contrario.
        """
        try:
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                response_format=response_format,
                speed=speed
            )

            # Guardar el audio en un archivo
            with open(output_file_path, 'wb') as audio_file:
                for chunk in response.iter_bytes():
                    audio_file.write(chunk)

            logger.info(f"Audio generado y guardado exitosamente en {output_file_path}")
            return

        except Exception as e:
            logger.error(f"Ocurrió un error durante la generación de audio: {e}")
            return

####################################################
# Clase AsyncOpenAI Toolkit (Versión Asíncrona)
####################################################

class AsyncOpenAI:
    def __init__(self, 
                 model=None, 
                 embeddings_model=None,
                 api_key=None, 
                 temperature=None, 
                 max_tokens=None,
                 response_format=None,
                 tools=None,
                 tool_choice=None,
                 ):
        """
        Inicializa una instancia asíncrona de OpenAiToolkit para manejar interacciones con OpenAI.

        Parámetros:
        - model (str): El modelo de OpenAI a utilizar. Si no se especifica, se obtiene de la variable de entorno 'OPENAI_MODEL'.
        - api_key (str): La clave API para autenticar las solicitudes a OpenAI. Si no se especifica, se obtiene de la variable de entorno 'OPENAI_API_KEY'.
        - temperature (float): Parámetro que controla la aleatoriedad de las respuestas. Valores más bajos dan respuestas más conservadoras.
        - max_tokens (int): El número máximo de tokens a generar en la respuesta.
        - response_format (str): Formato de la respuesta (puede ser 'json', 'json_schema', 'text', etc.).
        - tools (list): Herramientas adicionales que se pueden usar en el proceso.
        - tool_choice (str): La herramienta seleccionada para esta solicitud específica.
        """
        self.model = model or os.getenv("OPENAI_MODEL")
        self.embeddings_model = embeddings_model or os.getenv("OPENAI_EMBEDDINGS_MODEL") or "text-embedding-3-small"
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = AsyncOpenAIClient(
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        self.response_format = response_format
        self.tools = tools
        self.tool_choice = tool_choice

    ####################################################
    # Chat Asíncrono (Respuesta Completa)
    ####################################################
    
    async def chat(self,
                  messages,
                  temperature=None,
                  tools=None,
                  response_format=None):
        """
        Crea completaciones de chat de forma asíncrona utilizando la API de OpenAI.

        Args:
            messages (list of dict): Una lista de diccionarios que representan el historial de conversación.
            temperature (float, opcional): Controla la aleatoriedad de las respuestas.
            tools (list, opcional): Una lista de herramientas a utilizar en la llamada a la API.
            response_format (dict, opcional): El formato de la respuesta.

        Returns:
            dict: La respuesta de la API de OpenAI que contiene la completación del chat.
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens,
                response_format=response_format or self.response_format,
                stream=False,
                tools=tools or self.tools,
                tool_choice=self.tool_choice if (tools or self.tools) else None,
            )
            return response
        except Exception as e:
            logger.error(f"Ocurrió un error: {e}")
            return None

    ####################################################
    # Chat Asíncrono (Streaming)
    ####################################################

    async def stream(self,
                    messages,
                    temperature=None,
                    tools=None,
                    response_format=None):
        """
        Crea completaciones de chat de forma asíncrona utilizando la API de OpenAI con respuesta por streaming.

        Args:
            messages (list of dict): Una lista de diccionarios que representan el historial de conversación.
            temperature (float, opcional): Controla la aleatoriedad de las respuestas.
            tools (list, opcional): Una lista de herramientas a utilizar en la llamada a la API.
            response_format (dict, opcional): El formato de la respuesta.

        Returns:
            None: Imprime las respuestas de la API de OpenAI a medida que se reciben.
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens,
                response_format=response_format or self.response_format,
                stream=True,
                tools=tools or self.tools,
                tool_choice=self.tool_choice if (tools or self.tools) else None,
            )

            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="")

        except Exception as e:
            logger.error(f"Ocurrió un error: {e}")
            return None

    ####################################################
    # Chat Asíncrono (Formato Estructurado)
    ####################################################
    
    async def str_output(self, 
                        messages, 
                        response_format, 
                        temperature=None,
                        tools=None
                ):
        """
        Crea completaciones de chat de forma asíncrona con salida estructurada según un JSON Schema.

        Args:
            messages (list of dict): Una lista de diccionarios que representan el historial de conversación.
            response_format (BaseModel): Un esquema de Pydantic que define la estructura esperada de la respuesta.
            temperature (float, opcional): Controla la aleatoriedad de las respuestas.

        Returns:
            dict: La respuesta estructurada según el esquema proporcionado.
        """
        try:
            completion = await self.client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                response_format=response_format,
            )
            return completion
        except Exception as e:
            logger.error(f"Ocurrió un error al generar una salida estructurada: {e}")
            return None

    ####################################################
    # Embeddings Asíncronos
    ####################################################

    async def embeddings(self,
                        input: str,
                        model: str = None,
                        ):
        """
        Genera representaciones vectoriales (embeddings) de texto de forma asíncrona.

        Args:
            input (str): El texto de entrada para el cual se quieren generar los embeddings.
            model (str, opcional): El modelo de embeddings a utilizar.

        Returns:
            dict: La respuesta que contiene los embeddings generados.
        """
        try:
            input = input.replace("\n", " ")
            response = await self.client.embeddings.create(
                input=input,
                model=model or self.embeddings_model,
            )
            return response
        except Exception as e:
            logger.error(f"Ocurrió un error al generar los embeddings: {e}")
            return None

    def cosine_similarity(self, 
                         a: list, 
                         b: list,
                         ):
        """
        Calcula la similitud coseno entre dos vectores.
        
        Args:
            a (np.ndarray): El primer vector.
            b (np.ndarray): El segundo vector.

        Returns:
            float: Valor entre -1 y 1 que representa la similitud coseno.
        """
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    ####################################################
    # Speech to Text - STT Asíncrono
    ####################################################

    async def transcribe(self,
                        file_path,
                        model="whisper-1", 
                        response_format="text", 
                        language=None, 
                        temperature=None,
                        timestamp_granularities=None,
                        ):
        """
        Transcribe un archivo de audio de forma asíncrona.

        Args:
            file_path (str): Ruta al archivo de audio a transcribir.
            model (str, opcional): Modelo a utilizar para la transcripción.
            response_format (str, opcional): Formato de la respuesta.
            language (str, opcional): Código de idioma ISO-639-1.
            temperature (float, opcional): Temperatura de muestreo.
            timestamp_granularities (list, opcional): Lista de granularidades de marca de tiempo.

        Returns:
            dict or str: La transcripción del audio.
        """
        try:
            with open(file_path, "rb") as audio_file:
                transcription = await self.client.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                    response_format=response_format,
                    language=language,
                    temperature=temperature or self.temperature,
                    timestamp_granularities=timestamp_granularities
                )
            return transcription
        except Exception as e:
            logger.error(f"Ocurrió un error durante la transcripción: {e}")
            return None

    async def translate(self,
                       file_path, 
                       model="whisper-1", 
                       response_format="json", 
                       temperature=None,
                       timestamp_granularities=None,
                       ):
        """
        Traduce y transcribe un archivo de audio a inglés de forma asíncrona.

        Args:
            file_path (str): Ruta al archivo de audio a traducir.
            model (str, opcional): Modelo a utilizar para la traducción.
            response_format (str, opcional): Formato de la respuesta.
            temperature (float, opcional): Temperatura de muestreo.
            timestamp_granularities (list, opcional): Lista de granularidades de marca de tiempo.

        Returns:
            dict or str: La traducción del audio a texto en inglés.
        """
        try:
            with open(file_path, "rb") as audio_file:
                translation = await self.client.audio.translations.create(
                    model=model,
                    file=audio_file,
                    response_format=response_format,
                    temperature=temperature or self.temperature,
                    timestamp_granularities=timestamp_granularities
                )
            return translation
        except Exception as e:
            logger.error(f"Ocurrió un error durante la traducción: {e}")
            return None
        
    ####################################################
    # Text to Speech - TTS Asíncrono
    ####################################################

    async def speech(self, 
                    text, 
                    output_file_path="output.mp3", 
                    model="tts-1", 
                    voice="alloy", 
                    response_format="mp3",
                    speed=1.0):
        """
        Genera audio hablado a partir de texto de forma asíncrona.

        Args:
            text (str): El texto que se convertirá en audio.
            output_file_path (str): Ruta del archivo donde se guardará el audio.
            model (str, opcional): Modelo a utilizar para la generación de voz.
            voice (str, opcional): Voz a utilizar.
            response_format (str, opcional): Formato del archivo de audio de salida.
            speed (float, opcional): Velocidad de la voz.

        Returns:
            bool: True si la generación fue exitosa, False en caso contrario.
        """
        try:
            response = await self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                response_format=response_format,
                speed=speed
            )

            # Guardar el audio en un archivo de forma asíncrona
            async with aiofiles.open(output_file_path, 'wb') as audio_file:
                async for chunk in response.iter_bytes():
                    await audio_file.write(chunk)

            logger.info(f"Audio generado y guardado exitosamente en {output_file_path}")
            return True

        except Exception as e:
            logger.error(f"Ocurrió un error durante la generación de audio: {e}")
            return False

####################################################
# Documentación Adicional Basada en la API Oficial
####################################################

# Parámetros adicionales opcionales:
# - frequency_penalty (float, opcional): Penaliza tokens nuevos basados en su frecuencia en el texto hasta el momento. Rango: -2.0 a 2.0.
# - loggerit_bias (dict, opcional): Modifica la probabilidad de que aparezcan tokens específicos en la respuesta.
# - loggerprobs (bool, opcional): Si es True, retorna las probabilidades loggerarítmicas de los tokens generados.
# - presence_penalty (float, opcional): Penaliza tokens nuevos según si ya aparecieron en el texto, aumentando la probabilidad de que el modelo hable sobre nuevos temas.
# - stop (str/list, opcional): Hasta 4 secuencias donde la API dejará de generar tokens adicionales.
# - stream_options (dict, opcional): Opciones adicionales para la transmisión de la respuesta.
# - top_p (float, opcional): Realiza una "nucleus sampling" considerando solo tokens que sumen el `top_p`% de probabilidad total.
# - n (int, opcional): Número de completaciones de chat a generar por cada mensaje de entrada.
# - seed (int, opcional): Especifica una semilla para hacer esfuerzos por reproducir resultados de manera determinista.
# - service_tier (str, opcional): Especifica el nivel de latencia del servicio para procesar la solicitud.

# Formato de respuesta:
# - response_format (dict, opcional): Se puede especificar un formato como `json_object` o `json_schema` para garantizar que la respuesta del modelo coincida con un esquema JSON definido.