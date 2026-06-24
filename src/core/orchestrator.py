from src.tools.complexity_tool import analyze_complexity
from src.tools.explanation_tool import explain_code
from src.tools.test_tool import generate_tests
from src.services.cache_services import get_cached_response, save_response
import hashlib

def generate_hash(code, language) :
    return hashlib.sha256((code + language).encode()).hexdigest()



def full_review(code : str, language : str) -> str :
    
    code_hash = generate_hash(code, language)

    cached = get_cached_response(code_hash)
    if cached :
        print("cached hit")
        return cached



    explanation = explain_code(code, language, "interview")
    complexity = analyze_complexity(code)
    tests = generate_tests(code, language)
    report = f""" 
            Full Review Report : {explanation}
            Complexity Analysis : {complexity}
            Test Cases : {tests}
            """
    save_response(code_hash, report)
    
    return report