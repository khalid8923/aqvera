"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { Shell } from "@/components/Shell";
import { useAuth } from "@/components/AuthContext";

interface Deck {
  id: number;
  title: string;
  description: string | null;
  course_id: number | null;
  topic_id: number | null;
  is_ai_generated: boolean;
  created_at: string;
  updated_at: string;
}

interface Card {
  id: number;
  deck_id: number;
  front: string;
  back: string;
  interval: number;
  repeat_count: number;
  ease_factor: number;
  next_review_at: string | null;
  last_reviewed_at: string | null;
  lapses: number;
}

export default function FlashcardsPage() {
  const { apiFetch, isAuthenticated, isLoading } = useAuth();
  const [decks, setDecks] = useState<Deck[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [activeDeck, setActiveDeck] = useState<Deck | null>(null);
  const [cards, setCards] = useState<Card[]>([]);
  const [reviewMode, setReviewMode] = useState(false);
  const [cardIndex, setCardIndex] = useState(0);
  const [showBack, setShowBack] = useState(false);

  const fetchDecks = useCallback(async () => {
    try {
      const res = await apiFetch("/study/flashcards/decks");
      if (!res.ok) throw new Error("Failed to load decks");
      setDecks(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    }
  }, [apiFetch]);

  const fetchCards = useCallback(async (deckId: number) => {
    try {
      const res = await apiFetch(`/study/flashcards?deck_id=${deckId}&due_only=true`);
      if (!res.ok) throw new Error("Failed to load cards");
      setCards(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    }
  }, [apiFetch]);

  useEffect(() => {
    if (!isAuthenticated) return;
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchDecks();
  }, [fetchDecks, isAuthenticated]);

  if (isLoading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-muted">Loading your flashcards…</p>
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
            Please sign in to access your flashcards.
          </p>
          <Link href="/login" className="text-sage-dark hover:text-ink font-medium">
            Sign in
          </Link>
        </div>
      </Shell>
    );
  }

  async function createDeck() {
    const title = prompt("Enter deck title");
    if (!title) return;
    try {
      const res = await apiFetch("/study/flashcards/decks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
      });
      if (!res.ok) throw new Error("Failed to create deck");
      fetchDecks();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Create failed");
    }
  }

  async function addCard() {
    if (!activeDeck) return;
    const front = prompt("Enter front of card");
    if (!front) return;
    const back = prompt("Enter back of card");
    if (!back) return;
    try {
      const res = await apiFetch("/study/flashcards", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ deck_id: activeDeck.id, front, back }),
      });
      if (!res.ok) throw new Error("Failed to create card");
      fetchCards(activeDeck.id);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Create failed");
    }
  }

  async function reviewCard(quality: number) {
    if (!cards[cardIndex]) return;
    try {
      const res = await apiFetch(
        `/study/flashcards/${cards[cardIndex].id}/review`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ quality }),
        }
      );
      if (!res.ok) throw new Error("Review failed");
      setCardIndex((i) => i + 1);
      setShowBack(false);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Review failed");
    }
  }

  if (reviewMode && cards.length > 0) {
    const card = cards[cardIndex];
    return (
      <Shell>
        <div className="max-w-md mx-auto py-10">
          <div className="bg-white border border-border rounded-2xl p-8 min-h-[400px] flex flex-col items-center justify-center text-center shadow-xl">
            <div className="mb-6">
              <span className="text-xs text-muted uppercase tracking-wider">
                Card {cardIndex + 1} of {cards.length}
              </span>
            </div>
            <div className="mb-8 p-6 rounded-xl bg-surface border border-border">
              {showBack ? (
                <>
                  <h3 className="text-lg font-medium text-ink mb-4">Back</h3>
                  <p className="text-ink">{card.back}</p>
                </>
              ) : (
                <>
                  <h3 className="text-lg font-medium text-ink mb-4">Front</h3>
                  <p className="text-ink">{card.front}</p>
                </>
              )}
            </div>
            {!showBack ? (
              <button
                onClick={() => setShowBack(true)}
                className="bg-ink text-white px-8 py-3 rounded-lg text-sm font-medium hover:bg-navy transition-colors"
              >
                Show Answer
              </button>
            ) : (
              <div className="flex gap-3">
                <button
                  onClick={() => reviewCard(1)}
                  className="bg-terracotta text-white px-6 py-3 rounded-lg text-sm font-medium hover:bg-terracotta transition-colors"
                >
                  Again
                </button>
                <button
                  onClick={() => reviewCard(3)}
                  className="bg-sage-dark text-white px-6 py-3 rounded-lg text-sm font-medium hover:bg-sage transition-colors"
                >
                  Good
                </button>
                <button
                  onClick={() => reviewCard(5)}
                  className="bg-ink text-white px-6 py-3 rounded-lg text-sm font-medium hover:bg-navy transition-colors"
                >
                  Easy
                </button>
              </div>
            )}
          </div>
          <div className="mt-6 flex justify-between">
            <button
              onClick={() => setReviewMode(false)}
              className="text-muted hover:text-ink"
            >
              Exit review
            </button>
            <span className="text-sm text-muted">
              {card.lapses} lapses · {card.repeat_count} reviews
            </span>
          </div>
        </div>
      </Shell>
    );
  }

  return (
    <Shell>
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="flex items-center justify-between mb-2">
          <div>
            <span className="text-ink font-editorial text-2xl font-semibold">
              Flashcards
            </span>
            <p className="text-muted">
              Spaced repetition for lasting retention. SM-2 algorithm schedules
              reviews based on your performance.
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={createDeck}
              className="bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors flex items-center gap-2"
            >
              <span>+</span> New deck
            </button>
            {activeDeck && (
              <button
                onClick={addCard}
                className="bg-sage-dark text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-sage transition-colors flex items-center gap-2"
              >
                <span>+</span> Add card
              </button>
            )}
          </div>
        </div>

        {error && (
          <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta rounded-md p-4">
            {error}
          </div>
        )}

        <div className="grid md:grid-cols-3 gap-5">
          {decks.length === 0 ? (
            <div className="col-span-3 bg-white border border-border rounded-xl p-16 text-center">
              <p className="text-muted">No decks yet.</p>
              <button
                onClick={createDeck}
                className="mt-6 bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors"
              >
                Create your first deck
              </button>
            </div>
          ) : (
            decks.map((deck) => (
              <div
                key={deck.id}
                onClick={() => {
                  setActiveDeck(deck);
                  fetchCards(deck.id);
                }}
                className="cursor-pointer bg-white border border-border rounded-xl p-6 hover:border-sage-dark/40 transition-colors"
              >
                <h3 className="font-semibold text-ink mb-1">{deck.title}</h3>
                <p className="text-xs text-muted mb-4">
                  {deck.description || "No description"}
                </p>
                <div className="flex items-center gap-2 text-xs text-muted">
                  <span>{deck.is_ai_generated ? "AI-generated" : "Manual"}</span>
                  <span>•</span>
                  <span>{new Date(deck.updated_at).toLocaleDateString()}</span>
                </div>
              </div>
            ))
          )}
        </div>

        {activeDeck && (
          <section>
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="font-editorial text-xl font-semibold">{activeDeck.title}</h2>
                <p className="text-sm text-muted">
                  {activeDeck.description || ""}
                </p>
              </div>
              <div className="flex gap-3">
                <button
                  onClick={() => {
                    setReviewMode(true);
                    setCardIndex(0);
                    setShowBack(false);
                  }}
                  disabled={cards.length === 0}
                  className={`bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors ${
                    cards.length === 0 ? "opacity-50 cursor-not-allowed" : ""
                  }`}
                >
                  Start Review
                </button>
                <button
                  onClick={() => setActiveDeck(null)}
                  className="text-muted hover:text-ink"
                >
                  Back to decks
                </button>
              </div>
            </div>
            <div className="space-y-3">
              {cards.length === 0 ? (
                <div className="bg-white border border-border rounded-xl p-12 text-center">
                  <p className="text-muted">No cards in this deck yet.</p>
                </div>
              ) : (
                cards.map((card) => (
                  <div
                    key={card.id}
                    className="bg-white border border-border rounded-xl p-5 hover:bg-surface/50 transition-colors"
                  >
                    <div className="mb-3">
                      <h4 className="font-medium text-ink mb-1">Front</h4>
                      <p className="text-ink">{card.front}</p>
                    </div>
                    <div className="mb-3">
                      <h4 className="font-medium text-sage-dark mb-1">Back</h4>
                      <p className="text-muted">{card.back}</p>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-muted">
                      <span>Review: {card.repeat_count}</span>
                      <span>•</span>
                      <span>Lapses: {card.lapses}</span>
                      <span>•</span>
                      <span>
                        {card.next_review_at
                          ? new Date(card.next_review_at).toLocaleDateString()
                          : "Due now"}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </section>
        )}
      </div>
    </Shell>
  );
}
