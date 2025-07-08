# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Knowledge Base QA application that allows users to upload documents and ask questions about them using AI-powered question answering. The application consists of a FastAPI backend deployed on Railway and a Next.js frontend deployed on Vercel, using Supabase for database and storage.

## Architecture

### Backend (FastAPI)
- **Location**: `/backend/`
- **Entry point**: `app/main.py`
- **Database**: Supabase (PostgreSQL) with direct client usage (no SQLAlchemy ORM)
- **Storage**: Supabase Storage for document files
- **AI Service**: DeepSeek API for question answering
- **Deployment**: Railway using `railway.toml` configuration

### Frontend (Next.js)
- **Location**: `/frontend/`
- **Framework**: Next.js 15.3.5 with App Router
- **Styling**: Tailwind CSS v4
- **Language**: TypeScript
- **Deployment**: Vercel

### Key Components
- **Document Processing**: Text extraction from TXT/PDF files, image storage
- **Q&A System**: DeepSeek API integration for document-based question answering
- **File Organization**: Documents organized by category (txt, pdf, image) with collapsible folders
- **Document Preview**: Content viewing for uploaded documents

## Common Development Commands

### Backend Development
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run with custom host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Development
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server with Turbopack
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

## Environment Configuration

### Backend (.env)
Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key  
- `SUPABASE_SERVICE_KEY`: (Optional) Service role key for admin operations
- `DEEPSEEK_API_KEY`: DeepSeek API key for AI services
- `DEEPSEEK_BASE_URL`: DeepSeek API base URL (default: "https://api.deepseek.com/v1")
- `APP_NAME`: Application name (default: "Knowledge Base QA")
- `DEBUG`: Debug mode flag (default: false)
- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 10MB)
- `ALLOWED_EXTENSIONS`: List of allowed file extensions (default: [".txt", ".pdf", ".jpg", ".jpeg", ".png"])

### Frontend (.env.local)
Required environment variables:
- `NEXT_PUBLIC_API_URL`: Backend API URL
  - Development: `http://localhost:8000`
  - Production: `https://knowledgebaseqa-production.up.railway.app`

### Deployment Environment Variables

#### Vercel (Frontend)
Set in Vercel Dashboard → Project Settings → Environment Variables:
- `NEXT_PUBLIC_API_URL`: `https://knowledgebaseqa-production.up.railway.app`

#### Railway (Backend)
Set in Railway Dashboard → Project → Variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key
- `SUPABASE_SERVICE_KEY`: Your Supabase service role key
- `DEEPSEEK_API_KEY`: Your DeepSeek API key

## Database Schema

The application uses Supabase with the schema defined in `backend/supabase_schema.sql`. Key tables:
- `documents`: Document metadata and content
- Storage bucket: "documents" for file storage

## API Structure

### Documents API (`/api/documents/`)
- `POST /upload`: Upload multiple documents
- `GET /by-category`: Get documents organized by category
- `GET /{id}/preview`: Get document preview
- `DELETE /{id}`: Delete a document

### Chat API (`/api/chat/`)
- `POST /`: Ask questions about documents

## File Processing

Supported file types (defined in `backend/app/core/config.py`):
- Text files: `.txt`
- PDF files: `.pdf`
- Images: `.jpg`, `.jpeg`, `.png`
- Max file size: 10MB

## Key Implementation Details

### Database Access
- Uses Supabase client directly, not SQLAlchemy
- Two client instances: regular client and admin client (bypasses RLS)
- Located in `backend/app/core/database.py`

### Document Storage
- Files stored in Supabase Storage bucket named "documents"
- Organized by file type directories
- Handled by `backend/app/services/storage.py`

### AI Integration
- Uses DeepSeek API with OpenAI-compatible interface
- Client implementation in `backend/app/services/deepseek_client.py`
- Q&A agent logic in `backend/app/agents/qa_agent.py`

### Frontend Components
- `DocumentList.tsx`: File browser with category organization
- `DocumentUpload.tsx`: Drag-and-drop file upload
- `DocumentPreview.tsx`: Document content viewer
- `QAInterface.tsx`: Chat interface for asking questions

## Testing and Deployment

### Backend Testing
No specific test framework configured. Use standard Python testing practices.

### Frontend Testing
Uses Next.js default ESLint configuration with TypeScript support.

### Deployment
- Backend: Railway with automatic deployment from `railway.toml`
- Frontend: Vercel with automatic deployment
- Database: Supabase (managed service)

## Development Notes

- Backend uses direct Supabase client calls rather than ORM
- Frontend uses Next.js App Router (not Pages Router)
- File uploads handled via multipart form data
- Full-text search implemented using PostgreSQL capabilities
- Document categorization handled client-side based on file extensions