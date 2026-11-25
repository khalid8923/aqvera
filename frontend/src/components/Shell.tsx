"use client";

import { useState } from "react";
import { TopNav, Sidebar, MobileTopBar } from "@/components/Navigation";

export function Shell({ children }: { children: React.ReactNode }) {
  const [drawerOpen, setDrawerOpen] = useState(false);

  return (
    <div className="flex flex-col h-full">
      <MobileTopBar openDrawer={() => setDrawerOpen(true)} />
      <div className="flex flex-1 overflow-hidden relative">
        <Sidebar />
        <main className="flex-1 overflow-y-auto bg-paper">
          <TopNav openDrawer={() => setDrawerOpen(true)} />
          <div className="p-6">{children}</div>
        </main>

        {drawerOpen && (
          <div
            className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm md:hidden"
            onClick={() => setDrawerOpen(false)}
          />
        )}
      </div>
    </div>
  );
}
