"use client";

import Link from "next/link";
import { Shell } from "@/components/Shell";
import { AQVERAHorizontalLogo } from "@/components/AQVERALogo";
import { ACADEMIC_SECTIONS } from "@/lib/sections";

export default function SectionsPage() {
  return (
    <Shell>
      <div className="max-w-4xl mx-auto space-y-10">
        <div className="flex items-center gap-2 mb-2">
          <AQVERAHorizontalLogo size={20} variant="light" className="hidden lg:block" />
          <span className="text-ink font-editorial text-2xl font-semibold tracking-tight">
            Academic Sections
          </span>
        </div>
        <p className="text-muted">
          Explore AQVERA&apos;s academic domains. Select a section to browse its subjects and courses.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {ACADEMIC_SECTIONS.map((section) => (
            <Link
              key={section.id}
              href={`/sections/${section.id}`}
              className="group bg-white border border-border rounded-xl p-6 flex flex-col hover:border-sage-dark/40 transition-colors block"
            >
              <div className="w-10 h-10 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200">
                <span className="text-xl">{section.icon}</span>
              </div>
              <h3 className="font-semibold text-ink mb-1">{section.label}</h3>
              <p className="text-xs text-muted text-center mb-auto flex-1">
                {section.description}
              </p>
              <span className="mt-4 text-xs font-medium text-muted hover:text-ink transition-colors">
                Explore section →
              </span>
            </Link>
          ))}
        </div>
      </div>
    </Shell>
  );
}
