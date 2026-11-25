"use client";

import { useParams } from "next/navigation";
import Link from "next/link";
import { Shell } from "@/components/Shell";
import { AQVERAHorizontalLogo } from "@/components/AQVERALogo";
import { getSectionById } from "@/lib/sections";

export default function SectionPage() {
  const params = useParams();
  const sectionId = params.section as string;
  const section = getSectionById(sectionId);
  const subjects: Array<{ id: string; label: string; description: string }> = [];

  if (!section) {
    return (
      <Shell>
        <div className="max-w-3xl mx-auto text-center py-20">
          <h2 className="text-xl font-semibold text-ink mb-3">Section not found</h2>
          <p className="text-muted">The academic section you requested does not exist.</p>
        </div>
      </Shell>
    );
  }

  return (
    <Shell>
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="flex items-center gap-2 mb-2">
          <AQVERAHorizontalLogo size={20} variant="light" className="hidden lg:block" />
          <span className="text-ink font-editorial text-2xl font-semibold tracking-tight">
            {section.label}
          </span>
        </div>
        <p className="text-muted">{section.description}</p>

        <div className="bg-white border border-border rounded-xl p-6">
          <h2 className="font-editorial text-lg font-semibold mb-6">Subjects</h2>
          {subjects.length > 0 ? (
            <div className="space-y-3">
              {subjects.map((subject) => (
                <Link
                  key={subject.id}
                  href={`/courses?domain=${subject.id}`}
                  className="flex items-center justify-between bg-white border border-border rounded-xl px-5 py-4 hover:border-sage-dark/40 transition-colors block"
                >
                  <div>
                    <h3 className="font-semibold text-ink">{subject.label}</h3>
                    <p className="text-xs text-muted">{subject.description}</p>
                  </div>
                  <span className="text-xs text-muted">→</span>
                </Link>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <h3 className="font-semibold text-ink mb-2">No subjects available yet</h3>
              <p className="text-muted max-w-xs mx-auto">
                Subjects for this section will appear as courses are created and organized.
              </p>
            </div>
          )}
        </div>
      </div>
    </Shell>
  );
}
