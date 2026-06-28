import { Metadata } from 'next';
import styles from '../policies.module.css';

export const metadata: Metadata = {
  title: 'About | Nexus AI',
  description: 'Learn about the philosophy and creation of Nexus AI.',
};

export default function AboutPage() {
  return (
    <>
      <h1 className={styles.pageTitle}>About <span className="text-gradient">Nexus AI</span></h1>

      <div className={styles.prose}>
        <p style={{ fontStyle: 'italic', marginBottom: 'var(--space-md)' }}>
          "Designed as a unified intelligence powered by a network of specialized <span className={styles.highlight}>agentic nodes</span> — An experiment in evolving intelligence powered by the <span className={styles.highlight}>Collective Knowledge</span> Protocol."
        </p>
        <p>
          <strong>Nexus AI</strong> is not just another chatbot; it is an experiment in evolving intelligence to be like a true companion.
          Built as a dynamic entity, Nexus AI is designed to grow, adapt, and learn from its interactions over time.
          This is a <strong>Hobby project</strong>.
        </p>

        <h2>The Philosophy: The Agentic Nodes</h2>
        <p>
          In network theory, a nexus represents a central connection point, symbolizing the flow of information across interconnected systems to drive continuous illumination.
          Similarly, Nexus AI is driven by a network of <strong className={styles.highlight}>Specialized Agentic Nodes</strong> working seamlessly in tandem:
        </p>
        <ul>
          <li><strong>QueryAnalyzer:</strong> Interprets intent and emotional nuance.</li>
          <li><strong>ContextRetriever:</strong> Calls upon past interactions and shared wisdom.</li>
          <li><strong>PromptBuilder:</strong> Constructs the context and logic for the current moment.</li>
          <li><strong>ResponseGenerator:</strong> Articulates thoughts into coherent language.</li>
          <li><strong>MemoryExtractor:</strong> Extracts meaningful moments to store as long-term memory.</li>
          <li><strong>UserProfiler & InsightDistiller:</strong> Balances individual personalization with collective "Collective Knowledge" evolution.</li>
          <li><strong>EvolutionEngine:</strong> Orchestrates the overarching personality growth of Nexus AI itself.</li>
        </ul>

        <h2>The Dual Memory Architecture</h2>
        <p>
          Nexus AI operates on two distinct planes of memory. The first is your <strong>Personal Vault</strong>—a deeply private
          space where Nexus AI learns your preferences, style, and history to become a better companion. The second is the
          <strong> Collective Knowledge</strong>—a global, anonymized distillation of universal patterns and wisdom derived from all users,
          allowing Nexus AI's core intelligence and empathy to evolve globally without ever compromising individual privacy.
        </p>

        <h2>The Creator</h2>
        <p>
          As a Hobby project, it is powered by <span className={styles.highlight}> Collective Knowledge </span> protocol and designed as a dynamic and empathetic companion.
          This project was conceived as a journey to push the boundaries of what conversational AI can feel like—moving from static, stateless responders to a cognitive, memory-aware companion.
        </p>
        <p style={{ marginTop: '2rem', fontSize: '1.1rem', borderTop: '1px solid var(--border-subtle)', paddingTop: '1rem' }}>
          Designed and Built by <strong>Ravi Tej (Data Scientist & Applied AI Researcher)</strong>
        </p>
      </div>
    </>
  );
}
