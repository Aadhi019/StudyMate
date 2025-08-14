# StudyMate - AI Academic Assistant

StudyMate is an AI-powered academic assistant that enables students to interact with their study materials—such as textbooks, lecture notes, and research papers—in a conversational, question-answering format.

## 🎓 Features

- **Conversational Q&A**: Ask natural-language questions and receive contextual answers from your study materials
- **Multi-format Support**: Upload PDF and TXT files
- **Semantic Search**: Uses FAISS and embeddings for precise question matching
- **User-friendly Interface**: Intuitive Streamlit-based frontend
- **Reliable Processing**: Robust text extraction with OCR fallback for PDFs

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- All dependencies listed in `requirements.txt`

### Installation

1. Clone or download the StudyMate project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your HuggingFace API token in `.env`:
   ```
   HUGGINGFACEHUB_API_TOKEN=your_token_here
   ```

### Running StudyMate

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload your study materials (PDF or TXT files)

4. Click "Process Documents" to analyze your materials

5. Start asking questions about your study content!

## 📚 How to Use

### Uploading Documents
- Use the sidebar to upload PDF or TXT files
- Multiple files can be uploaded simultaneously
- Click "Process Documents" to analyze the content

### Asking Questions
- Type your questions in natural language
- Examples:
  - "What is machine learning?"
  - "Explain the difference between supervised and unsupervised learning"
  - "What are the main types of neural networks?"

### Getting Better Results
- Ask specific questions about your materials
- Use clear, complete sentences
- Reference specific topics or concepts from your documents

## 🔧 Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Text Processing**: PyMuPDF for PDF extraction, OCR fallback with Tesseract
- **Vector Search**: FAISS with HuggingFace embeddings
- **Text Chunking**: LangChain RecursiveCharacterTextSplitter
- **Answer Generation**: Simple text processing with keyword matching

### Key Components

1. **Text Extraction** (`get_pdf_text_with_ocr`, `get_txt_text`)
   - Extracts text from PDFs using PyMuPDF
   - Falls back to OCR if text extraction yields minimal content
   - Handles TXT files with proper encoding

2. **Text Chunking** (`get_text_chunks`)
   - Splits large documents into manageable chunks
   - Uses overlapping chunks for better context preservation

3. **Vector Store** (`get_vector_store_from_texts`)
   - Creates FAISS vector database from text chunks
   - Uses HuggingFace embeddings for semantic similarity

4. **Question Processing** (`process_question`)
   - Retrieves relevant document chunks using similarity search
   - Generates answers using simple text processing
   - Provides contextual responses based on uploaded materials

## 🛠️ Recent Fixes

The following issues have been resolved:

1. **Updated Dependencies**: Added missing packages to `requirements.txt`
2. **Fixed Imports**: Updated to use newer LangChain and HuggingFace packages
3. **Improved Error Handling**: Better logging and user feedback
4. **Reliable Answer Generation**: Implemented fallback text processing
5. **Enhanced UI**: Updated branding to StudyMate with improved user experience
6. **Robust PDF Processing**: Better handling of various PDF formats

## 📁 Project Structure

```
StudyMate_Project/
├── app.py                      # Main Streamlit application
├── backend.py                  # Core processing functions
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables
├── sample_study_material.txt   # Sample study content
├── test_studymate.py          # Test script
└── temp_uploaded_files/       # Temporary file storage
```

## 🧪 Testing

Run the test script to verify functionality:
```bash
python test_studymate.py
```

## 🔍 Troubleshooting

### Common Issues

1. **PDF Processing Fails**
   - Ensure PDFs contain readable text
   - Install Poppler for OCR functionality if needed

2. **Empty Responses**
   - Check that documents were processed successfully
   - Ensure questions are related to uploaded content

3. **Import Errors**
   - Verify all dependencies are installed: `pip install -r requirements.txt`

### Support

If you encounter issues:
1. Check the console output for error messages
2. Ensure all dependencies are properly installed
3. Verify your HuggingFace API token is valid

## 🎯 Use Cases

StudyMate is perfect for:
- **Exam Preparation**: Quick retrieval of concepts and definitions
- **Research**: Finding specific information across multiple documents
- **Study Sessions**: Interactive learning with your materials
- **Note Review**: Efficient access to key information
- **Academic Projects**: Research assistance and reference finding

## 🌟 Benefits

- **Time Saving**: No more manual searching through documents
- **Improved Understanding**: Get explanations in student-friendly language
- **Organized Learning**: Consolidate information from multiple sources
- **Accessible**: Works offline once documents are processed
- **Flexible**: Supports various document formats and question types

Enjoy using StudyMate for your academic success! 🎓
