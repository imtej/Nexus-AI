"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import styles from "./evolution.module.css";

interface EvolutionData {
  personality_version: string;
  evolution_stage: string;
  total_interactions: number;
  total_users: number;
  empathy_depth: number;
  knowledge_breadth: number;
  wisdom_score: number;
  curiosity_level: number;
  evolution_percentage: number;
  last_evolution_at: string | null;
}

const STAGE_COLORS: Record<string, string> = {
  nascent: "#6c63ff",
  growing: "#a29bfe",
  mature: "#f0b429",
  transcendent: "#ff6b6b",
};

const STAGE_LABELS: Record<string, string> = {
  nascent: "🌱 Nascent — Young & Curious",
  growing: "🌿 Growing — Forming Insights",
  mature: "🌳 Mature — Deeply Understanding",
  transcendent: "✨ Transcendent — Profound Wisdom",
};

export default function EvolutionPage() {
  const router = useRouter();
  const [evolution, setEvolution] = useState<EvolutionData | null>(null);

  useEffect(() => {
    // Auth check
    const supabase = createClient();
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (!session) router.push("/login");
    });

    // Fetch evolution
    fetch(
      `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/evolution`
    )
      .then((r) => r.json())
      .then((data) => setEvolution(data))
      .catch(() => {});
  }, []);

  if (!evolution) {
    return (
      <div className={styles.loading}>
        <div className={styles.loadingOrb} />
        <p>Loading evolution data...</p>
      </div>
    );
  }

  const stageColor = STAGE_COLORS[evolution.evolution_stage] || STAGE_COLORS.nascent;

  return (
    <div className={styles.container}>
      <div className={styles.bgGradient} />

      <header className={styles.header}>
        <button className="btn btn-ghost" onClick={() => router.push("/chat")}>
          ← Back to Chat
        </button>
        <h1>Nexus AI&apos;s Evolution</h1>
        <div style={{ width: 100 }} />
      </header>

      <main className={styles.content}>
        {/* Central Orb */}
        <div className={styles.orbSection}>
          <div
            className={styles.evolutionOrb}
            style={{
              background: `linear-gradient(135deg, ${stageColor}, var(--accent-warm))`,
              boxShadow: `0 0 60px ${stageColor}40, 0 0 120px ${stageColor}20`,
            }}
          />
          <h2 style={{ color: stageColor }}>
            {STAGE_LABELS[evolution.evolution_stage]}
          </h2>
          <p className="text-secondary">
            Version {evolution.personality_version}
          </p>
        </div>

        {/* Stats Grid */}
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <div className={styles.statHeader}>
              <span className={styles.statEmoji}>💜</span>
              <span>Empathy Depth</span>
            </div>
            <div className={styles.progressBar}>
              <div
                className={styles.progressFill}
                style={{
                  width: `${evolution.empathy_depth * 100}%`,
                  background: "#a29bfe",
                }}
              />
            </div>
            <span className={styles.statPercent}>
              {(evolution.empathy_depth * 100).toFixed(1)}%
            </span>
          </div>

          <div className={styles.statCard}>
            <div className={styles.statHeader}>
              <span className={styles.statEmoji}>📚</span>
              <span>Knowledge Breadth</span>
            </div>
            <div className={styles.progressBar}>
              <div
                className={styles.progressFill}
                style={{
                  width: `${evolution.knowledge_breadth * 100}%`,
                  background: "#45aaf2",
                }}
              />
            </div>
            <span className={styles.statPercent}>
              {(evolution.knowledge_breadth * 100).toFixed(1)}%
            </span>
          </div>

          <div className={styles.statCard}>
            <div className={styles.statHeader}>
              <span className={styles.statEmoji}>🦉</span>
              <span>Wisdom Score</span>
            </div>
            <div className={styles.progressBar}>
              <div
                className={styles.progressFill}
                style={{
                  width: `${evolution.wisdom_score * 100}%`,
                  background: "#f0b429",
                }}
              />
            </div>
            <span className={styles.statPercent}>
              {(evolution.wisdom_score * 100).toFixed(1)}%
            </span>
          </div>

          <div className={styles.statCard}>
            <div className={styles.statHeader}>
              <span className={styles.statEmoji}>✨</span>
              <span>Curiosity Level</span>
            </div>
            <div className={styles.progressBar}>
              <div
                className={styles.progressFill}
                style={{
                  width: `${evolution.curiosity_level * 100}%`,
                  background: "#2ed573",
                }}
              />
            </div>
            <span className={styles.statPercent}>
              {(evolution.curiosity_level * 100).toFixed(1)}%
            </span>
          </div>
        </div>

        {/* Counters */}
        <div className={styles.counters}>
          <div className={styles.counterCard}>
            <span className={styles.counterValue}>
              {evolution.total_interactions.toLocaleString()}
            </span>
            <span className={styles.counterLabel}>Total Conversations</span>
          </div>
          <div className={styles.counterCard}>
            <span className={styles.counterValue}>
              {evolution.total_users.toLocaleString()}
            </span>
            <span className={styles.counterLabel}>Minds Connected</span>
          </div>
          <div className={styles.counterCard}>
            <span className={styles.counterValue}>
              {evolution.evolution_percentage.toFixed(1)}%
            </span>
            <span className={styles.counterLabel}>Overall Evolution</span>
          </div>
        </div>
      </main>
    </div>
  );
}
