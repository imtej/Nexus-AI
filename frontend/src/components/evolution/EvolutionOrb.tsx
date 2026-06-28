"use client";

import { getStageColor } from "@/lib/utils";
import styles from "./EvolutionOrb.module.css";

interface EvolutionOrbProps {
  stage: string;
  size?: number;
}

/**
 * EvolutionOrb — animated gradient orb that changes color based on System's evolution stage.
 */
export default function EvolutionOrb({ stage, size = 120 }: EvolutionOrbProps) {
  const color = getStageColor(stage);

  return (
    <div className={styles.container} style={{ width: size, height: size }}>
      <div
        className={styles.orb}
        style={{
          background: `linear-gradient(135deg, ${color}, var(--accent-warm))`,
          boxShadow: `0 0 ${size * 0.4}px ${color}40, 0 0 ${size * 0.8}px ${color}20`,
        }}
      />
      <div
        className={styles.ring}
        style={{ borderColor: `${color}40` }}
      />
      <div
        className={styles.outerRing}
        style={{ borderColor: `${color}20` }}
      />
    </div>
  );
}
