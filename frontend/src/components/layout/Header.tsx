"use client";

import styles from "./Header.module.css";

interface HeaderProps {
  title?: string;
  onMenuClick?: () => void;
  rightAction?: React.ReactNode;
}

/**
 * Header — mobile-first top bar with menu toggle and optional right action.
 */
export default function Header({ title, onMenuClick, rightAction }: HeaderProps) {
  return (
    <header className={styles.header}>
      {onMenuClick && (
        <button className="btn btn-ghost btn-icon" onClick={onMenuClick}>
          ☰
        </button>
      )}
      <span className={styles.title}>{title || "Nexus AI"}</span>
      <div className={styles.right}>{rightAction || <div style={{ width: 36 }} />}</div>
    </header>
  );
}
