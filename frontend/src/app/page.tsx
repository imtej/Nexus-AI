"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";
import styles from "./page.module.css";

export default function LandingPage() {
  const router = useRouter();
  const [isLoaded, setIsLoaded] = useState(false);
  const [evolution, setEvolution] = useState({
    total_interactions: 0,
    total_users: 0,
    evolution_stage: "nascent",
    personality_version: "1.0.0",
  });

  useEffect(() => {
    setIsLoaded(true);

    // Check if already logged in
    const supabase = createClient();
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session) {
        router.replace("/chat");
      }
    });

    // Fetch evolution stats
    fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/evolution`)
      .then((r) => r.json())
      .catch(() => ({}))
      .then((data) => {
        if (data.total_interactions !== undefined) {
          setEvolution(data);
        }
      });
  }, []);

  return (
    <div className={styles.container}>
      {/* Ambient Background */}
      <div className={styles.bgGradient} />
      <div className={styles.bgOrbs}>
        <div className={styles.orb1} />
        <div className={styles.orb2} />
        <div className={styles.orb3} />
      </div>
      <div className={styles.gridOverlay} />

      {/* Header */}
      <header className={styles.header}>
        <div className={styles.logo}>
          <div className={styles.logoOrb} />
          <span className={styles.logoText}>Nexus AI</span>
        </div>
        <nav className={styles.nav}>
          <button
            className="btn btn-ghost"
            onClick={() => router.push("/login")}
          >
            Log in
          </button>
          <button
            className="btn btn-primary"
            onClick={() => router.push("/signup")}
          >
            Get Started
          </button>
        </nav>
      </header>

      {/* Hero Section */}
      <main className={`${styles.hero} ${isLoaded ? styles.heroVisible : ""}`}>
        <div className={styles.heroOrb}>
          <div className={styles.heroOrbInner} />
          <div className={styles.heroOrbRing} />
          <div className={styles.heroOrbRing2} />
        </div>

        <h1 className={styles.heroTitle}>
          Meet <span className="text-gradient">Nexus AI</span>
        </h1>

        <p className={styles.heroSubtitle}>
          An AI that{" "}
          <span className={styles.highlight}>evolves</span> with every
          conversation. Powered by the <span className={styles.highlight}>Collective Knowledge</span> Protocol — collective
          intelligence, personal memory, genuine connection.
        </p>

        <div className={styles.heroCta}>
          <button
            className="btn btn-primary btn-lg"
            onClick={() => router.push("/signup")}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
            Start Chatting — It&apos;s Free
          </button>
          <p className={styles.ctaNote}>
            1000 free conversations, no credit card or API Key needed
          </p>
        </div>

        {/* Evolution Stats */}
        <div className={styles.stats}>
          <div className={styles.statCard}>
            <span className={styles.statValue}>
              {evolution.total_interactions.toLocaleString()}
            </span>
            <span className={styles.statLabel}>Conversations</span>
          </div>
          <div className={styles.statDivider} />
          <div className={styles.statCard}>
            <span className={styles.statValue}>
              {evolution.total_users.toLocaleString()}
            </span>
            <span className={styles.statLabel}>Minds Connected</span>
          </div>
          <div className={styles.statDivider} />
          <div className={styles.statCard}>
            <span className={styles.statValue}>
              v{evolution.personality_version}
            </span>
            <span className={styles.statLabel}>
              {evolution.evolution_stage.charAt(0).toUpperCase() +
                evolution.evolution_stage.slice(1)}
            </span>
          </div>
        </div>
      </main>

      {/* Features */}
      <section className={`${styles.features} ${isLoaded ? styles.featuresVisible : ""}`}>
        <div className={styles.featureCard}>
          <div className={styles.featureIcon}>🧬</div>
          <h3>Evolving Intelligence</h3>
          <p>
            Nexus AI grows wiser with every conversation across all users. Watch
            its personality evolve in real-time.
          </p>
        </div>
        <div className={styles.featureCard}>
          <div className={styles.featureIcon}>🧠</div>
          <h3>Personal Memory</h3>
          <p>
            Nexus AI remembers you — your preferences, your stories, what
            matters to you. Like a friend who truly listens.
          </p>
        </div>
        <div className={styles.featureCard}>
          <div className={styles.featureIcon}>⚡</div>
          <h3>Agentic Nodes</h3>
          <p>
            A network of specialized AI agents work in harmony — analyzing queries, retrieving context,
            building prompts, generating responses, and extracting memory.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className={styles.footer}>
        <div className={styles.footerContent}>
          <div className={styles.footerColumn}>
            <h4><span className="text-gradient">Nexus AI</span></h4>
            <p>
              Designed as a unified intelligence powered by a network of specialized <span style={{ color: "var(--accent-primary)" }}>agentic nodes</span> — An experiment in evolving intelligence powered by the <span style={{ color: "var(--accent-primary)" }}>Collective Knowledge</span> Protocol.
            </p>
          </div>
          <div className={styles.footerColumn}>
            <h4>Project</h4>
            <Link href="/about" className={styles.footerLink}>About Nexus AI</Link>
            <Link href="https://github.com/imtej/Nexus-AI" className={styles.footerLink} target="_blank" rel="noopener noreferrer">GitHub Repository</Link>
          </div>
          <div className={styles.footerColumn}>
            <h4>Legal & Transparency</h4>
            <Link href="/privacy" className={styles.footerLink}>Privacy & Transparency</Link>
            <Link href="/terms" className={styles.footerLink}>Terms of Service</Link>
          </div>
        </div>

        <div className={styles.footerBottom}>
          <p>© {new Date().getFullYear()} Nexus AI: The Collective Knowledge Protocol</p>
        </div>
      </footer>
    </div>
  );
}
