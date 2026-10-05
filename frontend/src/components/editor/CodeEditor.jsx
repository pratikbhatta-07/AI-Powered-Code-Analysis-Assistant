import React from 'react';
import Editor from '@monaco-editor/react';

const CodeEditor = ({ value, onChange, language }) => {
  const handleEditorChange = (newValue) => {
    onChange(newValue || '');
  };

  return (
    <div className="h-full border border-dark-border rounded-lg overflow-hidden">
      <Editor
        height="100%"
        language={language}
        value={value}
        onChange={handleEditorChange}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          fontFamily: 'JetBrains Mono, Consolas, Monaco, Courier New, monospace',
          lineNumbers: 'on',
          rulers: [],
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          wordWrap: 'on',
          padding: { top: 16, bottom: 16 },
        }}
      />
    </div>
  );
};

export default CodeEditor;
