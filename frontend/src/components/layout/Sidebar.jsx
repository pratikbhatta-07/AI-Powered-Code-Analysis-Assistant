import React from 'react';

// Placeholder for future features like history, saved snippets, etc.
const Sidebar = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="w-64 bg-dark-surface border-r border-dark-border p-4">
      <h3 className="text-sm font-semibold text-gray-400 mb-4">History</h3>
      <p className="text-xs text-gray-500">Recent analyses will appear here</p>
    </div>
  );
};

export default Sidebar;
