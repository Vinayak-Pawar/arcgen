"use client";

import React, { useState, useRef } from 'react';
import { Upload, FileText, Image, X, AlertCircle, CheckCircle } from 'lucide-react';

interface FileUploadProps {
    onFileProcessed: (result: any) => void;
    onError: (error: string) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileProcessed, onError }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const acceptedTypes = [
        'application/pdf',
        'image/png',
        'image/jpeg',
        'image/jpg',
        'image/gif',
        'image/bmp',
        'image/webp'
    ];

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        const files = Array.from(e.dataTransfer.files);
        if (files.length > 0) {
            handleFile(files[0]);
        }
    };

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (files && files.length > 0) {
            handleFile(files[0]);
        }
    };

    const handleFile = async (file: File) => {
        // Validate file type
        if (!acceptedTypes.includes(file.type)) {
            onError('Unsupported file type. Please upload PDF or image files.');
            return;
        }

        // Validate file size (5MB limit)
        if (file.size > 5 * 1024 * 1024) {
            onError('File size exceeds 5MB limit.');
            return;
        }

        setUploadedFile(file);
        setIsUploading(true);

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('http://localhost:8000/generate-from-file', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            const result = await response.json();
            onFileProcessed(result);

        } catch (error: any) {
            onError(error.message || 'Failed to process file');
        } finally {
            setIsUploading(false);
        }
    };

    const clearFile = () => {
        setUploadedFile(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    const getFileIcon = (file: File) => {
        if (file.type === 'application/pdf') {
            return <FileText className="w-8 h-8 text-red-400" />;
        } else if (file.type.startsWith('image/')) {
            return <Image className="w-8 h-8 text-green-400" />;
        }
        return <Upload className="w-8 h-8 text-gray-400" />;
    };

    const formatFileSize = (bytes: number) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    return (
        <div className="w-full">
            {!uploadedFile ? (
                <div
                    className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer ${
                        isDragging
                            ? 'border-blue-500 bg-blue-500/10'
                            : 'border-gray-600 hover:border-gray-500'
                    }`}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                >
                    <Upload className={`w-12 h-12 mx-auto mb-4 ${isDragging ? 'text-blue-400' : 'text-gray-400'}`} />
                    <p className="text-lg font-medium text-white mb-2">
                        {isDragging ? 'Drop your file here' : 'Upload PDF or Image'}
                    </p>
                    <p className="text-sm text-gray-400 mb-4">
                        Drag & drop or click to select files
                    </p>
                    <p className="text-xs text-gray-500">
                        Supported: PDF, PNG, JPG, JPEG, GIF, BMP, WEBP (max 5MB)
                    </p>

                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf,.png,.jpg,.jpeg,.gif,.bmp,.webp"
                        onChange={handleFileSelect}
                        className="hidden"
                    />
                </div>
            ) : (
                <div className="bg-zinc-800 border border-white/10 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3">
                            {getFileIcon(uploadedFile)}
                            <div>
                                <p className="text-sm font-medium text-white truncate max-w-xs">
                                    {uploadedFile.name}
                                </p>
                                <p className="text-xs text-gray-400">
                                    {formatFileSize(uploadedFile.size)}
                                </p>
                            </div>
                        </div>
                        <button
                            onClick={clearFile}
                            className="text-gray-400 hover:text-white"
                        >
                            <X className="w-4 h-4" />
                        </button>
                    </div>

                    {isUploading && (
                        <div className="flex items-center gap-2 text-sm text-blue-400">
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-400"></div>
                            Processing file...
                        </div>
                    )}

                    {!isUploading && (
                        <div className="flex items-center gap-2 text-sm text-green-400">
                            <CheckCircle className="w-4 h-4" />
                            File ready for processing
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default FileUpload;
