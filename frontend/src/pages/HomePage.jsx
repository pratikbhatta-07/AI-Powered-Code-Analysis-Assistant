import React, { useState } from 'react';
import { Upload, FileText, Github } from 'lucide-react';
import CodeEditor from '../components/editor/CodeEditor';
import LanguageSelector from '../components/editor/LanguageSelector';
import GithubUrlInput from '../components/editor/GithubUrlInput';
import ModeSelector from '../components/analysis/ModeSelector';
import ResultPanel from '../components/analysis/ResultPanel';
import FullReviewPanel from '../components/analysis/FullReviewPanel';
import ComplexityBadge from '../components/analysis/ComplexityBadge';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorMessage from '../components/common/ErrorMessage';
import { useCodeInput } from '../hooks/useCodeInput';
import { useAnalysis } from '../hooks/useAnalysis';
import { INPUT_METHODS } from '../constants/modes';

const HomePage = () => {
  const {
    code,
    language,
    inputMethod,
    handleCodeChange,
    handleLanguageChange,
    handleInputMethodChange,
    handleFileUpload,
  } = useCodeInput();

  const {
    result,
    loading,
    error,
    selectedMode,
    analyze,
    handleModeChange,
  } = useAnalysis();

  const handleAnalyze = () => {
    analyze(code, language, selectedMode);
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  return (
    <div className="flex-1 flex overflow-hidden">
      {/* Left Panel - Input */}
      <div className="w-1/2 border-r border-dark-border flex flex-col p-6 gap-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white">Code Input</h2>
        </div>

        <LanguageSelector value={language} onChange={handleLanguageChange} />

        {/* Input Method Tabs */}
        <div className="flex gap-2 border-b border-dark-border pb-2">
          <button
            onClick={() => handleInputMethodChange(INPUT_METHODS.PASTE)}
            className={`flex items-center gap-2 px-4 py-2 rounded-t-lg transition-colors ${
              inputMethod === INPUT_METHODS.PASTE
                ? 'bg-dark-surface text-white'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <FileText className="w-4 h-4" />
            Paste Code
          </button>
          <button
            onClick={() => handleInputMethodChange(INPUT_METHODS.FILE)}
            className={`flex items-center gap-2 px-4 py-2 rounded-t-lg transition-colors ${
              inputMethod === INPUT_METHODS.FILE
                ? 'bg-dark-surface text-white'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <Upload className="w-4 h-4" />
            Upload File
          </button>
          <button
            onClick={() => handleInputMethodChange(INPUT_METHODS.GITHUB)}
            className={`flex items-center gap-2 px-4 py-2 rounded-t-lg transition-colors ${
              inputMethod === INPUT_METHODS.GITHUB
                ? 'bg-dark-surface text-white'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <Github className="w-4 h-4" />
            GitHub URL
          </button>
        </div>

        {/* Input Content */}
        <div className="flex-1 min-h-0">
          {inputMethod === INPUT_METHODS.PASTE && (
            <CodeEditor
              value={code}
              onChange={handleCodeChange}
              language={language}
            />
          )}

          {inputMethod === INPUT_METHODS.FILE && (
            <div className="flex flex-col items-center justify-center h-full border-2 border-dashed border-dark-border rounded-lg p-8">
              <Upload className="w-12 h-12 text-gray-400 mb-4" />
              <p className="text-gray-400 mb-4">Upload a code file</p>
              <input
                type="file"
                id="file-upload"
                className="hidden"
                onChange={handleFileChange}
                accept=".py,.js,.java,.cpp,.c,.ts,.go,.rs"
              />
              <Button
                variant="secondary"
                onClick={() => document.getElementById('file-upload')?.click()}
              >
                Choose File
              </Button>
              {code && (
                <div className="mt-4 w-full">
                  <CodeEditor
                    value={code}
                    onChange={handleCodeChange}
                    language={language}
                  />
                </div>
              )}
            </div>
          )}

          {inputMethod === INPUT_METHODS.GITHUB && (
            <div className="h-full flex flex-col">
              <GithubUrlInput onCodeFetched={handleCodeChange} />
              {code && (
                <div className="flex-1 mt-4">
                  <CodeEditor
                    value={code}
                    onChange={handleCodeChange}
                    language={language}
                  />
                </div>
              )}
            </div>
          )}
        </div>

        <ModeSelector
          selectedMode={selectedMode}
          onModeChange={(mode) => handleModeChange(code, language, mode)}
          disabled={loading || !code.trim()}
        />

        <Button
          onClick={handleAnalyze}
          disabled={loading || !code.trim()}
          size="lg"
          className="w-full"
        >
          {loading ? 'Analyzing...' : 'Analyze Code'}
        </Button>
      </div>

      {/* Right Panel - Output */}
      <div className="w-1/2 flex flex-col p-6 gap-4 overflow-hidden">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white">Analysis Result</h2>
          {result?.complexity && (
            <ComplexityBadge
              timeComplexity={result.complexity.time}
              spaceComplexity={result.complexity.space}
            />
          )}
        </div>

        <div className="flex-1 min-h-0 overflow-auto">
          {loading && <LoadingSpinner text="Analyzing your code..." />}

          {error && <ErrorMessage message={error} />}

          {!loading && !error && !result && (
            <div className="flex flex-col items-center justify-center h-full text-gray-400">
              <FileText className="w-16 h-16 mb-4 opacity-50" />
              <p className="text-lg">No analysis yet</p>
              <p className="text-sm mt-2">Enter code and click "Analyze Code" to start</p>
            </div>
          )}

          {!loading && !error && result && (
            <>
              {selectedMode === '5' ? (
                <FullReviewPanel result={result} />
              ) : (
                <ResultPanel content={result.result} />
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomePage;
