'use client';

import { useState } from 'react';
import { Upload, X, FileText, Image, FileIcon } from 'lucide-react';
import { documentApi } from '@/lib/api';

interface DocumentUploadProps {
  onUploadSuccess: () => void;
}

export default function DocumentUpload({ onUploadSuccess }: DocumentUploadProps) {
  const [files, setFiles] = useState<FileList | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(e.target.files);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files) {
      setFiles(e.dataTransfer.files);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = () => {
    setDragActive(false);
  };

  const handleUpload = async () => {
    if (!files || files.length === 0) return;

    setIsUploading(true);
    try {
      await documentApi.uploadDocuments(files);
      setFiles(null);
      onUploadSuccess();
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    switch (ext) {
      case 'txt':
        return <FileText className="w-4 h-4" />;
      case 'pdf':
        return <FileIcon className="w-4 h-4" />;
      case 'jpg':
      case 'jpeg':
      case 'png':
        return <Image className="w-4 h-4" />;
      default:
        return <FileIcon className="w-4 h-4" />;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-semibold mb-4">Upload Documents</h2>
      
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
        <p className="text-gray-600 mb-4">
          Drag and drop files here, or click to select files
        </p>
        <input
          type="file"
          multiple
          accept=".txt,.pdf,.jpg,.jpeg,.png"
          onChange={handleFileSelect}
          className="hidden"
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 cursor-pointer"
        >
          Select Files
        </label>
      </div>

      {files && files.length > 0 && (
        <div className="mt-4">
          <h3 className="font-medium mb-2">Selected Files:</h3>
          <div className="space-y-2">
            {Array.from(files).map((file, index) => (
              <div key={index} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                <div className="flex items-center space-x-2">
                  {getFileIcon(file.name)}
                  <span className="text-sm">{file.name}</span>
                  <span className="text-xs text-gray-500">
                    ({(file.size / 1024).toFixed(1)} KB)
                  </span>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 flex space-x-2">
            <button
              onClick={handleUpload}
              disabled={isUploading}
              className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 disabled:bg-gray-400"
            >
              {isUploading ? 'Uploading...' : 'Upload Files'}
            </button>
            <button
              onClick={() => setFiles(null)}
              className="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600"
            >
              Clear
            </button>
          </div>
        </div>
      )}
    </div>
  );
}