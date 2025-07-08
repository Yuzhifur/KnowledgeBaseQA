-- Knowledge Base QA Database Schema
-- Run this in your Supabase SQL editor

-- Create documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL CHECK (file_type IN ('txt', 'img', 'pdf')),
    file_path TEXT NOT NULL UNIQUE,
    file_size INTEGER NOT NULL,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    content TEXT, -- Extracted text content
    metadata JSONB, -- Additional metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for efficient querying
CREATE INDEX IF NOT EXISTS idx_documents_file_type ON documents(file_type);
CREATE INDEX IF NOT EXISTS idx_documents_upload_date ON documents(upload_date DESC);
CREATE INDEX IF NOT EXISTS idx_documents_filename ON documents(filename);

-- Create full-text search index on content
CREATE INDEX IF NOT EXISTS idx_documents_content_fts ON documents USING gin(to_tsvector('english', content));

-- Create storage bucket (run this in Supabase dashboard or via client)
-- This needs to be done via the Supabase interface:
-- 1. Go to Storage in your Supabase dashboard
-- 2. Create a new bucket named "documents"
-- 3. Set it to public if you want direct file access, or keep private for controlled access

-- Create RLS policies for documents table (optional, since no auth required)
-- ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Allow all operations" ON documents FOR ALL USING (true);

-- Create RLS policies for storage bucket
-- Since we don't have authentication, we need to allow all operations on the storage bucket
-- Run these commands in your Supabase SQL editor:

-- Allow all operations on the documents storage bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('documents', 'documents', true)
ON CONFLICT (id) DO UPDATE SET public = true;

-- Create storage policies to allow all operations (since no auth required)
CREATE POLICY "Allow all uploads" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'documents');

CREATE POLICY "Allow all downloads" ON storage.objects
FOR SELECT USING (bucket_id = 'documents');

CREATE POLICY "Allow all updates" ON storage.objects
FOR UPDATE USING (bucket_id = 'documents');

CREATE POLICY "Allow all deletes" ON storage.objects
FOR DELETE USING (bucket_id = 'documents');