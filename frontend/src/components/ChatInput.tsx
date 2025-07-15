import React, { useState, useRef } from 'react';
import { Send, Mic } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isProcessing: boolean;
}

const MAX_CHARS = 4000;

// ✅ Declare missing browser types (for TypeScript)
declare global {
  interface Window {
    webkitSpeechRecognition: any;
    SpeechRecognition: any;
  }

  interface SpeechRecognition extends EventTarget {
    lang: string;
    interimResults: boolean;
    maxAlternatives: number;
    start(): void;
    stop(): void;
    onstart: () => void;
    onend: () => void;
    onresult: (event: any) => void;
    onerror: (event: any) => void;
  }
}

const SpeechRecognitionClass =
  typeof window !== 'undefined' &&
  (window.SpeechRecognition || window.webkitSpeechRecognition);

const recognition: SpeechRecognition | null = SpeechRecognitionClass
  ? new SpeechRecognitionClass()
  : null;

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isProcessing }) => {
  const [message, setMessage] = useState('');
  const [isListening, setIsListening] = useState(false);
  const recognitionActive = useRef(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isProcessing) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const charsRemaining = MAX_CHARS - message.length;
  const isNearLimit = charsRemaining < 100;

  const toggleListening = () => {
    if (!recognition) {
      alert('Speech recognition is not supported in this browser.');
      return;
    }

    if (!recognitionActive.current) {
      recognition.lang = 'en-US';
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        setIsListening(true);
        recognitionActive.current = true;
        console.log('🎙️ Voice recognition started...');
      };

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        console.log('🗣️ You said:', transcript);
        setIsListening(false);
        recognitionActive.current = false;
        setMessage('');
        onSendMessage(transcript);
      };

      recognition.onerror = (event: any) => {
        console.error('Voice recognition error:', event.error);
        alert('Voice recognition failed. Please try again.');
        setIsListening(false);
        recognitionActive.current = false;
      };

      recognition.onend = () => {
        console.log('🎤 Voice recognition ended');
        setIsListening(false);
        recognitionActive.current = false;
      };

      recognition.start();
    } else {
      recognition.stop();
    }
  };

  return (
    <div className="bg-white dark:bg-gray-900 p-4">
      <div className="container mx-auto max-w-4xl">
        <form onSubmit={handleSubmit} className="relative">
          <div className="rounded-lg bg-white dark:bg-gray-800 shadow-sm transition-all">
            <textarea
              className="w-full px-4 py-3 pr-20 bg-transparent resize-none text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-0"
              placeholder="Type or speak your message here..."
              rows={1}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
              maxLength={MAX_CHARS}
              disabled={isProcessing}
              style={{ minHeight: '56px', maxHeight: '200px' }}
            />

            <div className="absolute right-3 bottom-2 flex items-center space-x-2">
              {message.length > 0 && (
                <span
                  className={`text-xs font-medium ${
                    isNearLimit
                      ? 'text-orange-500 dark:text-orange-400'
                      : 'text-gray-500 dark:text-gray-400'
                  }`}
                >
                  {charsRemaining}
                </span>
              )}

              {/* 🎤 Mic Button */}
              <button
                type="button"
                onClick={toggleListening}
                className="p-2 rounded-md bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                title={isListening ? 'Click to stop recording' : 'Click to speak'}
              >
                <Mic size={18} className={isListening ? 'text-green-500 animate-pulse' : ''} />
              </button>

              {/* 📨 Send Button */}
              <button
                type="submit"
                className={`p-2 rounded-md ${
                  message.trim() && !isProcessing
                    ? 'text-white bg-blue-600 hover:bg-blue-700'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                } transition-colors`}
                disabled={!message.trim() || isProcessing}
              >
                <Send size={18} />
              </button>
            </div>
          </div>
        </form>

        <div className="mt-2 text-xs text-center text-gray-500 dark:text-gray-400">
          ZDCO AI Assistant can make mistakes. Consider checking important information.
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
