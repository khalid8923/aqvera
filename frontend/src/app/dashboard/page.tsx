"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Shell } from "@/components/Shell";
import { AQVERAHorizontalLogo } from "@/components/AQVERALogo";
import { Dialog } from "@/components/Dialog";
import { ACADEMIC_SECTIONS } from "@/lib/sections";
import { useAuth } from "@/components/AuthContext";

interface Course {
  id: number;
  title: string;
  course_code: string | null;
  subject_domain: string | null;
  semester: string | null;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
}

interface Conversation {
  id: number;
  title: string;
  course_id: number | null;
  updated_at: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const { apiFetch, isAuthenticated, isLoading } = useAuth();
  const [courses, setCourses] = useState<Course[]>([]);
  const [recentChats, setRecentChats] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) return;
    let cancelled = false;
    async function load() {
      try {
        setLoading(true);
        const [courseRes, chatRes] = await Promise.all([
          apiFetch("/api/courses"),
          apiFetch("/api/conversations?limit=5"),
        ]);
        if (!courseRes.ok) throw new Error("Failed to load courses");
        if (!cancelled) setCourses(await courseRes.json());
        if (!cancelled && chatRes.ok) {
          setRecentChats(await chatRes.json());
        }
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : "Unknown error");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, [apiFetch, isAuthenticated]);

  if (isLoading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-muted">Loading your dashboard…</p>
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
            Please sign in to access your dashboard.
          </p>
          <Link href="/login" className="text-sage-dark hover:text-ink font-medium">
            Sign in
          </Link>
        </div>
      </Shell>
    );
  }

  const continueCourses = [...courses]
    .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
    .slice(0, 3)
    .map((c) => ({
      id: c.id,
      title: c.title,
      domain: c.subject_domain || "General",
      lastActivity: new Date(c.updated_at).toLocaleString(undefined, {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }),
    }));

  async function handleCreate(formData: FormData) {
    const title = formData.get("title") as string;
    const res = await apiFetch("/api/courses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        subject_domain: formData.get("subject_domain") || undefined,
        course_code: formData.get("course_code") || undefined,
        semester: formData.get("semester") || undefined,
        description: formData.get("description") || undefined,
      }),
    });
    if (!res.ok) {
      setError("Failed to create course");
      return;
    }
    const newCourse = await res.json();
    setCourses((prev) => [newCourse as Course, ...prev]);
    setError(null);
    setModalOpen(false);
  }

  async function handleNewChat() {
    try {
      const res = await apiFetch("/api/conversations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: "New conversation", course_id: null }),
      });
      if (!res.ok) throw new Error("Failed to create conversation");
      const conv = await res.json();
      setModalOpen(false);
      router.push(`/chat/${conv.id}`);
    } catch {
      setError("Failed to start new chat");
    }
  }

  if (loading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-muted">Loading your dashboard…</p>
        </div>
      </Shell>
    );
  }

  return (
    <Shell>
      <div className="max-w-5xl mx-auto space-y-10">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-2">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <AQVERAHorizontalLogo size={20} variant="light" className="hidden lg:block" />
              <span className="text-ink font-editorial text-2xl font-semibold tracking-tight">
                Dashboard
              </span>
            </div>
            <p className="text-muted">
              Your academic courses, sections, and recent conversations.
            </p>
          </div>
          <button
            onClick={() => setModalOpen(true)}
            className="bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors flex items-center gap-2"
          >
            <span>+</span> Create course
          </button>
        </div>

        {error && (
          <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta rounded-md p-4">
            {error}
          </div>
        )}

        {/* Academic Sections Featured Area */}
        <section>
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-editorial text-xl font-semibold">Academic Sections</h2>
            <Link href="/sections">
              <span className="text-sm font-medium text-muted hover:text-ink transition-colors">
                View all →
              </span>
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {ACADEMIC_SECTIONS.map((section) => (
              <Link
                key={section.id}
                href={`/sections/${section.id}`}
                className="group relative block bg-white border border-border rounded-xl p-6 hover:border-sage-dark/40 transition-colors"
              >
                <div className="w-10 h-10 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200">
                  <span className="text-xl">{section.icon}</span>
                </div>
                <h3 className="font-semibold text-ink mb-1">{section.label}</h3>
                <p className="text-xs text-muted">Explore courses</p>
              </Link>
            ))}
          </div>
        </section>

        {/* Continue Learning (real courses, sorted by recent activity) */}
        <section>
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-editorial text-xl font-semibold">Continue Learning</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {continueCourses.length > 0 ? (
              continueCourses.map((course) => (
                <Link
                  key={course.id}
                  href={`/courses/${course.id}`}
                  className="group bg-white border border-border rounded-xl p-5 hover:border-sage-dark/40 transition-colors"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded bg-surface flex items-center justify-center">
                        <span className="text-sm">📘</span>
                      </div>
                      <span className="text-xs text-muted">{course.lastActivity}</span>
                    </div>
                  </div>
                  <h3 className="font-semibold text-ink mb-1">{course.title}</h3>
                  <p className="text-xs text-muted mb-4">{course.domain}</p>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium text-sage-dark">Open course</span>
                    <span className="text-xs text-muted">→</span>
                  </div>
                </Link>
              ))
            ) : (
              <div className="col-span-3 bg-white border border-border rounded-xl p-12 text-center">
                <h3 className="font-medium text-ink mb-2">No courses yet</h3>
                <p className="text-sm text-muted mb-4">
                  Create your first course to continue learning.
                </p>
              </div>
            )}
          </div>
        </section>

        {/* Recent Conversations (real) */}
        <section>
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-editorial text-xl font-semibold">Recent Conversations</h2>
            <Link href="/chat">
              <span className="text-sm font-medium text-muted hover:text-ink transition-colors">
                View all →
              </span>
            </Link>
          </div>
          <div className="space-y-3">
            {recentChats.length > 0 ? (
              recentChats.map((chat) => (
                <Link
                  key={chat.id}
                  href={`/chat/${chat.id}?course=${chat.course_id ?? ""}`}
                  className="group flex items-center justify-between bg-white border border-border rounded-xl px-5 py-4 hover:border-sage-dark/40 transition-colors block"
                >
                  <div>
                    <h3 className="font-semibold text-ink">{chat.title}</h3>
                    <p className="text-xs text-muted">
                      {new Date(chat.updated_at).toLocaleString(undefined, {
                        month: "short",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                  <span className="text-xs text-muted">→</span>
                </Link>
              ))
            ) : (
              <div className="bg-white border border-border rounded-xl p-12 text-center">
                <h3 className="font-medium text-ink mb-2">No conversations yet</h3>
                <p className="text-sm text-muted">
                  Start a new conversation from any course or the dashboard.
                </p>
              </div>
            )}
          </div>
        </section>

        {/* Quick Actions */}
        <section>
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-editorial text-xl font-semibold">Quick Actions</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <button
              onClick={() => setModalOpen(true)}
              className="bg-white border border-border rounded-xl p-6 text-left hover:border-sage-dark/40 transition-colors"
            >
              <div className="w-10 h-10 rounded-lg bg-terracotta/10 flex items-center justify-center mb-3 text-terracotta">
                📎
              </div>
              <h3 className="font-semibold text-ink mb-1">Upload Materials</h3>
              <p className="text-xs text-muted">
                Coming soon: attach lecture notes and documents
              </p>
            </button>
            <button
              onClick={handleNewChat}
              className="bg-white border border-border rounded-xl p-6 text-left hover:border-sage-dark/40 transition-colors"
            >
              <div className="w-10 h-10 rounded-lg bg-sage/10 flex items-center justify-center mb-3 text-sage-dark">
                💬
              </div>
              <h3 className="font-semibold text-ink mb-1">Start New Chat</h3>
              <p className="text-xs text-muted">
                Begin a new learning conversation
              </p>
            </button>
            <button
              onClick={() => router.push("/courses")}
              className="bg-white border border-border rounded-xl p-6 text-left hover:border-sage-dark/40 transition-colors"
            >
              <div className="w-10 h-10 rounded-lg bg-sage-dark/10 flex items-center justify-center mb-3 text-sage-dark">
                📚
              </div>
              <h3 className="font-semibold text-ink mb-1">Explore Courses</h3>
              <p className="text-xs text-muted">
                Browse the course library
              </p>
            </button>
          </div>
        </section>

        {/* Courses area (secondary) */}
        {courses.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-editorial text-xl font-semibold">Your Courses</h2>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
              {courses.map((course) => (
                <div
                  key={course.id}
                  className="bg-white border border-border rounded-xl p-5 hover:border-sage-dark/40 transition-colors"
                >
                  <div className="flex justify-between items-start mb-3">
                    <span
                      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-medium ${
                        course.is_archived
                          ? "bg-terracotta/10 text-terracotta border border-terracotta/20"
                          : "bg-sage/10 text-sage-dark border border-sage/20"
                      }`}
                    >
                      {course.subject_domain || "General"}
                    </span>
                    {course.is_archived && (
                      <span className="text-xs text-muted">Archived</span>
                    )}
                  </div>
                  <h3 className="font-semibold text-ink mb-2">{course.title}</h3>
                  {course.course_code && (
                    <p className="text-xs text-muted mb-3">{course.course_code}</p>
                  )}
                  <div className="flex items-center justify-between text-xs text-muted">
                    <span>{course.semester}</span>
                    <Link
                      href={`/courses/${course.id}`}
                      className="px-3 py-1.5 rounded border border-border hover:bg-surface text-sm"
                    >
                      Open
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Create course modal */}
        <Dialog open={modalOpen} onClose={() => setModalOpen(false)} title="Create course">
          <form onSubmit={(e) => {
            e.preventDefault();
            handleCreate(new FormData(e.target as HTMLFormElement));
          }}>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Course title *</label>
                <input
                  name="title"
                  required
                  className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                />
              </div>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Course code</label>
                  <input
                    name="course_code"
                    className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Semester</label>
                  <input
                    name="semester"
                    className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Subject domain</label>
                <input
                  name="subject_domain"
                  className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                  placeholder="e.g. Mathematics"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <textarea
                  name="description"
                  rows={3}
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
                <button type="submit" className="bg-ink text-white px-6 py-2 rounded-md hover:bg-navy transition-colors">
                  Create course
                </button>
              </div>
            </div>
          </form>
        </Dialog>
      </div>
    </Shell>
  );
}
