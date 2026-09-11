# Domain Docs

This is a single-context repository.

## Before exploring

Read these files when they exist:

- `CONTEXT.md` at the repository root
- Relevant decisions under `docs/adr/`

If these files do not exist, proceed silently. The `/domain-modeling` skill creates them when domain terms or decisions need to be recorded.

## File structure

```text
/
├── CONTEXT.md
├── docs/adr/
└── src/
```

## Vocabulary

When naming domain concepts in issue titles, refactor proposals, hypotheses, or tests, use the terminology defined in `CONTEXT.md`.

If a needed concept is not yet defined there, consider whether the glossary needs to be updated.

## ADR conflicts

If a proposed change contradicts an existing ADR, explicitly identify the conflict instead of silently overriding it.
