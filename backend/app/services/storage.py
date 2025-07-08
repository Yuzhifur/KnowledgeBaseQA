from fastapi import UploadFile
import uuid
from datetime import datetime
from typing import Optional
from ..core.database import db
from ..models.document import DocumentType


class StorageService:
    def __init__(self):
        self.supabase = db.get_client()
        self.bucket_name = "documents"
    
    def _get_file_type(self, filename: str) -> DocumentType:
        """Determine file type based on extension"""
        ext = filename.lower().split('.')[-1]
        if ext == 'txt':
            return DocumentType.TXT
        elif ext == 'pdf':
            return DocumentType.PDF
        elif ext in ['jpg', 'jpeg', 'png']:
            return DocumentType.IMG
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _generate_file_path(self, file_type: DocumentType, filename: str) -> str:
        """Generate organized file path"""
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{file_type.value}/{timestamp}_{unique_id}_{filename}"
    
    async def upload_file(self, file: UploadFile) -> dict:
        """Upload file to Supabase storage"""
        try:
            file_type = self._get_file_type(file.filename)
            file_path = self._generate_file_path(file_type, file.filename)
            
            # Read file content
            content = await file.read()
            
            # Upload to Supabase storage
            result = self.supabase.storage.from_(self.bucket_name).upload(
                file_path, content, file_options={"content-type": file.content_type}
            )
            
            if result.error:
                raise Exception(f"Upload failed: {result.error}")
            
            return {
                "file_path": file_path,
                "file_type": file_type,
                "file_size": len(content),
                "storage_path": result.data.path
            }
            
        except Exception as e:
            raise Exception(f"File upload failed: {str(e)}")
    
    def get_file_url(self, file_path: str) -> str:
        """Get public URL for file"""
        try:
            result = self.supabase.storage.from_(self.bucket_name).get_public_url(file_path)
            return result.data.publicUrl
        except Exception as e:
            raise Exception(f"Failed to get file URL: {str(e)}")
    
    async def get_file_content(self, file_path: str) -> bytes:
        """Download file content from storage"""
        try:
            result = self.supabase.storage.from_(self.bucket_name).download(file_path)
            if result.error:
                raise Exception(f"Download failed: {result.error}")
            return result.data
        except Exception as e:
            raise Exception(f"Failed to download file: {str(e)}")


storage_service = StorageService()