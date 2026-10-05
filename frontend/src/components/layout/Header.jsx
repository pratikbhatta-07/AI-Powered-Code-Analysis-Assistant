import React, { useState, useEffect } from 'react';
import { Code2, Moon, Sun } from 'lucide-react';

const Header = () => {
  const [isDark, setIsDark] = useState(true);

  useEffect(() => {
    // Check system preference or saved preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    const shouldBeDark = savedTheme === 'dark' || (!savedTheme && prefersDark);
    setIsDark(shouldBeDark);
    
    if (shouldBeDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  const toggleTheme = () => {
    setIsDark(!isDark);
    if (!isDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  };

  return (
    <header className="bg-dark-surface border-b border-dark-border px-6 py-4">
      <div className="max-w-screen-2xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-accent-primary/10 p-2 rounded-lg">
            <Code2 className="w-6 h-6 text-accent-primary" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Code Analysis Assistant</h1>
            <p className="text-xs text-gray-400">AI-powered code review and explanation</p>
          </div>
        </div>

        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg hover:bg-dark-hover transition-colors"
          aria-label="Toggle theme"
        >
          {isDark ? (
            <Sun className="w-5 h-5 text-gray-400" />
          ) : (
            <Moon className="w-5 h-5 text-gray-400" />
          )}
        </button>
      </div>
    </header>
  );
};

export default Header;
