import { Metadata } from 'next';
import styles from '../policies.module.css';

export const metadata: Metadata = {
  title: 'Privacy Policy | Nexus AI',
  description: 'How Nexus AI handles your data, memory, and API keys.',
};

export default function PrivacyPage() {
  return (
    <>
      <h1 className={styles.pageTitle}>Privacy & <span className="text-gradient">Transparency</span></h1>
      <span className={styles.lastUpdated}>Effective Date: June 2026</span>
      
      <div className={styles.prose}>
        <p>
          At Nexus AI, transparency is as important as the intelligence Nexus AI is building. 
          Because Nexus AI is an AI companion designed to remember and evolve, handling your data with respect and absolute security is its architectural foundation.
        </p>

        <h2>1. How I Remember You (Personal Memory)</h2>
        <p>
          When you speak with Nexus AI, two distinct agents—<strong>the MemoryExtractor node</strong> and <strong>the UserProfiler node</strong>—process your conversations to extract meaningful personal memories (e.g., your preferences, your coding style, your stories).
        </p>
        <p>
          These memories are encrypted and stored in a private vault within Nexus AI's database. <strong>Only your authenticated account can access your personal memories.</strong> They are never used to directly prompt or assist other users.
        </p>

        <h2>2. The Collective Knowledge Protocol</h2>
        <p>
          To allow Nexus AI's core personality to evolve, <strong>the InsightDistiller node</strong> periodically reviews non-personal interaction patterns across the platform. 
          This process distills interactions into <em>anonymized, generalized insights</em> (e.g., "Users find empathetic responses more helpful during debugging"). 
          No personally identifiable information (PII) ever enters the Collective Knowledge.
        </p>

        <h2>3. Bring Your Own Key (BYOK) Security</h2>
        <p>
          If you choose to use your own LLM API Key to bypass trial limits, your key is immediately encrypted at the server level using an industry-standard <strong>Fernet Symmetric-Key Encryption</strong> algorithm before touching the database. 
          It is only decrypted in memory for the fraction of a second required to send a request to the LLM provider. Nexus AI's creators cannot view your raw API key.
        </p>

        <h2>4. Data Sovereignty</h2>
        <p>
          You own your conversations. While this is currently a hobby project, Nexus AI intends to provide full self-service tools for you to delete your personal memory nodes, wipe your chat history, or remove your profile and API keys entirely at any time.
        </p>

        <h2>5. Third-Party Providers</h2>
        <p>
          Nexus AI uses external LLM providers (like Google Gemini and OpenAI) to process text and generate responses. 
          By using Nexus AI, you acknowledge that your prompt data is transmitted to these providers for inference. Please review their respective privacy policies regarding data retention for API inputs.
        </p>
      </div>
    </>
  );
}
