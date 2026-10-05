from src.tools.complexity_tool import analyze_complexity
from src.tools.explanation_tool import explain_code
from src.tools.test_tool import generate_tests
from src.tools.find_bug_tool import find_bug

from src.services.cache_services import get_cached_response, save_response
import hashlib


def generate_hash(code: str, language: str) -> str:
    # Use md5 to stay consistent with the individual tool cache keys
    normalized_code = "\n".join(line.strip() for line in code.strip().splitlines())
    text = f"{language.strip()}:full_review:{normalized_code}"
    return hashlib.md5(text.encode()).hexdigest()


def full_review(code: str, language: str) -> str:

    code_hash = generate_hash(code, language)

    cached = get_cached_response(code_hash)
    if cached:
        print("⚡ Cache hit")
        return cached

    # Pass mode "2" (interview style) so the prompt key lookup in each tool works correctly
    explanation = explain_code(code, language, "2")
    complexity = analyze_complexity(code)
    tests = generate_tests(code, language, "2")
    bugs = find_bug(code, language, "2")

    report = (
        f"Full Review Report\n"
        f"{'='*60}\n\n"
        f"Explanation:\n{explanation}\n\n"
        f"{'='*60}\n\n"
        f"Complexity Analysis:\n{complexity}\n\n"
        f"{'='*60}\n\n"
        f"Test Cases:\n{tests}\n\n"
        f"{'='*60}\n\n"
        f"Potential Bugs:\n{bugs}\n"
    )

    save_response(code_hash, report)

    return report
