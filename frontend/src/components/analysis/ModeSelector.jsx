import React from 'react';
import { 
  GraduationCap, 
  Briefcase, 
  TestTube, 
  Bug, 
  Layers 
} from 'lucide-react';
import { ANALYSIS_MODES } from '../../constants/modes';

const iconMap = {
  GraduationCap,
  Briefcase,
  TestTube,
  Bug,
  Layers,
};

const ModeSelector = ({ selectedMode, onModeChange, disabled }) => {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-400">
        Analysis Mode
      </label>
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-2">
        {ANALYSIS_MODES.map((mode) => {
          const Icon = iconMap[mode.icon];
          const isSelected = selectedMode === mode.id;

          return (
            <button
              key={mode.id}
              onClick={() => onModeChange(mode.id)}
              disabled={disabled}
              className={`
                relative flex flex-col items-center gap-2 p-3 rounded-lg border transition-all
                ${
                  isSelected
                    ? 'bg-accent-primary/10 border-accent-primary text-accent-primary'
                    : 'bg-dark-surface border-dark-border text-gray-400 hover:border-dark-hover hover:text-white'
                }
                ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
              `}
            >
              <Icon className="w-5 h-5" />
              <span className="text-xs font-medium text-center">{mode.name}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default ModeSelector;
