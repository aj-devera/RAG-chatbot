from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from typing import List, Optional
import streamlit as st
import unicodedata
import re
import tempfile
import os

class DocumentProcessingPipeline:
    """
    A comprehensive pipeline for processing PDF documents
    with multiple stages of extraction and cleaning
    """
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Perform text cleaning:
        - Remove extra whitespaces
        - Normalize unicode characters
        - Remove special characters
        """
        # Normalize unicode characters
        text = unicodedata.normalize('NFKD', text)
        
        # Remove non-printable characters
        text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
        
        # Replace multiple whitespaces with single space
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @classmethod
    def extract_text_from_pdf(cls, file_path: str) -> List[Document]:
        """
        Extract text from PDF using PyPDFLoader
        """
        try:
            # Use PyPDFLoader for text extraction
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            # Clean text for each document
            cleaned_documents = []
            for doc in documents:
                doc.page_content = cls.clean_text(doc.page_content)
                cleaned_documents.append(doc)
            
            return cleaned_documents
        
        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}")
            return []
    
    @staticmethod
    def split_documents(documents: List[Document], 
                        chunk_size: int = 1000, 
                        chunk_overlap: int = 200) -> List[Document]:
        """
        Split documents into manageable chunks with configurable parameters
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        return text_splitter.split_documents(documents)
    
    @classmethod
    def process_pdfs(cls, 
                     uploaded_files, 
                     chunk_size: int = 1000, 
                     chunk_overlap: int = 200) -> Optional[FAISS]:
        """
        Comprehensive PDF processing pipeline
        """
        all_documents = []
        
        for uploaded_file in uploaded_files:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_path = temp_file.name
            
            try:
                # Extract text
                documents = cls.extract_text_from_pdf(temp_file_path)
                
                # Split documents
                split_docs = cls.split_documents(
                    documents, 
                    chunk_size=chunk_size, 
                    chunk_overlap=chunk_overlap
                )
                
                all_documents.extend(split_docs)
            
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
            
            finally:
                # Always clean up temporary file
                os.unlink(temp_file_path)
        
        # Create vector store
        if all_documents:
            embeddings = OpenAIEmbeddings()
            return FAISS.from_documents(all_documents, embeddings)
        
        return None