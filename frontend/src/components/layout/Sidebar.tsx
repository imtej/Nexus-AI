"use client";

import { useRouter } from "next/navigation";
import styles from "./Sidebar.module.css";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

/**
 * Sidebar — collapsible sidebar wrapper for the dashboard.
 */
export default function Sidebar({ isOpen, onClose, children }: SidebarProps) {
  const router = useRouter();

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && <div className={styles.overlay} onClick={onClose} />}

      <aside className={`${styles.sidebar} ${isOpen ? styles.open : ""}`}>
        <div className={styles.header}>
          <div className={styles.logo} onClick={() => router.push("/")}>
            <div className={styles.logoOrb} />
            <span>Nexus AI</span>
          </div>
          <button className="btn btn-ghost btn-icon" onClick={onClose} title="Close sidebar">
            ✕
          </button>
        </div>

        {children}
      </aside>
    </>
  );
}
