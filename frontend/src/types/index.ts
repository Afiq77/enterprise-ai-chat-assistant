import { ModuleType } from '../utils/moduleDetection';

export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: string;
  moduleType?: ModuleType;
}

export interface Session {
  id: string;
  title: string;
  messages: Message[];
  createdAt: string;
  moduleType?: ModuleType;
} 