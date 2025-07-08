from fastapi import UploadFile
import uuid
from datetime import datetime
from typing import Optional
from ..core.database import db
from ..models.document import DocumentType


class StorageService:
    def __init__(self):
        self.supabase = db.get_admin_client()  # Use admin client for storage operations
        self.bucket_name = "documents"
        # Skip bucket check since it's manually created
        print(f"Using storage bucket: {self.bucket_name}")
    
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
    
    def _ensure_bucket_exists(self):
        """Ensure the storage bucket exists, create if it doesn't"""
        try:
            # Try to get bucket info
            buckets_result = self.supabase.storage.list_buckets()
            
            # Handle different response formats
            if hasattr(buckets_result, 'error') and buckets_result.error:
                print(f"Error listing buckets: {buckets_result.error}")
                return
            
            # Get buckets list - handle both direct list and wrapped response
            buckets = buckets_result.data if hasattr(buckets_result, 'data') else buckets_result
            
            if not isinstance(buckets, list):
                print(f"Unexpected bucket list format: {type(buckets)}")
                print(f"Bucket list content: {buckets}")
                return
            
            # Check if our bucket exists
            bucket_names = [bucket.name if hasattr(bucket, 'name') else bucket.get('name', '') for bucket in buckets]
            bucket_exists = self.bucket_name in bucket_names
            
            print(f"Found buckets: {bucket_names}")
            
            if bucket_exists:
                print(f"Bucket '{self.bucket_name}' already exists")
            else:
                print(f"Bucket '{self.bucket_name}' does not exist, but you've manually created it.")
                print(f"Skipping automatic creation since bucket should exist.")
                
        except Exception as e:
            print(f"Error checking bucket: {str(e)}")
            print(f"Assuming bucket '{self.bucket_name}' exists since you created it manually")
    
    def _generate_file_path(self, file_type: DocumentType, filename: str) -> str:
        """Generate organized file path"""
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{file_type.value}/{timestamp}_{unique_id}_{filename}"
    
    async def upload_file(self, file: UploadFile) -> dict:
        """Upload file to Supabase storage"""
        try:
            print(f"Starting upload for file: {file.filename}")
            
            # Validate file type
            file_type = self._get_file_type(file.filename)
            file_path = self._generate_file_path(file_type, file.filename)
            
            print(f"Generated file path: {file_path}")
            
            # Read file content
            content = await file.read()
            print(f"Read {len(content)} bytes from file")
            
            # Upload to Supabase storage
            print(f"Uploading to bucket: {self.bucket_name}")
            result = self.supabase.storage.from_(self.bucket_name).upload(
                file_path, content, file_options={"content-type": file.content_type}
            )
            
            print(f"Upload result type: {type(result)}")
            print(f"Upload result: {result}")
            
            # Handle different response formats
            if hasattr(result, 'error') and result.error:
                print(f"Upload error details: {result.error}")
                raise Exception(f"Upload failed: {result.error}")
            elif hasattr(result, 'status_code') and result.status_code >= 400:
                print(f"Upload failed with status: {result.status_code}")
                raise Exception(f"Upload failed with status: {result.status_code}")
            
            print(f"Upload successful!")
            
            return {
                "file_path": file_path,
                "file_type": file_type,
                "file_size": len(content),
                "storage_path": file_path
            }
            
        except ValueError as e:
            print(f"File type validation error: {str(e)}")
            raise Exception(f"Invalid file type: {str(e)}")
        except Exception as e:
            print(f"Unexpected upload error: {str(e)}")
            raise Exception(f"File upload failed: {str(e)}")
    
    def get_file_url(self, file_path: str) -> str:
        """Get public URL for file"""
        try:
            result = self.supabase.storage.from_(self.bucket_name).get_public_url(file_path)
            print(f"Get public URL result: {result}")
            print(f"Result type: {type(result)}")
            
            # Handle different response formats
            if hasattr(result, 'data') and hasattr(result.data, 'publicUrl'):
                return result.data.publicUrl
            elif hasattr(result, 'publicUrl'):
                return result.publicUrl
            elif isinstance(result, dict) and 'publicUrl' in result:
                return result['publicUrl']
            else:
                print(f"Unexpected URL result format: {result}")
                # Fallback: construct URL manually
                supabase_url = self.supabase.supabase_url
                return f"{supabase_url}/storage/v1/object/public/{self.bucket_name}/{file_path}"
        except Exception as e:
            print(f"Error getting file URL: {str(e)}")
            raise Exception(f"Failed to get file URL: {str(e)}")
    
    async def get_file_content(self, file_path: str) -> bytes:
        """Download file content from storage"""
        try:
            result = self.supabase.storage.from_(self.bucket_name).download(file_path)
            
            # Handle different response formats
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Download failed: {result.error}")
            elif hasattr(result, 'data'):
                return result.data
            elif isinstance(result, bytes):
                return result
            else:
                raise Exception(f"Unexpected download result format: {type(result)}")
        except Exception as e:
            raise Exception(f"Failed to download file: {str(e)}")


storage_service = StorageService()