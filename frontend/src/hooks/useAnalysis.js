import { useState } from 'react';
import { analyzeCode } from '../services/api';

/**
 * Hook to manage code analysis state and API calls
 */
export const useAnalysis = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedMode, setSelectedMode] = useState('2'); // Default to interview mode

  const analyze = async (code, language, mode = selectedMode) => {
    if (!code.trim()) {
      setError('Please enter some code to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await analyzeCode(code, language, mode);
      setResult(response);
      setSelectedMode(mode);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleModeChange = async (code, language, newMode) => {
    setSelectedMode(newMode);
    await analyze(code, language, newMode);
  };

  const clearResult = () => {
    setResult(null);
    setError(null);
  };

  return {
    result,
    loading,
    error,
    selectedMode,
    analyze,
    handleModeChange,
    clearResult,
  };
};
