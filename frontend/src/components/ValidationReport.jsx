import React, { useState } from 'react';
import { FiAlertTriangle, FiAlertCircle, FiCheckCircle, FiChevronDown, FiChevronUp, FiX } from 'react-icons/fi';

const ValidationReport = ({ validation }) => {
  const [showErrors, setShowErrors] = useState(true);
  const [showWarnings, setShowWarnings] = useState(true);

  if (!validation) return null;

  const { is_valid, errors, warnings, missing_elements, recommendations, total_issues, error_count, warning_count } = validation;

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
      case 'high':
        return 'text-red-400 bg-red-500/10 border-red-500/30';
      case 'medium':
        return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30';
      case 'low':
        return 'text-blue-400 bg-blue-500/10 border-blue-500/30';
      default:
        return 'text-gray-400 bg-gray-500/10 border-gray-500/30';
    }
  };

  return (
    <div className="glass-card p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-2xl font-bold text-white flex items-center gap-2">
          {is_valid ? (
            <FiCheckCircle className="text-green-400" />
          ) : (
            <FiAlertTriangle className="text-red-400" />
          )}
          Validation Report
        </h3>
        <div className="flex items-center gap-2">
          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${is_valid ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
            {is_valid ? 'Valid' : 'Issues Found'}
          </span>
        </div>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-white/5 p-4 rounded-lg text-center">
          <div className="text-3xl font-bold text-white">{total_issues}</div>
          <div className="text-sm text-gray-400">Total Issues</div>
        </div>
        <div className="bg-red-500/10 p-4 rounded-lg text-center border border-red-500/30">
          <div className="text-3xl font-bold text-red-400">{error_count}</div>
          <div className="text-sm text-gray-400">Errors</div>
        </div>
        <div className="bg-yellow-500/10 p-4 rounded-lg text-center border border-yellow-500/30">
          <div className="text-3xl font-bold text-yellow-400">{warning_count}</div>
          <div className="text-sm text-gray-400">Warnings</div>
        </div>
      </div>

      {/* Errors Section */}
      {errors && errors.length > 0 && (
        <div className="mb-4">
          <button
            onClick={() => setShowErrors(!showErrors)}
            className="flex items-center justify-between w-full mb-2"
          >
            <h4 className="text-lg font-semibold text-red-400 flex items-center gap-2">
              <FiX className="text-xl" />
              Errors ({errors.length})
            </h4>
            {showErrors ? <FiChevronUp /> : <FiChevronDown />}
          </button>

          {showErrors && (
            <div className="space-y-2">
              {errors.map((error, index) => (
                <div key={index} className={`p-4 rounded-lg border ${getSeverityColor(error.severity)}`}>
                  <div className="flex items-start gap-3">
                    <FiAlertCircle className="text-xl mt-1 flex-shrink-0" />
                    <div className="flex-1">
                      <div className="font-semibold mb-1">{error.type}</div>
                      <div className="text-sm opacity-90 mb-2">{error.message}</div>
                      {error.location && (
                        <div className="text-xs opacity-70">
                          <span className="font-semibold">Location:</span> {error.location}
                        </div>
                      )}
                      {error.severity && (
                        <div className="mt-1">
                          <span className="text-xs px-2 py-1 rounded bg-black/20 uppercase">
                            {error.severity}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Warnings Section */}
      {warnings && warnings.length > 0 && (
        <div className="mb-4">
          <button
            onClick={() => setShowWarnings(!showWarnings)}
            className="flex items-center justify-between w-full mb-2"
          >
            <h4 className="text-lg font-semibold text-yellow-400 flex items-center gap-2">
              <FiAlertTriangle className="text-xl" />
              Warnings ({warnings.length})
            </h4>
            {showWarnings ? <FiChevronUp /> : <FiChevronDown />}
          </button>

          {showWarnings && (
            <div className="space-y-2">
              {warnings.map((warning, index) => (
                <div key={index} className={`p-4 rounded-lg border ${getSeverityColor(warning.severity)}`}>
                  <div className="flex items-start gap-3">
                    <FiAlertTriangle className="text-xl mt-1 flex-shrink-0" />
                    <div className="flex-1">
                      <div className="font-semibold mb-1">{warning.type}</div>
                      <div className="text-sm opacity-90 mb-2">{warning.message}</div>
                      {warning.location && (
                        <div className="text-xs opacity-70">
                          <span className="font-semibold">Location:</span> {warning.location}
                        </div>
                      )}
                      {warning.severity && (
                        <div className="mt-1">
                          <span className="text-xs px-2 py-1 rounded bg-black/20 uppercase">
                            {warning.severity}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Missing Elements */}
      {missing_elements && missing_elements.length > 0 && (
        <div className="mb-4 bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
          <h4 className="text-lg font-semibold text-purple-400 mb-2">Missing Elements</h4>
          <div className="flex flex-wrap gap-2">
            {missing_elements.map((element, index) => (
              <span key={index} className="bg-purple-500/20 text-purple-300 px-3 py-1 rounded-full text-sm">
                {element}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
          <h4 className="text-lg font-semibold text-green-400 mb-2 flex items-center gap-2">
            <FiCheckCircle />
            Recommendations
          </h4>
          <ul className="space-y-1">
            {recommendations.map((rec, index) => (
              <li key={index} className="text-sm text-gray-300 flex items-start gap-2">
                <span className="text-green-400 mt-1">•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* All Clear Message */}
      {is_valid && total_issues === 0 && (
        <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-6 text-center">
          <FiCheckCircle className="text-5xl text-green-400 mx-auto mb-3" />
          <p className="text-lg font-semibold text-white mb-2">Sab kuch sahi hai!</p>
          <p className="text-sm text-gray-300">IFC file mein koi errors ya warnings nahi hain.</p>
        </div>
      )}
    </div>
  );
};

export default ValidationReport;
