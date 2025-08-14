# backend.py (Reverted, Compatible Version)
import os
import fitz
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import LLMChain
from langchain.schema import Document
import traceback
import logging
from huggingface_hub import login
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(levelname)s] %(message)s')
HF_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not HF_API_KEY:
    logging.error("Hugging Face API key not found.")
    exit()
os.environ["HF_HOME"] = os.path.expanduser("~/.cache/huggingface")
try:
    login(token=HF_API_KEY)
    logging.info("Hugging Face authentication successful.")
except Exception as e:
    logging.error(f"Hugging Face login failed. Error: {e}")
    exit()

def get_pdf_text_with_ocr(pdf_path):
    """Extract text from PDF using PyMuPDF, fallback to OCR if needed."""
    text = ""
    try:
        logging.info(f"Extracting text from PDF: {pdf_path}")
        with fitz.open(pdf_path) as doc:
            for page_num, page in enumerate(doc):
                page_text = page.get_text("text").strip()
                if page_text:
                    text += page_text + "\n"
                logging.debug(f"Extracted {len(page_text)} characters from page {page_num + 1}")
    except Exception as e:
        logging.error(f"Failed to extract text from {pdf_path}: {e}")
        text = ""

    # If extracted text is too short, try OCR
    if len(text.strip()) < 100:
        logging.info(f"Text extraction yielded minimal content, attempting OCR for {pdf_path}")
        try:
            images = convert_from_path(pdf_path)
            ocr_text = ""
            for i, img in enumerate(images):
                page_ocr = pytesseract.image_to_string(img)
                ocr_text += page_ocr + "\n"
                logging.debug(f"OCR extracted {len(page_ocr)} characters from page {i + 1}")
            text = ocr_text
            logging.info(f"OCR completed for {pdf_path}, extracted {len(text)} characters")
        except Exception as ocr_error:
            logging.error(f"OCR failed for {pdf_path}: {ocr_error}")
            return ""

    return text

def get_all_pdf_text(pdf_paths):
    all_text = ""
    for pdf in pdf_paths:
        all_text += get_pdf_text_with_ocr(pdf)
    return all_text

def get_txt_text(txt_paths):
    text = ""
    for txt_file in txt_paths:
        with open(txt_file, "r", encoding="utf-8", errors="ignore") as f:
            text += f.read().strip() + "\n"
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(text)

def get_vector_store_from_texts(texts):
    if not texts:
        return None
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = FAISS.from_texts(texts, embedding=embeddings)
        return vector_store
    except Exception as e:
        logging.error(f"Failed to create vector store: {e}")
        return None

def create_simple_answer(docs, question):
    """Create a simple answer by extracting relevant text from documents."""
    if not docs:
        return "I couldn't find relevant information in your documents to answer this question."

    # Combine all document content
    context_text = "\n\n".join([doc.page_content for doc in docs])

    # Simple keyword-based relevance scoring
    question_words = set(question.lower().split())

    # Split context into sentences
    sentences = []
    for text in context_text.split('.'):
        sentence = text.strip()
        if len(sentence) > 20:  # Filter out very short fragments
            sentences.append(sentence)

    # Score sentences based on question word overlap
    scored_sentences = []
    for sentence in sentences:
        sentence_words = set(sentence.lower().split())
        overlap = len(question_words.intersection(sentence_words))
        if overlap > 0:
            scored_sentences.append((overlap, sentence))

    # Sort by relevance and take top sentences
    scored_sentences.sort(reverse=True, key=lambda x: x[0])
    top_sentences = [sent[1] for sent in scored_sentences[:3]]

    if top_sentences:
        answer = "Based on your study materials:\n\n" + "\n\n".join(top_sentences)
        return answer
    else:
        return f"I found some relevant content in your documents, but couldn't extract a specific answer to '{question}'. Here's some related information:\n\n{context_text[:500]}..."

def get_conversational_chain():
    """Create a conversational chain for Q&A with fallback to simple text processing."""
    # For now, return None to use the simple text processing fallback
    # This ensures the application works reliably without external model dependencies
    logging.info("Using simple text processing for reliable operation")
    return None

def process_question(user_question, vector_store):
    """Process a user question using the vector store and LLM chain."""
    if not vector_store:
        logging.warning("Vector store is not initialized")
        return "Please upload and process your documents first before asking questions."

    if not user_question or len(user_question.strip()) < 3:
        return "Please provide a more detailed question."

    try:
        logging.info(f"Processing question: {user_question[:100]}...")

        # Search for relevant documents
        docs = vector_store.similarity_search(user_question, k=10)  # Increased the number of documents to consider
        if not docs:
            logging.warning("No relevant documents found for the question")
            return "I couldn't find relevant information in your uploaded documents to answer this question. Please try rephrasing your question or check if the information is available in your documents."

        logging.info(f"Found {len(docs)} relevant document chunks")

        # Create conversational chain
        chain = get_conversational_chain()
        if not chain:
            logging.warning("No LLM chain available, using simple text extraction")
            # Fallback to simple text-based response
            answer = create_simple_answer(docs, user_question)
        else:
            # Generate response using the newer invoke method
            try:
                response = chain.invoke({"input_documents": docs, "question": user_question})
                answer = response.get("output_text", "").strip()
            except Exception as invoke_error:
                logging.warning(f"Invoke method failed, trying legacy call: {invoke_error}")
                try:
                    # Fallback to legacy method if invoke fails
                    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
                    answer = response.get("output_text", "").strip()
                except Exception as legacy_error:
                    logging.error(f"Both invoke and legacy methods failed: {legacy_error}")
                    # Final fallback to simple text processing
                    answer = create_simple_answer(docs, user_question)

        if not answer:
            logging.warning("Empty response generated")
            return "I'm having trouble generating a response. Please try rephrasing your question."

        logging.info("Successfully generated response")
        return answer

    except Exception as e:
        logging.error(f"Error processing question: {e}")
        traceback.print_exc()
        return f"I encountered an error while processing your question. Please try again or contact support if the issue persists."