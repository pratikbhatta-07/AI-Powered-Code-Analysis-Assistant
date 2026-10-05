import React from 'react';
import ResultPanel from './ResultPanel';
import ComplexityBadge from './ComplexityBadge';
import { FileText, Zap, TestTube, Bug } from 'lucide-react';

const FullReviewPanel = ({ result }) => {
  if (!result || !result.fullReview) {
    return <ResultPanel content={result?.result || ''} title="Full Review" />;
  }

  const { explanation, complexity, tests, bugs } = result.fullReview;

  const sections = [
    {
      title: 'Explanation',
      content: explanation,
      icon: FileText,
      color: 'text-blue-400',
    },
    {
      title: 'Complexity Analysis',
      content: complexity,
      icon: Zap,
      color: 'text-yellow-400',
    },
    {
      title: 'Test Cases',
      content: tests,
      icon: TestTube,
      color: 'text-purple-400',
    },
    {
      title: 'Bug Report',
      content: bugs,
      icon: Bug,
      color: 'text-red-400',
    },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-white">Full Review Report</h2>
        {complexity && <ComplexityBadge timeComplexity={complexity} />}
      </div>

      {sections.map((section, index) => {
        const Icon = section.icon;
        return (
          <div
            key={index}
            className="bg-dark-surface border border-dark-border rounded-lg overflow-hidden"
          >
            <div className="flex items-center gap-2 px-4 py-3 border-b border-dark-border">
              <Icon className={`w-5 h-5 ${section.color}`} />
              <h3 className="text-sm font-semibold text-white">{section.title}</h3>
            </div>
            <div className="p-4">
              <p className="text-sm text-gray-300 whitespace-pre-wrap">{section.content}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default FullReviewPanel;
