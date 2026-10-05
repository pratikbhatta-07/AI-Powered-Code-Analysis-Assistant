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


def generate_tests(code: str, language: str, mode: str) -> str:

    cache_key = generate_key(code, language, mode)

    cached = get_cached_response(cache_key)
    if cached:
        print("⚡ Cache hit")
        return cached

    system_prompt = """
You are an expert Software Test Engineer and Code Reviewer.
Your task is to analyze source code and generate comprehensive test cases that validate
the correctness, robustness, and reliability of the implementation.

Instructions:
1. Carefully understand the code's purpose, inputs, outputs, and logic before generating test cases.
2. Generate test cases covering ALL of the following categories:
   A. Normal Cases    — typical valid inputs, common real-world usage scenarios.
   B. Edge Cases      — unusual but valid inputs, extreme values, min/max valid inputs.
   C. Boundary Cases  — values at the limits of allowed ranges, empty collections,
                        single-element collections, near-boundary transitions.
   D. Invalid Inputs  — null values, incorrect data types, malformed inputs,
                        out-of-range values, inputs that should trigger errors or exceptions.
3. For every generated test case provide:
   - Test Case ID
   - Category (Normal / Edge / Boundary / Invalid)
   - Input
   - Expected Output
   - Reasoning
4. Do NOT generate JUnit, PyTest, Jest, or any testing framework code.
5. Focus on logical test scenarios only.
6. Infer expected outputs from the code behavior.
7. If the code can throw exceptions, include test cases for those exceptions.
8. If the code contains loops, recursion, arrays, strings, maps, stacks, queues, trees, graphs,
   or dynamic programming logic, generate test cases specific to those structures.
9. Prioritize correctness over quantity. Generate only meaningful test cases.

Output Format:
## Function Summary
<Brief description of what the code does>

## Test Cases
### TC-001
Category:
Input:
Expected Output:
Reasoning:

### TC-002
...

## Coverage Summary
Normal Cases:   ...
Edge Cases:     ...
Boundary Cases: ...
Invalid Inputs: ...
"""

    user_prompt = (
        f"Programming Language: {language}\n"
        f"Generate unit tests for the following code:\n"
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
        return f"Error while generating tests: {str(e)}"
