import React from 'react';
import { BotIcon, UserIcon } from 'lucide-react';
import { Message as MessageType } from '../types';

interface MessageProps {
  message: MessageType;
}

const Message: React.FC<MessageProps> = ({ message }) => {
  const isAI = message.sender === 'ai';
  
  // Format time (e.g., "2:45 PM")
  const formattedTime = new Date(message.timestamp).toLocaleTimeString([], { 
    hour: 'numeric', 
    minute: '2-digit'
  });
  
  return (
    <div className={`py-6 ${isAI ? 'bg-white dark:bg-gray-900' : 'bg-gray-50 dark:bg-gray-800'}`}>
      <div className="container mx-auto px-4 sm:px-6 md:px-8 flex">
        <div className="mr-4 pt-1">
          {isAI ? (
            <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center">
              <BotIcon size={16} className="text-white" />
            </div>
          ) : (
            <div className="h-8 w-8 rounded-full bg-gray-700 dark:bg-gray-600 flex items-center justify-center">
              <UserIcon size={16} className="text-white" />
            </div>
          )}
        </div>
        <div className="flex-1 max-w-3xl">
          <div className="flex items-center mb-1 text-sm">
            <span className="font-medium text-gray-800 dark:text-gray-200">
              {isAI ? 'ZDCO Assistant' : 'You'}
            </span>
            <span className="ml-2 text-gray-500 dark:text-gray-400">{formattedTime}</span>
          </div>
          <div className="prose dark:prose-invert prose-p:leading-relaxed prose-pre:bg-gray-100 dark:prose-pre:bg-gray-800 prose-pre:text-sm max-w-none">
            <p className="text-gray-700 dark:text-gray-300 whitespace-pre-line">{message.content}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Message;