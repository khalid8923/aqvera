"use client";

import * as React from "react";

interface DialogProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

export function Dialog({ open, onClose, title, children }: DialogProps) {
  const backdropRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (!open) return;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  if (!open) return null;

  return (
    <>
      <div
        ref={backdropRef}
        className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm"
        onClick={onClose}
      />
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 bg-white rounded-xl p-8 w-full max-w-md shadow-xl border border-border">
        {title && (
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-editorial text-xl font-semibold">{title}</h2>
            <button
              onClick={onClose}
              className="p-2 text-muted hover:text-ink"
              aria-label="Close dialog"
            >
              ✕
            </button>
          </div>
        )}
        {children}
      </div>
    </>
  );
}
