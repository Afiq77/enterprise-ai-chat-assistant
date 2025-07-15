import React from 'react';
import { MessageSquare, Moon, Sun } from 'lucide-react';

interface ChatHeaderProps {
  darkMode: boolean;
  toggleDarkMode: () => void;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ darkMode, toggleDarkMode }) => {
  return (
    <header className="sticky top-0 z-10 border-b bg-white dark:bg-gray-900 dark:border-gray-700 border-gray-200">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <MessageSquare className="h-6 w-6 text-blue-600 dark:text-blue-400" />
          <h1 className="text-xl font-semibold text-gray-800 dark:text-white">ZDCO AI Assistant</h1>
        </div>
        <button
          onClick={toggleDarkMode}
          className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
        >
          {darkMode ? 
            <Sun className="h-5 w-5 text-gray-600 dark:text-gray-300" /> : 
            <Moon className="h-5 w-5 text-gray-600" />
          }
        </button>
      </div>
    </header>
  );
};

export default ChatHeader;