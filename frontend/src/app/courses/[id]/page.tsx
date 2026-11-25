"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Shell } from "@/components/Shell";
import { Dialog } from "@/components/Dialog";
import { useAuth } from "@/components/AuthContext";

interface Course {
  id: number;
  title: string;
  university: string | null;
  department: string | null;
  course_code: string | null;
  semester: string | null;
  description: string | null;
  primary_language: string;
  subject_domain: string | null;
  is_archived: boolean;
}

interface Conversation {
  id: number;
  title: string;
  course_id: number | null;
  owner_id: number;
  created_at: string;
  updated_at: string;
  messages: { id: number; role: string; content: string }[];
}

export default function CourseWorkspacePage({
  params,
}: { params: Promise<{ id: string }> }) {
  const router = useRouter();
  const { apiFetch, isAuthenticated, isLoading } = useAuth();
  const [course, setCourse] = useState<Course | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [newTitle, setNewTitle] = useState("");

  useEffect(() => {
    if (!isAuthenticated) return;
    let cancelled = false;
    async function load() {
      try {
        const { id } = await params;
        const courseId = parseInt(id, 10);
        setLoading(true);
        const courseRes = await apiFetch(
          `/api/courses/${courseId}`
        );
        if (!courseRes.ok) {
          if (!cancelled) setError("Course not found");
          return;
        }
        if (!cancelled) setCourse(await courseRes.json());

        const convRes = await apiFetch(
          `/api/conversations?course_id=${courseId}`
        );
        if (!cancelled && convRes.ok) {
          setConversations(await convRes.json());
        }
      } catch {
        if (!cancelled) setError("Failed to load course");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, [params, apiFetch, isAuthenticated]);

  if (isLoading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-96 p-6 bg-paper text-ink">
          <p className="text-muted">Loading your account…</p>
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
            Please sign in to access your course workspace.
          </p>
          <Link href="/login" className="text-sage-dark hover:text-ink font-medium">
            Sign in
          </Link>
        </div>
      </Shell>
    );
  }

  if (loading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-96 p-6 bg-paper text-ink">
          <p className="text-muted">Loading course…</p>
        </div>
      </Shell>
    );
  }

  if (error || !course) {
    return (
      <Shell>
        <div className="max-w-3xl mx-auto text-center py-20 bg-paper text-ink p-6">
          <h2 className="text-xl font-semibold mb-3">{error || "Course not found"}</h2>
          <Link href="/courses" className="text-sage-dark hover:text-ink underline">
            Return to course library
          </Link>
        </div>
      </Shell>
    );
  }

  const { id: courseId } = course;

  async function handleCreateConversation(e: React.FormEvent) {
    e.preventDefault();
    if (!newTitle.trim()) return;
    try {
      const res = await apiFetch("/api/conversations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newTitle, course_id: courseId }),
      });
      if (!res.ok) throw new Error("Failed to create conversation");
      const conv = await res.json();
      setConversations((prev) => [conv, ...prev]);
      setNewTitle("");
      setModalOpen(false);
      router.push(`/chat/${conv.id}?course=${courseId}`);
    } catch {
      // error handled by UI
    }
  }

  return (
    <Shell>
      <div className="max-w-5xl mx-auto space-y-8 p-0 bg-paper text-ink min-h-screen">
        <nav className="flex items-center gap-1 text-xs text-muted mb-6">
          <Link href="/courses" className="hover:text-ink">
            Course Library
          </Link>
          <span>/</span>
          <span className="text-ink">{course.title}</span>
        </nav>

        <div className="bg-white border border-border rounded-xl p-8 mb-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="font-editorial text-2xl font-semibold mb-1">
                {course.title}
              </h1>
              {course.subject_domain && (
                <p className="text-xs text-muted uppercase tracking-wider">
                  {course.subject_domain}
                </p>
              )}
            </div>
            <button
              onClick={() => setModalOpen(true)}
              className="bg-ink text-white px-4 py-2 rounded-md text-xs font-medium hover:bg-navy transition-colors flex items-center gap-1"
            >
              <span>+</span> New chat
            </button>
          </div>
          <div className="grid md:grid-cols-4 gap-4 text-sm">
            <div className="p-4 rounded border border-border bg-surface">
              <div className="text-xs text-muted uppercase tracking-wider mb-1">
                University
              </div>
              <div className="text-ink">{course.university || "—"}</div>
            </div>
            <div className="p-4 rounded border border-border bg-surface">
              <div className="text-xs text-muted uppercase tracking-wider mb-1">
                Department
              </div>
              <div className="text-ink">{course.department || "—"}</div>
            </div>
            <div className="p-4 rounded border border-border bg-surface">
              <div className="text-xs text-muted uppercase tracking-wider mb-1">
                Semester
              </div>
              <div className="text-ink">{course.semester || "—"}</div>
            </div>
            <div className="p-4 rounded border border-border bg-surface">
              <div className="text-xs text-muted uppercase tracking-wider mb-1">
                Language
              </div>
              <div className="text-ink">{course.primary_language}</div>
            </div>
          </div>
        </div>

        <section>
          <h2 className="font-semibold mb-4">Conversations</h2>
          {conversations.length > 0 ? (
            <div className="space-y-3">
              {conversations.map((conv) => (
                <Link
                  key={conv.id}
                  href={`/chat/${conv.id}?course=${courseId}`}
                  className="flex items-center justify-between bg-white border border-border rounded-xl px-5 py-4 hover:border-sage-dark/40 transition-colors block"
                >
                  <div>
                    <h3 className="font-semibold text-ink">{conv.title}</h3>
                    <p className="text-xs text-muted">
                      {new Date(conv.updated_at).toLocaleString(undefined, {
                        month: "short",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                  <span className="text-xs text-muted">→</span>
                </Link>
              ))}
            </div>
          ) : (
            <div className="bg-white border border-border rounded-xl p-12 text-center">
              <div className="w-12 h-12 rounded-full bg-surface flex items-center justify-center mx-auto mb-4">
                💬
              </div>
              <h3 className="font-medium text-ink mb-2">No conversations yet</h3>
              <p className="text-sm text-muted mb-4">
                Start a new conversation to begin learning this course.
              </p>
            </div>
          )}
        </section>

        {/* New chat modal */}
        <Dialog open={modalOpen} onClose={() => setModalOpen(false)} title="New conversation">
          <form onSubmit={handleCreateConversation}>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Conversation title</label>
                <input
                  name="title"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  defaultValue={`New chat — ${course.title}`}
                  className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                />
              </div>
              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="px-4 py-2 text-muted border border-border rounded-md hover:bg-surface"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!newTitle.trim()}
                  className="bg-ink text-white px-6 py-2 rounded-md hover:bg-navy disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Start chat
                </button>
              </div>
            </div>
          </form>
        </Dialog>
      </div>
    </Shell>
  );
}
