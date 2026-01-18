import React, { useState } from 'react';
import {
  FiInfo,
  FiLayers,
  FiPackage,
  FiHome,
  FiDownload,
  FiRefreshCw,
  FiSquare,
  FiGrid,
  FiColumns,
  FiStar
} from 'react-icons/fi';
import StatsCard from './StatsCard';
import CostingCard from './CostingCard';
import ValidationReport from './ValidationReport';

const ResultsDisplay = ({ results, onReset }) => {
  const [showFullAnalysis, setShowFullAnalysis] = useState(true);

  if (!results) return null;

  const { building_data, analysis, filename } = results;
  const { project_info, element_counts, materials, spaces, validation, costing } = building_data;

  const downloadResults = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `analysis-${filename}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="w-full space-y-6 animate-fade-in">
      {/* Header Section */}
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-white">Analysis Results</h2>
        <div className="flex gap-3">
          <button onClick={downloadResults} className="btn-secondary flex items-center gap-2">
            <FiDownload /> Download
          </button>
          <button onClick={onReset} className="btn-secondary flex items-center gap-2">
            <FiRefreshCw /> New Analysis
          </button>
        </div>
      </div>

      {/* Project Information */}
      <StatsCard title="Project Information" icon={<FiInfo />}>
        <div className="space-y-2">
          <div>
            <span className="font-semibold text-white">Project: </span>
            <span>{project_info.project_name}</span>
          </div>
          <div>
            <span className="font-semibold text-white">Building: </span>
            <span>{project_info.building_name}</span>
          </div>
          <div>
            <span className="font-semibold text-white">File: </span>
            <span>{filename}</span>
          </div>
        </div>
      </StatsCard>

      {/* Validation Report - Show errors and warnings */}
      {validation && <ValidationReport validation={validation} />}

      {/* Total Costing */}
      {costing && <CostingCard costing={costing} />}

      {/* Element Statistics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-card p-4 text-center hover:bg-white/15 transition-all">
          <FiSquare className="text-4xl text-blue-400 mx-auto mb-2" />
          <div className="text-3xl font-bold text-white">{element_counts.walls}</div>
          <div className="text-sm text-gray-400">Walls</div>
        </div>

        <div className="glass-card p-4 text-center hover:bg-white/15 transition-all">
          <FiPackage className="text-4xl text-green-400 mx-auto mb-2" />
          <div className="text-3xl font-bold text-white">{element_counts.doors}</div>
          <div className="text-sm text-gray-400">Doors</div>
        </div>

        <div className="glass-card p-4 text-center hover:bg-white/15 transition-all">
          <FiSquare className="text-4xl text-cyan-400 mx-auto mb-2" />
          <div className="text-3xl font-bold text-white">{element_counts.windows}</div>
          <div className="text-sm text-gray-400">Windows</div>
        </div>

        <div className="glass-card p-4 text-center hover:bg-white/15 transition-all">
          <FiGrid className="text-4xl text-purple-400 mx-auto mb-2" />
          <div className="text-3xl font-bold text-white">{element_counts.slabs}</div>
          <div className="text-sm text-gray-400">Slabs</div>
        </div>

        <div className="glass-card p-4 text-center hover:bg-white/15 transition-all">
          <FiColumns className="text-4xl text-yellow-400 mx-auto mb-2" />
          <div className="text-3xl font-bold text-white">{element_counts.columns}</div>
          <div className="text-sm text-gray-400">Columns</div>
        </div>

        <div className="glass-card p-4 text-center hover:bg-white/15 transition-all">
          <FiLayers className="text-4xl text-orange-400 mx-auto mb-2" />
          <div className="text-3xl font-bold text-white">{element_counts.beams}</div>
          <div className="text-sm text-gray-400">Beams</div>
        </div>

        <div className="glass-card p-4 text-center hover:bg-white/15 transition-all">
          <FiStar className="text-4xl text-pink-400 mx-auto mb-2" />
          <div className="text-3xl font-bold text-white">{element_counts.stairs}</div>
          <div className="text-sm text-gray-400">Stairs</div>
        </div>

        <div className="glass-card p-4 text-center hover:bg-white/15 transition-all">
          <FiHome className="text-4xl text-red-400 mx-auto mb-2" />
          <div className="text-3xl font-bold text-white">{element_counts.roofs}</div>
          <div className="text-sm text-gray-400">Roofs</div>
        </div>
      </div>

      {/* Materials Used */}
      <StatsCard title="Materials Used" icon={<FiPackage />}>
        <div className="flex flex-wrap gap-2">
          {materials && materials.length > 0 ? (
            materials.map((material, index) => (
              <span
                key={index}
                className="bg-blue-500/20 text-blue-300 px-3 py-1 rounded-full text-sm border border-blue-500/30"
              >
                {material}
              </span>
            ))
          ) : (
            <span className="text-gray-400">No materials data available</span>
          )}
        </div>
      </StatsCard>

      {/* Spaces/Rooms */}
      <StatsCard title="Spaces & Rooms" icon={<FiHome />}>
        <div className="space-y-2">
          <div className="text-lg font-semibold text-white mb-3">
            Total Spaces: {spaces.length}
          </div>
          {spaces && spaces.length > 0 && spaces[0].name !== "No spaces found" ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 max-h-40 overflow-y-auto">
              {spaces.map((space, index) => (
                <div key={index} className="bg-white/5 p-2 rounded border border-white/10">
                  <div className="font-semibold text-white text-sm">{space.name}</div>
                  <div className="text-xs text-gray-400">{space.long_name}</div>
                </div>
              ))}
            </div>
          ) : (
            <span className="text-gray-400">No spaces data available</span>
          )}
        </div>
      </StatsCard>

      {/* AI Analysis */}
      <div className="glass-card p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-2xl font-bold text-white flex items-center gap-2">
            <FiStar className="text-purple-400" />
            AI Analysis
          </h3>
          <button
            onClick={() => setShowFullAnalysis(!showFullAnalysis)}
            className="text-sm text-blue-400 hover:text-blue-300"
          >
            {showFullAnalysis ? 'Hide' : 'Show'}
          </button>
        </div>
        {showFullAnalysis && (
          <div className="prose prose-invert max-w-none">
            <div className="bg-black/20 p-4 rounded-lg border border-white/10 whitespace-pre-wrap">
              {analysis}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsDisplay;
