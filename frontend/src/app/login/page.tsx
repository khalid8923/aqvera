"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Shell } from "@/components/Shell";
import { useAuth } from "@/components/AuthContext";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") || "/dashboard";
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login(email, password);
      router.push(callbackUrl);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Login failed";
      setError(message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Shell>
      <div className="max-w-md mx-auto space-y-8 p-6">
        <div className="flex items-center gap-2 mb-6">
          <span className="text-ink font-editorial text-2xl font-semibold tracking-tight">
            AQVERA
          </span>
        </div>

        <h1 className="text-3xl font-editorial font-semibold text-center text-ink">
          Welcome back
        </h1>

        {error && (
          <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta rounded-md p-4 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium mb-1 text-ink">Email address</label>
            <input
              type="email"
              required
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none text-ink"
              placeholder="you@university.edu"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1 text-ink">Password</label>
            <input
              type="password"
              required
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none text-ink"
            />
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {submitting ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p className="text-center text-sm text-muted">
          Don&apos;t have an account?{" "}
          <Link href="/register" className="text-sage-dark hover:text-ink font-medium">
            Create an account
          </Link>
        </p>
      </div>
    </Shell>
  );
}
