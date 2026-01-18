import React, { useState, useRef, useEffect } from 'react';
import { FiSend, FiMessageSquare, FiCopy, FiChevronRight, FiChevronLeft } from 'react-icons/fi';
import LoadingSpinner from './LoadingSpinner';

const ChatPanel = ({ onAskQuestion, disabled }) => {
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const handleAsk = async () => {
    if (!question.trim() || loading) return;

    const userQuestion = question.trim();
    setQuestion('');
    setLoading(true);

    // Add user question to chat
    setChatHistory((prev) => [
      ...prev,
      { type: 'question', content: userQuestion, timestamp: new Date() }
    ]);

    try {
      const answer = await onAskQuestion(userQuestion);
      setChatHistory((prev) => [
        ...prev,
        { type: 'answer', content: answer, timestamp: new Date() }
      ]);
    } catch (error) {
      setChatHistory((prev) => [
        ...prev,
        { type: 'error', content: 'Failed to get answer. Please try again.', timestamp: new Date() }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    // Could add a toast notification here
  };

  return (
    <>
      {/* Toggle Button for Mobile */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`fixed right-4 top-4 z-50 lg:hidden btn-primary p-3 rounded-full ${
          isOpen ? 'hidden' : 'block'
        }`}
      >
        <FiMessageSquare className="text-xl" />
      </button>

      {/* Chat Panel */}
      <div
        className={`fixed lg:relative right-0 top-0 h-screen lg:h-auto w-full lg:w-96 glass-card transform transition-transform duration-300 z-40 flex flex-col ${
          isOpen ? 'translate-x-0' : 'translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Header */}
        <div className="p-4 border-b border-white/20 flex items-center justify-between">
          <h3 className="text-xl font-bold text-white flex items-center gap-2">
            <FiMessageSquare />
            Ask About Building
          </h3>
          <button
            onClick={() => setIsOpen(false)}
            className="lg:hidden text-white hover:text-gray-300"
          >
            <FiChevronRight className="text-2xl" />
          </button>
        </div>

        {/* Chat History */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {chatHistory.length === 0 && !disabled && (
            <div className="text-center text-gray-400 py-8">
              <FiMessageSquare className="text-4xl mx-auto mb-2 opacity-50" />
              <p>Upload a file and ask questions about your building!</p>
              <div className="mt-4 text-sm space-y-2">
                <p className="font-semibold text-white">Example questions:</p>
                <p className="text-xs">• How many rooms are there?</p>
                <p className="text-xs">• What materials are used?</p>
                <p className="text-xs">• Tell me about the structure</p>
              </div>
            </div>
          )}

          {disabled && chatHistory.length === 0 && (
            <div className="text-center text-gray-400 py-8">
              <p>Please upload an IFC file first to start asking questions.</p>
            </div>
          )}

          {chatHistory.map((item, index) => (
            <div
              key={index}
              className={`${
                item.type === 'question'
                  ? 'ml-auto bg-blue-500/20 border-blue-500/30'
                  : item.type === 'error'
                  ? 'bg-red-500/20 border-red-500/30'
                  : 'bg-white/10 border-white/20'
              } max-w-[85%] p-3 rounded-lg border`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 whitespace-pre-wrap text-sm">
                  {item.content}
                </div>
                {item.type === 'answer' && (
                  <button
                    onClick={() => copyToClipboard(item.content)}
                    className="text-gray-400 hover:text-white transition-colors flex-shrink-0"
                    title="Copy response"
                  >
                    <FiCopy />
                  </button>
                )}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {item.timestamp.toLocaleTimeString()}
              </div>
            </div>
          ))}

          {loading && (
            <div className="bg-white/10 border border-white/20 max-w-[85%] p-3 rounded-lg">
              <LoadingSpinner message="Thinking..." />
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-white/20">
          <div className="flex gap-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={disabled ? "Upload a file first..." : "Ask a question..."}
              disabled={disabled || loading}
              className="flex-1 bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <button
              onClick={handleAsk}
              disabled={disabled || loading || !question.trim()}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-500 disabled:cursor-not-allowed text-white p-2 rounded-lg transition-colors"
            >
              <FiSend className="text-xl" />
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default ChatPanel;
