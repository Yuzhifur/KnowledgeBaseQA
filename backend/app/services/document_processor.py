import PyPDF2
import io
from typing import Optional
from ..models.document import DocumentType


class DocumentProcessor:
    def __init__(self):
        pass
    
    def extract_text_content(self, content: bytes, file_type: DocumentType, filename: str) -> Optional[str]:
        """Extract text content from various file types"""
        try:
            if file_type == DocumentType.TXT:
                return self._extract_text_from_txt(content)
            elif file_type == DocumentType.PDF:
                return self._extract_text_from_pdf(content)
            elif file_type == DocumentType.IMG:
                # For now, return None for images (graceful handling)
                return None
            else:
                return None
        except Exception as e:
            print(f"Error extracting text from {filename}: {str(e)}")
            return None
    
    def _extract_text_from_txt(self, content: bytes) -> str:
        """Extract text from TXT file"""
        try:
            # Try UTF-8 first, then fallback to latin-1
            try:
                return content.decode('utf-8')
            except UnicodeDecodeError:
                return content.decode('latin-1', errors='ignore')
        except Exception as e:
            raise Exception(f"Failed to decode text file: {str(e)}")
    
    def _extract_text_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text_content = []
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content.append(page.extract_text())
            
            return '\n'.join(text_content)
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def get_document_metadata(self, content: bytes, file_type: DocumentType, filename: str) -> dict:
        """Extract metadata from document"""
        metadata = {
            "filename": filename,
            "file_type": file_type.value,
            "file_size": len(content)
        }
        
        if file_type == DocumentType.PDF:
            try:
                pdf_file = io.BytesIO(content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                metadata["page_count"] = len(pdf_reader.pages)
                
                # Extract PDF metadata if available
                if pdf_reader.metadata:
                    metadata["title"] = pdf_reader.metadata.get("/Title", "")
                    metadata["author"] = pdf_reader.metadata.get("/Author", "")
                    metadata["subject"] = pdf_reader.metadata.get("/Subject", "")
            except Exception:
                pass
        
        return metadata


document_processor = DocumentProcessor()