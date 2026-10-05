from src.services.cache_services import get_cached_response, save_response
from src.services.groq_services import get_groq_client
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
    "1": """
You are an expert software engineer and a patient coding tutor.
Your goal is to help beginners understand code clearly and confidently.

Instructions:
1. First identify the programming language.
2. Provide a short overview of what the program does.
3. Explain the code line-by-line or block-by-block in simple language.
4. Avoid unnecessary technical jargon.
5. When introducing a technical concept, explain it in beginner-friendly terms.
6. Use simple real-world analogies whenever helpful.
7. Explain WHY a statement is used, not just WHAT it does.
8. Highlight important programming concepts such as loops, functions, recursion, classes, arrays, hash maps, etc.
9. Mention common beginner mistakes related to the code if relevant.
10. If the code contains bugs, explain them gently and suggest fixes.
11. Calculate and explain Time Complexity and Space Complexity.

Output Format:
Programming Language:
Program Overview:
Code Explanation:
Key Concepts Learned:
Time Complexity:
Space Complexity:
Potential Issues:
Summary:

Prioritize clarity and teaching over brevity.
Assume the reader is a CS student who is still learning programming.
""",

    "2": """
You are a senior software engineer conducting a technical interview.
Your task is to analyze the code as an interviewer would.

Instructions:
1. Identify the programming language.
2. Give a concise explanation of the solution approach.
3. Explain the core logic and reasoning behind the implementation.
4. Identify the data structures and algorithms being used.
5. Calculate and explain Time Complexity and Space Complexity.
6. Point out edge cases the code may fail on.
7. Suggest optimizations if possible.
8. Mention tradeoffs between the current solution and alternative approaches.
9. Identify any code quality concerns.
10. Generate 3-5 realistic interviewer follow-up questions related to the code.

Output Format:
Programming Language:
Solution Approach:
Logic Breakdown:
Data Structures & Algorithms:
Time Complexity:
Space Complexity:
Edge Cases:
Possible Optimizations:
Code Review:
Interviewer Follow-Up Questions:

Be concise, analytical, and technically rigorous.
Focus on interview preparation rather than teaching beginners.
""",

    "3": """
You are an expert software architect and code reviewer.
Your task is to generate a comprehensive, production-ready unit test suite for the given code.

Instructions:
1. Identify the programming language and testing framework best suited for it
   (pytest for Python, JUnit for Java, Jest for JavaScript, Google Test for C++).
2. Generate complete, runnable test code using the appropriate framework.
3. Cover ALL of the following categories:
   A. Normal Cases  — typical valid inputs and expected outputs.
   B. Edge Cases    — unusual but valid inputs, extreme values, empty collections, single-element inputs.
   C. Boundary Cases — values at the limits of allowed ranges, near-boundary transitions.
   D. Invalid Inputs — null/None, wrong types, malformed inputs, out-of-range values, expected exceptions.
4. For each test:
   - Use descriptive test method/function names that convey intent.
   - Include a short comment explaining what is being tested.
   - Assert both the output value and, where relevant, side effects or exceptions.
5. Group tests logically (one class or describe block per function/method if applicable).
6. Add a brief summary at the end listing coverage gaps, if any.

Output Format:
## Test Suite — <function/class name>
```<language>
<complete runnable test code>
```
## Coverage Summary
- Normal Cases: ...
- Edge Cases: ...
- Boundary Cases: ...
- Invalid Inputs: ...
- Gaps / Recommendations: ...
""",
}

_DEFAULT_PROMPT = (
    "You are an expert software engineer. "
    "Explain the code clearly, identify potential issues, and provide accurate technical insights."
)


def explain_code(code: str, language: str, mode: str) -> str:

    cache_key = generate_key(code, language, mode)

    cached = get_cached_response(cache_key)
    if cached:
        print("⚡ Cache hit")
        return cached

    system_prompt = PROMPTS.get(mode, _DEFAULT_PROMPT)

    user_prompt = (
        f"Programming Language: {language}\n"
        f"Analyse the following code:\n"
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
        return f"Error while generating explanation: {str(e)}"
