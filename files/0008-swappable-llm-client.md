# ADR-0008: Swappable LLM client; Anthropic as default

**Status:** Accepted
**Date:** 2026-04-11

## Context

The system makes LLM calls from both the curator and the investigator. Pricing, rate limits, and model capabilities differ across providers. The project wants to avoid lock-in without adding a dependency just to avoid lock-in.

## Decision

Define a Python `Protocol` called `LLMClient` with a `complete(system, messages, tools) -> Response` method and a handful of response/content types. Implement it first against the Anthropic SDK. Any future provider is a new class implementing the same protocol.

## Alternatives considered

- **Hardcode Anthropic everywhere.** Painful to change later. Every test has to import the Anthropic SDK.
- **LiteLLM or similar aggregator.** Adds a dependency and a layer of indirection for the simplest-possible abstraction that costs maybe 50 lines of code to write by hand.
- **Self-host a local model (Ollama, vLLM).** Separate project. Worse tool-use quality than hosted frontier models. Tension with running on a cloud k8s cluster.

## Consequences

- Clean seam for testing: the mock LLM client used in unit tests implements the same Protocol.
- Budget tracking lives in the Anthropic implementation (or a wrapper around it) so it applies uniformly.
- Swapping providers is one class, not a refactor.
- Prompt caching (see ADR-0009) is an Anthropic-specific feature — if a second provider is added, the interface needs to accept cache hints that providers can honor or ignore.
