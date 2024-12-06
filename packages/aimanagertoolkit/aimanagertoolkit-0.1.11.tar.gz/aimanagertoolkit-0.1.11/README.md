# AiManagerToolkit 🤖

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-✔️-blue)

`AiManagerToolkit` es una librería Python diseñada para simplificar la interacción con la API de Azure OpenAI. Esta herramienta proporciona una forma flexible y eficiente de gestionar conversaciones con modelos de lenguaje, integrar herramientas personalizadas, generar respuestas estructuradas, y manejar funcionalidades de voz y texto, ideal para desarrolladores que buscan aprovechar la potencia de la inteligencia artificial en sus aplicaciones.

## Características ✨

- **Soporte para Azure OpenAI:** Fácil integración con la plataforma de Azure.
- **Herramientas Personalizadas:** Define y registra herramientas para mejorar las interacciones con el modelo.
- **Salidas Estructuradas:** Genera respuestas en formato JSON basadas en esquemas definidos.
- **Chat Sincrónico y Streaming:** Manejo de conversaciones tanto en modo sincrónico como en streaming.
- **Embeddings:** Generación y manejo de embeddings de texto.
- **Speech to Text (STT):** Transcripción y traducción de audio a texto.
- **Text to Speech (TTS):** Generación de audio a partir de texto.
- **Logging Configurable:** Sistema de logging integrado para monitorear y depurar las interacciones.
- **Manejo Avanzado de Mensajes:** Nueva clase Message para una gestión eficiente de conversaciones y tipos de contenido.

## Instalación 🚀

Puedes instalar `AiManagerToolkit` desde PyPI utilizando pip:

```bash
pip install AiManagerToolkit
```

## Uso Básico 💻

### 1. Configuración Inicial 🛠️

Configura la conexión a la API de Azure OpenAI utilizando variables de entorno o parámetros en el código.

#### Configuración utilizando `.env` 🌐

Crea un archivo `.env` en el directorio raíz de tu proyecto con las credenciales necesarias:

```env
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_ENDPOINT=https://tu-endpoint.azure.com/
AZURE_OPENAI_API_KEY=tu-clave-api
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_EMBEDDINGS_MODEL=text-embedding-3-small
```

#### Configuración en el Código 🔧

Puedes pasar la configuración directamente en tu código:

```python
from aimanagertoolkit.ai import AzureAI, OpenAI

# Para Azure OpenAI
azure_ai = AzureAI(
    model="gpt-4o",
    azure_endpoint="https://tu-endpoint.azure.com/",
    api_key="tu-clave-api",
    temperature=0.7
)

# Para OpenAI
openai_ai = OpenAI(
    api_key="tu-clave-api-openai",
    model="gpt-4",
    temperature=0.7
)
```

### 2. Ejemplo de Uso de Chat 🔄

```python
from aimanagertoolkit.ai import AzureAI
from aimanagertoolkit.messages import AzureAI

azure_ai = AzureAI()

conversation = Message("Eres un asistente útil.")
conversation.add_message(UserMessage("¿Cuál es el estado de mi pedido?"))

response = azure_ai.chat(conversation)
print(response.choices[0].message.content)
```

### 3. Generación de Embeddings 📊

```python
embedding = azure_ai.embeddings("Texto para generar embedding")
print(embedding.data[0].embedding)
```

### 4. Transcripción de Audio 🎙️

```python
transcription = azure_ai.transcribe("ruta/al/archivo/audio.mp3")
print(transcription)
```

### 5. Generación de Voz 🔊

```python
azure_ai.speech("Texto para convertir en voz", output_file_path="salida.mp3")
```

### 6. Cálculo de Similitud Coseno 📐

```python
vector1 = [1, 2, 3]
vector2 = [4, 5, 6]
similarity = azure_ai.cosine_similarity(vector1, vector2)
print(f"Similitud coseno: {similarity}")
```

### 7. Manejo Avanzado de Mensajes 💬

```python
from AiManagerToolkit import Message, SystemMessage, UserMessage

# Iniciar una conversación
conversation = Message(SystemMessage("Eres un asistente útil."))

# Añadir mensajes a la conversación
conversation.add_message(UserMessage("Hola, ¿cómo estás?"))
conversation.add_message("¿Puedes ayudarme con una tarea?")

# Obtener la conversación completa
full_conversation = conversation.get_full_conversation()
```


## Contribuciones 👥

¡Las contribuciones son bienvenidas! Si deseas contribuir al proyecto, sigue estos pasos:

1. Realiza un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/mi-nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/mi-nueva-funcionalidad`).
5. Crea un nuevo Pull Request.

## Roadmap 🛤️

- [ ] Mejoras en la documentación con ejemplos avanzados.
- [ ] Añadir más tests unitarios y de integración.
- [ ] Soporte para operaciones avanzadas con Azure OpenAI.
- [ ] Integración con más servicios de Azure AI.

## Licencia 📄

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

---

¡Gracias por usar `AiManagerToolkit`! Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue en el repositorio. 😊