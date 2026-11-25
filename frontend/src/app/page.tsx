import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen bg-paper text-ink">
      <nav className="border-b border-border bg-white/80 backdrop-blur sticky top-0 z-20">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <svg
              width="24"
              height="24"
              viewBox="0 0 32 32"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M16 2 L4 14 L16 26 L28 14 L16 2 Z"
                fill="#101D2B"
                stroke="#315C50"
                strokeWidth="1.5"
                strokeLinejoin="round"
              />
              <path
                d="M8 12 L16 4 L24 12"
                fill="none"
                stroke="#315C50"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M10 16 L16 10 L22 16"
                fill="none"
                stroke="#315C50"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                opacity={0.6}
              />
              <path
                d="M16 2 L16 26"
                fill="none"
                stroke="#315C50"
                strokeWidth="1.5"
                strokeLinecap="round"
              />
            </svg>
            <span className="font-bold text-xl tracking-tight">AQVERA</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="hidden sm:block">
              <button className="text-sm font-medium text-muted hover:text-ink px-4 py-2">
                Sign in
              </button>
            </Link>
            <Link href="/dashboard">
              <button className="bg-ink text-white px-6 py-2.5 rounded-md text-sm font-medium hover:bg-navy transition-colors">
                Start learning
              </button>
            </Link>
          </div>
        </div>
      </nav>

      <main className="flex-1">
        <section className="max-w-6xl mx-auto px-6 py-20 text-center">
          <h1 className="font-editorial text-4xl md:text-6xl font-semibold leading-tight mb-6">
            Your learning deserves more than
            <br />
            another AI chat.
          </h1>
          <p className="text-lg text-muted max-w-prose mx-auto mb-10">
            AQVERA turns your university materials into a structured learning
            experience that understands your progress and helps you move forward.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/dashboard">
              <button className="bg-ink text-white px-8 py-3.5 rounded-md text-lg font-medium hover:bg-navy transition-colors">
                Start learning
              </button>
            </Link>
            <Link href="/courses">
              <button className="bg-surface border border-border text-ink px-8 py-3.5 rounded-md text-lg font-medium hover:bg-surface transition-colors">
                Explore AQVERA
              </button>
            </Link>
          </div>
        </section>

        <section className="py-24 border-y border-border bg-white">
          <div className="max-w-6xl mx-auto px-6">
            <h2 className="font-editorial text-2xl md:text-3xl mb-12">How AQVERA works</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div>
                <h3 className="font-semibold mb-4">1. Upload your materials</h3>
                <p className="text-muted leading-relaxed">
                  Share your course documents, lecture notes, and readings.
                  AQVERA extracts the academic structure from your own sources.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-4">2. Structured courses</h3>
                <p className="text-muted leading-relaxed">
                  Materials become courses with modules, topics, and learning
                  objectives — all traceable to your source documents.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-4">3. Adaptive progress</h3>
                <p className="text-muted leading-relaxed">
                  The system tracks what you&apos;ve mastered and recommends what to
                  study next, with clear reasoning for every suggestion.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="py-24">
          <div className="max-w-6xl mx-auto px-6">
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              <div>
                <h2 className="font-editorial text-2xl md:text-3xl mb-6">
                  Consistent academic teaching across every subject
                </h2>
                <p className="text-muted leading-relaxed mb-8">
                  AQVERA applies a single, versioned teaching methodology to
                  every domain. AI models provide capabilities — the platform
                  owns the learning experience.
                </p>
                <ul className="space-y-4 text-left">
                  <li className="flex items-start gap-3">
                    <span className="text-sage-dark">✓</span>
                    <span className="text-ink">Versioned teaching methodology</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-sage-dark">✓</span>
                    <span className="text-ink">No fixed learning-style labels</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-sage-dark">✓</span>
                    <span className="text-ink">Evidence-based mastery estimation</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-sage-dark">✓</span>
                    <span className="text-ink">Provider-independent AI</span>
                  </li>
                </ul>
              </div>
              <div className="bg-surface border border-border rounded-lg p-8">
                <h3 className="font-semibold mb-4">Product preview</h3>
                <div className="flex items-center gap-4 text-muted text-sm">
                  <span className="w-2 h-2 rounded-full bg-terracotta" />
                  <span>Student Dashboard</span>
                </div>
                <div className="flex items-center gap-4 text-muted text-sm mt-4">
                  <span className="w-2 h-2 rounded-full bg-terracotta" />
                  <span>Course Workspace</span>
                </div>
                <div className="flex items-center gap-4 text-muted text-sm mt-4">
                  <span className="w-2 h-2 rounded-full bg-terracotta" />
                  <span>Assessment Interface</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="py-24 text-center">
          <div className="max-w-prose mx-auto px-6">
            <h2 className="font-editorial text-2xl md:text-3xl mb-8">
              Start your first course today
            </h2>
            <Link href="/dashboard">
              <button className="bg-ink text-white px-8 py-3.5 rounded-md text-lg font-medium hover:bg-navy transition-colors inline-block">
                Create your course
              </button>
            </Link>
          </div>
        </section>
      </main>

      <footer className="border-t border-border bg-white py-12">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-3">
            <svg
              width="20"
              height="20"
              viewBox="0 0 32 32"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M16 2 L4 14 L16 26 L28 14 L16 2 Z"
                fill="#101D2B"
                stroke="#315C50"
                strokeWidth="1.5"
                strokeLinejoin="round"
              />
            </svg>
            <span className="font-bold">AQVERA</span>
          </div>
          <p className="text-sm text-muted">
            Academic learning platform. Built for students, owned by students.
          </p>
        </div>
      </footer>
    </div>
  );
}
