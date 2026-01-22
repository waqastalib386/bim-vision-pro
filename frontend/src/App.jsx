import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FiActivity } from 'react-icons/fi';
import FileUpload from './components/FileUpload';
import ResultsDisplay from './components/ResultsDisplay';
import ChatPanel from './components/ChatPanel';
import LoadingScreen from './components/LoadingScreen';

// API URL - uses environment variable for production, falls back to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0); // 0 = not loading, 1-4 = steps
  const [loadingProgress, setLoadingProgress] = useState(0); // 0-100
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState('checking'); // checking, online, offline
  const [backendMessage, setBackendMessage] = useState('Connecting to server...');

  // Wake up backend on app load (important for Render free tier)
  useEffect(() => {
    const wakeUpBackend = async () => {
      try {
        setBackendStatus('checking');
        setBackendMessage('Waking up server... (this may take 30-60 seconds on first load)');

        const response = await axios.get(`${API_BASE_URL}/`, {
          timeout: 60000, // 60 second timeout for cold start
        });

        if (response.data.status === 'ok') {
          setBackendStatus('online');
          setBackendMessage('Server ready');
          console.log('Backend is online:', response.data.message);
        }
      } catch (err) {
        console.error('Backend health check failed:', err);
        setBackendStatus('offline');
        setBackendMessage('Server unavailable. Please refresh the page.');
      }
    };

    wakeUpBackend();
  }, []);

  const handleAnalyze = async (file) => {
    setLoading(true);
    setError(null);
    setLoadingStep(1);
    setLoadingProgress(10);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Step 1: Uploading (10-30%)
      setLoadingStep(1);
      setLoadingProgress(20);

      // Simulate upload progress
      const uploadProgress = setInterval(() => {
        setLoadingProgress(prev => Math.min(prev + 5, 30));
      }, 200);

      // Let browser automatically set Content-Type with boundary for multipart/form-data
      const startTime = Date.now();
      const response = await axios.post(`${API_BASE_URL}/api/upload-ifc`, formData, {
        timeout: 600000, // 10 minutes timeout for large files
        onUploadProgress: (progressEvent) => {
          clearInterval(uploadProgress);
          if (progressEvent.total) {
            // Calculate upload progress (0-30%)
            const percentCompleted = Math.round((progressEvent.loaded / progressEvent.total) * 30);
            setLoadingProgress(Math.min(percentCompleted, 30));
          }
        }
      });

      clearInterval(uploadProgress);

      // Step 2: Parsing (30-50%)
      setLoadingStep(2);
      setLoadingProgress(35);
      await new Promise(resolve => setTimeout(resolve, 500));
      setLoadingProgress(50);

      // Step 3: AI Analysis (50-85%)
      setLoadingStep(3);
      setLoadingProgress(55);

      // Simulate AI processing progress based on whether cached or not
      const isCached = response.data.cached;
      if (isCached) {
        setLoadingProgress(85);
      } else {
        // Gradually increase progress during AI analysis
        const aiProgress = setInterval(() => {
          setLoadingProgress(prev => Math.min(prev + 3, 85));
        }, 300);

        await new Promise(resolve => setTimeout(resolve, 1000));
        clearInterval(aiProgress);
      }

      // Step 4: Finalizing (85-100%)
      setLoadingStep(4);
      setLoadingProgress(90);
      await new Promise(resolve => setTimeout(resolve, 300));
      setLoadingProgress(100);

      // Show results
      setResults(response.data);
      setError(null);

      // Log performance
      const totalTime = (Date.now() - startTime) / 1000;
      console.log(`Analysis completed in ${totalTime.toFixed(2)}s`, isCached ? '(cached)' : '');
    } catch (err) {
      console.error('Error analyzing file:', err);
      setError(
        err.response?.data?.detail ||
        'Failed to analyze file. Please check if the backend server is running.'
      );
      setResults(null);
    } finally {
      setLoading(false);
      setLoadingStep(0);
      setLoadingProgress(0);
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
      {/* Backend Warming Up Overlay */}
      {backendStatus === 'checking' && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="glass-card p-8 max-w-md mx-4 text-center">
            <div className="text-6xl mb-4 animate-bounce">🔍</div>
            <h3 className="text-2xl font-bold mb-4 text-cyan-400">Starting BIM Vision Pro</h3>
            <div className="mb-4">
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div className="bg-gradient-to-r from-blue-500 to-cyan-500 h-full rounded-full animate-pulse w-3/4"></div>
              </div>
            </div>
            <p className="text-gray-300 mb-2">{backendMessage}</p>
            <p className="text-sm text-gray-400">
              The server is starting up. This happens on first visit and takes about 30-60 seconds.
            </p>
          </div>
        </div>
      )}

      {/* Header */}
      <header className="glass-card mx-4 mt-4 mb-8">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="text-4xl">🔍</div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  BIM Vision Pro
                </h1>
                <p className="text-sm text-cyan-400">AI-Powered Building Analysis</p>
              </div>
            </div>
            <div className="hidden md:block">
              <div className="flex items-center gap-2 text-sm">
                {backendStatus === 'online' && (
                  <>
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-green-400">{backendMessage}</span>
                  </>
                )}
                {backendStatus === 'checking' && (
                  <>
                    <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></div>
                    <span className="text-yellow-400">{backendMessage}</span>
                  </>
                )}
                {backendStatus === 'offline' && (
                  <>
                    <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                    <span className="text-red-400">{backendMessage}</span>
                  </>
                )}
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
                <h2 className="text-4xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  See Your Buildings Differently
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

            {/* Loading Screen with Progress */}
            {loading && (
              <LoadingScreen
                currentStep={loadingStep}
                progress={loadingProgress}
              />
            )}

            {/* File Upload Section */}
            {!results && !loading && (
              <FileUpload
                onAnalyze={handleAnalyze}
                loading={loading}
                disabled={backendStatus !== 'online'}
                backendStatus={backendStatus}
              />
            )}

            {/* Results Display */}
            {results && !loading && (
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
      <footer className="container mx-auto px-4 py-8 text-center border-t border-slate-700/50 mt-12">
        <div className="mb-4">
          <div className="text-3xl mb-2">🔍</div>
          <h3 className="text-lg font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            BIM Vision Pro
          </h3>
          <p className="text-sm text-cyan-400">AI-Powered Building Analysis</p>
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
