# Final Project Report: AI-Powered Video Content Analysis Pipeline

**Project Goal:** To develop an end-to-end pipeline that automates the process of analyzing video content, generating detailed visual descriptions, synthesizing a narrative script, and producing a complete audio-video report using locally hosted AI models.

**Scope & Focus:** This project was centered on demonstrating the capabilities of **local Large Language Models (LLMs)** for multimedia processing, rather than mastering complex video editing techniques. The pipeline successfully integrates multiple specialized local services—from frame extraction to speech synthesis—to achieve an autonomous workflow.

## 1. System Architecture and Methodology
The system operates in a five-stage pipeline:

### **Stage 1: Video Deconstruction (Framing)**
*   **Function:** Converts the source video (`Videos/Real Madrid vs FC Barcelona...mp4`) into a sequence of discrete, analyzable image frames.
*   **Technical Detail:** We utilized `imageio` and `polars` to read the video frame by frame at a controlled rate (e.g., 2 FPS). The raw PNG bytes of each frame were then efficiently stored in a Parquet file (`first_time.parquet`). This approach provided superior compression and data handling compared to traditional methods.

### **Stage 2: Visual Feature Extraction (Captioning)**
*   **Function:** Analyzes the sequence of frames to generate detailed, descriptive captions for key moments.
*   **Technical Detail:** The system processes frames in batches, encoding each frame into a Base64 data URL. A powerful Vision LLM API (configured via LM Studio) receives the image batch alongside a highly specific prompt defining the context (e.g., "El Clásico match," detailed player lineups). This stage successfully translated visual input into structured text descriptions of action and tactical positions.

### **Stage 3: Narrative Script Generation (Summarization)**
*   **Function:** Takes multiple, segmented captions and synthesizes them into a single, coherent narrative script suitable for professional narration.
*   **Technical Detail:** A hierarchical prompting mechanism was designed. Captions are grouped (e.g., every 20 descriptions) and fed to the Narrative LLM. This model is prompted not just to summarize, but to maintain **narrative continuity and tone**, bridging the gaps between distinct visual segments into smooth, timed passages perfect for a voiceover.

### **Stage 4: Audio Production (Text-to-Speech)**
*   **Function:** Converts the finalized narrative script into high-quality, synthetic speech audio files.
*   **Technical Detail:** We utilized specialized TTS engines (e.g., OmniVoice) configured to run locally on Apple Silicon (`device_map="mps"`). The synthesis process requires referencing a sample voice and text to ensure style consistency across all generated segments.

### **Stage 5: Final Video Assembly (Showcase)**
*   **Function:** Combines the original video timeline with the synthesized audio narrative to produce the final report video.
*   **Technical Detail:** This stage uses `moviepy` to concatenate all individual audio clips into a single, continuous sound track. This track is then mapped onto a selected segment of the original video and rendered as the final output (`salida.mp4`).

## 2. Achievements & Demonstrations
The core success lies in proving the connectivity of multiple local AI services:

*   **Local Model Interoperability:** The entire workflow was executed using locally hosted LLMs, demonstrating that complex multimedia pipelines can operate entirely offline (via LM Studio).
*   **Scalable Data Handling:** Use of Parquet for frame storage proved highly efficient for large datasets.
*   **Multi-Modal Reasoning:** Successful implementation of a pipeline requiring vision analysis (Image $\rightarrow$ Text) followed by advanced language synthesis (Text Sequence $\rightarrow$ Coherent Script $\rightarrow$ Audio).

## 3. Future Enhancements & Advanced Capabilities

While the project successfully demonstrated the core capabilities, several areas present opportunities for further development:

1.  **Advanced Model Optimization:** The current workflow can be significantly optimized using techniques like **model quantization and merging (GGUF/MLX)** to reduce memory footprint and increase inference speed.
2.  **Real-time Processing:** Transitioning the frame extraction loop from batch processing to a real-time streaming architecture would enhance usability.
3.  **[Optional] Custom Model Fine-Tuning:** As explored in the final notebook, using advanced frameworks (like `mlx_tune` with LoRA) allows for the fine-tuning of foundation models on highly specific domain data, tailoring the AI's output to a precise style or subject matter beyond what generic prompting can achieve.

***
**Conclusion:** This project successfully established a functional framework for automated video analysis using only local inference resources, demonstrating robust engineering integration across multiple specialized AI components.