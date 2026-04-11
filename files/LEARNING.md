# Learning Journal

Things I now understand that I didn't understand before. One entry per learning moment, written within a day or two while it's still fresh.

## How to use this file

- **Entries are dated.** Newest at the top.
- **Write what was confusing, not just what you learned.** The confusion is the more valuable record. "I thought services and pods were the same thing" is more useful than "services route traffic to pods" — the first one captures what your mental model used to be and how it had to change.
- **One paragraph to one page per entry.** Not a tutorial, not a diary. A specific thing that clicked.
- **It's okay for entries to be wrong in hindsight.** Don't edit old entries. If you later realize your understanding was off, write a new entry that corrects it.

## Template

```
## YYYY-MM-DD — [topic]

**What I was confused about:** …

**What I thought was true that wasn't:** …

**What actually clicked:** …

**Example that helped it land:** …
```

---

<!-- Entries go below this line, newest first -->

## 2026-04-11 — Integrating Claude Code into a project without touching the API

**What I was confused about:** The plan called for a "Claude Code GitHub integration" for PR review and I assumed that meant I had to wire up the Anthropic API myself — get a key, write code that calls it, add a workflow that invokes it manually.

**What I thought was true that wasn't:** That using Claude in CI required writing API integration code, the same way you'd integrate any other service.

**What actually clicked:**
Just use the github app auth path using claude in terminal

**Example that helped it land:** Ran `/install-github-app` inside the Claude Code CLI, merged the PR it opened, then opened a test PR and Claude posted a review comment automatically. Zero API code written.
