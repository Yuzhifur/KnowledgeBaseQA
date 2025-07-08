import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Document types
export interface Document {
  id: string;
  filename: string;
  file_type: 'txt' | 'img' | 'pdf';
  file_size: number;
  upload_date: string;
  metadata?: Record<string, unknown>;
}

export interface DocumentPreview {
  id: string;
  filename: string;
  file_type: 'txt' | 'img' | 'pdf';
  content?: string;
  file_url?: string;
}

export interface DocumentsByCategory {
  txt: Document[];
  img: Document[];
  pdf: Document[];
}

export interface ChatResponse {
  answer: string;
  cited_documents: string[];
  document_details: {
    id: string;
    filename: string;
    file_type: string;
  }[];
}

// API functions
export const documentApi = {
  async uploadDocuments(files: FileList): Promise<Document[]> {
    const formData = new FormData();
    Array.from(files).forEach(file => {
      formData.append('files', file);
    });
    
    const response = await api.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  async getDocumentsByCategory(): Promise<DocumentsByCategory> {
    const response = await api.get('/api/documents/by-category');
    return response.data;
  },

  async getDocumentPreview(documentId: string): Promise<DocumentPreview> {
    const response = await api.get(`/api/documents/${documentId}/preview`);
    return response.data;
  },

  async deleteDocument(documentId: string): Promise<void> {
    await api.delete(`/api/documents/${documentId}`);
  },
};

export const chatApi = {
  async askQuestion(question: string): Promise<ChatResponse> {
    const response = await api.post('/api/chat/', { question });
    return response.data;
  },
};