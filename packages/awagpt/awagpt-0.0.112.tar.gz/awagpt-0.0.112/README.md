# AwaGPT

**AwaGPT** is a powerful Python library designed by **Awarri Technologies** for developers to interact with advanced localalized language and audio models that have been trained with local Nigerian data. It provides a seamless way to use these **SOTA models** to generate text, stream responses, transcribe audio, and translate text. The translation and Text generative Model has been adapted to work efficiently on the 3 Nigerian languages **(Yoruba, Hausa, Igbo)** and English, but the audio model has only been finetuned on Nigerian accented English.

## Features

1. **Text Generation**  
   Generate coherent and contextually relevant text based on prompts.
   
2. **Text Streaming**  
   Stream responses from the API for real-time interaction.
   
3. **Audio Transcription**  
   Convert audio files or base64-encoded audio data into text.
   
4. **Text Translation**  
   Translate text between different languages with ease.

---

## Installation

Install the package via pip:

```bash
pip install awagpt
```

---

## Usage

### 1. **Initialization**

To use AwaGPT, you need to initialize it with an API key. You can also configure the optional parameters.

```python
from awagpt import AwaGPT

awagpt = AwaGPT(
    api_key="your_api_key_here", 
    chat_interface=True,        # Optional: Enable chat interface (default: False)
    system_instruction="Provide concise answers"  # Optional system instruction
)
```

### 2. **Generate Text**

Generate text based on a prompt:

```python
response = awagpt.generate_text(prompt="Explain the theory of relativity.")
print(response)
```

### 3. **Stream Text**

Stream text for real-time updates:

```python
for chunk in awagpt.stream_text(prompt="Tell me a story about AI in healthcare."):
    print(chunk, end="")
```

### 4. **Transcribe Audio**

Transcribe audio from a base64 string or a file path:

```python
# Using a file path
transcription = awagpt.transcribe_audio("path/to/audio.mp3")
print(transcription)

# Using base64 data
transcription = awagpt.transcribe_audio("data:audio/wav;base64,...")
print(transcription)
```

### 5. **Translate Text**

Translate text from one language to another:

```python
translated_text = awagpt.translate_text(
    base_lang="en", 
    target_lang="fr", 
    text_to_translate="Hello, how are you?"
)
print(translated_text)  # Output: Bonjour, comment ça va?
```

---

## Methods

### `generate_text(prompt: str) -> str`
Generates text based on the provided prompt.

- **Args**:
  - `prompt` (str): Input prompt.
  
- **Returns**: 
  - Generated text (str).

### `stream_text(prompt: str) -> Iterator[str]`
Streams text chunks based on the provided prompt.

- **Args**:
  - `prompt` (str): Input prompt.
  
- **Yields**: 
  - Text chunks (str).

### `transcribe_audio(data: Union[str, bytes]) -> str`
Transcribes audio input.

- **Args**:
  - `data` (str): File path or base64-encoded audio data.
  
- **Returns**:
  - Transcribed text (str).

### `translate_text(base_lang: str, target_lang: str, text_to_translate: str) -> str`
Translates text between specified languages.

- **Args**:
  - `base_lang` (str): Source language code.
  - `target_lang` (str): Target language code.
  - `text_to_translate` (str): Text to be translated.
  
- **Returns**:
  - Translated text (str).

---

## Error Handling

AwaGPT includes robust error handling to ensure a smooth experience:

- **ValueError**: Raised when required parameters are missing or inputs are invalid.
- **HTTPError**: Raised for HTTP-related issues, such as bad responses or connectivity problems.
- **RequestException**: Captures any other request-related errors.

---

## Requirements

- Python 3.7+
- Dependencies:
  - `requests`

Install dependencies automatically during package installation.

---

## Contributing

We welcome contributions! Please follow the steps below:

1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request with detailed information on your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Contact

For questions or support, please reach out at [support@awagpt.com](mailto:info@awagpt.com).

Happy coding! 🚀