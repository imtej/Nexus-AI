"use client";

import { timeAgo, truncate } from "@/lib/utils";
import styles from "./ConversationList.module.css";

interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

interface ConversationListProps {
  conversations: Conversation[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
}

/**
 * ConversationList — sidebar list of past conversations.
 */
export default function ConversationList({
  conversations,
  activeId,
  onSelect,
  onDelete,
}: ConversationListProps) {
  if (conversations.length === 0) {
    return (
      <div className={styles.empty}>
        <p>No conversations yet</p>
        <p className="text-sm text-secondary">Start chatting with Nexus AI!</p>
      </div>
    );
  }

  return (
    <div className={styles.list}>
      {conversations.map((conv) => (
        <div
          key={conv.id}
          className={`${styles.item} ${activeId === conv.id ? styles.active : ""}`}
          onClick={() => onSelect(conv.id)}
        >
          <div className={styles.info}>
            <span className={styles.title}>
              {truncate(conv.title || "New conversation", 35)}
            </span>
            <span className={styles.time}>{timeAgo(conv.updated_at)}</span>
          </div>
          <button
            className={styles.deleteBtn}
            onClick={(e) => {
              e.stopPropagation();
              onDelete(conv.id);
            }}
            title="Delete conversation"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
}
