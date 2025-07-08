from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List, Optional
import uuid
from datetime import datetime
from ..models.document import DocumentResponse, DocumentPreview, DocumentType
from ..services.storage import storage_service
from ..services.document_processor import document_processor
from ..core.database import db

router = APIRouter()


@router.post("/upload", response_model=List[DocumentResponse])
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload multiple documents"""
    uploaded_docs = []
    supabase = db.get_client()
    
    for file in files:
        try:
            # Upload file to storage
            upload_result = await storage_service.upload_file(file)
            
            # Read file content for processing
            file.file.seek(0)  # Reset file pointer
            content = await file.read()
            
            # Extract text content
            text_content = document_processor.extract_text_content(
                content, upload_result["file_type"], file.filename
            )
            
            # Get metadata
            metadata = document_processor.get_document_metadata(
                content, upload_result["file_type"], file.filename
            )
            
            # Save to database
            doc_data = {
                "filename": file.filename,
                "file_type": upload_result["file_type"].value,
                "file_path": upload_result["file_path"],
                "file_size": upload_result["file_size"],
                "content": text_content,
                "metadata": metadata,
                "upload_date": datetime.utcnow().isoformat(),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            result = supabase.table("documents").insert(doc_data).execute()
            
            if result.error:
                raise HTTPException(status_code=500, detail=f"Database error: {result.error}")
            
            doc_record = result.data[0]
            uploaded_docs.append(DocumentResponse(
                id=doc_record["id"],
                filename=doc_record["filename"],
                file_type=DocumentType(doc_record["file_type"]),
                file_size=doc_record["file_size"],
                upload_date=datetime.fromisoformat(doc_record["upload_date"].replace('Z', '+00:00')),
                metadata=doc_record["metadata"]
            ))
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload {file.filename}: {str(e)}")
    
    return uploaded_docs


@router.get("/", response_model=List[DocumentResponse])
async def get_documents(file_type: Optional[DocumentType] = Query(None)):
    """Get all documents, optionally filtered by type"""
    supabase = db.get_client()
    
    try:
        query = supabase.table("documents").select("id, filename, file_type, file_size, upload_date, metadata")
        
        if file_type:
            query = query.eq("file_type", file_type.value)
        
        result = query.order("upload_date", desc=True).execute()
        
        if result.error:
            raise HTTPException(status_code=500, detail=f"Database error: {result.error}")
        
        documents = []
        for doc in result.data:
            documents.append(DocumentResponse(
                id=doc["id"],
                filename=doc["filename"],
                file_type=DocumentType(doc["file_type"]),
                file_size=doc["file_size"],
                upload_date=datetime.fromisoformat(doc["upload_date"].replace('Z', '+00:00')),
                metadata=doc["metadata"]
            ))
        
        return documents
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch documents: {str(e)}")


@router.get("/by-category")
async def get_documents_by_category():
    """Get documents organized by category"""
    supabase = db.get_client()
    
    try:
        result = supabase.table("documents").select("id, filename, file_type, file_size, upload_date, metadata").order("upload_date", desc=True).execute()
        
        if result.error:
            raise HTTPException(status_code=500, detail=f"Database error: {result.error}")
        
        # Organize by category
        categories = {"txt": [], "img": [], "pdf": []}
        
        for doc in result.data:
            doc_response = DocumentResponse(
                id=doc["id"],
                filename=doc["filename"],
                file_type=DocumentType(doc["file_type"]),
                file_size=doc["file_size"],
                upload_date=datetime.fromisoformat(doc["upload_date"].replace('Z', '+00:00')),
                metadata=doc["metadata"]
            )
            categories[doc["file_type"]].append(doc_response)
        
        return categories
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch documents: {str(e)}")


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """Get specific document by ID"""
    supabase = db.get_client()
    
    try:
        # Validate UUID
        uuid.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid document ID format")
    
    try:
        result = supabase.table("documents").select("id, filename, file_type, file_size, upload_date, metadata").eq("id", document_id).execute()
        
        if result.error:
            raise HTTPException(status_code=500, detail=f"Database error: {result.error}")
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc = result.data[0]
        return DocumentResponse(
            id=doc["id"],
            filename=doc["filename"],
            file_type=DocumentType(doc["file_type"]),
            file_size=doc["file_size"],
            upload_date=datetime.fromisoformat(doc["upload_date"].replace('Z', '+00:00')),
            metadata=doc["metadata"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch document: {str(e)}")


@router.get("/{document_id}/preview", response_model=DocumentPreview)
async def get_document_preview(document_id: str):
    """Get document preview with content"""
    supabase = db.get_client()
    
    try:
        # Validate UUID
        uuid.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid document ID format")
    
    try:
        result = supabase.table("documents").select("*").eq("id", document_id).execute()
        
        if result.error:
            raise HTTPException(status_code=500, detail=f"Database error: {result.error}")
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc = result.data[0]
        file_type = DocumentType(doc["file_type"])
        
        preview = DocumentPreview(
            id=doc["id"],
            filename=doc["filename"],
            file_type=file_type,
            content=doc["content"] if file_type != DocumentType.IMG else None
        )
        
        # For images, provide the file URL
        if file_type == DocumentType.IMG:
            preview.file_url = storage_service.get_file_url(doc["file_path"])
        
        return preview
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch document preview: {str(e)}")


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document"""
    supabase = db.get_client()
    
    try:
        # Validate UUID
        uuid.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid document ID format")
    
    try:
        # Get document info first
        result = supabase.table("documents").select("file_path").eq("id", document_id).execute()
        
        if result.error:
            raise HTTPException(status_code=500, detail=f"Database error: {result.error}")
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Document not found")
        
        file_path = result.data[0]["file_path"]
        
        # Delete from storage
        storage_result = supabase.storage.from_("documents").remove([file_path])
        
        # Delete from database
        db_result = supabase.table("documents").delete().eq("id", document_id).execute()
        
        if db_result.error:
            raise HTTPException(status_code=500, detail=f"Database error: {db_result.error}")
        
        return {"message": "Document deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")