"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { Shell } from "@/components/Shell";
import { useAuth } from "@/components/AuthContext";

interface Assessment {
  id: number;
  title: string;
  description: string | null;
  course_id: number | null;
  topic_id: number | null;
  time_limit_minutes: number | null;
  is_mock_exam: boolean;
  is_ai_generated: boolean;
  created_at: string;
}

export default function AssessmentsPage() {
  const { apiFetch, isAuthenticated, isLoading } = useAuth();
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchAssessments = useCallback(async () => {
    try {
      const res = await apiFetch("/study/assessments");
      if (!res.ok) throw new Error("Failed to load assessments");
      setAssessments(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    }
  }, [apiFetch]);

  useEffect(() => {
    if (!isAuthenticated) return;
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchAssessments();
  }, [fetchAssessments, isAuthenticated]);

  if (isLoading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-muted">Loading your assessments…</p>
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
            Please sign in to access your assessments.
          </p>
          <Link href="/login" className="text-sage-dark hover:text-ink font-medium">
            Sign in
          </Link>
        </div>
      </Shell>
    );
  }

  async function createAssessment() {
    const title = prompt("Enter assessment title");
    if (!title) return;
    try {
      const res = await apiFetch("/study/assessments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
      });
      if (!res.ok) throw new Error("Failed to create assessment");
      fetchAssessments();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Create failed");
    }
  }

  async function startAttempt(assessmentId: number) {
    try {
      const res = await apiFetch(`/study/assessments/${assessmentId}/attempts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) throw new Error("Failed to start attempt");
      const attempt = await res.json();
      // For now, show a simple confirmation
      alert(`Assessment attempt started (ID: ${attempt.id}). Answer submission via API.`);
      fetchAssessments();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Start failed");
    }
  }

  return (
    <Shell>
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="flex items-center justify-between mb-2">
          <div>
            <span className="text-ink font-editorial text-2xl font-semibold">
              Assessments
            </span>
            <p className="text-muted">
              Practice quizzes, mock exams, and progress tracking. Objective
              grading with explanations.
            </p>
          </div>
          <button
            onClick={createAssessment}
            className="bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors flex items-center gap-2"
          >
            <span>+</span> New assessment
          </button>
        </div>

        {error && (
          <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta rounded-md p-4">
            {error}
          </div>
        )}

        {assessments.length === 0 ? (
          <div className="bg-white border border-border rounded-xl p-16 text-center">
            <p className="text-muted">No assessments yet.</p>
            <button
              onClick={createAssessment}
              className="mt-6 bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors"
            >
              Create your first assessment
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {assessments.map((a) => (
              <div
                key={a.id}
                className="bg-white border border-border rounded-xl p-6 hover:border-sage-dark/40 transition-colors"
              >
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-ink">{a.title}</h3>
                    <p className="text-xs text-muted">
                      {a.description || "No description"}
                    </p>
                  </div>
                  <span
                    className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium ${
                      a.is_mock_exam
                        ? "bg-terracotta/10 text-terracotta border border-terracotta/20"
                        : "bg-sage/10 text-sage-dark border border-sage/20"
                    }`}
                  >
                    {a.is_mock_exam ? "Mock Exam" : "Quiz"}
                  </span>
                </div>
                <div className="flex items-center gap-4 text-xs text-muted">
                  <span>{a.course_id ? `Course #${a.course_id}` : "General"}</span>
                  <span>•</span>
                  <span>{new Date(a.created_at).toLocaleDateString()}</span>
                  {a.time_limit_minutes && (
                    <>
                      <span>•</span>
                      <span>{a.time_limit_minutes} min</span>
                    </>
                  )}
                </div>
                <button
                  onClick={() => startAttempt(a.id)}
                  className="mt-4 text-sage-dark hover:text-ink text-sm font-medium underline"
                >
                  Start attempt →
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </Shell>
  );
}
