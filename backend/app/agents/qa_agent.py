from typing import List, Dict, Any
from ..core.database import db
from ..services.deepseek_client import deepseek_client


class QAAgent:
    def __init__(self):
        self.supabase = db.get_client()
    
    async def answer_question(self, question: str) -> Dict[str, Any]:
        """Answer a question using relevant documents"""
        try:
            # Find relevant documents
            relevant_docs = await self._find_relevant_documents(question)
            
            if not relevant_docs:
                return {
                    "answer": "I couldn't find any relevant documents to answer your question.",
                    "cited_documents": [],
                    "document_details": []
                }
            
            # Generate answer using DeepSeek
            result = await deepseek_client.generate_answer(question, relevant_docs)
            
            # Add document details for citation
            document_details = []
            for doc in relevant_docs:
                document_details.append({
                    "id": doc["id"],
                    "filename": doc["filename"],
                    "file_type": doc["file_type"]
                })
            
            return {
                "answer": result["answer"],
                "cited_documents": result["cited_documents"],
                "document_details": document_details
            }
            
        except Exception as e:
            raise Exception(f"QA Agent error: {str(e)}")
    
    async def _find_relevant_documents(self, question: str) -> List[Dict[str, Any]]:
        """Find documents relevant to the question using text search"""
        try:
            # Use PostgreSQL full-text search
            # This is a simple approach - in production, you might want to use vector embeddings
            search_query = self._prepare_search_query(question)
            
            # Search in document content and filename
            result = self.supabase.table("documents").select("*").or_(
                f"content.fts.{search_query},filename.ilike.%{question}%"
            ).limit(5).execute()
            
            if result.error:
                print(f"Search error: {result.error}")
                # Fallback to simple text search
                return await self._fallback_search(question)
            
            # Filter out documents without content (like images)
            relevant_docs = []
            for doc in result.data:
                if doc["content"] and doc["content"].strip():
                    relevant_docs.append(doc)
            
            return relevant_docs
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            # Fallback to simple search
            return await self._fallback_search(question)
    
    async def _fallback_search(self, question: str) -> List[Dict[str, Any]]:
        """Fallback search method using simple text matching"""
        try:
            # Get all documents with content
            result = self.supabase.table("documents").select("*").not_.is_("content", "null").execute()
            
            if result.error:
                return []
            
            # Simple keyword matching
            keywords = question.lower().split()
            relevant_docs = []
            
            for doc in result.data:
                if doc["content"]:
                    content_lower = doc["content"].lower()
                    filename_lower = doc["filename"].lower()
                    
                    # Check if any keyword appears in content or filename
                    score = 0
                    for keyword in keywords:
                        if keyword in content_lower:
                            score += content_lower.count(keyword)
                        if keyword in filename_lower:
                            score += 2  # Filename matches are more important
                    
                    if score > 0:
                        doc["_score"] = score
                        relevant_docs.append(doc)
            
            # Sort by relevance score and return top 5
            relevant_docs.sort(key=lambda x: x["_score"], reverse=True)
            return relevant_docs[:5]
            
        except Exception as e:
            print(f"Fallback search error: {str(e)}")
            return []
    
    def _prepare_search_query(self, question: str) -> str:
        """Prepare search query for PostgreSQL full-text search"""
        # Remove special characters and create search terms
        words = question.lower().split()
        # Join with OR for broader search
        return " | ".join(words)


qa_agent = QAAgent()