import React from 'react';

const StatsCard = ({ title, icon, children, className = "" }) => {
  return (
    <div className={`glass-card p-6 hover:bg-white/15 transition-all duration-300 transform hover:-translate-y-1 ${className}`}>
      <div className="flex items-center gap-3 mb-4">
        <div className="text-3xl text-blue-400">
          {icon}
        </div>
        <h3 className="text-xl font-bold text-white">{title}</h3>
      </div>
      <div className="text-gray-300">
        {children}
      </div>
    </div>
  );
};

export default StatsCard;
