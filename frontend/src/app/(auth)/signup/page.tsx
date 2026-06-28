"use client";

import { useState, useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";
import styles from "../auth.module.css";

export default function SignupPage() {
  const router = useRouter();
  const pathname = usePathname();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const supabase = createClient();
    
    // Initial check
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session) {
        router.replace("/chat");
      }
    });

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      if (session) {
        router.replace("/chat");
      }
    });

    // Defeat the Browser's bfcache
    const handlePageShow = (event: PageTransitionEvent) => {
      if (event.persisted) {
        window.location.reload();
      }
    };
    window.addEventListener("pageshow", handlePageShow);

    return () => {
      subscription.unsubscribe();
      window.removeEventListener("pageshow", handlePageShow);
    };
  }, [router, pathname]);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const supabase = createClient();
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: displayName,
        },
      },
    });

    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      setSuccess(true);
      setLoading(false);
    }
  };

  const handleGoogleSignup = async () => {
    const supabase = createClient();
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/chat`,
      },
    });
  };

  if (success) {
    return (
      <div className={styles.container}>
        <div className={styles.bgGradient} />
        <div className={styles.card}>
          <div className={styles.header}>
            <div className={styles.logoOrb} />
            <h1>Check your email</h1>
            <p>
              We&apos;ve sent a confirmation link to <strong>{email}</strong>. 
              Click it to start your journey with Nexus AI.
            </p>
          </div>
          <button
            className="btn btn-secondary btn-lg"
            onClick={() => router.push("/login")}
            style={{ width: "100%" }}
          >
            Back to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.bgGradient} />

      <div className={styles.card}>
        <div style={{ marginBottom: "1.5rem", textAlign: "left" }}>
          <Link href="/" style={{ color: "var(--text-secondary)", fontSize: "0.9rem", display: "inline-flex", alignItems: "center", gap: "0.5rem" }}>
            <span>←</span> Back to Home
          </Link>
        </div>
        <div className={styles.header}>
          <div
            className={styles.logoOrb}
            onClick={() => router.push("/")}
          />
          <h1>Begin your journey</h1>
          <p>Create an account to meet Nexus AI — {process.env.NEXT_PUBLIC_FREE_CHAT_LIMIT || "4"} free conversations await</p>
        </div>

        <button
          className={`${styles.googleBtn} btn btn-secondary btn-lg`}
          onClick={handleGoogleSignup}
          style={{ width: "100%" }}
        >
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path d="M17.64 9.205c0-.639-.057-1.252-.164-1.841H9v3.481h4.844a4.14 4.14 0 01-1.796 2.716v2.259h2.908c1.702-1.567 2.684-3.875 2.684-6.615z" fill="#4285F4"/>
            <path d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 009 18z" fill="#34A853"/>
            <path d="M3.964 10.71A5.41 5.41 0 013.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.997 8.997 0 000 9c0 1.452.348 2.827.957 4.042l3.007-2.332z" fill="#FBBC05"/>
            <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 00.957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z" fill="#EA4335"/>
          </svg>
          Continue with Google
        </button>

        <div className={styles.divider}>
          <span>or</span>
        </div>

        <form onSubmit={handleSignup} className={styles.form}>
          <div className={styles.field}>
            <label htmlFor="displayName">Name</label>
            <input
              id="displayName"
              type="text"
              className="input"
              placeholder="What should Nexus AI call you?"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              className="input"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className={styles.field}>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              className="input"
              placeholder="At least 6 characters"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              minLength={6}
              required
            />
          </div>

          {error && <p className={styles.error}>{error}</p>}

          <button
            type="submit"
            className="btn btn-primary btn-lg"
            disabled={loading}
            style={{ width: "100%" }}
          >
            {loading ? "Creating account..." : "Create Account"}
          </button>
          
          <p style={{ fontSize: '12px', color: 'var(--text-tertiary)', textAlign: 'center', marginTop: 'var(--space-md)' }}>
            By continuing, you agree to our <Link href="/terms" style={{ color: 'var(--text-secondary)', textDecoration: 'underline' }}>Terms of Service</Link> and <Link href="/privacy" style={{ color: 'var(--text-secondary)', textDecoration: 'underline' }}>Privacy Policy</Link>.
          </p>
        </form>

        <p className={styles.footer}>
          Already have an account?{" "}
          <Link href="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
