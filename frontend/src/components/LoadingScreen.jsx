import React from 'react';
import ProgressBar from './ProgressBar';
import { FiUploadCloud, FiFileText, FiCpu, FiCheckCircle } from 'react-icons/fi';

const LoadingScreen = ({ currentStep = 0, progress = 0 }) => {
  const steps = [
    {
      id: 1,
      icon: <FiUploadCloud className="text-3xl" />,
      title: "Uploading File",
      description: "File is being uploaded to the server...",
      color: "blue"
    },
    {
      id: 2,
      icon: <FiFileText className="text-3xl" />,
      title: "Parsing IFC Structure",
      description: "Building elements are being extracted...",
      color: "green"
    },
    {
      id: 3,
      icon: <FiCpu className="text-3xl" />,
      title: "AI Analysis",
      description: "Intelligent insights are being generated...",
      color: "purple"
    },
    {
      id: 4,
      icon: <FiCheckCircle className="text-3xl" />,
      title: "Finalizing Results",
      description: "Results are being prepared...",
      color: "orange"
    }
  ];

  return (
    <div className="glass-card p-8 max-w-2xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="text-5xl mb-4">⚡</div>
        <h2 className="text-2xl font-bold text-white mb-2">
          Processing Your Building
        </h2>
        <p className="text-gray-400">
          Please wait while we analyze your IFC file...
        </p>
      </div>

      {/* Progress bar */}
      <div className="mb-8">
        <ProgressBar
          progress={progress}
          step={steps[currentStep - 1]?.title || "Processing..."}
          color={steps[currentStep - 1]?.color || "blue"}
        />
      </div>

      {/* Steps list */}
      <div className="space-y-4">
        {steps.map((step) => {
          const isCompleted = step.id < currentStep;
          const isCurrent = step.id === currentStep;
          const isPending = step.id > currentStep;

          return (
            <div
              key={step.id}
              className={`flex items-start gap-4 p-4 rounded-lg transition-all duration-300 ${
                isCurrent
                  ? 'bg-blue-500/20 border border-blue-500/30'
                  : isCompleted
                  ? 'bg-green-500/10 border border-green-500/20'
                  : 'bg-slate-800/40 border border-slate-700/30'
              }`}
            >
              {/* Icon */}
              <div
                className={`flex-shrink-0 ${
                  isCompleted
                    ? 'text-green-400'
                    : isCurrent
                    ? 'text-blue-400 animate-pulse'
                    : 'text-gray-500'
                }`}
              >
                {step.icon}
              </div>

              {/* Content */}
              <div className="flex-1">
                <h3
                  className={`font-semibold mb-1 ${
                    isCompleted
                      ? 'text-green-400'
                      : isCurrent
                      ? 'text-blue-400'
                      : 'text-gray-400'
                  }`}
                >
                  {step.title}
                </h3>
                <p className="text-sm text-gray-400">{step.description}</p>
              </div>

              {/* Status indicator */}
              <div className="flex-shrink-0">
                {isCompleted ? (
                  <div className="w-6 h-6 rounded-full bg-green-500/20 border-2 border-green-500 flex items-center justify-center">
                    <div className="w-2 h-2 rounded-full bg-green-500"></div>
                  </div>
                ) : isCurrent ? (
                  <div className="w-6 h-6 rounded-full bg-blue-500/20 border-2 border-blue-500 flex items-center justify-center">
                    <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
                  </div>
                ) : (
                  <div className="w-6 h-6 rounded-full bg-slate-700/50 border-2 border-slate-600"></div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer tip */}
      <div className="mt-6 p-4 bg-cyan-500/10 border border-cyan-500/30 rounded-lg">
        <p className="text-sm text-cyan-300 text-center">
          💡 <strong>Tip:</strong> First upload takes longer. Subsequent uploads of the same file are super fast (cached)!
        </p>
      </div>
    </div>
  );
};

export default LoadingScreen;
