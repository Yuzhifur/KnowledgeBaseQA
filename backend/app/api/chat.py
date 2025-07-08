from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from ..agents.qa_agent import qa_agent

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


class DocumentDetail(BaseModel):
    id: str
    filename: str
    file_type: str


class ChatResponse(BaseModel):
    answer: str
    cited_documents: List[str]
    document_details: List[DocumentDetail]


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer a question using the knowledge base"""
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Get answer from QA agent
        result = await qa_agent.answer_question(request.question)
        
        # Format document details
        document_details = []
        for doc in result["document_details"]:
            document_details.append(DocumentDetail(
                id=doc["id"],
                filename=doc["filename"],
                file_type=doc["file_type"]
            ))
        
        return ChatResponse(
            answer=result["answer"],
            cited_documents=result["cited_documents"],
            document_details=document_details
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chat"}