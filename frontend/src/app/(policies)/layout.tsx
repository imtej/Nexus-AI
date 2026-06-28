import Link from "next/link";
import styles from "./policies.module.css";

export default function PoliciesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className={styles.container}>
      {/* Background Ambience */}
      <div className={styles.bgGradient} />
      <div className={styles.bgOrbs}>
        <div className={styles.orb1} />
        <div className={styles.orb2} />
      </div>

      {/* Navigation */}
      <nav className={styles.nav}>
        <Link href="/" className={styles.backBtn}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
          Back to Nexus AI
        </Link>
      </nav>

      {/* Content wrapper */}
      <main className={styles.contentWrapper}>
        <div className={styles.glassCard}>
          {children}
        </div>
      </main>
    </div>
  );
}
