"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Shell } from "@/components/Shell";
import { useAuth } from "@/components/AuthContext";

interface Material {
  id: number;
  original_filename: string;
  content_type: string;
  file_size_bytes: number;
  status: string;
  created_at: string;
}

export default function ResourcesPage() {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [statusLoading, setStatusLoading] = useState<Record<number, boolean>>({});
  const [processing, setProcessing] = useState<Record<number, boolean>>({});
  const { apiFetch, isAuthenticated, isLoading } = useAuth();

  async function loadMaterials() {
    try {
      setLoading(true);
      const res = await apiFetch("/api/materials");
      if (!res.ok) throw new Error("Failed to load materials");
      setMaterials(await res.json());
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
        const res = await apiFetch("/api/materials");
        if (!res.ok) throw new Error("Failed to load materials");
        if (!cancelled) setMaterials(await res.json());
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
  }, [apiFetch, isAuthenticated]);

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
            Please sign in to access your study resources.
          </p>
          <Link href="/login" className="text-sage-dark hover:text-ink font-medium">
            Sign in
          </Link>
        </div>
      </Shell>
    );
  }

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    setUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await apiFetch("/api/materials/upload", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Upload failed" }));
        throw new Error(err.detail || "Upload failed");
      }
      setFile(null);
      await loadMaterials();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  async function handleProcess(id: number) {
    setProcessing((prev) => ({ ...prev, [id]: true }));
    try {
      const res = await apiFetch(`/api/materials/${id}/process`, {
        method: "POST",
      });
      if (!res.ok) throw new Error("Processing failed");
      await loadMaterials();
    } catch {
      // processing failure is non-fatal; status will show error
    } finally {
      setProcessing((prev) => {
        const rest = { ...prev };
        delete rest[id];
        return rest;
      });
    }
  }

  async function handleStatus(id: number) {
    setStatusLoading((prev) => ({ ...prev, [id]: true }));
    try {
      const res = await apiFetch(`/api/materials/${id}/status`);
      if (!res.ok) throw new Error("Failed to load status");
      const status = await res.json();
      setMaterials((prev) =>
        prev.map((m) => (m.id === id ? { ...m, status: status.status } : m))
      );
    } catch {
      // status check failure is non-fatal
    } finally {
      setStatusLoading((prev) => {
        const rest = { ...prev };
        delete rest[id];
        return rest;
      });
    }
  }

  const sizeKB = (bytes: number) => (bytes / 1024).toFixed(1);

  if (loading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-muted">Loading your materials…</p>
        </div>
      </Shell>
    );
  }

  return (
    <Shell>
      <div className="max-w-3xl mx-auto space-y-8">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-ink font-editorial text-2xl font-semibold">
            Study Resources
          </span>
        </div>
        <p className="text-muted mb-8">
          Upload your academic materials (PDF, DOCX, PPTX, TXT, images, audio,
          video). AQVERA validates, stores, and processes them into learning
          content traceable to your sources.
        </p>

        {error && (
          <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta rounded-md p-4">
            {error}
          </div>
        )}

        {/* Upload card */}
        <div className="bg-white border border-border rounded-xl p-6">
          <h3 className="font-semibold mb-4">Upload Material</h3>
          <form onSubmit={handleUpload} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">File</label>
              <input
                type="file"
                onChange={(e) => {
                  if (e.target.files?.[0]) setFile(e.target.files[0]);
                }}
                className="w-full border border-border rounded-md px-3 py-2 text-sm"
              />
            </div>
            <p className="text-xs text-muted">
              Supported: PDF, DOCX, PPTX, TXT, images (PNG/JPG), audio (MP3/WAV),
              video (MP4). Max 50 MB.
            </p>
            <button
              type="submit"
              disabled={!file || uploading}
              className="bg-ink text-white px-6 py-2.5 rounded-md text-sm font-medium hover:bg-navy disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {uploading ? "Processing…" : "Upload"}
            </button>
          </form>
        </div>

        {/* Materials list */}
        <div className="bg-white border border-border rounded-xl">
          <div className="border-b border-border px-6 py-4">
            <h3 className="font-semibold">Your Materials</h3>
          </div>
          <div className="divide-y divide-border">
            {materials.length === 0 ? (
              <div className="px-6 py-12 text-center">
                <p className="text-muted">No materials uploaded yet.</p>
                <p className="text-xs text-muted mt-2">
                  Upload your first academic document to get started.
                </p>
              </div>
            ) : (
              materials.map((m) => (
                <div key={m.id} className="px-6 py-4 flex items-center justify-between">
                  <div>
                    <div className="font-medium text-ink">{m.original_filename}</div>
                    <div className="text-xs text-muted">
                      {m.content_type} · {sizeKB(m.file_size_bytes)} KB · {m.status}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    {m.status === "uploaded" && (
                      <button
                        onClick={() => handleProcess(m.id)}
                        disabled={processing[m.id]}
                        className="text-xs text-sage-dark hover:text-ink underline"
                      >
                        {processing[m.id] ? "Processing…" : "Process"}
                      </button>
                    )}
                    <button
                      onClick={() => handleStatus(m.id)}
                      disabled={statusLoading[m.id]}
                      className="text-xs text-sage-dark hover:text-ink underline"
                    >
                      {statusLoading[m.id] ? "Checking…" : "Check status"}
                    </button>
                    <span
                      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium ${
                        m.status === "completed"
                          ? "bg-sage/10 text-sage-dark border border-sage/20"
                          : m.status === "failed"
                            ? "bg-terracotta/10 text-terracotta border border-terracotta/20"
                            : "bg-surface text-ink border border-border"
                      }`}
                    >
                      {m.status}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </Shell>
  );
}
