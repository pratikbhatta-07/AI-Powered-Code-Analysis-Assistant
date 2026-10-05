import React from 'react';
import { Zap, Database } from 'lucide-react';

const ComplexityBadge = ({ timeComplexity, spaceComplexity }) => {
  if (!timeComplexity && !spaceComplexity) return null;

  const getComplexityColor = (complexity) => {
    if (!complexity) return 'gray';
    if (complexity.includes('O(1)') || complexity.includes('O(log')) return 'green';
    if (complexity.includes('O(n)')) return 'blue';
    if (complexity.includes('O(n²)') || complexity.includes('O(n^2)')) return 'yellow';
    return 'red';
  };

  const timeColor = getComplexityColor(timeComplexity);
  const spaceColor = getComplexityColor(spaceComplexity);

  const colorClasses = {
    green: 'bg-green-500/10 text-green-400 border-green-500/30',
    blue: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    yellow: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30',
    red: 'bg-red-500/10 text-red-400 border-red-500/30',
    gray: 'bg-gray-500/10 text-gray-400 border-gray-500/30',
  };

  return (
    <div className="flex flex-wrap gap-2">
      {timeComplexity && (
        <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border ${colorClasses[timeColor]}`}>
          <Zap className="w-4 h-4" />
          <span className="text-sm font-mono font-medium">{timeComplexity}</span>
        </div>
      )}
      {spaceComplexity && (
        <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border ${colorClasses[spaceColor]}`}>
          <Database className="w-4 h-4" />
          <span className="text-sm font-mono font-medium">{spaceComplexity}</span>
        </div>
      )}
    </div>
  );
};

export default ComplexityBadge;
