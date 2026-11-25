"use client";

import { Shell } from "@/components/Shell";

export default function SettingsPage() {
  return (
    <Shell>
      <div className="max-w-3xl mx-auto">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-ink font-editorial text-2xl font-semibold">Settings</span>
        </div>
        <p className="text-muted mb-8">Account and application preferences.</p>

        <div className="bg-white border border-border rounded-xl p-8">
          <h2 className="font-semibold mb-6">Account</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-ink font-medium">Development account</p>
                <p className="text-xs text-muted">dev@aqvera.local</p>
              </div>
              <span className="px-2.5 py-1 rounded bg-surface text-sage-dark text-xs border border-sage/20">
                Local dev only
              </span>
            </div>
            <div className="pt-4 border-t border-border">
              <p className="text-xs text-muted uppercase tracking-wider mb-3">
                Authentication note
              </p>
              <p className="text-muted text-sm">
                Phase 1 uses a local development access mode (no password
                required). Full authentication with password hashing, sessions,
                and token expiration will be implemented in a later phase.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Shell>
  );
}
