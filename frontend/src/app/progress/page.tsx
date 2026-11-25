"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { Shell } from "@/components/Shell";
import { useAuth } from "@/components/AuthContext";

interface TopicMastery {
  id: number;
  topic_id: number;
  estimated_mastery: number;
  confidence: number;
  evidence_count: number;
  last_interaction_at: string | null;
}

export default function ProgressPage() {
  const { apiFetch, isAuthenticated, isLoading } = useAuth();
  const [mastery, setMastery] = useState<TopicMastery[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchMastery = useCallback(async () => {
    try {
      const res = await apiFetch("/study/mastery");
      if (!res.ok) throw new Error("Failed to load progress");
      setMastery(await res.json());
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    }
  }, [apiFetch]);

  useEffect(() => {
    if (!isAuthenticated) return;
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchMastery();
  }, [fetchMastery, isAuthenticated]);

  if (isLoading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-muted">Loading your progress…</p>
        </div>
      </Shell>
    );
  }

  if (!isAuthenticated) {
    return (
      <Shell>
        <div className="max-w-md mx-auto text-center py-20 bg-paper text-ink p-6">
          <h2 className="text-xl font-semibold mb-3">Sign in required</h2>
          <p className="text-muted mb-6">
            Please sign in to view your progress.
          </p>
          <Link href="/login" className="text-sage-dark hover:text-ink font-medium">
            Sign in
          </Link>
        </div>
      </Shell>
    );
  }

  const average = mastery.length
    ? mastery.reduce((sum, m) => sum + m.estimated_mastery, 0) / mastery.length
    : 0;

  return (
    <Shell>
      <div className="max-w-4xl mx-auto space-y-8">
        <div>
          <span className="text-ink font-editorial text-2xl font-semibold">
            Progress
          </span>
          <p className="text-muted">
            Your evidence-based mastery across topics. Mastery updates from
            actual assessment and review activity, not predictions.
          </p>
        </div>

        {error && (
          <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta rounded-md p-4">
            {error}
          </div>
        )}

        <div className="bg-white border border-border rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-semibold text-ink">Overall Mastery</h3>
              <p className="text-sm text-muted">
                Average across {mastery.length} assessed topic(s)
              </p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-mono font-bold text-ink">
                {(average * 100).toFixed(0)}%
              </div>
              <p className="text-xs text-muted">evidence-based estimate</p>
            </div>
          </div>
          <div className="w-full bg-surface rounded-full h-2 mb-4">
            <div
              className="bg-sage-dark h-2 rounded-full transition-all duration-500"
              style={{ width: `${Math.round(average * 100)}%` }}
            ></div>
          </div>
        </div>

        {mastery.length === 0 ? (
          <div className="bg-white border border-border rounded-xl p-16 text-center">
            <p className="text-muted">
              No mastery data yet. Complete assessments and flashcard reviews
              to build your topic mastery profile.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {mastery.map((m) => (
              <div
                key={m.topic_id}
                className="bg-white border border-border rounded-xl p-5"
              >
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-ink">Topic #{m.topic_id}</h4>
                  <span className="text-xs font-mono text-muted">
                    {m.evidence_count} evidence point(s)
                  </span>
                </div>
                <div className="w-full bg-surface rounded-full h-2 mb-2">
                  <div
                    className="bg-sage-dark h-2 rounded-full"
                    style={{ width: `${Math.round(m.estimated_mastery * 100)}%` }}
                  ></div>
                </div>
                <div className="flex justify-between text-xs text-muted">
                  <span>
                    Mastery: {(m.estimated_mastery * 100).toFixed(0)}%
                  </span>
                  <span>
                    Confidence: {(m.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Shell>
  );
}
