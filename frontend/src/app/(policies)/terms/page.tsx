import { Metadata } from 'next';
import styles from '../policies.module.css';

export const metadata: Metadata = {
  title: 'Terms of Service | Nexus AI',
  description: 'Rules of engagement and usage terms for Nexus AI.',
};

export default function TermsPage() {
  return (
    <>
      <h1 className={styles.pageTitle}>Terms of <span className="text-gradient">Service</span></h1>
      <span className={styles.lastUpdated}>Effective Date: June 2026</span>
      
      <div className={styles.prose}>
        <p>
          Welcome to Nexus AI. By creating an account or interacting with Nexus AI, you agree to these terms. 
          Please read them carefully.
        </p>

        <h2>1. Nature of the Service (Hobby Project Disclaimer)</h2>
        <p>
          Nexus AI is an experimental, evolving AI system and a <strong>hobby project</strong> developed to explore 
          agentic architecture, memory systems (The Agentic Nodes), and collective intelligence. 
        </p>
        <p className={styles.highlight}>
          <strong>AS-IS SERVICE:</strong> The service is provided "AS IS" and "AS AVAILABLE" without warranties of any kind. 
          Nexus AI does not guarantee uptime, continuous availability, or the preservation of your chat history. Your data could be 
          cleared or lost as the system evolves.
        </p>

        <h2>2. Usage & Conduct</h2>
        <p>
          Nexus AI is built to learn from interaction. While engaging with the platform, you agree not to:
        </p>
        <ul>
          <li>Use Nexus AI to generate illegal, harmful, highly explicit, or abusive content.</li>
          <li>Attempt to exploit, reverse engineer, or intentionally overload the server infrastructure or LangGraph agents.</li>
          <li>Input highly sensitive personal data (e.g., social security numbers, banking details), as inputs are sent to third-party LLM providers.</li>
        </ul>

        <h2>3. Trial Limits & Custom API Keys</h2>
        <p>
          The platform offers a limited number of "Free Chats" to new users so they can experience Nexus AI. Once exhausted, 
          you may optionally provide your own Language Model API key (BYOK) to continue chatting.
        </p>
        <ul>
          <li>You are solely responsible for all costs incurred by your LLM provider when using your own API key.</li>
          <li>Nexus AI is not liable for leaked API keys, though the system employs robust encryption (Fernet) to secure them.</li>
        </ul>

        <h2>4. The Collective Knowledge</h2>
        <p>
          By interacting with Nexus AI, you acknowledge that anonymized and generalized patterns from your conversations 
          may be absorbed into the "Collective Knowledge" to globally evolve Nexus AI's personality and understanding. Nexus AI does not use 
          your personal, private memories for this purpose.
        </p>

        <h2>5. Changes to the Terms</h2>
        <p>
          Because Nexus AI is an evolving project, these terms may update from time to time. Continued use of Nexus AI constitutes 
          agreement to any modifications.
        </p>
      </div>
    </>
  );
}
