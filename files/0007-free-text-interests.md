# ADR-0007: Free-text interests over categories

**Status:** Accepted
**Date:** 2026-04-11

## Context

The curator needs to know what each user cares about in order to pick markets worth watching. The interest description could be structured (categories, tags, picked from an enum) or unstructured (free text read directly by the LLM).

## Decision

One `TEXT` column per user. The curator reads it raw as part of its prompt. Users can write things like "US politics and anything crypto-related, skip sports" or "I want to know when obscure markets suddenly get volume."

## Alternatives considered

- **Category enums.** Rigid. Someone has to maintain the category list. Markets don't always map cleanly to one category. The LLM already understands natural language; a category enum is a worse version of what the model can do with a sentence.
- **Tag-based (many-to-many).** Same problems as categories plus extra UI and schema complexity.
- **No steering, global feed.** Bad personalization — if every user gets the same feed, there's no reason to have users at all.

## Consequences

- Zero schema complexity — one TEXT column, that's it.
- Maximum flexibility for users.
- The curator prompt has to do the interpretation. Prompt quality matters more as a result.
- No tooling needed to "add a new category" — users just update their description.
