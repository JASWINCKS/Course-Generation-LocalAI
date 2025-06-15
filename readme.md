# 🎓 AI Course Generator

Transform videos into comprehensive course modules using local AI models. This application processes video content, transcribes it, and generates structured course materials with quizzes, all running locally on your machine.

## ✨ Features

- **Video Processing**
  - YouTube URL support
  - Local video file support
  - Automatic audio extraction
  - High-quality video processing

- **AI-Powered Transcription**
  - Powered by OpenAI Whisper
  - Multiple model size options
  - Accurate speech-to-text conversion
  - Automatic language detection

- **Local LLM Integration**
  - Ollama support
  - LM Studio support
  - Automatic model detection
  - Multiple model options

- **Course Generation**
  - Structured content organization
  - Learning objectives
  - Section summaries
  - Multiple-choice quizzes
  - Interactive content

- **Export Options**
  - PDF export
  - DOCX export
  - Customizable formatting
  - Professional layout

## 🛠️ Technical Stack

| Component        | Technologies Used                                    |
|------------------|-----------------------------------------------------|
| Video Processing | `ffmpeg`, `moviepy`                                 |
| Transcription    | `openai-whisper`                                    |
| LLM Integration  | Ollama / LM Studio                                  |
| Export           | `python-docx`, `pdfkit`                             |
| UI Framework     | Streamlit                                           |

## 📁 Project Structure

```
course-generator/
├── app.py                 # Main Streamlit application
├── course_generator/      # Core functionality modules
│   ├── __init__.py
│   ├── config.py         # Configuration management
│   ├── course_generator.py # Course content generation
│   ├── exporter.py       # PDF and DOCX export
│   ├── local_llm.py      # Local LLM integration
│   ├── model_detector.py # LLM model detection
│   ├── transcriber.py    # Audio transcription
│   └── video_processor.py # Video processing
├── output/               # Generated course materials
├── temp/                # Temporary processing files
└── requirements.txt     # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system
- Either Ollama or LM Studio running locally

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd course-generator
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg**
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)
   - Linux: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`

### Setting Up LLM Hosts

#### Option 1: Ollama
1. Install from [ollama.ai](https://ollama.ai)
2. Start server: `ollama serve`
3. Pull model: `ollama pull mistral`

#### Option 2: LM Studio
1. Download from [lmstudio.ai](https://lmstudio.ai)
2. Download Mistral-7B-Instruct model
3. Enable API server

## 💻 Usage

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Access the UI**
   - Open `http://localhost:8501` in your browser

3. **Process a Video**
   - Choose input type (YouTube URL or video file)
   - Select processing options
   - Click "Generate Course"

## ⚡ Performance Considerations

### Video Processing
- Recommended length: 10-30 minutes
- Optimal resolution: 720p or 1080p
- Supported formats: MP4, AVI, MOV

### Model Selection
- **Whisper Models**
  - tiny: Fast, basic accuracy
  - base: Balanced performance
  - small: Recommended default
  - medium: Higher accuracy
  - large: Best accuracy

- **LLM Models**
  - Mistral 7B: Best overall
  - Llama 2 7B: Good alternative
  - Phi-2: Lightweight option

### Hardware Requirements
- **Minimum**
  - CPU: 8+ cores
  - RAM: 16GB
  - Storage: 10GB free space

- **Recommended**
  - GPU: NVIDIA 8GB+ VRAM
  - RAM: 32GB
  - Storage: 20GB+ free space

### Processing Times
| Video Length | CPU Only    | With GPU    |
|-------------|-------------|-------------|
| 10 minutes  | 15-30 min   | 5-10 min    |
| 30 minutes  | 45-90 min   | 15-30 min   |

## 🔧 Troubleshooting

### Common Issues

1. **FFmpeg Not Found**
   - Verify installation
   - Check system PATH
   - Restart application

2. **LLM Host Unavailable**
   - Check service status
   - Verify API endpoints
   - Check firewall settings

3. **Slow Processing**
   - Reduce video quality
   - Use smaller models
   - Enable GPU acceleration
   - Close other applications

4. **Memory Issues**
   - Use smaller models
   - Process shorter videos
   - Increase swap space
   - Free up system memory

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI Whisper for transcription
- Ollama and LM Studio for local LLM hosting
- Streamlit for the web interface
- FFmpeg for video processing

---

## 🚀 Project Overview

Creating courses from videos is a time-consuming, manual task. This AI assistant helps educators and trainers by transforming videos into complete course modules with:

- 🧠 Structured course outlines
- 📘 Summarized learning material
- ❓ Auto-generated quizzes (MCQs)
- 🧾 Exportable formats (PDF, DOCX)

This tool supports both **video file uploads** and **YouTube links**, and leverages **OpenAI's GPT** and **Whisper** models to understand and generate content.

---

## 📦 Features

✅ Upload `.mp4` video or paste a YouTube link  
✅ Transcribe using Whisper or STT API  
✅ Segment content into logical sections  
✅ Generate titles, objectives, summaries, and quizzes with GPT  
✅ Export to PDF or DOCX  
✅ Clean modular Python codebase for easy extension

---

## 🛠️ Tech Stack

| Component      | Tool/Library                                                        |
| -------------- | ------------------------------------------------------------------- |
| Language       | Python                                                              |
| Video Download | [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)                        |
| Audio Extract  | `ffmpeg`, `moviepy`                                                 |
| Transcription  | [`openai-whisper`](https://github.com/openai/whisper) or AssemblyAI |
| LLM API        | Ollama or LM Studio                                                        |
| Export         | `python-docx`, `pdfkit`                                             |
| Optional UI    | Streamlit / Flask / Django                                          |

---


