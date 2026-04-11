# ADR-0004: Write the agent loop by hand

**Status:** Accepted
**Date:** 2026-04-11

## Context

Several frameworks offer pre-built agent abstractions: LangChain, LlamaIndex, CrewAI, AutoGen, and the Claude Agent SDK. The investigator needs a tool-use loop. The obvious question is whether to adopt one of these frameworks or write the loop directly against the Anthropic SDK.

## Decision

Write the loop by hand using the Anthropic SDK directly. ~40 lines of Python in `investigator/loop.py`.

## Alternatives considered

- **LangChain / LlamaIndex / CrewAI / AutoGen.** Thick, leaky abstractions. Docs lag the libraries. When something goes wrong you debug the framework instead of your own logic. For a learning project specifically, adopting a framework means you learn the framework, not the underlying concepts.
- **Claude Agent SDK.** More honest than third-party frameworks — it's from Anthropic and it handles tool-use orchestration and context management without pretending to be a universal abstraction. Reasonable choice, but hides the exact mechanics this project is meant to teach. Adopt later if the hand-written loop becomes a real bottleneck.

## Consequences

- ~40 lines of loop code owned by this project.
- Full understanding of what an agent loop actually is — turns, tool calls, stop reasons, message accumulation.
- Tool definitions live as Python data structures in `investigator/tools.py` and are trivial to inspect and modify.
- Framework adoption is an explicit later decision, not a starting assumption.
