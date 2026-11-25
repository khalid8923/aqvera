# PRODUCT_EXPERIENCE_PRINCIPLES.md

# AQVERA — Product Experience Principles

Status: DECIDED

## Product Experience Vision

AQVERA is an Adaptive Academic Learning Platform for university students. It transforms students' academic materials into organized learning experiences that adapt to evidence of the student's understanding over time.

The platform owns the learning experience. AI models are supporting capabilities, not the entire product. Teaching methodology provides instructional consistency. Academic materials provide evidence. The adaptive engine determines the next useful learning step.

No single AI model should control the entire academic experience.

## Core UX Principles

| Principle | Description |
|-----------|-------------|
| Platform owns the experience | AI provides capabilities; the platform orchestrates instruction, assessment, and adaptation. The UI must make the platform's role visible, not hide it behind a chat. |
| Teaching methodology is versioned | A single, versioned teaching methodology applies across all domains. The interface must not imply that each student gets a separately invented methodology. |
| Adaptive responds to evidence | Adaptation responds to demonstrated student performance and learning needs, not to fixed learning-style labels or assumptions. |
| Academic materials are evidence | Uploaded documents are sources of truth. The UI must show traceability from course content back to source materials where available. |
| Student understanding and control | Students must understand what the system is doing and why, and retain appropriate control over their learning path, courses, and preferences. |
| No fabricated state | Unimplemented functionality must never appear operational. Never fabricate progress, mastery percentages, lesson completion, AI analysis, upload processing, or generated content. |
| Privacy, clarity, trust | Minimize PII sent to external providers. Use clear language. Build trust through honest states, visible evidence, and explainable recommendations. |
| Clarity over visual complexity | The interface prioritizes academic clarity, not decorative UI. Every visual choice must serve a learning or comprehension purpose. |

## Student Needs

- Know what to study next and why.
- See evidence behind mastery estimates and recommendations.
- Upload academic materials and understand their processing status.
- Navigate between courses, topics, lessons, and assessments without disorientation.
- Complete assessments and receive clear feedback without being shown answers prematurely.
- Return to unfinished activities and resume where they left off.
- Trust that their data and uploaded materials are handled privately.

## Trust and Transparency Principles

- Every adaptive recommendation states why it was selected and what evidence supports it.
- Mastery is estimated from structured assessment evidence, never silently assigned by AI.
- AI-generated content is attributed and validated against structured contracts before use.
- Processing states (upload, extraction, generation) are shown honestly with progress, never simulated.
- Errors are identified in text, not communicated by color alone.
- Unimplemented features are marked "coming soon" or hidden, never shown as functional placeholders with fake data.

## Cognitive Load Management

- One primary action per screen where possible.
- Short, actionable instructions; academically appropriate language.
- Progressive disclosure: show advanced options only when relevant.
- Consistent terminology across the product.
- Consistent navigation and layout so students build spatial memory.
- Avoid decorative animation; motion only when it conveys state change or relationship.

## Learning-Oriented Interaction Principles

- Assessment interfaces never reveal correct answers before completion unless the activity permits it.
- Feedback communicates what is understood, what remains weak, why a recommendation was made, and what to do next.
- Learning evidence is traceable; records are immutable; corrections are new records.
- Visualizations are deterministic where academic correctness matters (mathematics, science).
- Students can review previous learning and see mastery by course, module, topic, and objective.

## What Makes AQVERA Different

| AQVERA | Generic LMS | AI Chatbot |
|--------|-------------|------------|
| Platform owns full learning experience | Course repository; instruction separate | Chat wrapper; no instructional ownership |
| Versioned teaching methodology | Instructor-dependent | Prompt-dependent, inconsistent |
| Evidence-based mastery estimation | Completion-based or single-answer | No mastery model, or silently assigned |
| Traceability to academic materials | File attachments, unstructured | No source grounding |
| Explainable adaptive recommendations | Fixed prerequisites | Hallucinated rationale |
| Provider-independent AI | None | Single vendor lock-in |
| Honest UI states, no fabricated progress | Often polished but empty | Often overconfident, unverifiable |
