"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";
import { api } from "@/lib/api";
import styles from "./settings.module.css";

export default function SettingsPage() {
  const router = useRouter();
  const [token, setToken] = useState("");
  const [provider, setProvider] = useState("gemini");
  const [apiKey, setApiKey] = useState("");
  const [hasApiKey, setHasApiKey] = useState(false);
  const [freeChats, setFreeChats] = useState(0);
  const [hiveMindOptIn, setHiveMindOptIn] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const supabase = createClient();
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (!session) {
        router.push("/login");
        return;
      }
      setToken(session.access_token);

      api.getProfile(session.access_token).then((data) => {
        const profile = data.profile;
        setProvider(profile.llm_provider || "gemini");
        setHasApiKey(profile.has_api_key || false);
        setFreeChats(profile.free_chats_remaining || 0);
        setHiveMindOptIn(profile.collective_knowledge_opt_in ?? true);
      }).catch(() => {});
    });
  }, []);

  const handleSaveApiKey = async () => {
    if (!apiKey.trim() || !token) return;
    setSaving(true);
    setMessage("");

    try {
      await api.setApiKey(provider, apiKey.trim(), token);
      setHasApiKey(true);
      setApiKey("");
      setMessage("API key saved successfully! You now have unlimited chats.");
    } catch (err) {
      setMessage(`Error: ${err instanceof Error ? err.message : "Failed to save"}`);
    }
    setSaving(false);
  };

  const handleRemoveApiKey = async () => {
    if (!token) return;
    try {
      await api.removeApiKey(token);
      setHasApiKey(false);
      setMessage("API key removed.");
    } catch (err) {
      setMessage(`Error: ${err instanceof Error ? err.message : "Failed to remove"}`);
    }
  };

  const handleToggleHiveMind = async () => {
    if (!token) return;
    const newValue = !hiveMindOptIn;
    setHiveMindOptIn(newValue);
    await api.updateProfile({ collective_knowledge_opt_in: newValue }, token);
  };

  const handleLogout = async () => {
    const supabase = createClient();
    await supabase.auth.signOut();
    router.push("/");
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <button className="btn btn-ghost" onClick={() => router.push("/chat")}>
          ← Back to Chat
        </button>
        <h1>Settings</h1>
        <div style={{ width: 100 }} />
      </header>

      <main className={styles.content}>
        {/* API Key Section */}
        <section className={styles.section}>
          <h2>🔑 LLM API Key</h2>
          <p className="text-secondary text-sm">
            {hasApiKey
              ? "You have an API key configured. You have unlimited chats."
              : freeChats > 0
              ? `You have ${freeChats} free chats remaining. Add your API key for unlimited access.`
              : "Your free trial has ended. Add your API key to continue."}
          </p>

          <div className={styles.providerSelect}>
            <label>Provider</label>
            <div className={styles.providerOptions}>
              {[
                { id: "gemini", label: "Google Gemini" },
                { id: "openai", label: "OpenAI" },
                { id: "anthropic", label: "Anthropic Claude" },
              ].map((p) => (
                <button
                  key={p.id}
                  className={`${styles.providerBtn} ${
                    provider === p.id ? styles.providerActive : ""
                  }`}
                  onClick={() => setProvider(p.id)}
                >
                  {p.label}
                </button>
              ))}
            </div>
          </div>

          <div className={styles.apiKeyInput}>
            <input
              type="password"
              className="input"
              placeholder={
                hasApiKey
                  ? "••••••••••••••••"
                  : `Enter your ${provider} API key`
              }
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
            <button
              className="btn btn-primary"
              onClick={handleSaveApiKey}
              disabled={!apiKey.trim() || saving}
            >
              {saving ? "Saving..." : "Save Key"}
            </button>
          </div>

          {hasApiKey && (
            <button
              className="btn btn-ghost btn-sm"
              onClick={handleRemoveApiKey}
              style={{ color: "var(--accent-red)" }}
            >
              Remove API Key
            </button>
          )}

          {message && (
            <p
              className={styles.message}
              style={{
                color: message.startsWith("Error")
                  ? "var(--accent-red)"
                  : "var(--accent-green)",
              }}
            >
              {message}
            </p>
          )}
        </section>

        {/* Collective Knowledge */}
        <section className={styles.section}>
          <h2>🧬 Collective Knowledge</h2>
          <p className="text-secondary text-sm">
            When enabled, Nexus AI may distill anonymized insights from your
            conversations to enrich the global Collective Knowledge. No personal data is shared.
          </p>
          <label className={styles.toggle}>
            <input
              type="checkbox"
              checked={hiveMindOptIn}
              onChange={handleToggleHiveMind}
            />
            <span className={styles.toggleSlider} />
            <span>Contribute to the Collective Knowledge</span>
          </label>
        </section>

        {/* Legal & Transparency */}
        <section className={styles.section}>
          <h2>⚖️ Legal & Transparency</h2>
          <p className="text-secondary text-sm" style={{ marginBottom: "var(--space-md)" }}>
            Review how your data is handled and the rules of engagement for interacting with Nexus AI.
          </p>
          <div style={{ display: "flex", gap: "var(--space-md)" }}>
            <Link href="/privacy" className="btn btn-secondary btn-sm">Privacy Policy</Link>
            <Link href="/terms" className="btn btn-secondary btn-sm">Terms of Service</Link>
          </div>
        </section>

        {/* Account */}
        <section className={styles.section}>
          <h2>Account</h2>
          <button className="btn btn-secondary" onClick={handleLogout}>
            Sign Out
          </button>
        </section>
      </main>
    </div>
  );
}
