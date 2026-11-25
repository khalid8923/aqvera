"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { Shell } from "@/components/Shell";
import { useAuth } from "@/components/AuthContext";

interface Note {
  id: number;
  title: string;
  content: string;
  course_id: number | null;
  topic_id: number | null;
  notebook_id: number | null;
  is_pinned: boolean;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
}

export default function NotesPage() {
  const { apiFetch, isAuthenticated, isLoading } = useAuth();
  const [notes, setNotes] = useState<Note[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [openNote, setOpenNote] = useState<Note | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editContent, setEditContent] = useState("");

  const fetchNotes = useCallback(async () => {
    try {
      const res = await apiFetch("/study/notes");
      if (!res.ok) throw new Error("Failed to load notes");
      setNotes(await res.json());
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    }
  }, [apiFetch]);

  useEffect(() => {
    if (!isAuthenticated) return;
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchNotes();
  }, [fetchNotes, isAuthenticated]);

  if (isLoading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-muted">Loading your notes…</p>
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
            Please sign in to access your notes.
          </p>
          <Link href="/login" className="text-sage-dark hover:text-ink font-medium">
            Sign in
          </Link>
        </div>
      </Shell>
    );
  }

  async function saveNote() {
    if (!openNote) return;
    try {
      const res = await apiFetch(`/study/notes/${openNote.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: editTitle, content: editContent }),
      });
      if (!res.ok) throw new Error("Failed to save note");
      setOpenNote(await res.json());
      fetchNotes();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Save failed");
    }
  }

  async function createNote() {
    const title = prompt("Enter note title");
    if (!title) return;
    try {
      const res = await apiFetch("/study/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content: "" }),
      });
      if (!res.ok) throw new Error("Failed to create note");
      const note = await res.json();
      setOpenNote(note);
      setEditTitle(note.title);
      setEditContent(note.content);
      fetchNotes();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Create failed");
    }
  }

  async function deleteNote(id: number) {
    if (!confirm("Delete this note?")) return;
    try {
      const res = await apiFetch(`/study/notes/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete");
      if (openNote?.id === id) setOpenNote(null);
      fetchNotes();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Delete failed");
    }
  }

  const pinnedNotes = notes.filter((n) => n.is_pinned);
  const regularNotes = notes.filter((n) => !n.is_pinned);

  return (
    <Shell>
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="flex items-center justify-between mb-2">
          <div>
            <span className="text-ink font-editorial text-2xl font-semibold">
              Notes
            </span>
            <p className="text-muted">
              Your personal knowledge base. Notes link to courses and topics.
            </p>
          </div>
          <button
            onClick={createNote}
            className="bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors flex items-center gap-2"
          >
            <span>+</span> New note
          </button>
        </div>

        {error && (
          <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta rounded-md p-4">
            {error}
          </div>
        )}

        {notes.length === 0 && (
          <div className="bg-white border border-border rounded-xl p-16 text-center">
            <p className="text-muted">No notes yet.</p>
            <button
              onClick={createNote}
              className="mt-6 bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors"
            >
              Create your first note
            </button>
          </div>
        )}

        {pinnedNotes.length > 0 && (
          <section>
            <h2 className="font-editorial text-xl font-semibold mb-4">Pinned</h2>
            <div className="grid md:grid-cols-3 gap-5">
              {pinnedNotes.map((note) => (
                <NoteCard key={note.id} note={note} onDelete={deleteNote} />
              ))}
            </div>
          </section>
        )}

        <section>
          <h2 className="font-editorial text-xl font-semibold mb-4">
            {regularNotes.length > 0 ? "All Notes" : "Notes"}
          </h2>
          <div className="space-y-3">
            {regularNotes.map((note) => (
              <NoteCard key={note.id} note={note} onDelete={deleteNote} />
            ))}
          </div>
        </section>

        {openNote && (
          <section className="bg-white border border-border rounded-xl p-6">
            <h2 className="font-editorial text-xl font-semibold mb-4">
              {openNote.title}
            </h2>
            <div className="flex items-center gap-4 text-xs text-muted mb-4">
              <span>{new Date(openNote.updated_at).toLocaleDateString()}</span>
              {openNote.is_pinned && <span className="text-terracotta">📌 Pinned</span>}
            </div>
            <textarea
              value={editContent}
              onChange={(e) => setEditContent(e.target.value)}
              className="w-full min-h-[400px] p-4 border border-border rounded-lg text-ink font-mono text-sm leading-relaxed focus:ring-2 focus:ring-sage-dark focus:outline-none"
              onBlur={saveNote}
            />
            <div className="mt-4 flex items-center gap-4">
              <input
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                onBlur={saveNote}
                className="w-full px-3 py-2 border border-border rounded-lg text-ink focus:ring-2 focus:ring-sage-dark focus:outline-none"
                defaultValue={openNote.title}
              />
              <button
                onClick={() => setOpenNote(null)}
                className="text-muted hover:text-ink"
              >
                Close
              </button>
            </div>
          </section>
        )}
      </div>
    </Shell>
  );
}

function NoteCard({
  note,
  onDelete,
}: {
  note: Note;
  onDelete: (id: number) => void;
}) {
  return (
    <div
      className={`group cursor-pointer p-5 rounded-lg border ${
        note.is_pinned ? "bg-sage/20 border-sage/30" : "bg-white border-border"
      } hover:border-sage-dark/40 transition-colors`}
    >
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-ink group-hover:text-sage-dark transition-colors">
          {note.title}
        </h3>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(note.id);
          }}
          className="text-terracotta hover:bg-terracotta/10 p-1 rounded transition-colors"
          aria-label="Delete note"
        >
          ✕
        </button>
      </div>
      <p className="text-sm text-muted line-clamp-2 mb-3">{note.content}</p>
      <div className="flex items-center gap-2 text-xs text-muted">
        <span>
          {new Date(note.updated_at).toLocaleDateString()}
        </span>
        {note.is_pinned && <span className="text-terracotta">📌</span>}
      </div>
    </div>
  );
}
