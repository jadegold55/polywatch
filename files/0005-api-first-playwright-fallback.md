# ADR-0005: Polymarket API first, Playwright as fallback

**Status:** Accepted
**Date:** 2026-04-11

## Context

Polymarket exposes market data through its CLOB and Gamma HTTP APIs. Structured data (markets, prices, volume, resolution status) is available there. Some UI-only content (comments, social signals, news links posted in discussion) is not in the API. The investigator benefits from access to both.

## Decision

Use the HTTP API for all structured data. Use Playwright only for content not exposed by the API, and only from the investigator's tools — never from the evaluator's hot loop.

## Alternatives considered

- **Playwright-only.** Slow, fragile, wasteful. Scraping the same data the API would hand over in JSON is pointless.
- **API-only.** Loses the investigator's ability to cite social signals, which is a meaningful part of what makes a notification useful ("price moved because this comment thread went viral").

## Consequences

- The evaluator never touches a browser. Its tick cost is predictable and low.
- The investigator has browser access as *one tool among several*, not as the default.
- Playwright Chromium is installed in the worker image and thus in the investigator's pod. The evaluator could use a slimmer image in theory; keeping a single shared worker image is simpler and the size overhead is acceptable.
- Cost and flakiness of browser automation are bounded — only investigations pay for it, and only when the agent decides to call the tool.
