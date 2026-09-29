from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "beginner"
) -> str:

    prompt = f"""
You are EduGenie.

Create a personalized learning path.

Topic:
{topic}

Learner Level:
{level}

Use this structure:

1. Learning Goal

2. Prerequisites

3. Beginner Level

4. Intermediate Level

5. Advanced Level

6. Weekly Timeline

7. Practice Projects

8. Revision Strategy

9. Recommended Resource Types

Make the learning path practical,
progressive and easy to follow.

Do not invent specific URLs.
"""

    return generate_text(
        prompt,
        temperature=0.35
    )