import React, { useState } from 'react';
import { FiDollarSign, FiChevronDown, FiChevronUp, FiInfo } from 'react-icons/fi';

const CostingCard = ({ costing }) => {
  const [showBreakdown, setShowBreakdown] = useState(true);

  if (!costing) return null;

  const { breakdown, subtotal, contingency, total_cost, currency, note } = costing;

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-2xl font-bold text-white flex items-center gap-2">
          <FiDollarSign className="text-green-400" />
          Total Cost Estimation
        </h3>
        <button
          onClick={() => setShowBreakdown(!showBreakdown)}
          className="text-blue-400 hover:text-blue-300 transition-colors"
        >
          {showBreakdown ? <FiChevronUp className="text-xl" /> : <FiChevronDown className="text-xl" />}
        </button>
      </div>

      {/* Total Cost Display */}
      <div className="bg-gradient-to-r from-green-500/20 to-blue-500/20 border border-green-500/30 rounded-lg p-6 mb-4">
        <div className="text-center">
          <p className="text-gray-300 text-sm mb-2">Estimated Total Cost</p>
          <p className="text-4xl font-bold text-white">{formatCurrency(total_cost)}</p>
          <p className="text-gray-400 text-xs mt-2">({currency})</p>
        </div>
      </div>

      {/* Cost Breakdown */}
      {showBreakdown && (
        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-white">Cost Breakdown</h4>

          <div className="space-y-2">
            {Object.entries(breakdown).map(([key, value]) => (
              value > 0 && (
                <div key={key} className="flex justify-between items-center bg-white/5 p-3 rounded">
                  <span className="text-gray-300 capitalize">{key.replace('_', ' ')}</span>
                  <span className="text-white font-semibold">{formatCurrency(value)}</span>
                </div>
              )
            ))}
          </div>

          <div className="border-t border-white/20 pt-3 mt-3">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-300">Subtotal</span>
              <span className="text-white font-semibold">{formatCurrency(subtotal)}</span>
            </div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-300">Contingency & Overhead (20%)</span>
              <span className="text-white font-semibold">{formatCurrency(contingency)}</span>
            </div>
            <div className="flex justify-between items-center text-lg font-bold pt-2 border-t border-white/20">
              <span className="text-white">Total</span>
              <span className="text-green-400">{formatCurrency(total_cost)}</span>
            </div>
          </div>

          {/* Note */}
          <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3 flex items-start gap-2">
            <FiInfo className="text-blue-400 mt-1 flex-shrink-0" />
            <p className="text-sm text-gray-300">{note}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default CostingCard;
