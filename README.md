# Multi-Vertical AI Learning & Communication Platform

One backend, one database, one voice + LLM pipeline serving three verticals:

- **Kids (5-11)** — adaptive learning companion
- **Spoken English** — voice-first fluency partner
- **Interview Simulator** — interview & confidence-building coach

See `platform-implementation-roadmap.pdf` / `platform-system-architecture.pdf` for the full design.

## Status

- **Phase 0 (Setup)** — done: docker-compose, requirements.txt, .env.example
- **Phase 1 (Backend foundation)** — done: all 6 models, Alembic initial migration, JWT auth, API gateway wiring
- **Phase 2 (Shared core)** — done: character engine, pgvector memory service, OpenRouter LLM client, Whisper/ElevenLabs voice pipeline, Redis rate limiter
- **Phase 3 (Verticals)** — done: sessions/messages/progress endpoints for all 3 verticals, each wired to its own post-message hook (kids difficulty, english scoring, interview state machine), plus a 30+ character seed script
- **Phase 4 (Frontend)** — scaffolded: Next.js web (vertical picker → character list → chat → progress) and Expo mobile (hold-to-talk voice screen). Not yet run/tested — `npm install` has not been executed in this environment.
- **Phase 5 (Ship)** — not done: nothing has been deployed; no hosting account is connected here

### What has NOT been verified
Nothing in this repo has run against a real Postgres/Redis instance or real API keys — only Python import/syntax checks were run. Before relying on it:
1. `docker compose up`, then `alembic upgrade head` inside the backend container
2. `python -m app.scripts.seed_characters` to populate characters
3. Fill real `OPENROUTER_API_KEY` / `ELEVENLABS_API_KEY` in `.env` and smoke-test signup → session → message → voice round-trip
4. `npm install` in both `frontend-web` and `frontend-mobile` and run them against the live backend

## Local dev

```bash
cp .env.example .env   # fill in DB_PASSWORD, JWT_SECRET, OPENROUTER_API_KEY, ELEVENLABS_API_KEY
docker compose up
```

Then, inside the backend container:

```bash
alembic init migrations
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

## Structure

```
backend/
  app/
    main.py            # FastAPI app + router wiring (API gateway)
    core/               # config, db session, character engine, memory service, rate limit
    models/             # SQLAlchemy models (users, characters, sessions, messages, memory_facts, progress)
    routers/             # auth, voice (whisper/elevenlabs)
    verticals/
      kids/              # adaptive difficulty engine
      english/           # correction & scoring
      interview/          # state machine
frontend-web/           # Next.js (Phase 4)
frontend-mobile/        # Expo React Native (Phase 4)
```

## Next steps

1. Add Alembic migration setup + seed script for 10-15 characters per vertical (Step 6).
2. Wire `core/memory.py` and `routers/voice.py` to real OpenAI/ElevenLabs keys and test round-trip.
3. Build `sessions`/`messages` endpoints (referenced in the API reference doc, not yet implemented here).
4. Scaffold `frontend-web` (Next.js) and `frontend-mobile` (Expo) — Phase 4.

<!-- deploy retry -->
