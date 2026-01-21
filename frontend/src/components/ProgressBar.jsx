import React from 'react';

const ProgressBar = ({ progress = 0, step = "", color = "blue" }) => {
  // Clamp progress between 0 and 100
  const clampedProgress = Math.min(Math.max(progress, 0), 100);

  // Color variants
  const colorClasses = {
    blue: "from-blue-600 to-cyan-600",
    green: "from-green-600 to-emerald-600",
    purple: "from-purple-600 to-pink-600",
    orange: "from-orange-600 to-red-600"
  };

  const gradientClass = colorClasses[color] || colorClasses.blue;

  return (
    <div className="w-full">
      {/* Step text */}
      {step && (
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-300">{step}</span>
          <span className="text-sm font-bold text-cyan-400">{clampedProgress}%</span>
        </div>
      )}

      {/* Progress bar container */}
      <div className="w-full h-3 bg-slate-800/80 rounded-full overflow-hidden border border-slate-700/50">
        {/* Progress bar fill */}
        <div
          className={`h-full bg-gradient-to-r ${gradientClass} transition-all duration-500 ease-out relative`}
          style={{ width: `${clampedProgress}%` }}
        >
          {/* Shimmer effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
        </div>
      </div>
    </div>
  );
};

export default ProgressBar;
