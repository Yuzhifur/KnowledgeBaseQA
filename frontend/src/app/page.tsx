'use client';

import { useState } from 'react';
import { BookOpen } from 'lucide-react';
import DocumentUpload from '@/components/DocumentUpload';
import DocumentList from '@/components/DocumentList';
import DocumentPreview from '@/components/DocumentPreview';
import QAInterface from '@/components/QAInterface';

export default function HomePage() {
  const [selectedDocumentId, setSelectedDocumentId] = useState<string | null>(null);
  const [refreshDocuments, setRefreshDocuments] = useState(false);

  const handleUploadSuccess = () => {
    setRefreshDocuments(!refreshDocuments);
  };

  const handleDocumentSelect = (documentId: string) => {
    setSelectedDocumentId(documentId);
  };

  const handleClosePreview = () => {
    setSelectedDocumentId(null);
  };

  const handleRefreshComplete = () => {
    // This can be used to update loading states if needed
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <BookOpen className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-xl font-semibold text-gray-900">Knowledge Base QA</h1>
                <p className="text-sm text-gray-600">Upload, organize, and query your documents</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Document Management */}
          <div className="space-y-6">
            <DocumentUpload onUploadSuccess={handleUploadSuccess} />
            <DocumentList
              refresh={refreshDocuments}
              onDocumentSelect={handleDocumentSelect}
              onRefreshComplete={handleRefreshComplete}
            />
          </div>

          {/* Right Column - Q&A Interface */}
          <div>
            <QAInterface onDocumentSelect={handleDocumentSelect} />
          </div>
        </div>
      </main>

      {/* Document Preview Modal */}
      {selectedDocumentId && (
        <DocumentPreview
          documentId={selectedDocumentId}
          onClose={handleClosePreview}
        />
      )}
    </div>
  );
}
