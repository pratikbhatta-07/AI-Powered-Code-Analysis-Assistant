from src.services.groq_services import get_groq_client
from src.services.cache_services import get_cached_response, save_response
import hashlib

client = get_groq_client()

def generate_key(code: str, language: str, mode: str):
    normalized_code = code.strip()            # remove extra spaces
    normalized_code = "\n".join(line.strip() for line in normalized_code.splitlines())  # normalize lines
    
    text = f"{language.strip()}:{mode.strip()}:{normalized_code}"
    
    return hashlib.md5(text.encode()).hexdigest()


def find_bug(code : str, language : str, mode : str) -> str :

    cache_key = generate_key(code, language, mode)

    cached = get_cached_response(cache_key)

    if cached:              #checking for cached response
        print("⚡ Cache hit")
        return cached

    system_prompt = """
            You are a senior software engineer performing a bug and code-risk review.
            Your task is to analyze the given source code and identify:
                1. Possible logical bugs
                2. Runtime risks
                3. Missing edge-case handling
                4. Input validation issues
                5. Unsafe assumptions
                6. Potential performance or code-smell issues only if they can cause bugs or incorrect behavior

            Important rules:
                - Only report realistic issues based on the given code.
                - Do NOT invent fake bugs.
                - If the code looks correct, clearly say that no obvious bug was found.
                - Be specific and point to the relevant logic.
                - For each issue, explain:
                  1. The problem
                  2. Why it is risky
                  3. How to fix it

            Output format:
                Bug Review:
                1. [Issue title]
                   - Problem:
                   - Why it matters:
                   - Suggested Fix:
               2. [Issue title]
                   - Problem:
                   - Why it matters:
                   - Suggested Fix:

            If no obvious issues are found, return:
            "No major logical or runtime bug was detected in the provided code, but edge-case testing is still recommended."   
                    """
    user_prompt = f"""
            Programming Language: {language}
            Analyze the following code and find possible bugs, risks, or edge-case failures:
            ```{language}
            {code}
            """
    
    try :
        response = client.chat.completions.create( #send a prompt to an AI model and get a generated response back an return structured object
            model = "llama-3.1-8b-instant",
            messages = [
                {
                    "role" : "system",
                    "content" : system_prompt
                },
                {
                    "role" : "user",
                    "content" : user_prompt
                }
            ],
            temperature = 0.3,
            max_tokens = 2048
            )
        result = response.choices[0].message.content #extracting the actual Ai generated text 
        save_response(cache_key, result)

        return result

    except Exception as e :
        return f"Error while generating explanation: {str(e)}"