import React from 'react';
import { AlertCircle, X } from 'lucide-react';

const ErrorMessage = ({ message, onDismiss }) => {
  if (!message) return null;

  return (
    <div className="bg-accent-error/10 border border-accent-error/30 rounded-lg p-4 flex items-start gap-3">
      <AlertCircle className="w-5 h-5 text-accent-error flex-shrink-0 mt-0.5" />
      <div className="flex-1">
        <p className="text-sm text-accent-error font-medium">Error</p>
        <p className="text-sm text-gray-300 mt-1">{message}</p>
      </div>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="text-gray-400 hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
