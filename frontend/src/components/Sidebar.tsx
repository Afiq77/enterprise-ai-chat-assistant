import React from 'react';

interface SidebarProps {
  sessions: { id: string; title: string }[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onNewChat: () => void;
  onClearAll: () => void; // ✅ NEW
}

const Sidebar: React.FC<SidebarProps> = ({
  sessions,
  activeId,
  onSelect,
  onNewChat,
  onClearAll, // ✅ NEW
}) => {
  return (
    <div className="w-64 bg-white dark:bg-gray-800 border-r dark:border-gray-700 flex flex-col">
      <div className="p-4 border-b dark:border-gray-700">
      <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-3">
          💬 ZDCO Chats
        </h2>
        <div className="flex items-center justify-between space-x-2">
          <button
            className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
            onClick={onNewChat}
          >
            ➕ New Chat
          </button>
          <button
            className="text-sm text-red-600 dark:text-red-400 hover:underline"
            onClick={onClearAll}
          >
            🗑️ Clear All Chats
          </button>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {sessions.map((session) => (
          <button
            key={session.id}
            className={`block w-full text-left px-3 py-2 rounded ${
              session.id === activeId
                ? 'bg-blue-100 dark:bg-blue-600 text-blue-800 dark:text-white'
                : 'text-gray-800 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
            onClick={() => onSelect(session.id)}
          >
            {session.title}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
