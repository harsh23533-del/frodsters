# Multi-Vertical AI Learning & Communication Platform

One backend, one database, one voice + LLM pipeline serving three verticals:

- **Kids (5-11)** — adaptive learning companion
- **Spoken English** — voice-first fluency partner
- **Interview Simulator** — interview & confidence-building coach

See `platform-implementation-roadmap.pdf` / `platform-system-architecture.pdf` for the full design.

## Status

Phase 0 (env/repo) and Phase 1 (backend foundation: models, auth, gateway) scaffolded.
Phase 2 shared-core stubs (character engine, memory service, voice pipeline) in place.
Phase 3 vertical logic (kids difficulty, english scoring, interview state machine) stubbed
with the pure functions from the roadmap — LLM wiring pending API keys.

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
