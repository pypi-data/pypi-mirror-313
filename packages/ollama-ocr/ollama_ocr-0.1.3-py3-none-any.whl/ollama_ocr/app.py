import streamlit as st
from .ocr_processor import OCRProcessor
import tempfile
import os
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="OCR with Ollama",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    .main {
        background-color: #f8f9fa;
    }
    .stButton button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stSelectbox {
        margin-bottom: 1rem;
    }
    .upload-text {
        text-align: center;
        padding: 2rem;
        border: 2px dashed #ccc;
        border-radius: 10px;
        background-color: #ffffff;
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def get_available_models():
    return ["llava:7b", "llama3.2-vision:11b"]

def main():
    st.title("🔍 Vision OCR Lab")
    st.markdown("<p style='text-align: center; color: #666;'>Powered by Ollama Vision Models</p>", unsafe_allow_html=True)

    # Sidebar controls
    with st.sidebar:
        st.header("🎮 Controls")
        
        selected_model = st.selectbox(
            "🤖 Select Vision Model",
            get_available_models(),
            index=0,
        )
        
        format_type = st.selectbox(
            "📄 Output Format",
            ["markdown", "text", "json", "structured", "key_value"],
            help="Choose how you want the extracted text to be formatted"
        )
        
        st.markdown("---")
        
        # Model info box
        if selected_model == "llava:7b":
            st.info("LLaVA 7B: Efficient vision-language model optimized for real-time processing")
        else:
            st.info("Llama 3.2 Vision: Advanced model with high accuracy for complex text extraction")

    # Initialize OCR Processor
    processor = OCRProcessor(model_name=selected_model)

    # Main content area with tabs
    tab1, tab2 = st.tabs(["📸 Image Processing", "ℹ️ About"])
    
    with tab1:
        # File upload area
        uploaded_file = st.file_uploader(
            "Drop your image here",
            type=['png', 'jpg', 'jpeg', 'tiff', 'bmp'],
            help="Supported formats: PNG, JPG, JPEG, TIFF, BMP"
        )

        if uploaded_file is not None:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📸 Input Image")
                image = Image.open(uploaded_file)
                # Using use_container_width instead of deprecated use_column_width
                st.image(image, use_container_width=True, caption="Input Image")
                
                with st.expander("📋 Image Details", expanded=True):
                    st.markdown(f"""
                        - **Size**: {image.size}
                        - **Format**: {image.format}
                    """)

            with col2:
                st.subheader("📝 Extracted Text")
                with st.spinner(f"✨ Magic happening with {selected_model}..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        temp_path = tmp_file.name

                    try:
                        result = processor.process_image(temp_path, format_type)
                        
                        # Create a container for the result
                        with st.container():
                            if format_type == "markdown":
                                st.markdown(result)
                            elif format_type == "json":
                                st.json(result)
                            else:
                                st.text_area("", value=result, height=400)
                        
                        # Add some spacing
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Download button in a container
                        with st.container():
                            st.download_button(
                                label="📥 Download Extracted Text",
                                data=result,
                                file_name=f"extracted_text_{format_type}.txt",
                                mime="text/plain",
                            )
                    finally:
                        os.unlink(temp_path)
        else:
            st.markdown("""
                <div class='upload-text'>
                    <h3>👆 Upload an Image to Start</h3>
                    <p style='color: #666;'>Drag and drop your image here or click to browse</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("## About Vision OCR Lab")
        st.write("Extract text from images using state-of-the-art vision models:")
        
        st.markdown("### Available Models")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### LLaVA 7B")
            st.markdown("""
            - Efficient vision-language model
            - Optimized for real-time processing
            - Good for general text extraction
            """)
            
        with col2:
            st.markdown("#### Llama 3.2 Vision")
            st.markdown("""
            - Advanced vision capabilities
            - High accuracy for complex documents
            - Better at handling structured content
            """)
        
        st.markdown("### Output Formats")
        st.markdown("""
        - **Markdown**: Preserves text formatting with headers and lists
        - **Text**: Clean, plain text output
        - **JSON**: Structured data in JSON format
        - **Structured**: Organized tables and lists
        - **Key-Value**: Extracts paired information
        """)
        
        st.markdown("---")
        
        st.markdown("### 💡 Tips")
        st.info("""
        - Use Markdown format for well-structured documents
        - JSON format works best for data extraction
        - Key-Value is ideal for forms and labeled content
        """)

if __name__ == "__main__":
    main()