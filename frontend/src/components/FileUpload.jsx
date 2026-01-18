import React, { useState } from 'react';
import { FiUploadCloud, FiFile, FiX } from 'react-icons/fi';
import LoadingSpinner from './LoadingSpinner';

const FileUpload = ({ onAnalyze, loading }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.name.toLowerCase().endsWith('.ifc')) {
        setSelectedFile(file);
      } else {
        alert('Please select a valid .ifc file');
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (file.name.toLowerCase().endsWith('.ifc')) {
        setSelectedFile(file);
      } else {
        alert('Please select a valid .ifc file');
      }
    }
  };

  const handleAnalyze = () => {
    if (selectedFile) {
      onAnalyze(selectedFile);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        className={`glass-card p-8 transition-all duration-300 ${
          dragActive ? 'border-blue-500 bg-blue-500/10' : ''
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {loading ? (
          <LoadingSpinner message="Analyzing your building..." />
        ) : selectedFile ? (
          <div className="text-center">
            <div className="flex items-center justify-center gap-3 mb-4">
              <FiFile className="text-4xl text-green-400" />
              <div className="text-left">
                <p className="text-lg font-semibold text-white">{selectedFile.name}</p>
                <p className="text-sm text-gray-400">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
              <button
                onClick={clearFile}
                className="ml-auto text-red-400 hover:text-red-300 transition-colors"
                title="Remove file"
              >
                <FiX className="text-2xl" />
              </button>
            </div>
            <button
              onClick={handleAnalyze}
              className="btn-primary w-full mt-4"
            >
              Analyze Building
            </button>
          </div>
        ) : (
          <div className="text-center">
            <FiUploadCloud className="text-6xl text-blue-400 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-white mb-2">Upload IFC File</h3>
            <p className="text-gray-400 mb-6">
              Drag and drop your IFC file here, or click to browse
            </p>
            <input
              type="file"
              accept=".ifc"
              onChange={handleFileChange}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="btn-primary cursor-pointer inline-block">
              Choose File
            </label>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
