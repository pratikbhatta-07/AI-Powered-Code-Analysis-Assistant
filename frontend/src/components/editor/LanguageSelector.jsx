import React from 'react';
import { ChevronDown } from 'lucide-react';
import { LANGUAGES } from '../../constants/modes';

const LanguageSelector = ({ value, onChange }) => {
  return (
    <div className="relative">
      <label className="block text-sm font-medium text-gray-400 mb-2">
        Language
      </label>
      <div className="relative">
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full bg-dark-surface border border-dark-border rounded-lg px-4 py-2.5 text-white appearance-none cursor-pointer hover:border-dark-hover focus:outline-none focus:ring-2 focus:ring-accent-primary/50 transition-colors"
        >
          {LANGUAGES.map((lang) => (
            <option key={lang.id} value={lang.id}>
              {lang.name}
            </option>
          ))}
        </select>
        <ChevronDown className="w-4 h-4 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
      </div>
    </div>
  );
};

export default LanguageSelector;
