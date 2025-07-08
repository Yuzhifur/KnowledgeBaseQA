# Knowledge Base QA Application

A web application for uploading, organizing, and querying documents using AI-powered question answering.

## Features

- **Document Upload**: Support for TXT, PDF, and Image files
- **Document Organization**: Files organized by category with collapsible folders
- **Document Preview**: View content of uploaded documents
- **AI-Powered Q&A**: Ask questions about your documents using DeepSeek API
- **File Citations**: See which documents were used to answer questions

## Architecture

- **Frontend**: Next.js with TypeScript and Tailwind CSS (deployed on Vercel)
- **Backend**: FastAPI with Python (deployed on Railway)
- **Database/Storage**: Supabase (PostgreSQL + Storage)
- **AI**: DeepSeek API for question answering

## Setup Instructions

### Prerequisites

- Node.js 18+
- Python 3.8+
- Supabase account
- DeepSeek API key

### Backend Setup

1. **Clone and navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Supabase**:
   - Create a new Supabase project
   - Go to SQL Editor and run the schema from `supabase_schema.sql`
   - Create a storage bucket named "documents"
   - Copy your project URL and anon key

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your credentials:
   ```
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

5. **Run the backend**:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.local.example .env.local
   ```
   Edit `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Run the frontend**:
   ```bash
   npm run dev
   ```

5. **Open the application**:
   Visit `http://localhost:3000` in your browser

## Deployment

### Backend (Railway)

1. **Connect your repository to Railway**
2. **Set environment variables** in Railway dashboard
3. **Deploy** - Railway will automatically use `railway.toml` configuration

### Frontend (Vercel)

1. **Connect your repository to Vercel**
2. **Set environment variables**:
   - `NEXT_PUBLIC_API_URL`: Your deployed backend URL
3. **Deploy** - Vercel will automatically build and deploy

## Usage

1. **Upload Documents**: Use the drag-and-drop interface to upload TXT, PDF, or image files
2. **Browse Documents**: View uploaded documents organized by type in collapsible folders
3. **Preview Documents**: Click the eye icon to preview document content
4. **Ask Questions**: Use the Q&A interface to ask questions about your documents
5. **View Citations**: See which documents were used to answer your questions

## API Endpoints

### Documents
- `POST /api/documents/upload` - Upload multiple documents
- `GET /api/documents/by-category` - Get documents organized by category
- `GET /api/documents/{id}/preview` - Get document preview
- `DELETE /api/documents/{id}` - Delete a document

### Chat
- `POST /api/chat/` - Ask a question about documents

## File Support

- **TXT**: Full text content indexing and search
- **PDF**: Text extraction and indexing
- **Images**: Storage and preview (AI processing not implemented)

## Technical Notes

- Uses Supabase client directly (not SQLAlchemy) for database operations
- Implements full-text search with PostgreSQL
- DeepSeek API provides OpenAI-compatible interface
- File storage organized by type in Supabase Storage
- Frontend uses server-side rendering with Next.js App Router

## License

MIT License