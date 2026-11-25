"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Shell } from "@/components/Shell";
import { useAuth } from "@/components/AuthContext";

type OnboardingStep =
  | "welcome"
  | "language"
  | "interests"
  | "course"
  | "material"
  | "tutor";

const STEP_TITLES: Record<OnboardingStep, string> = {
  welcome: "Welcome to AQVERA",
  language: "Choose your language",
  interests: "Select your interests",
  course: "Create your first course",
  material: "Upload your first material",
  tutor: "Meet your AI tutor",
};

export default function OnboardingPage() {
  const router = useRouter();
  const { completeOnboardingStep, getOnboarding, isLoading } = useAuth();
  const [currentStep, setCurrentStep] = useState<OnboardingStep>("welcome");
  const [onboardingLoading, setOnboardingLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    async function initOnboarding() {
      setOnboardingLoading(true);
      try {
        const data = await getOnboarding();
        if (data) {
          // Find the first incomplete step
          const order: OnboardingStep[] = [
            "welcome",
            "language",
            "interests",
            "course",
            "material",
            "tutor",
          ];
          const stepKeys: Record<OnboardingStep, string> = {
            welcome: "welcome_seen",
            language: "language_selected",
            interests: "interests_selected",
            course: "first_course_created",
            material: "first_material_uploaded",
            tutor: "tutor_introduced",
          };
          for (const s of order) {
            const key = stepKeys[s];
            if (!cancelled && !(data as Record<string, boolean>)[key]) {
              setCurrentStep(s);
              break;
            }
          }
          if (!cancelled && data.completed) {
            router.push("/dashboard");
          }
        }
      } catch {
        // ignore
      } finally {
        if (!cancelled) setOnboardingLoading(false);
      }
    }
    if (!isLoading) {
      void initOnboarding();
    }
    return () => {
      cancelled = true;
    };
  }, [isLoading, getOnboarding, router]);

  async function completeStep(step: OnboardingStep) {
    setOnboardingLoading(true);
    try {
      const keyMap: Record<OnboardingStep, string> = {
        welcome: "welcome_seen",
        language: "language_selected",
        interests: "interests_selected",
        course: "first_course_created",
        material: "first_material_uploaded",
        tutor: "tutor_introduced",
      };
      await completeOnboardingStep(keyMap[step]);

      const order: OnboardingStep[] = [
        "welcome",
        "language",
        "interests",
        "course",
        "material",
        "tutor",
      ];
      const currentIndex = order.indexOf(currentStep);
      if (currentIndex + 1 < order.length) {
        setCurrentStep(order[currentIndex + 1]);
      } else {
        router.push("/dashboard");
      }
    } catch {
      // error handled by UI
    } finally {
      setOnboardingLoading(false);
    }
  }

  if (isLoading || onboardingLoading) {
    return (
      <Shell>
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-muted">Setting up your account…</p>
        </div>
      </Shell>
    );
  }

  const stepConfigs: Record<OnboardingStep, () => React.ReactNode> = {
    welcome: () => (
      <WelcomeStep onNext={() => completeStep("welcome")} />
    ),
    language: () => (
      <LanguageStep onNext={() => completeStep("language")} />
    ),
    interests: () => (
      <InterestsStep onNext={() => completeStep("interests")} />
    ),
    course: () => (
      <CourseStep onNext={() => completeStep("course")} />
    ),
    material: () => (
      <MaterialStep onNext={() => completeStep("material")} />
    ),
    tutor: () => (
      <TutorStep onNext={() => completeStep("tutor")} />
    ),
  };

  return (
    <Shell>
      <div className="max-w-2xl mx-auto space-y-8 p-6">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-ink font-editorial text-2xl font-semibold tracking-tight">
            AQVERA
          </span>
        </div>

        <div className="bg-white border border-border rounded-xl p-8">
          <h2 className="text-2xl font-editorial font-semibold text-ink mb-2">
            {STEP_TITLES[currentStep]}
          </h2>
          <p className="text-muted text-sm mb-6">
            Step {["welcome", "language", "interests", "course", "material", "tutor"].indexOf(currentStep) + 1} of 6
          </p>

          {stepConfigs[currentStep]()}
        </div>

        <p className="text-center text-sm text-muted">
          Already have an account?{" "}
          <Link href="/login" className="text-sage-dark hover:text-ink font-medium">
            Sign in
          </Link>
        </p>
      </div>
    </Shell>
  );
}

function WelcomeStep({ onNext }: { onNext: () => void }) {
  return (
    <div className="text-center">
      <div className="w-16 h-16 rounded-full bg-sage/10 flex items-center justify-center mx-auto mb-6 text-sage-dark text-2xl">
        🎓
      </div>
      <h3 className="text-xl font-semibold text-ink mb-3">Welcome to AQVERA</h3>
      <p className="text-muted mb-6 max-w-sm mx-auto leading-relaxed">
        AQVERA helps you turn your course materials into a structured learning
        experience with AI tutoring, assessments, and progress tracking.
      </p>
      <button
        onClick={onNext}
        className="bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors"
      >
        Get started
      </button>
    </div>
  );
}

function LanguageStep({ onNext }: { onNext: () => void }) {
  const [language, setLanguage] = useState("en");
  const languages = [
    { code: "en", label: "English" },
    { code: "ar", label: "العربية (Arabic)" },
    { code: "es", label: "Español" },
    { code: "fr", label: "Français" },
    { code: "de", label: "Deutsch" },
  ];

  return (
    <div className="space-y-4">
      <p className="text-muted">
        Select your preferred language for the platform interface and learning
        content.
      </p>
      <div className="space-y-3">
        {languages.map((l) => (
          <button
            key={l.code}
            onClick={() => setLanguage(l.code)}
            className={`w-full text-left px-4 py-3 rounded-md border text-sm ${
              language === l.code
                ? "bg-sage/50 border-sage-dark text-ink font-medium"
                : "border-border text-muted hover:bg-surface"
            }`}
          >
            {l.label}
          </button>
        ))}
      </div>
      <button
        onClick={onNext}
        disabled={!language}
        className="w-full bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy disabled:opacity-50 transition-colors"
      >
        Continue
      </button>
    </div>
  );
}

function InterestsStep({ onNext }: { onNext: () => void }) {
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const interests = [
    "Mathematics",
    "Programming & Computer Science",
    "Physics",
    "Chemistry",
    "Biology & Life Sciences",
    "History",
    "Literature & Writing",
    "Economics",
    "Psychology",
    "Languages",
  ];

  function toggle(interest: string) {
    const next = new Set(selected);
    if (next.has(interest)) next.delete(interest);
    else next.add(interest);
    setSelected(next);
  }

  return (
    <div className="space-y-4">
      <p className="text-muted">
        Select the academic areas you&apos;re interested in. This helps AQVERA
        recommend relevant courses and materials.
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {interests.map((interest) => (
          <button
            key={interest}
            onClick={() => toggle(interest)}
            className={`px-4 py-3 rounded-md border text-sm ${
              selected.has(interest)
                ? "bg-sage/50 border-sage-dark text-ink font-medium"
                : "border-border text-muted hover:bg-surface"
            }`}
          >
            {interest}
          </button>
        ))}
      </div>
      <button
        onClick={onNext}
        disabled={selected.size === 0}
        className="w-full bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy disabled:opacity-50 transition-colors"
      >
        Continue
      </button>
    </div>
  );
}

function CourseStep({ onNext }: { onNext: () => void }) {
  const [title, setTitle] = useState("");
  const [domain, setDomain] = useState("mathematics");
  const [error, setError] = useState("");

  const domains = [
    { id: "mathematics", label: "Mathematics & Statistics" },
    { id: "computer_science", label: "Programming & Computer Science" },
    { id: "physics", label: "Physics" },
    { id: "chemistry", label: "Chemistry" },
    { id: "biology", label: "Biology & Life Sciences" },
    { id: "history", label: "History" },
    { id: "literature", label: "Literature & Writing" },
    { id: "economics", label: "Economics" },
    { id: "psychology", label: "Psychology" },
    { id: "languages", label: "Languages" },
  ];

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) {
      setError("Please enter a course title");
      return;
    }
    setError("");
    try {
      const res = await fetch("/api/courses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, subject_domain: domain }),
      });
      if (!res.ok) throw new Error("Failed to create course");
      await onNext();
    } catch {
      setError("Failed to create course. Please try again.");
    }
  }

  return (
    <div className="space-y-4">
      <p className="text-muted">
        Create your first course to begin organizing your learning materials.
      </p>
      {error && (
        <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta rounded-md p-3 text-sm">
          {error}
        </div>
      )}
      <form onSubmit={handleCreate} className="space-y-3">
        <div>
          <label className="block text-sm font-medium mb-1 text-ink">Course title</label>
          <input
            required
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none text-ink"
            placeholder="e.g. Introduction to Calculus"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1 text-ink">Subject domain</label>
          <select
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            className="w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none text-ink bg-white"
          >
            {domains.map((d) => (
              <option key={d.id} value={d.id}>
                {d.label}
              </option>
            ))}
          </select>
        </div>
        <button
          type="submit"
          className="w-full bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors"
        >
          Create course
        </button>
      </form>
    </div>
  );
}

function MaterialStep({ onNext }: { onNext: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    setError("");
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("/api/materials/upload", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Upload failed");
      await onNext();
    } catch {
      setError("Failed to upload material. Please try again.");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="space-y-4">
      <p className="text-muted">
        Upload your first learning material (PDF, DOCX, PPTX, or TXT). AQVERA
        will process it so you can ask questions and generate study content.
      </p>
      {error && (
        <div className="bg-terracotta/10 border border-terracotta/20 text-terracotta rounded-md p-3 text-sm">
          {error}
        </div>
      )}
      <div>
        <label className="block text-sm font-medium mb-2 text-ink">Choose file</label>
        <input
          type="file"
          accept=".pdf,.docx,.pptx,.txt"
          onChange={(e) => {
            if (e.target.files?.[0]) setFile(e.target.files[0]);
          }}
          className="w-full border border-border rounded-md px-3 py-2 text-sm"
        />
      </div>
      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        className="w-full bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy disabled:opacity-50 transition-colors"
      >
        {uploading ? "Processing…" : "Upload material"}
      </button>
    </div>
  );
}

function TutorStep({ onNext }: { onNext: () => void }) {
  return (
    <div className="text-center">
      <div className="w-16 h-16 rounded-full bg-sage/10 flex items-center justify-center mx-auto mb-6 text-sage-dark text-2xl">
        💬
      </div>
      <h3 className="text-xl font-semibold text-ink mb-3">Meet your AI tutor</h3>
      <p className="text-muted mb-6 max-w-sm mx-auto leading-relaxed">
        Your AI tutor can answer questions about your course materials, explain
        difficult concepts, and help you prepare for assessments. Ask anything
        in your course workspace.
      </p>
      <button
        onClick={onNext}
        className="bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors"
      >
        Finish setup
      </button>
    </div>
  );
}
