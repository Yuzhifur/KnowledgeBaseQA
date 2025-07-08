'use client';

import { useState, useEffect } from 'react';
import { ChevronDown, ChevronRight, FileText, Image, FileIcon, Eye, Trash2 } from 'lucide-react';
import { documentApi, Document, DocumentsByCategory } from '@/lib/api';

interface DocumentListProps {
  refresh: boolean;
  onDocumentSelect: (documentId: string) => void;
  onRefreshComplete: () => void;
}

export default function DocumentList({ refresh, onDocumentSelect, onRefreshComplete }: DocumentListProps) {
  const [documents, setDocuments] = useState<DocumentsByCategory>({
    txt: [],
    img: [],
    pdf: []
  });
  const [expandedCategories, setExpandedCategories] = useState<{[key: string]: boolean}>({
    txt: true,
    img: true,
    pdf: true
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDocuments();
  }, [refresh]);

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const docs = await documentApi.getDocumentsByCategory();
      setDocuments(docs);
    } catch (error) {
      console.error('Failed to load documents:', error);
    } finally {
      setLoading(false);
      onRefreshComplete();
    }
  };

  const toggleCategory = (category: string) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  const handleDelete = async (documentId: string, filename: string) => {
    if (confirm(`Are you sure you want to delete "${filename}"?`)) {
      try {
        await documentApi.deleteDocument(documentId);
        loadDocuments();
      } catch (error) {
        console.error('Failed to delete document:', error);
        alert('Failed to delete document. Please try again.');
      }
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'txt':
        return <FileText className="w-5 h-5" />;
      case 'img':
        return <Image className="w-5 h-5" />;
      case 'pdf':
        return <FileIcon className="w-5 h-5" />;
      default:
        return <FileIcon className="w-5 h-5" />;
    }
  };

  const getCategoryTitle = (category: string) => {
    switch (category) {
      case 'txt':
        return 'Text Files';
      case 'img':
        return 'Images';
      case 'pdf':
        return 'PDF Files';
      default:
        return category.toUpperCase();
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-2">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            <div className="h-4 bg-gray-200 rounded w-2/3"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Document Library</h2>
      
      <div className="space-y-4">
        {Object.entries(documents).map(([category, docs]) => (
          <div key={category} className="border border-gray-200 rounded-lg">
            <button
              onClick={() => toggleCategory(category)}
              className="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center space-x-3">
                {getCategoryIcon(category)}
                <span className="font-medium">{getCategoryTitle(category)}</span>
                <span className="text-sm text-gray-500">({docs.length})</span>
              </div>
              {expandedCategories[category] ? (
                <ChevronDown className="w-5 h-5" />
              ) : (
                <ChevronRight className="w-5 h-5" />
              )}
            </button>
            
            {expandedCategories[category] && (
              <div className="border-t border-gray-200">
                {docs.length === 0 ? (
                  <div className="p-4 text-gray-500 text-center">
                    No {category} files uploaded yet
                  </div>
                ) : (
                  <div className="divide-y divide-gray-100">
                    {docs.map((doc) => (
                      <div key={doc.id} className="p-4 hover:bg-gray-50 transition-colors">
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2">
                              <span className="font-medium text-gray-900">{doc.filename}</span>
                              <span className="text-sm text-gray-500">
                                {formatFileSize(doc.file_size)}
                              </span>
                            </div>
                            <div className="text-sm text-gray-500 mt-1">
                              Uploaded {formatDate(doc.upload_date)}
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => onDocumentSelect(doc.id)}
                              className="p-2 text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
                              title="Preview document"
                            >
                              <Eye className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => handleDelete(doc.id, doc.filename)}
                              className="p-2 text-red-600 hover:bg-red-50 rounded-md transition-colors"
                              title="Delete document"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}