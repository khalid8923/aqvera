"use client";

import { useEffect, useRef, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { Shell } from "@/components/Shell";
import { AQVERAHorizontalLogo } from "@/components/AQVERALogo";
import { useAuth } from "@/components/AuthContext";

interface Message {
  id: number | string;
  role: "user" | "assistant";
  content: string;
  conversation_id: number;
  sources?: Array<{ document_title: string; section?: string; page?: number; slide?: number }>;
  evidence_type?: string;
}

interface Conversation {
  id: number;
  title: string;
  course_id: number | null;
  owner_id: number;
  created_at: string;
  updated_at: string;
  messages: Message[];
}

interface AIStatus {
  configured: boolean;
  provider: string | null;
  message: string | null;
}

export default function ChatPage() {
  const { apiFetch } = useAuth();
  const searchParams = useSearchParams();
  const router = useRouter();
  const conversationIdRaw = searchParams.get("conv");
  const conversationId = conversationIdRaw ? parseInt(conversationIdRaw, 10) : null;

  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [loading, setLoading] = useState(!conversationId);
  const [error, setError] = useState<string | null>(
    !conversationId ? "No conversation specified" : null
  );
  const [aiStatus, setAIStatus] = useState<AIStatus | null>(null);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversation]);

  useEffect(() => {
    async function fetchAIStatus() {
      try {
        const res = await apiFetch("/api/conversations/ai-status");
        if (res.ok) {
          setAIStatus(await res.json());
        }
      } catch {
        // AI status is informational; ignore failures
      }
    }
    fetchAIStatus();
  }, []);

  useEffect(() => {
    if (!conversationId) return;
    let cancelled = false;
    async function loadConversation() {
      try {
        setLoading(true);
        const res = await apiFetch(`/api/conversations/${conversationId}`);
        if (!res.ok) {
          if (res.status === 404) {
            if (!cancelled) setError("Conversation not found");
          } else {
            if (!cancelled) setError("Failed to load conversation");
          }
          return;
        }
        if (!cancelled) {
          setConversation(await res.json());
          setError(null);
        }
      } catch {
        if (!cancelled) setError("Failed to load conversation");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    loadConversation();
    return () => {
      cancelled = true;
    };
  }, [conversationId, apiFetch]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || sending || !conversation) return;

    const body = input;
    setInput("");
    setSending(true);

    // Persist user message
    try {
      const res = await apiFetch(
        `/api/conversations/${conversation.id}/messages`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ role: "user", content: body }),
        }
      );
      if (!res.ok) throw new Error("Failed to send message");
      const created = await res.json();

      setConversation((prev) =>
        prev
          ? {
              ...prev,
              messages: [...prev.messages, created as Message],
            }
          : null
      );
    } catch {
      setSending(false);
      return;
    }

    // Get AI response via the ai/ tutoring module
    try {
      const aiRes = await apiFetch("/ai/tutor/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: conversation.id,
          question: body,
          course_id: conversation.course_id,
          lesson_id: null,
        }),
      });
      if (!aiRes.ok) throw new Error("AI response failed");
      const aiData = await aiRes.json();

      const assistantMsg: Message = {
        id: Date.now(),
        role: "assistant",
        content: aiData.answer || "I'm unable to respond right now.",
        conversation_id: conversation.id,
        sources: aiData.sources,
        evidence_type: aiData.evidence_type,
      };
      setConversation((prev) =>
        prev ? { ...prev, messages: [...prev.messages, assistantMsg] } : null
      );
    } catch {
      // If AI unavailable, show an honest message instead of fabricating.
      const assistantMsg: Message = {
        id: Date.now(),
        role: "assistant",
        content:
          "AI responses are not available right now. No AI provider is configured. " +
          "Your message was saved; you can ask again once a provider is added.",
        conversation_id: conversation.id,
      };
      setConversation((prev) =>
        prev ? { ...prev, messages: [...prev.messages, assistantMsg] } : null
      );
    } finally {
      setSending(false);
    }
  }

  if (loading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-96 p-6 bg-paper text-ink">
          <p className="text-muted">Loading conversation…</p>
        </div>
      </Shell>
    );
  }

  if (error) {
    return (
      <Shell>
        <div className="max-w-3xl mx-auto text-center py-20 bg-paper text-ink p-6">
          <h2 className="text-xl font-semibold mb-3">{error}</h2>
          <button
            onClick={() => router.push("/dashboard")}
            className="text-sage-dark hover:text-ink underline"
          >
            Return to dashboard
          </button>
        </div>
      </Shell>
    );
  }

  if (!conversation) {
    return (
      <Shell>
        <div className="max-w-3xl mx-auto text-center py-20 bg-paper text-ink p-6">
          <h2 className="text-xl font-semibold mb-3">No conversation</h2>
          <button
            onClick={() => router.push("/dashboard")}
            className="text-sage-dark hover:text-ink underline"
          >
            Return to dashboard
          </button>
        </div>
      </Shell>
    );
  }

  return (
    <Shell>
      <div className="flex flex-col bg-paper text-ink">
        {/* Chat header (course context) */}
        <header className="md:flex items-center justify-between border-b border-border bg-white px-6 py-4 flex-shrink-0 z-10">
          <div className="flex items-center gap-3">
            <AQVERAHorizontalLogo size={20} variant="light" className="hidden" />
            <div>
              <h1 className="font-editorial text-lg font-semibold">
                {conversation.title}
              </h1>
              <p className="text-xs text-muted">
                {conversation.course_id
                  ? `Course #${conversation.course_id}`
                  : "General conversation"}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button className="p-2 text-muted hover:text-ink transition-colors" aria-label="Attach file">
              📎
            </button>
            <button className="p-2 text-muted hover:text-ink transition-colors" aria-label="Select course">
              📚
            </button>
          </div>
        </header>

        {/* AI provider status banner */}
        {!aiStatus?.configured && (
          <div className="border-b border-border bg-terracotta/10 px-6 py-3 flex-shrink-0">
            <div className="max-w-4xl mx-auto flex items-start gap-3 text-xs text-terracotta">
              <span>⚠</span>
              <div>
                {aiStatus?.message || "AI provider not configured."}
              </div>
            </div>
          </div>
        )}

        {/* Messages area */}
        <main
          className="min-h-[40vh] overflow-y-auto p-6 space-y-5"
          ref={messagesEndRef}
        >
          {conversation.messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-xl p-4 ${
                  msg.role === "user"
                    ? "bg-ink text-white rounded-tr-none"
                    : "bg-white border border-border text-ink rounded-tl-none"
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>
                {msg.evidence_type && msg.role === "assistant" && (
                  <span className="block text-[10px] mt-1 opacity-60 text-sage-dark">
                    {msg.evidence_type}
                  </span>
                )}
                <span className="block text-[10px] mt-1 opacity-60">
                  {msg.role === "user" ? "You" : "AQVERA AI"}
                </span>
              </div>
            </div>
          ))}
          {sending && (
            <div className="flex justify-start">
              <div className="bg-white border border-border rounded-xl p-4 text-ink animate-pulse">
                <span className="text-xs">Sending…</span>
              </div>
            </div>
          )}
        </main>

        {/* Composer */}
        <form
          onSubmit={handleSend}
          className="border-t border-border bg-white px-6 py-4 flex-shrink-0"
        >
          <div className="flex items-end gap-3">
            <button
              type="button"
              disabled={sending}
              className="p-2 text-muted hover:text-ink disabled:opacity-50 transition-colors"
              aria-label="Attach file"
            >
              📎
            </button>
            <button
              type="button"
              disabled={sending}
              className="p-2 text-muted hover:text-ink disabled:opacity-50 transition-colors"
              aria-label="Select course"
            >
              📚
            </button>
            <div className="flex-1 relative">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask anything about your courses…"
                rows={1}
                className="w-full resize-none border-none focus:ring-0 py-2 text-sm leading-6 text-ink placeholder:text-muted"
              />
            </div>
            <button
              type="submit"
              disabled={!input.trim() || sending}
              className="bg-ink text-white px-5 py-2.5 rounded-md text-sm font-medium hover:bg-navy disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-1"
            >
              <span className="text-xs">Send</span>
            </button>
          </div>
          <div className="mt-2 flex justify-end text-[10px] text-muted">
            AI responses are generated with academic context. Review for accuracy.
          </div>
        </form>
      </div>
    </Shell>
  );
}
