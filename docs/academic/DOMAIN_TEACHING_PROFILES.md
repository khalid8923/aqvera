# DOMAIN_TEACHING_PROFILES.md

# AQVERA — Domain Teaching Profiles

## Purpose

Domain teaching profiles extend the Standard Teaching Methodology with domain-specific instructional behavior. The core methodology (mastery estimation, evidence rules, decision pipeline, validation rules) remains unchanged across domains. Each profile defines how the standard is applied in a specific academic domain.

## Profile Structure

Each domain teaching profile includes:

| Field | Description |
|-------|-------------|
| id | UUID |
| name | Display name |
| domain | Domain identifier (mathematics, computer_science, physics, languages, humanities) |
| description | Profile description |
| methodology_version | Reference to active methodology version |
| concept_ordering | Domain-specific ordering of concepts |
| activity_types | Domain-appropriate activity types |
| visualizations | Domain-specific visualization capabilities |
| misconception_patterns | Domain-specific common misconceptions |
| terminology | Domain-specific terms and definitions |
| assessment_types | Preferred assessment types for the domain |
| is_active | Whether this is the active profile for the domain |

## Mathematics Profile (PROPOSED — Initial Domain)

**Domain:** mathematics

### Concept Ordering
Foundational arithmetic → algebra → functions → geometry → trigonometry → calculus → statistics. Prerequisite graph enforced: a student must demonstrate mastery of prerequisite objectives before advancing.

### Activity Types
- Worked examples
- Step-by-step problem solving
- Function graphing (visual)
- Equation manipulation
- Numerical problem sets
- Mathematical expression evaluation

### Visualizations
- Function graphing (deterministic)
- Equation visualization
- Calculus visualizations (derivatives, integrals)
- Statistical charts and distributions

### Assessment Types
- Multiple choice
- Numerical problems (deterministic validation)
- Mathematical expressions (deterministic validation)
- Short answer
- Conceptual questions

### Common Misconceptions
- Sign errors in algebra
- Order of operations confusion
- Misunderstanding of function notation
- Confusion between derivative and integral
- Misinterpreting graphs

### Prerequisite Relationships
Explicit prerequisite graph: e.g., "solving linear equations" requires "understanding variables" and "arithmetic with negative numbers".

## Computer Science Profile (DEFERRED)

**Domain:** computer_science

### Activity Types
- Code tracing
- Algorithm visualization
- Data structure manipulation
- Programming exercises (sandboxed execution deferred)
- Code flow diagramming

### Visualizations
- Algorithm visualization
- Data structure visualization
- Execution traces
- Code flow diagrams

### Assessment Types
- Multiple choice
- Short answer
- Programming exercises (without direct code execution in main process)
- Conceptual questions

### Common Misconceptions
- Off-by-one errors
- Confusion between reference and value types
- Misunderstanding recursion
- Variable scope confusion

## Physics Profile (DEFERRED)

**Domain:** physics

### Activity Types
- Conceptual diagrams
- Scientific graphing
- Interactive simulations (where feasible)
- Numerical problem solving

### Visualizations
- Scientific graphs
- Conceptual diagrams
- Force/vector diagrams
- Motion simulations

### Assessment Types
- Multiple choice
- Numerical problems
- Short answer
- Conceptual questions

## Languages Profile (DEFERRED)

**Domain:** languages

### Activity Types
- Grammar exercises
- Vocabulary building
- Sentence construction
- Reading comprehension

### Visualizations
- Grammar diagrams
- Vocabulary maps
- Sentence structure visualization

### Assessment Types
- Multiple choice
- Multiple select
- Short answer
- Language exercises

## Humanities Profile (DEFERRED)

**Domain:** humanities

### Activity Types
- Timeline construction
- Concept mapping
- Relationship analysis
- Essay writing (subjective evaluation with criteria)

### Visualizations
- Historical timelines
- Concept maps
- Event-concept relationship diagrams

### Assessment Types
- Multiple choice
- Short answer
- Conceptual questions
- Essay (subjective evaluation with criteria and confidence)

## Adding a New Domain

To add a domain teaching profile:

1. Create the profile record in `TeachingProfiles`.
2. Define concept ordering, activity types, visualizations, misconception patterns.
3. Map prerequisite relationships for domain objectives.
4. Register domain-appropriate assessment types.
5. The core methodology and adaptive engine require no changes — the profile is data, not code.

## Profile vs. Methodology

| Teaching Methodology (Core) | Domain Profile (Extension) |
|----------------------------|---------------------------|
| Mastery estimation rules | Domain concepts and ordering |
| Evidence strength rules | Domain activity types |
| Decision pipeline | Domain visualizations |
| No fixed learning styles | Domain misconceptions |
| Versioned standard | Assessment preferences |
| AI boundaries | Terminology |
