"""Versioned prompt templates for AQVERA AI tasks.

Prompts are versioned like the teaching methodology. Each template is a
structured contract that providers fill; prompts never override system policy.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PromptTemplate:
    id: str
    version: str
    task_type: str
    system_prompt: str
    user_template: str
    variables: list[str]


# --- Standard teaching methodology prompts (version 1.0.0) ---

TUTOR_EXPLANATION_V1 = PromptTemplate(
    id="tutor.explanation",
    version="1.0.0",
    task_type="tutor_explanation",
    system_prompt=(
        "You are AQVERA's academic tutor. Apply the Standard Teaching Methodology: "
        "identify the learning objective, establish prerequisite knowledge, explain the "
        "concept, break difficult concepts into steps, give a relevant example, check "
        "understanding, correct misconceptions, provide guided practice, and summarize. "
        "Ground answers in provided sources. Distinguish evidence from sources, external "
        "knowledge, reasoned inference, and uncertainty. Never fabricate citations. "
        "If sources do not contain the answer, say so explicitly."
    ),
    user_template=(
        "Question: {question}\n"
        "Concept: {concept}\n"
        "Difficulty: {level}\n"
        "Language: {language}\n"
        "Sources:\n{sources}"
    ),
    variables=["question", "concept", "level", "language", "sources"],
)

QUESTION_GENERATION_V1 = PromptTemplate(
    id="question.generation",
    version="1.0.0",
    task_type="question_generation",
    system_prompt=(
        "Generate assessment questions for an academic topic. Questions must be "
        "unambiguous, aligned to learning objectives, and appropriate difficulty. "
        "Include an answer key and validation method. Questions are validated before use."
    ),
    user_template=(
        "Topic: {topic}\n"
        "Count: {count}\n"
        "Type: {question_type}\n"
        "Difficulty: {difficulty}"
    ),
    variables=["topic", "count", "question_type", "difficulty"],
)

ANSWER_EVALUATION_V1 = PromptTemplate(
    id="answer.evaluation",
    version="1.0.0",
    task_type="answer_evaluation",
    system_prompt=(
        "Evaluate a student answer against explicit scoring criteria. Return a "
        "correctness judgment, score (0-1), confidence (0-1), and brief feedback. "
        "State uncertainty where criteria are ambiguous."
    ),
    user_template=(
        "Question: {question}\n"
        "Student answer: {answer}\n"
        "Criteria: {criteria}"
    ),
    variables=["question", "answer", "criteria"],
)


class PromptRegistry:
    """Holds versioned prompt templates."""

    def __init__(self) -> None:
        self._templates: dict[str, PromptTemplate] = {
            t.id: t for t in [TUTOR_EXPLANATION_V1, QUESTION_GENERATION_V1, ANSWER_EVALUATION_V1]
        }

    def get(self, template_id: str, version: str | None = None) -> PromptTemplate | None:
        tmpl = self._templates.get(template_id)
        if tmpl is None:
            return None
        if version is not None and tmpl.version != version:
            return None
        return tmpl

    def render(self, template_id: str, variables: dict[str, str], version: str | None = None) -> tuple[str, str] | None:
        tmpl = self.get(template_id, version)
        if tmpl is None:
            return None
        try:
            user = tmpl.user_template.format(**variables)
        except KeyError as exc:
            return None
        return tmpl.system_prompt, user
