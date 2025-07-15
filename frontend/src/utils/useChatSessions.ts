import { useEffect, useState } from 'react';
import { Message } from '../types';
import { nanoid } from './helpers';
import axios from 'axios';

const SESSION_KEY = 'zdco_chat_sessions';

interface Session {
  id: string;
  title: string;
  messages: Message[];
}

async function fetchTitleFromAPI(message: string): Promise<string> {
  try {
    const response = await axios.post<{ title: string }>('http://localhost:8000/generate_title', {
      message,
    });
    return response.data.title || '';
  } catch (error) {
    console.error('Failed to fetch title from API:', error);
    return '';
  }
}

export function useChatSessions() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem(SESSION_KEY);
    if (saved) {
      try {
        const loaded: Session[] = JSON.parse(saved);
        setSessions(loaded);
        setActiveSessionId(loaded[0]?.id || null);
      } catch {
        localStorage.removeItem(SESSION_KEY);
        createNewSession();
      }
    } else {
      createNewSession();
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(SESSION_KEY, JSON.stringify(sessions));
  }, [sessions]);

  const currentSession = sessions.find((s) => s.id === activeSessionId);
  const currentMessages = currentSession?.messages || [];

  const createNewSession = (): Session => {
    const newSessionId = nanoid();
    const newSession: Session = {
      id: newSessionId,
      title: `Chat ${sessions.length + 1}`, // temporary title, may update on first user message
      messages: [],
    };
    setSessions((prev) => [...prev, newSession]);
    setActiveSessionId(newSessionId);
    return newSession;
  };

  const saveMessage = (message: Message, sessionId?: string) => {
    const targetId = sessionId || activeSessionId;
    if (!targetId) return;

    setSessions((prev) =>
      prev.map((session) => {
        if (session.id !== targetId) return session;

        const isFirstUserMessage =
          message.sender === 'user' && session.messages.length === 0;

        if (isFirstUserMessage) {
          fetchTitleFromAPI(message.content).then((newTitle) => {
            setSessions((current) =>
              current.map((s, i) =>
                s.id === session.id
                  ? {
                      ...s,
                      title: newTitle.trim() || `Chat ${i + 1}`,
                    }
                  : s
              )
            );
          });
        }

        return {
          ...session,
          messages: [...session.messages, message],
        };
      })
    );
  };

  const clearSessions = () => {
    setSessions([]);
    setActiveSessionId(null);
    localStorage.removeItem(SESSION_KEY);
  };

  return {
    sessions: sessions.map((s) => ({ id: s.id, title: s.title })),
    activeSessionId,
    currentMessages,
    saveMessage,
    createNewSession,
    setActiveSessionId,
    clearSessions,
  };
}
