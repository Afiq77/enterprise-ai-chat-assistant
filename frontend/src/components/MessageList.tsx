import React, { useEffect, useRef } from 'react';
import { Message } from '../types';
import { ModuleType } from '../utils/moduleDetection';
import TypingIndicator from './TypingIndicator';

interface MessageListProps {
  messages: Message[];
  isTyping: boolean;
  onRerun: (message: Message) => void;
}

const getModuleIndicator = (moduleType: ModuleType) => {
  switch (moduleType) {
    case 'order':
      return '📦';
    case 'afaqy':
      return '🚛';
    default:
      return '';
  }
};

const MessageList: React.FC<MessageListProps> = ({ messages, isTyping, onRerun }) => {
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
        <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center mb-4">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-8 w-8 text-blue-600 dark:text-blue-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        </div>
        <h2 className="text-lg font-medium text-gray-800 dark:text-white mb-2">
          Welcome to ZDCO AI Assistant
        </h2>
        <p className="text-gray-600 dark:text-gray-400 max-w-md">
          Ask me anything about ZDCO services, products, or any other information you need assistance with.
        </p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${
            message.sender === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          <div
            className={`max-w-[80%] rounded-lg p-3 ${
              message.sender === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700'
            }`}
          >
            {message.moduleType && (
              <div className="text-xs mb-1 opacity-75">
                {getModuleIndicator(message.moduleType)} 
                {message.moduleType.charAt(0).toUpperCase() + message.moduleType.slice(1)} Module
              </div>
            )}
            <div className="whitespace-pre-wrap">{message.content}</div>
            {message.sender === 'user' && (
              <button
                onClick={() => onRerun(message)}
                className="text-xs opacity-75 hover:opacity-100 mt-2"
              >
                ↻ Rerun
              </button>
            )}
          </div>
        </div>
      ))}
      {isTyping && (
        <div className="flex justify-start">
          <div className="bg-gray-200 dark:bg-gray-700 rounded-lg p-3">
            <div className="animate-pulse">Typing...</div>
          </div>
        </div>
      )}
      <div ref={endOfMessagesRef} />
    </div>
  );
};

export default MessageList;
