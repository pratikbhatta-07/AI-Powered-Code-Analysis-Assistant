import { useState } from 'react';

/**
 * Hook to manage code input state
 */
export const useCodeInput = () => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [inputMethod, setInputMethod] = useState('paste'); // paste, file, github

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
  };

  const handleInputMethodChange = (method) => {
    setInputMethod(method);
  };

  const handleFileUpload = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setCode(e.target.result);
    };
    reader.readAsText(file);
  };

  const clearCode = () => {
    setCode('');
  };

  return {
    code,
    language,
    inputMethod,
    handleCodeChange,
    handleLanguageChange,
    handleInputMethodChange,
    handleFileUpload,
    clearCode,
  };
};
