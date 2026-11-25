"use client";

import { Shell } from "@/components/Shell";

export default function LearningPage() {
  return (
    <Shell>
      <div className="max-w-3xl mx-auto">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-ink font-editorial text-2xl font-semibold">Learning Progress</span>
        </div>
        <p className="text-muted mb-8">Track your mastery across courses and topics.</p>

        <div className="bg-white border border-border rounded-xl p-8 text-center">
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
          <h2 className="text-xl font-semibold mb-3">Coming in Phase 2</h2>
          <p className="text-muted max-w-xs mx-auto">
            Adaptive learning progress tracking, mastery estimation, and
            personalized recommendations will be implemented in Phase 2.
          </p>
        </div>
      </div>
    </Shell>
  );
}
