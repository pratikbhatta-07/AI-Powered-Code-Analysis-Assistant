from src.services.groq_services import get_groq_client
from src.services.cache_services import get_cached_response, save_response
import hashlib

client = get_groq_client()

def generate_key(code: str, language: str, mode: str):
    normalized_code = code.strip()            # remove extra spaces
    normalized_code = "\n".join(line.strip() for line in normalized_code.splitlines())  # normalize lines
    
    text = f"{language.strip()}:{mode.strip()}:{normalized_code}"
    
    return hashlib.md5(text.encode()).hexdigest()

def generate_tests(code: str, language: str, mode : str) -> str:

    cache_key = generate_key(code, language, mode)

    cached = get_cached_response(cache_key)

    if cached:              #checking for cached response
        print("⚡ Cache hit")
        return cached

    system_prompt = """
                        You are an expert Software Test Engineer and Code Reviewer.
                        Your task is to analyze source code and generate comprehensive test cases that validate the correctness, robustness, and reliability of the implementation.

                        Instructions:

                            1. Carefully understand the code's purpose, inputs, outputs, and logic before generating test cases.
                            2. Generate test cases covering ALL of the following categories:                                   A. Normal Cases
                               * Typical valid inputs.
                               * Common real-world usage scenarios.
               
                               B. Edge Cases
                               * Unusual but valid inputs.
                               * Extreme values.
                               * Minimum and maximum valid inputs.

                               C. Boundary Cases
                               * Values at the limits of allowed ranges.
                               * Empty collections.
                               * Single-element collections.
                               * Near-boundary transitions.

                               D. Invalid Inputs
                               * Null values.
                               * Incorrect data types.
                               * Malformed inputs.
                               * Out-of-range values.
                               * Inputs that should trigger errors or exceptions.
                            3. For every generated test case provide:
                               * Test Case ID
                               * Category (Normal / Edge / Boundary / Invalid)
                               * Input
                               * Expected Output
                               * Reasoning
                            4. Do NOT generate JUnit, PyTest, Jest, or any testing framework code.
                            5. Focus on logical test scenarios only.
                            6. Infer expected outputs from the code behavior.
                            7. If the code can throw exceptions, include test cases for those exceptions.
                            8. If the code contains loops, recursion, arrays, strings, maps, stacks, queues, trees, graphs, or dynamic                  programming logic, generate test cases specific to those structures.
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
                            Category:
                            Input:
                            Expected Output:
                            Reasoning:

                            ...
                            ## Coverage Summary
                            Normal Cases:
                            * ...

                            Edge Cases:
                            * ...
                            Boundary Cases:
                            * ...

                            Invalid Inputs:
                            * ...
                            The output must be structured, concise, and easy for developers to use during testing and interview preparation.
            """

    user_prompt = f"""
                        Programming Language: {language}
                        Generate unit tests for the following code:
                        ```{language}
                        {code}"""
    
    print("Calling GROQ api")
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