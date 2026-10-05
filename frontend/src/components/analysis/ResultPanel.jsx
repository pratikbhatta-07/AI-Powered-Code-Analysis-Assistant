import React from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import { Copy, Check } from 'lucide-react';
import 'highlight.js/styles/github-dark.css';

const ResultPanel = ({ content, title = 'Analysis Result' }) => {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-dark-surface border border-dark-border rounded-lg overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-dark-border">
        <h3 className="text-sm font-semibold text-white">{title}</h3>
        <button
          onClick={handleCopy}
          className="flex items-center gap-2 px-3 py-1.5 text-xs text-gray-400 hover:text-white hover:bg-dark-hover rounded transition-colors"
        >
          {copied ? (
            <>
              <Check className="w-4 h-4" />
              Copied
            </>
          ) : (
            <>
              <Copy className="w-4 h-4" />
              Copy
            </>
          )}
        </button>
      </div>

      <div className="p-6 overflow-y-auto max-h-[calc(100vh-300px)] scrollbar-thin">
        <div className="prose prose-invert prose-sm max-w-none">
          <ReactMarkdown
            rehypePlugins={[rehypeHighlight]}
            components={{
              code: ({ node, inline, className, children, ...props }) => {
                if (inline) {
                  return (
                    <code className="bg-dark-bg px-1.5 py-0.5 rounded text-accent-primary" {...props}>
                      {children}
                    </code>
                  );
                }
                return (
                  <code className={className} {...props}>
                    {children}
                  </code>
                );
              },
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

export default ResultPanel;
