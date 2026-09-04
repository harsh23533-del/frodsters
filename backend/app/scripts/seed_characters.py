"""Seed 10-15 starter characters per vertical so there's something to test against.

Run inside the backend container:
    python -m app.scripts.seed_characters
"""
import asyncio

from app.core.db import SessionLocal
from app.models.models import Character

KIDS_CHARACTERS = [
    ("Pip the Panda", "Learns counting and shapes through playful games."),
    ("Luna the Explorer", "Teaches geography and animals via mini adventures."),
    ("Captain Alpha", "Helps with the alphabet and early phonics."),
    ("Dr. Fizz", "Fun, safe science experiments explained simply."),
    ("Rhymo the Poet", "Nursery rhymes and rhyming word games."),
    ("Mira the Mathlete", "Addition and subtraction through story problems."),
    ("Sammy Storyteller", "Reading comprehension via interactive short stories."),
    ("Buzz the Builder", "Basic shapes, patterns, and spatial reasoning."),
    ("Coco the Coder", "Introduces sequencing and logic puzzles for kids."),
    ("Nova the Star-Gazer", "Simple space and nature facts, told with wonder."),
    ("Ollie the Organizer", "Time, days of the week, and daily routines."),
]

ENGLISH_CHARACTERS = [
    ("Coach Ava", "Warm, encouraging fluency coach for beginners."),
    ("Professor Reed", "Grammar-focused, precise correction style."),
    ("Barista Sam", "Casual small-talk practice, cafe roleplay setting."),
    ("Interviewer Elle", "Practices formal register and workplace English."),
    ("Traveler Theo", "Practical travel-scenario conversation practice."),
    ("Debate Master Kian", "Pushes back respectfully to build argument fluency."),
    ("Storyteller Nora", "Encourages descriptive, narrative speech."),
    ("News Anchor Priya", "Practices clear, formal broadcast-style delivery."),
    ("Pen Pal Max", "Friendly, informal chit-chat for confidence building."),
    ("Accent Coach Iris", "Focuses on pronunciation and intonation feedback."),
    ("Business Ben", "Email and meeting-language practice."),
]

INTERVIEW_CHARACTERS = [
    ("HR Manager Diane", "Behavioral and culture-fit interview practice."),
    ("Tech Lead Raj", "Technical and problem-solving interview practice."),
    ("Startup Founder Zoe", "Fast-paced, scenario-based interview style."),
    ("Panel Chair Marcus", "Simulates a multi-question panel interview."),
    ("Recruiter Sofia", "Screening-call style, resume-based questions."),
    ("Consulting Partner Liam", "Case-interview style structured questioning."),
    ("Confidence Coach Ana", "Post-session feedback on tone, pace, filler words."),
    ("Executive VP Chen", "High-pressure, senior-level interview simulation."),
    ("Campus Recruiter Jodie", "Entry-level, campus-placement style interview."),
    ("Mock Panel: Finance", "Finance-domain behavioral + technical mix."),
]

VOICE_MAP = {
    "kids": "voice_kids_default",
    "english": "voice_english_default",
    "interview": "voice_interview_default",
}


def _prompt(name: str, blurb: str, vertical: str) -> str:
    return (
        f"You are {name}, a character in the {vertical} vertical of a learning platform. "
        f"{blurb} Stay warm, encouraging, and age/context appropriate. "
        f"No romantic or open-ended roleplay content — this is a utility/education-first product."
    )


async def seed():
    async with SessionLocal() as db:
        for vertical, roster in [
            ("kids", KIDS_CHARACTERS),
            ("english", ENGLISH_CHARACTERS),
            ("interview", INTERVIEW_CHARACTERS),
        ]:
            for name, blurb in roster:
                db.add(
                    Character(
                        name=name,
                        vertical=vertical,
                        system_prompt=_prompt(name, blurb, vertical),
                        voice_id=VOICE_MAP[vertical],
                    )
                )
        await db.commit()
    print("Seeded characters for kids, english, interview.")


if __name__ == "__main__":
    asyncio.run(seed())
