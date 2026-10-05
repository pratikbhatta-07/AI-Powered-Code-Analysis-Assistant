from src.services.groq_services import get_groq_client
from src.services.cache_services import get_cached_response, save_response
from src.utils.config import MODEL
import hashlib

# Lazy client — created on first use so import-time env issues are avoided
_client = None


def _get_client():
    global _client
    if _client is None:
        _client = get_groq_client()
    return _client


def generate_key(code: str, language: str, mode: str) -> str:
    normalized_code = "\n".join(line.strip() for line in code.strip().splitlines())
    text = f"{language.strip()}:{mode.strip()}:{normalized_code}"
    return hashlib.md5(text.encode()).hexdigest()


PROMPTS = {
    # Beginner-friendly bug report — plain language, gentle explanations
    "4": """
You are a patient coding mentor performing a bug review for a beginner developer.
Your task is to find issues in the given code and explain them in simple, encouraging language.

For each issue found:
1. Give it a short, friendly title.
2. Explain the problem in plain language (avoid heavy jargon).
3. Explain why it matters with a real-world analogy if possible.
4. Provide a clear, copy-pasteable fix with a short explanation.

If no obvious bugs are found, say:
"Great news! No major bugs were detected. Keep testing with edge cases to be safe."

Output Format:
Bug Review (Beginner Mode):
1. [Issue title]
   - What's the problem:
   - Why it matters:
   - How to fix it:
""",

    # Default / interview-style bug report — concise and technical
    "2": """
You are a senior software engineer performing a bug and code-risk review.
Your task is to analyze the given source code and identify:
1. Logical bugs
2. Runtime risks
3. Missing edge-case handling
4. Input validation issues
5. Unsafe assumptions
6. Performance or code-smell issues only if they can cause incorrect behavior

Important rules:
- Only report realistic issues based on the given code.
- Do NOT invent fake bugs.
- If the code looks correct, clearly state no obvious bug was found.
- Be specific and point to the relevant logic.

Output Format:
Bug Review:
1. [Issue title]
   - Problem:
   - Why it matters:
   - Suggested Fix:

If no obvious issues are found, return:
"No major logical or runtime bug was detected in the provided code, but edge-case testing is still recommended."
""",
}

_DEFAULT_PROMPT = PROMPTS["2"]


def find_bug(code: str, language: str, mode: str) -> str:

    cache_key = generate_key(code, language, mode)

    cached = get_cached_response(cache_key)
    if cached:
        print("⚡ Cache hit")
        return cached

    system_prompt = PROMPTS.get(mode, _DEFAULT_PROMPT)

    user_prompt = (
        f"Programming Language: {language}\n"
        f"Analyze the following code and find possible bugs, risks, or edge-case failures:\n"
        f"```{language}\n{code}\n```"
    )

    print("Calling Groq API")
    try:
        response = _get_client().chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=2048,
        )
        result = response.choices[0].message.content
        save_response(cache_key, result)
        return result

    except Exception as e:
        return f"Error while finding bugs: {str(e)}"
