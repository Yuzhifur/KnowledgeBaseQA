from openai import OpenAI
from typing import List, Dict, Any
from ..core.config import settings


class DeepSeekClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL
        )
    
    async def generate_answer(self, question: str, context_documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate answer using DeepSeek API with document context"""
        try:
            # Prepare context from documents
            context = self._prepare_context(context_documents)
            
            # Create prompt
            prompt = self._create_prompt(question, context)
            
            # Call DeepSeek API
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided documents. Keep your answers concise and always cite the documents you used."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            answer = response.choices[0].message.content
            used_documents = [doc["id"] for doc in context_documents]
            
            return {
                "answer": answer,
                "cited_documents": used_documents,
                "context_length": len(context)
            }
            
        except Exception as e:
            raise Exception(f"DeepSeek API error: {str(e)}")
    
    def _prepare_context(self, documents: List[Dict[str, Any]]) -> str:
        """Prepare document context for the prompt"""
        context_parts = []
        
        for doc in documents:
            if doc.get("content"):
                context_parts.append(f"Document: {doc['filename']}\nContent: {doc['content'][:1000]}...")
        
        return "\n\n".join(context_parts)
    
    def _create_prompt(self, question: str, context: str) -> str:
        """Create the prompt for DeepSeek API"""
        return f"""Based on the following documents, please answer the question. Keep your answer concise and cite the documents you used.

Documents:
{context}

Question: {question}

Please provide a short answer and list which documents you referenced."""


deepseek_client = DeepSeekClient()