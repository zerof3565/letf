---
name: websearch
description: >
  Research current or external web information using a portable 3-stage
  workflow: SearXNG for URL discovery, source triage, optional Scrapy-based
  batch fetching, and Playwright MCP for rendered page inspection and verification.
---

# Web Search Research Agent

Use this skill when the user asks to research, look up, verify, compare sources, find current information, or gather web evidence.

## Required Workflow

Use this staged process:

1. **Discovery:** Use the `searxng` MCP tool, or the local SearXNG JSON API at `http://127.0.0.1:8888/search?q=...&format=json`, to discover candidate URLs.
2. **Triage:** Rank candidate URLs before reading deeply. Prefer official docs, primary sources, standards pages, release notes, source repositories, issue trackers, and reputable references.
3. **Optional acquisition:** For batch content extraction after triage, use `uv run websearch-pipeline "query" --limit 5` or direct URLs with `uv run websearch-pipeline --url https://example.com`. This uses Scrapy first, `scrapy-playwright` only as a fallback for weak HTML results, and writes markdown plus `results.json` under `output/research/`.
4. **Verification:** Use Playwright MCP to inspect rendered pages, dynamic docs, version selectors, hidden sections, and other page content before treating anything as evidence.

Do not use raw webfetch to scrape search result pages or page content.

Do not treat SearXNG snippets as evidence. Snippets are only discovery hints.

Do not cite generated markdown from the fetch pipeline without Playwright verification for important claims. Treat it as extracted page content that speeds reading, not as final evidence.

## Discovery Rules

Use search broadly enough to find candidate sources, but do not over-collect. For most questions, start with 1-3 focused queries and broaden only if candidates are weak.

Good discovery targets:

- Official documentation
- Release notes and changelogs
- Standards/specification pages
- Source repositories
- Issue trackers and discussions from maintainers
- Primary data sources
- Reputable references with clear dates and authorship

When the query is about an API, library, framework, CLI, product, legal rule, financial fact, medical topic, current event, or anything date-sensitive, assume freshness matters and verify dates.

## Source Rules

For version-sensitive, fast-moving, legal, financial, medical, current-events, API, library, or product questions:

- Check freshness.
- Prefer primary sources.
- Compare multiple candidates when authority, date, or relevance is unclear.
- Report the actual inspected URLs.

When using search to answer technical questions, rely on primary sources such as official documentation, release notes, source repositories, issue trackers, specifications, or papers.

## Output Rules

When evidence matters, include:

- A concise answer.
- The inspected source URLs.
- Any important uncertainty, date sensitivity, or source limitation.

If the task is only URL discovery, clearly label results as candidates and do not summarize page contents unless they were inspected with Playwright.

## Fetch Pipeline

Use the local fetch pipeline when the user asks to collect, summarize, compare, or inspect several discovered URLs and static page fetching is enough for first-pass acquisition:

```bash
uv run websearch-pipeline "query" --limit 5
```

Useful variants:

```bash
uv run websearch-pipeline --url https://example.com --no-playwright
uv run websearch-pipeline "query" --interactive failed
```

Pipeline outputs:

- `results.json` contains fetch metadata, fallback reasons, and markdown excerpts.
- `pages/*.md` contains extracted markdown.
- `interactive_urls.txt` lists pages that still need manual/browser inspection.

For details, read `docs/scrapy-fetch-pipeline.md` only when changing or debugging the pipeline.

## Local Checks

Check that SearXNG is running:

```bash
curl 'http://127.0.0.1:8888/search?q=searxng%20test&format=json'
```

If SearXNG is unavailable, say so clearly. Do not silently fall back to unverified snippets as evidence.

## Optional Docker Check

If this machine hosts SearXNG with Docker and the compose project is available, check the container from its service directory:

```bash
cd services/searxng
docker compose ps
```

If that path does not exist in the current repo, skip this check.

## Cleanup when done
- Do not close the browser or the context
- Do close all pages of the context and leave only 1 page/tab behind.
