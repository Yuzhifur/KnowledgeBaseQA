'use client';

import { useState, useEffect } from 'react';
import { X, FileText, Image, FileIcon } from 'lucide-react';
import { documentApi, DocumentPreview as DocumentPreviewType } from '@/lib/api';

interface DocumentPreviewProps {
  documentId: string;
  onClose: () => void;
}

export default function DocumentPreview({ documentId, onClose }: DocumentPreviewProps) {
  const [document, setDocument] = useState<DocumentPreviewType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDocument();
  }, [documentId]);

  const loadDocument = async () => {
    try {
      setLoading(true);
      setError(null);
      const doc = await documentApi.getDocumentPreview(documentId);
      setDocument(doc);
    } catch (err) {
      console.error('Failed to load document:', err);
      setError('Failed to load document preview');
    } finally {
      setLoading(false);
    }
  };

  const getFileIcon = (fileType: string) => {
    switch (fileType) {
      case 'txt':
        return <FileText className="w-6 h-6" />;
      case 'img':
        return <Image className="w-6 h-6" />;
      case 'pdf':
        return <FileIcon className="w-6 h-6" />;
      default:
        return <FileIcon className="w-6 h-6" />;
    }
  };

  const renderContent = () => {
    if (!document) return null;

    switch (document.file_type) {
      case 'txt':
      case 'pdf':
        return (
          <div className="bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
            <pre className="whitespace-pre-wrap text-sm font-mono">
              {document.content || 'No content available'}
            </pre>
          </div>
        );
      case 'img':
        return (
          <div className="text-center">
            {document.file_url ? (
              <img
                src={document.file_url}
                alt={document.filename}
                className="max-w-full max-h-96 mx-auto rounded-lg"
              />
            ) : (
              <div className="bg-gray-50 p-8 rounded-lg">
                <Image className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                <p className="text-gray-600">Image preview not available</p>
              </div>
            )}
          </div>
        );
      default:
        return (
          <div className="bg-gray-50 p-8 rounded-lg text-center">
            <FileIcon className="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <p className="text-gray-600">Preview not available for this file type</p>
          </div>
        );
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-4 border-b">
          <div className="flex items-center space-x-3">
            {document && getFileIcon(document.file_type)}
            <div>
              <h3 className="font-semibold text-lg">
                {document?.filename || 'Loading...'}
              </h3>
              <p className="text-sm text-gray-600">
                {document?.file_type.toUpperCase()} File
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <div className="p-4 overflow-y-auto max-h-[calc(90vh-80px)]">
          {loading && (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
          )}
          
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-700">{error}</p>
            </div>
          )}
          
          {!loading && !error && renderContent()}
        </div>
      </div>
    </div>
  );
}