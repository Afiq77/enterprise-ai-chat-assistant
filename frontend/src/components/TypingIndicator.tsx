import React from 'react';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex items-center space-x-1">
      <div className="w-2 h-2 rounded-full bg-blue-600 dark:bg-blue-400 animate-pulse" style={{ animationDelay: '0ms' }}></div>
      <div className="w-2 h-2 rounded-full bg-blue-600 dark:bg-blue-400 animate-pulse" style={{ animationDelay: '300ms' }}></div>
      <div className="w-2 h-2 rounded-full bg-blue-600 dark:bg-blue-400 animate-pulse" style={{ animationDelay: '600ms' }}></div>
    </div>
  );
};

export default TypingIndicator;