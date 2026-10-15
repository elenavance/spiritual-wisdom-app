import os

from openai import OpenAI

from readings.services.reading_prompts import (
    SYSTEM_PROMPT,
    build_reading_prompt,
)


def generate_birth_reading(profile_data, calculation_data, language="en"):
    """
    Generate a reflective reading from an existing calculated birth chart.
    Requires OPENAI_API_KEY in the environment or local .env configuration.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key or api_key == "your-api-key-here":
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. Add your API key to .env."
        )

    prompt = build_reading_prompt(
        profile_data=profile_data,
        calculation_data=calculation_data,
        language=language,
    )

    client = OpenAI(
        api_key=api_key,
        timeout=45.0,
        max_retries=1,
    )

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        instructions=SYSTEM_PROMPT,
        input=prompt,
        max_output_tokens=1800,
    )

    reading = response.output_text.strip()

    if not reading:
        raise RuntimeError("The AI provider returned an empty reading.")

    return reading
