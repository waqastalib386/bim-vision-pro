import React, { useState } from 'react';
import axios from 'axios';
import { FiActivity } from 'react-icons/fi';
import FileUpload from './components/FileUpload';
import ResultsDisplay from './components/ResultsDisplay';
import ChatPanel from './components/ChatPanel';

// API URL - uses environment variable for production, falls back to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async (file) => {
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/upload-ifc`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
      setError(null);
    } catch (err) {
      console.error('Error analyzing file:', err);
      setError(
        err.response?.data?.detail ||
        'Failed to analyze file. Please check if the backend server is running.'
      );
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  const handleAskQuestion = async (question) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/ask-question`, {
        question: question,
      });

      return response.data.answer;
    } catch (err) {
      console.error('Error asking question:', err);
      throw new Error(
        err.response?.data?.detail ||
        'Failed to get answer. Please try again.'
      );
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="glass-card mx-4 mt-4 mb-8 border-cyan-500/30">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="text-4xl">🔍</div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                  BIM Vision Pro
                </h1>
                <p className="text-sm text-cyan-400">See Your Buildings Differently</p>
              </div>
            </div>
            <div className="hidden md:block">
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <div className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse"></div>
                <span>Server Connected</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 pb-8">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Left Section - Upload & Results */}
          <div className="flex-1">
            {/* Hero Section */}
            {!results && !loading && (
              <div className="text-center mb-8">
                <div className="text-6xl mb-4">🔍</div>
                <h2 className="text-4xl md:text-6xl font-bold mb-4">
                  <span className="bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
                    See Your Buildings Differently
                  </span>
                </h2>
                <p className="text-xl text-cyan-300 mb-4">
                  AI-Powered Building Analysis Platform
                </p>
                <p className="text-lg text-gray-400 mb-8">
                  Upload your IFC files and unlock intelligent insights about your building models
                </p>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="glass-card p-4 mb-6 border-2 border-red-500/50 bg-red-500/10">
                <div className="flex items-start gap-3">
                  <div className="text-red-400 text-xl">⚠️</div>
                  <div>
                    <h3 className="text-red-400 font-semibold mb-1">Error</h3>
                    <p className="text-gray-300 text-sm">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {/* File Upload Section */}
            {!results && (
              <FileUpload onAnalyze={handleAnalyze} loading={loading} />
            )}

            {/* Results Display */}
            {results && (
              <ResultsDisplay results={results} onReset={handleReset} />
            )}

            {/* Features Section - Show when no results */}
            {!results && !loading && (
              <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="glass-card p-6 text-center">
                  <div className="text-4xl mb-3">🏗️</div>
                  <h3 className="text-lg font-semibold text-white mb-2">
                    Detailed Analysis
                  </h3>
                  <p className="text-sm text-gray-400">
                    Get comprehensive insights about your building structure
                  </p>
                </div>
                <div className="glass-card p-6 text-center">
                  <div className="text-4xl mb-3">🤖</div>
                  <h3 className="text-lg font-semibold text-white mb-2">
                    AI-Powered
                  </h3>
                  <p className="text-sm text-gray-400">
                    Powered by Claude AI for intelligent analysis
                  </p>
                </div>
                <div className="glass-card p-6 text-center">
                  <div className="text-4xl mb-3">💬</div>
                  <h3 className="text-lg font-semibold text-white mb-2">
                    Ask Questions
                  </h3>
                  <p className="text-sm text-gray-400">
                    Interactive chat to explore your building data
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Right Section - Chat Panel */}
          {results && (
            <div className="lg:w-96">
              <ChatPanel
                onAskQuestion={handleAskQuestion}
                disabled={!results}
              />
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 text-center border-t border-cyan-500/20 mt-12">
        <div className="mb-4">
          <div className="text-3xl mb-2">🔍</div>
          <h3 className="text-lg font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            BIM Vision Pro
          </h3>
          <p className="text-sm text-cyan-400">See Your Buildings Differently</p>
        </div>
        <p className="text-gray-400 text-sm">
          Powered by AI | Built with React + FastAPI
        </p>
        <p className="text-gray-500 text-xs mt-2">
          © 2026 BIM Vision Pro. All rights reserved.
        </p>
      </footer>
    </div>
  );
}

export default App;
