# ai_agent_word
# Voice-Controlled AI Word Assistant

A desktop-based AI-powered assistant that allows users to control **Microsoft Word** using **voice commands**. Users can dictate text, format documents, manage content, and generate AI-powered text seamlessly.

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Architecture](#architecture)  
7. [Models Used](#models-used)  
8. [Challenges](#challenges)  
9. [Future Improvements](#future-improvements)  
10. [License](#license)  

---

## Project Overview
This project leverages **speech recognition**, **semantic embeddings**, and **AI text generation** to allow hands-free interaction with Microsoft Word. It improves productivity by enabling users to perform actions via voice commands rather than manual input.

Key objectives:  
- Dictate text in Word.  
- Apply formatting (bold, italic, underline, alignment).  
- Generate text using AI on specific topics.  
- Undo/redo actions and delete words, lines, or paragraphs.  

---

## Features
- Real-time speech-to-text using Hugging Face ASR models.  
- Semantic command matching for flexible voice commands.  
- AI-powered text generation using Google Gemini API.  
- Word document management (new, save, close).  
- Text formatting (bold, italic, underline, alignment).  
- Undo last action, delete last word/line/paragraph.  
- Page border addition, bullet points, font resizing.  
- Continuous listening and fallback to free dictation.  

---

## Tech Stack

| Component             | Technology/Library                     | Purpose                                      |
|-----------------------|---------------------------------------|----------------------------------------------|
| Speech Recognition    | Hugging Face Transformers (ASR)       | Convert spoken words into text.             |
| Semantic Matching     | sentence-transformers                  | Encode commands and match input.            |
| AI Text Generation    | Google Gemini API                      | Generate text on specified topics.          |
| Document Control      | win32com.client, python-docx           | Interface with Microsoft Word.              |
| Audio Input           | sounddevice                             | Capture real-time microphone audio.         |
| Python Environment    | venv                                   | Isolated environment for dependencies.      |
| Optional GPU          | NVIDIA RTX 3050 + PyTorch CUDA         | Accelerate ASR model inference.            |

---

## Installation

1. Clone the repository:  
```bash
git clone <repository_url>
cd agent
````

2. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. Upgrade pip:

```bash
pip install --upgrade pip
```

4. Install dependencies (adjust versions based on your Python):

```bash
pip install -r requirements.txt
```

5. Optional: Install GPU-enabled PyTorch for faster ASR inference:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

## Usage

1. Launch the assistant:

```bash
python main.py
```

2. Available commands:

* `write text` → Dictate free-form text.
* `bold`, `italic`, `underline` → Apply formatting.
* `align left/right/center/justify` → Paragraph alignment.
* `generate text` → AI-generated paragraph for a topic.
* `new document`, `save document`, `close document`.
* `delete last word/line/paragraph`.
* `undo` → Undo last action.
* `exit` → Stop the assistant.

3. The assistant will continuously listen to your voice input. If the spoken input does not match a command, it will default to free dictation (text insertion).

---

## Architecture

```
Audio Input → Hugging Face ASR → Preprocessed Text → Semantic Matching → Command Mapping → Word API → Output
Fallback: Free-text dictation if no command matched
```

---

## Models Used

| Task                | Model                        | Library                   | Purpose                                |
| ------------------- | ---------------------------- | ------------------------- | -------------------------------------- |
| ASR                 | facebook/wav2vec2-large-960h | Hugging Face Transformers | Speech-to-text conversion              |
| Semantic Embeddings | all-MiniLM-L6-v2             | Sentence-Transformers     | Encode commands & input for similarity |
| Text Generation     | Google Gemini API            | genai Client              | Generate text for topics               |

---

## Challenges

* Accuracy of ASR in noisy environments.
* Latency in AI text generation.
* Command misclassification.
* Dependency on Microsoft Word (Windows-only).
* GPU availability impacts real-time performance.
* Library version conflicts (sounddevice, numpy, python-docx).

---

## Future Improvements

* Fine-tune ASR for domain-specific vocabulary.
* Multilingual support.
* Cross-platform compatibility.
* Enhanced NLP features (summarization, translation, QA).
* Customizable voice commands.
* Real-time streaming and continuous inference.
* Optimize embeddings with FAISS for larger command sets.
* Batch processing for faster AI generation.

---

## License

This project is licensed under the MIT License.

---

### Author

Sachin Kumar
Divyansh Gupta
