#!/usr/bin/env python3
"""
Test script for StudyMate functionality
"""

import os
import sys
from backend import (
    get_all_pdf_text,
    get_txt_text,
    get_text_chunks,
    get_vector_store_from_texts,
    process_question
)

def test_pdf_processing():
    """Test PDF text extraction"""
    print("🔍 Testing PDF processing...")
    
    # Check if sample PDFs exist
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    if not pdf_files:
        print("❌ No PDF files found in current directory")
        return False
    
    print(f"📄 Found PDF files: {pdf_files}")
    
    try:
        # Test PDF text extraction
        raw_text = get_all_pdf_text(pdf_files[:1])  # Test with first PDF
        if raw_text and len(raw_text.strip()) > 50:
            print(f"✅ PDF text extraction successful: {len(raw_text)} characters extracted")
            return True
        else:
            print("❌ PDF text extraction failed or returned minimal content")
            return False
    except Exception as e:
        print(f"❌ PDF processing error: {e}")
        return False

def test_text_chunking():
    """Test text chunking functionality"""
    print("\n🔍 Testing text chunking...")
    
    sample_text = """
    This is a sample text for testing the chunking functionality.
    It contains multiple sentences and paragraphs to ensure that
    the text splitter works correctly. The chunking process is
    important for creating manageable pieces of text that can be
    processed by the embedding model and stored in the vector database.
    """
    
    try:
        chunks = get_text_chunks(sample_text)
        if chunks and len(chunks) > 0:
            print(f"✅ Text chunking successful: {len(chunks)} chunks created")
            return True
        else:
            print("❌ Text chunking failed")
            return False
    except Exception as e:
        print(f"❌ Text chunking error: {e}")
        return False

def test_vector_store():
    """Test vector store creation"""
    print("\n🔍 Testing vector store creation...")
    
    sample_chunks = [
        "This is the first chunk of text about machine learning.",
        "This is the second chunk discussing natural language processing.",
        "The third chunk covers deep learning and neural networks."
    ]
    
    try:
        vector_store = get_vector_store_from_texts(sample_chunks)
        if vector_store:
            print("✅ Vector store creation successful")
            return vector_store
        else:
            print("❌ Vector store creation failed")
            return None
    except Exception as e:
        print(f"❌ Vector store creation error: {e}")
        return None

def test_question_processing(vector_store):
    """Test question processing"""
    print("\n🔍 Testing question processing...")
    
    if not vector_store:
        print("❌ Cannot test question processing without vector store")
        return False
    
    test_question = "What is machine learning?"
    
    try:
        response = process_question(test_question, vector_store)
        if response and len(response.strip()) > 10:
            print(f"✅ Question processing successful")
            print(f"📝 Response: {response[:100]}...")
            return True
        else:
            print("❌ Question processing failed or returned minimal response")
            return False
    except Exception as e:
        print(f"❌ Question processing error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎓 StudyMate Functionality Test")
    print("=" * 50)
    
    results = []
    
    # Test PDF processing
    results.append(test_pdf_processing())
    
    # Test text chunking
    results.append(test_text_chunking())
    
    # Test vector store
    vector_store = test_vector_store()
    results.append(vector_store is not None)
    
    # Test question processing
    results.append(test_question_processing(vector_store))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"✅ Passed: {sum(results)}/{len(results)} tests")
    
    if all(results):
        print("🎉 All tests passed! StudyMate is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
