import streamlit as st
import os
import asyncio
import nest_asyncio
import torch
from course_generator.video_processor import VideoProcessor
from course_generator.transcriber import Transcriber
from course_generator.course_generator import CourseGenerator
from course_generator.exporter import CourseExporter
from course_generator.config import Config
from course_generator.model_detector import ModelDetector
import tempfile
import logging
import time
from datetime import timedelta

# Disable PyTorch's custom class handling for Streamlit
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'
torch.set_num_threads(4)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize configuration
try:
    Config.setup()
except ValueError as e:
    st.error(f"Configuration Error: {str(e)}")
    st.stop()

st.set_page_config(
    page_title="AI Course Generator",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Course Generator")
st.markdown("Transform videos into complete course modules with AI")

# Initialize session state
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Detect available models
model_detector = ModelDetector()
ollama_available, lmstudio_available, ollama_models, lmstudio_models = model_detector.detect_available_models()

# Input section
st.header("Input")
input_type = st.radio("Choose input type:", ["YouTube URL", "Video File"])

if input_type == "YouTube URL":
    video_source = st.text_input("Enter YouTube URL:")
else:
    video_source = st.file_uploader("Upload video file", type=['mp4'])

# Processing options
st.header("Processing Options")
model_size = st.selectbox(
    "Whisper Model Size",
    ["tiny", "base", "small", "medium", "large"],
    index=["tiny", "base", "small", "medium", "large"].index(Config.DEFAULT_WHISPER_MODEL)
)

# LLM options
st.header("LLM Options")

# Determine available host types
available_hosts = []
if ollama_available:
    available_hosts.append("Ollama")
if lmstudio_available:
    available_hosts.append("LM Studio")

if not available_hosts:
    st.error("No LLM hosts (Ollama or LM Studio) are available. Please start one of them.")
    st.stop()

host_type = st.radio(
    "Select LLM Host",
    available_hosts,
    index=0
).lower().replace(" ", "")

# Select model based on host type
if host_type == "ollama":
    if not ollama_models:
        st.error("No models found in Ollama. Please install at least one model.")
        st.stop()
    default_model = model_detector.get_default_model("ollama", ollama_models)
    llm_model = st.selectbox(
        "Select Ollama Model",
        ollama_models,
        index=ollama_models.index(default_model) if default_model in ollama_models else 0
    )
else:  # lmstudio
    if not lmstudio_models:
        st.error("No models found in LM Studio. Please load at least one model.")
        st.stop()
    default_model = model_detector.get_default_model("lmstudio", lmstudio_models)
    llm_model = st.selectbox(
        "Select LM Studio Model",
        lmstudio_models,
        index=lmstudio_models.index(default_model) if default_model in lmstudio_models else 0
    )

# Export options
st.header("Export Options")
export_format = st.multiselect(
    "Select export format(s):",
    ["PDF", "DOCX"],
    default=[Config.DEFAULT_EXPORT_FORMAT]
)

# Process button
if st.button("Generate Course", disabled=st.session_state.processing):
    if not video_source:
        st.error("Please provide a video source")
    else:
        st.session_state.processing = True
        progress_bar = st.progress(0)
        start_time = time.time()
        
        try:
            # Initialize components
            video_processor = VideoProcessor()
            transcriber = Transcriber(model_size=model_size)
            course_generator = CourseGenerator(model_name=llm_model, host_type=host_type)
            exporter = CourseExporter()
            
            # Process video
            st.text("Processing video...")
            video_start = time.time()
            if input_type == "YouTube URL":
                video_path, audio_path = video_processor.process_video(video_source)
            else:
                # Save uploaded file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                    tmp_file.write(video_source.getvalue())
                    video_path = tmp_file.name
                audio_path = video_processor.extract_audio(video_path)
            video_time = time.time() - video_start
            progress_bar.progress(25)
            
            # Transcribe audio
            st.text("Transcribing audio...")
            transcribe_start = time.time()
            transcription = transcriber.transcribe(audio_path)
            segments = transcriber.segment_transcription(transcription)
            transcribe_time = time.time() - transcribe_start
            progress_bar.progress(50)
            
            # Generate course content
            st.text("Generating course content...")
            course_content = course_generator.generate_course_content(segments)
            progress_bar.progress(75)
            
            # Export course
            st.text("Exporting course...")
            export_start = time.time()
            os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
            
            # Sanitize the course title for filenames
            safe_title = exporter._sanitize_filename(course_content["title"])
            
            if "PDF" in export_format:
                pdf_path = os.path.join(Config.OUTPUT_DIR, f"{safe_title}.pdf")
                exporter.export_to_pdf(course_content, pdf_path)
                st.download_button(
                    "Download PDF",
                    open(pdf_path, "rb").read(),
                    file_name=f"{safe_title}.pdf",
                    mime="application/pdf"
                )
            
            if "DOCX" in export_format:
                docx_path = os.path.join(Config.OUTPUT_DIR, f"{safe_title}.docx")
                exporter.export_to_docx(course_content, docx_path)
                st.download_button(
                    "Download DOCX",
                    open(docx_path, "rb").read(),
                    file_name=f"{safe_title}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            export_time = time.time() - export_start
            
            progress_bar.progress(100)
            total_time = time.time() - start_time
            
            # Display timing metrics
            st.success("Course generation completed!")
            st.markdown("### Generation Metrics")
            metrics = course_content["generation_metrics"]
            st.markdown(f"""
            - **Total Processing Time**: {str(timedelta(seconds=int(total_time)))}
            - **Video Processing**: {str(timedelta(seconds=int(video_time)))}
            - **Transcription**: {str(timedelta(seconds=int(transcribe_time)))}
            - **Content Generation**: {metrics['total_time']}
              - Initial Generation: {metrics['initial_generation']}
              - Section Generation: {metrics['section_generation']}
            - **Export**: {str(timedelta(seconds=int(export_time)))}
            - **Total API Calls**: {metrics['total_api_calls']}
            - **Sections Processed**: {metrics['sections_processed']}
            - **Average Time per Section**: {metrics['average_time_per_section']}
            """)
            
        except Exception as e:
            logger.error(f"Error during course generation: {str(e)}", exc_info=True)
            st.error(f"An error occurred: {str(e)}")
        finally:
            st.button("Refresh", on_click=lambda: setattr(st.session_state, 'processing', False))
            if 'video_processor' in locals():
                video_processor.cleanup()

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by AI Course Generator") 