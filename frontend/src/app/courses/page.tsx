"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Shell } from "@/components/Shell";
import { AQVERAHorizontalLogo } from "@/components/AQVERALogo";
import { useRouter } from "next/navigation";
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
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showArchived, setShowArchived] = useState(false);
  const { apiFetch, isAuthenticated, isLoading } = useAuth();

  const router = useRouter();

  async function fetchCourses() {
    try {
      setLoading(true);
      const res = await apiFetch(
        `/api/courses?include_archived=${showArchived}`
      );
      if (!res.ok) throw new Error("Failed to load courses");
      setCourses(await res.json());
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!isAuthenticated) return;
    let cancelled = false;
    async function load() {
      try {
        setLoading(true);
        const res = await apiFetch(
          `/api/courses?include_archived=${showArchived}`
        );
        if (!res.ok) throw new Error("Failed to load courses");
        if (!cancelled) setCourses(await res.json());
        if (!cancelled) setError(null);
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
  }, [apiFetch, showArchived, isAuthenticated]);

  if (isLoading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-64">
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
            Please sign in to access your course library.
          </p>
          <Link href="/login" className="text-sage-dark hover:text-ink font-medium">
            Sign in
          </Link>
        </div>
      </Shell>
    );
  }

  async function handleCreate(formData: FormData) {
    const res = await apiFetch("/api/courses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: formData.get("title"),
        university: formData.get("university") || undefined,
        department: formData.get("department") || undefined,
        course_code: formData.get("course_code") || undefined,
        semester: formData.get("semester") || undefined,
        description: formData.get("description") || undefined,
        primary_language: formData.get("primary_language") || "en",
        subject_domain: formData.get("subject_domain") || undefined,
      }),
    });
    if (!res.ok) {
      setError("Failed to create course");
      return;
    }
    const newCourse = await res.json();
    setCourses([newCourse, ...courses]);
    setError(null);
    const modal = document.getElementById("create-course-modal");
    if (modal) modal.classList.add("hidden");
  }

  async function handleUpdate(id: number, formData: FormData) {
    const updates: Record<string, unknown> = {};
    const fields = ["title", "university", "department", "course_code", "semester", "description", "primary_language", "subject_domain"];
    fields.forEach((f) => {
      const val = formData.get(f);
      if (val !== null && val !== "") updates[f] = val;
    });
    const isArchived = formData.get("is_archived");
    if (isArchived !== null) updates["is_archived"] = isArchived === "on";

    const res = await apiFetch(`/api/courses/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updates),
    });
    if (!res.ok) {
      setError("Failed to update course");
      return;
    }
    setError(null);
    const modal = document.getElementById(`edit-course-modal-${id}`);
    if (modal) modal.classList.add("hidden");
    fetchCourses();
  }

  async function handleArchive(id: number) {
    const res = await apiFetch(`/api/courses/${id}/archive`, {
      method: "PATCH",
    });
    if (!res.ok) {
      setError("Failed to archive course");
      return;
    }
    setError(null);
    fetchCourses();
  }

  async function handleDelete(id: number) {
    if (!confirm("Are you sure you want to delete this course?")) return;
    const res = await apiFetch(`/api/courses/${id}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      setError("Failed to delete course");
      return;
    }
    setError(null);
    fetchCourses();
  }

  if (loading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-muted">Loading courses…</p>
        </div>
      </Shell>
    );
  }

  const visibleCourses = showArchived ? courses : courses.filter((c) => !c.is_archived);

  return (
    <Shell>
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-8">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <AQVERAHorizontalLogo size={20} variant="light" className="hidden lg:block" />
              <span className="text-ink font-editorial text-2xl font-semibold tracking-tight">
                Course Library
              </span>
            </div>
            <p className="text-muted">Manage your academic courses.</p>
          </div>
          <button
            onClick={() => {
              const modal = document.getElementById("create-course-modal");
              if (modal) modal.classList.remove("hidden");
            }}
            className="bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors flex items-center gap-2"
          >
            <span>+</span> Create course
          </button>
        </div>

        {error && (
          <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta rounded-md p-4 mb-6">
            {error}
          </div>
        )}

        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={() => setShowArchived(!showArchived)}
            className={`px-3 py-1.5 rounded border rounded-md text-sm ${
              showArchived ? "bg-surface text-ink border-border" : "bg-white text-muted border-border hover:bg-surface"
            }`}
          >
            {showArchived ? "Hide archived" : "Show archived"}
          </button>
        </div>

        {visibleCourses.length === 0 && (
          <div className="bg-white border border-border rounded-xl p-16 text-center">
            <div className="w-16 h-16 rounded-full bg-surface flex items-center justify-center mx-auto mb-6">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <path
                  d="M16 2 L4 14 L16 26 L28 14 L16 2 Z"
                  fill="#101D2B"
                  stroke="#315C50"
                  strokeWidth="1.5"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <h2 className="text-xl font-semibold mb-3">
              {showArchived ? "No archived courses" : "No courses yet"}
            </h2>
            <p className="text-muted max-w-xs mx-auto mb-6">
              {showArchived
                ? "You have no archived courses."
                : "Create your first course to get started."}
            </p>
            {!showArchived && (
              <button
                onClick={() => {
                  const modal = document.getElementById("create-course-modal");
                  if (modal) modal.classList.remove("hidden");
                }}
                className="bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors"
              >
                Create your first course
              </button>
            )}
          </div>
        )}

        {visibleCourses.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse bg-white">
              <thead>
                <tr className="border-b border-border">
                  <th className="px-4 py-3 text-xs font-medium text-muted">Title</th>
                  <th className="px-4 py-3 text-xs font-medium text-muted">Code</th>
                  <th className="px-4 py-3 text-xs font-medium text-muted">Domain</th>
                  <th className="px-4 py-3 text-xs font-medium text-muted">Semester</th>
                  <th className="px-4 py-3 text-xs font-medium text-muted">Status</th>
                  <th className="px-4 py-3 text-xs font-medium text-muted">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {visibleCourses.map((course) => (
                  <tr key={course.id} className="hover:bg-surface/50 transition-colors">
                    <td className="px-4 py-4">
                      <div className="font-semibold text-ink">{course.title}</div>
                      {course.description && (
                        <div className="text-xs text-muted mt-1">
                          {course.description}
                        </div>
                      )}
                    </td>
                    <td className="px-4 py-4 text-sm text-muted">
                      {course.course_code || "—"}
                    </td>
                    <td className="px-4 py-4 text-sm text-muted">
                      {course.subject_domain || "—"}
                    </td>
                    <td className="px-4 py-4 text-sm text-muted">
                      {course.semester || "—"}
                    </td>
                    <td className="px-4 py-4">
                      <span
                        className={`inline-flex items-center gap-1.5 px-2 py-1 rounded text-xs font-medium ${
                          course.is_archived
                            ? "bg-terracotta/10 text-terracotta border border-terracotta/20"
                            : "bg-sage/10 text-sage-dark border border-sage/20"
                        }`}
                      >
                        {course.is_archived ? "Archived" : "Active"}
                      </span>
                    </td>
                    <td className="px-4 py-4">
                      <div className="flex gap-2">
                        <button
                          onClick={() => router.push(`/courses/${course.id}`)}
                          className="px-3 py-1.5 rounded border border-border text-sm hover:bg-surface"
                        >
                          Open
                        </button>
                        <button
                          onClick={() => {
                            const modal = document.getElementById(`edit-course-modal-${course.id}`);
                            if (modal) modal.classList.remove("hidden");
                          }}
                          className="px-3 py-1.5 rounded border border-border text-sm hover:bg-surface"
                        >
                          Edit
                        </button>
                        {!course.is_archived && (
                          <button
                            onClick={() => handleArchive(course.id)}
                            className="px-3 py-1.5 rounded border border-border text-sm hover:bg-surface"
                          >
                            Archive
                          </button>
                        )}
                        <button
                          onClick={() => handleDelete(course.id)}
                          className="px-3 py-1.5 rounded border border-border text-sm hover:bg-surface text-terracotta"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Create course modal */}
        <div
          id="create-course-modal"
          className="fixed inset-0 z-50 hidden"
          aria-modal="true"
          role="dialog"
        >
          <div className="fixed inset-0 bg-black/40 backdrop-blur-sm" onClick={() => document.getElementById("create-course-modal")?.classList.add("hidden")} />
          <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl p-8 w-full max-w-md shadow-xl border border-border">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-editorial text-xl font-semibold">Create course</h2>
              <button
                onClick={() => document.getElementById("create-course-modal")?.classList.add("hidden")}
                className="p-2 text-muted hover:text-ink"
              >
                ✕
              </button>
            </div>
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
                    <label className="block text-sm font-medium mb-1">University</label>
                    <input name="university" className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Department</label>
                    <input name="department" className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none" />
                  </div>
                </div>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Course code</label>
                    <input name="course_code" className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none" placeholder="e.g. MATH101" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Semester</label>
                    <input name="semester" className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none" placeholder="e.g. Fall 2026" />
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
                    onClick={() => document.getElementById("create-course-modal")?.classList.add("hidden")}
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
          </div>
        </div>

        {/* Edit course modals */}
        {visibleCourses.map((course) => (
          <div
            key={course.id}
            id={`edit-course-modal-${course.id}`}
            className="fixed inset-0 z-50 hidden"
            aria-modal="true"
            role="dialog"
          >
            <div className="fixed inset-0 bg-black/40 backdrop-blur-sm" onClick={() => document.getElementById(`edit-course-modal-${course.id}`)?.classList.add("hidden")} />
            <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl p-8 w-full max-w-md shadow-xl border border-border">
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-editorial text-xl font-semibold">Edit course</h2>
                <button
                  onClick={() => document.getElementById(`edit-course-modal-${course.id}`)?.classList.add("hidden")}
                  className="p-2 text-muted hover:text-ink"
                >
                  ✕
                </button>
              </div>
              <form onSubmit={(e) => {
                e.preventDefault();
                handleUpdate(course.id, new FormData(e.target as HTMLFormElement));
              }}>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Course title *</label>
                    <input
                      name="title"
                      defaultValue={course.title}
                      required
                      className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                    />
                  </div>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">University</label>
                      <input
                        name="university"
                        defaultValue={course.university || ""}
                        className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Department</label>
                      <input
                        name="department"
                        defaultValue={course.department || ""}
                        className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                      />
                    </div>
                  </div>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Course code</label>
                      <input
                        name="course_code"
                        defaultValue={course.course_code || ""}
                        className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Semester</label>
                      <input
                        name="semester"
                        defaultValue={course.semester || ""}
                        className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Subject domain</label>
                    <input
                      name="subject_domain"
                      defaultValue={course.subject_domain || ""}
                      className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Description</label>
                    <textarea
                      name="description"
                      defaultValue={course.description || ""}
                    rows={3}
                      className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none"
                    />
                  </div>
                  <div className="flex items-center gap-2 pt-2">
                    <input
                      name="is_archived"
                      type="checkbox"
                      defaultChecked={course.is_archived}
                      className="rounded border-border"
                    />
                    <label className="text-sm text-muted">Archived</label>
                  </div>
                  <div className="flex justify-end gap-3 pt-6">
                    <button
                      type="button"
                      onClick={() => document.getElementById(`edit-course-modal-${course.id}`)?.classList.add("hidden")}
                      className="px-4 py-2 text-muted border border-border rounded-md hover:bg-surface"
                    >
                      Cancel
                    </button>
                    <button type="submit" className="bg-ink text-white px-6 py-2 rounded-md hover:bg-navy transition-colors">
                      Save changes
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        ))}
      </div>
    </Shell>
  );
}
