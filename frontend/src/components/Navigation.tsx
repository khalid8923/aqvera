"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import Link from "next/link";
import { AQVERAHorizontalLogo } from "@/components/AQVERALogo";
import { useAuth } from "@/components/AuthContext";
import { ACADEMIC_SECTIONS } from "@/lib/sections";

export const MAIN_NAV_ITEMS = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/courses", label: "Course Library" },
  { href: "/sections", label: "Academic Sections" },
  { href: "/learning", label: "Learning Progress" },
  { href: "/resources", label: "Study Resources" },
  { href: "/settings", label: "Settings" },
];

interface Conversation {
  id: number;
  title: string;
  course_id: number | null;
  updated_at: string;
}

export function TopNav({ openDrawer }: { openDrawer: () => void }) {
  const { user, logout, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <header className="border-b border-border bg-white sticky top-0 z-20">
        <div className="flex items-center justify-between px-6 py-4">
          <button
            onClick={openDrawer}
            className="md:hidden p-2 text-muted hover:text-ink"
            aria-label="Open navigation"
            disabled
          >
            ☰
          </button>
          <div className="hidden md:flex items-center gap-4">
            <AQVERAHorizontalLogo size={24} variant="light" />
          </div>
          <div className="ml-auto flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded border border-border text-xs text-muted">
              Loading…
            </div>
          </div>
        </div>
      </header>
    );
  }

  return (
    <header className="border-b border-border bg-white sticky top-0 z-20">
      <div className="flex items-center justify-between px-6 py-4">
        <button
          onClick={openDrawer}
          className="md:hidden p-2 text-muted hover:text-ink"
          aria-label="Open navigation"
        >
          ☰
        </button>
        <div className="hidden md:flex items-center gap-4">
          <AQVERAHorizontalLogo size={24} variant="light" />
        </div>
        <div className="ml-auto flex items-center gap-4">
          {isAuthenticated ? (
            <div className="flex items-center gap-3">
              <div className="hidden sm:flex flex-col items-end text-right">
                <p className="text-sm text-ink font-medium">{user?.email}</p>
                <button
                  onClick={logout}
                  className="text-xs text-terracotta hover:bg-terracotta/10 px-2 py-1 rounded transition-colors"
                >
                  Sign out
                </button>
              </div>
              <div className="w-8 h-8 rounded-full bg-surface flex items-center justify-center text-xs font-medium text-ink">
                {user?.email?.charAt(0).toUpperCase() || "?"}
              </div>
            </div>
          ) : (
            <Link href="/login">
              <button className="bg-ink text-white px-5 py-2 rounded-md text-sm font-medium hover:bg-navy transition-colors">
                Sign in
              </button>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}

export function Sidebar() {
  const { isAuthenticated, isLoading } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  const [recentChats, setRecentChats] = useState<Conversation[]>([]);
  const [chatsLoading, setChatsLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    async function loadChats() {
      if (!isAuthenticated) return;
      setChatsLoading(true);
      try {
        const res = await fetch("/api/conversations?limit=5");
        if (!cancelled && res.ok) {
          setRecentChats(await res.json());
        }
      } catch {
        // ignore; recent chats is supplemental
      } finally {
        if (!cancelled) setChatsLoading(false);
      }
    }
    loadChats();
    return () => {
      cancelled = true;
    };
  }, [isAuthenticated]);

  if (isLoading) {
    return null;
  }

  return (
    <aside className="hidden md:flex flex-col w-64 border-r border-border bg-white h-[calc(100vh-4rem)] sticky top-[4rem]">
      <div className="p-6">
        <AQVERAHorizontalLogo size={24} variant="light" />
      </div>

      <nav className="flex-1 px-4 space-y-6">
        {/* Main Navigation */}
        <div className="space-y-1">
          {MAIN_NAV_ITEMS.map((item) => {
            const active = pathname === item.href;
            return (
              <a
                key={item.href}
                href={item.href}
                onClick={() => router.push(item.href)}
                className={`flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium transition-colors ${
                  active
                    ? "bg-surface text-ink"
                    : "text-muted hover:text-ink hover:bg-surface/50"
                }`}
              >
                {item.label}
              </a>
            );
          })}
        </div>

        {isAuthenticated && (
          <>
            {/* Academic Sections Group */}
            <div className="pt-2">
              <h3 className="px-4 py-2 text-[10px] uppercase tracking-wider text-muted font-medium">
                Academic Sections
              </h3>
              <div className="space-y-1">
                {ACADEMIC_SECTIONS.map((section) => {
                  const active = pathname === `/sections/${section.id}`;
                  return (
                    <a
                      key={section.id}
                      href={`/sections/${section.id}`}
                      onClick={() => router.push(`/sections/${section.id}`)}
                      className={`flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium transition-colors ${
                        active
                          ? "bg-surface text-ink"
                          : "text-muted hover:text-ink hover:bg-surface/50"
                      }`}
                    >
                      {section.label}
                    </a>
                  );
                })}
              </div>
            </div>

            {/* Recent Chats Group */}
            <div className="pt-2">
              <h3 className="px-4 py-2 text-[10px] uppercase tracking-wider text-muted font-medium">
                Recent Chats
              </h3>
              <div className="space-y-1">
                {chatsLoading ? (
                  <div className="px-4 py-3 text-xs text-muted">Loading…</div>
                ) : recentChats.length === 0 ? (
                  <div className="px-4 py-3 text-xs text-muted text-center">
                    No recent conversations
                  </div>
                ) : (
                  recentChats.map((conv: Conversation) => (
                    <Link
                      key={conv.id}
                      href={`/chat/${conv.id}?course=${conv.course_id ?? ""}`}
                      onClick={() =>
                        router.push(`/chat/${conv.id}?course=${conv.course_id ?? ""}`)
                      }
                      className="flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium text-muted hover:text-ink hover:bg-surface/50 transition-colors"
                    >
                      {conv.title}
                    </Link>
                  ))
                )}
              </div>
            </div>
          </>
        )}
      </nav>

      <div className="p-4 border-t border-border">
        {isAuthenticated ? (
          <button
            onClick={() => router.push("/dashboard")}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium text-ink bg-surface hover:bg-surface/80 transition-colors"
          >
            + New Chat
          </button>
        ) : (
          <button
            onClick={() => router.push("/login")}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium text-ink bg-surface hover:bg-surface/80 transition-colors"
          >
            Sign in to continue
          </button>
        )}
      </div>
    </aside>
  );
}

export function MobileTopBar({ openDrawer }: { openDrawer: () => void }) {
  return (
    <header className="md:hidden border-b border-border bg-white px-4 py-3 flex items-center justify-between z-20">
      <AQVERAHorizontalLogo size={24} variant="light" />
      <button
        onClick={openDrawer}
        className="p-2 text-muted hover:text-ink"
        aria-label="Open navigation"
      >
        ☰
      </button>
    </header>
  );
}
