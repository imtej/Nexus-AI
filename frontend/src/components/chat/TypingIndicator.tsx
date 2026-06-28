import styles from "./TypingIndicator.module.css";

/**
 * TypingIndicator — shows animated dots when Nexus AI is thinking.
 */
export default function TypingIndicator() {
  return (
    <div className={styles.container}>
      <div className={styles.orb} />
      <div className={styles.dots}>
        <span className={styles.dot} />
        <span className={styles.dot} />
        <span className={styles.dot} />
      </div>
    </div>
  );
}
