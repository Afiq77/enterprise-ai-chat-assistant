import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ChatHeader from './ChatHeader';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import Sidebar from './Sidebar';
import { Message } from '../types';
import { nanoid } from '../utils/helpers';
import { useChatSessions } from '../utils/useChatSessions';
import { detectModuleType, ModuleType } from '../utils/moduleDetection';

const API_URL = 'http://localhost:8000';

const ChatInterface: React.FC = () => {
  const [isTyping, setIsTyping] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  const {
    sessions,
    activeSessionId,
    currentMessages,
    saveMessage,
    createNewSession,
    setActiveSessionId,
    clearSessions,
  } = useChatSessions();

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode((prev) => !prev);
  };

  const handleSendMessage = async (content: string) => {
    // Detect module type for the query
    const moduleType = detectModuleType(content);
    
    // Use explicit session ID
    let sessionId = activeSessionId;
  
    if (!sessionId) {
      const newSession = createNewSession(); // returns session with id
      sessionId = newSession.id;
    }
  
    const userMessage: Message = {
      id: nanoid(),
      content,
      sender: 'user',
      timestamp: new Date().toISOString(),
      moduleType,
    };
  
    // Save message to the correct session
    saveMessage(userMessage, sessionId);
    setIsTyping(true);
  
    try {
      // Choose endpoint based on module type
      const endpoint = moduleType === 'order' ? '/chat_order' : '/chat';
      
      const response = await axios.post<{ response: string | string[] }>(
        `${API_URL}${endpoint}`,
        { query: content },
        {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
        }
      );
  
      // Handle both string and array responses
      const responseContent = Array.isArray(response.data.response) 
        ? response.data.response.join('\n') 
        : response.data.response;

      // Process the response to ensure newlines are preserved
      const processedContent = responseContent.replace(/\. /g, '.\n');

      const aiMessage: Message = {
        id: nanoid(),
        content: processedContent,
        sender: 'ai',
        timestamp: new Date().toISOString(),
        moduleType,
      };
  
      saveMessage(aiMessage, sessionId);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        id: nanoid(),
        content: '❌ Unable to reach server.',
        sender: 'ai',
        timestamp: new Date().toISOString(),
        moduleType,
      };
      saveMessage(errorMessage, sessionId);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors">
      <Sidebar
        sessions={sessions}
        activeId={activeSessionId}
        onSelect={setActiveSessionId}
        onNewChat={createNewSession}
        onClearAll={clearSessions}
      />

      <div className="flex flex-col flex-1">
        <ChatHeader darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
        <MessageList
          messages={currentMessages}
          isTyping={isTyping}
          onRerun={(message: Message) => handleSendMessage(message.content)}
        />
        <ChatInput onSendMessage={handleSendMessage} isProcessing={isTyping} />
      </div>
    </div>
  );
};

export default ChatInterface;
