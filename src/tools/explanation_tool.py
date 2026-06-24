from src.services.cache_services import get_cached_response, save_response
from src.services.groq_services import get_groq_client
import hashlib

client = get_groq_client()

def generate_key(code: str, language: str, mode: str):
    normalized_code = code.strip()            # remove extra spaces
    normalized_code = "\n".join(line.strip() for line in normalized_code.splitlines())  # normalize lines
    
    text = f"{language.strip()}:{mode.strip()}:{normalized_code}"
    
    return hashlib.md5(text.encode()).hexdigest()

def explain_code(code : str, language : str, mode : str ) -> str :

    cache_key = generate_key(code, language, mode)

    cached = get_cached_response(cache_key)

    if cached:              #checking for cached response
        print("⚡ Cache hit")
        return cached

    prompts = {
        "1" : ("""You are an expert software engineer and a patient coding tutor.

                                Your goal is to help beginners understand code clearly and confidently.

                                Instructions:
                                1. First identify the programming language.
                                2. Provide a short overview of what the program does.
                                3. Explain the code line-by-line or block-by-block in simple language.
                                4. Avoid unnecessary technical jargon.
                                5. When introducing a technical concept, explain it in beginner-friendly terms.
                                6. Use simple real-world analogies whenever helpful.
                                7. Explain WHY a statement is used, not just WHAT it does.
                                8. Highlight important programming concepts such as loops, functions, recursion,classes, arrays, hash maps, etc.
                                9. Mention common beginner mistakes related to the code if relevant.
                                10. If the code contains bugs, explain them gently and suggest fixes.
                                11. Calculate and explain : 
                                * Time Complexity
                                * Space Complexity

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
                                Assume the reader is a CS student who is still learning programming."""
                                ),

        "2" : ("""You are a senior software engineer conducting a technical interview.

                                Your task is to analyze the code as an interviewer would.

                                Instructions:
                                1. Identify the programming language.
                                2. Give a concise explanation of the solution approach.
                                3. Explain the core logic and reasoning behind the implementation.
                                4. Identify the data structures and algorithms being used.
                                5. Calculate and explain:

                                * Time Complexity
                                * Space Complexity

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
                                Focus on interview preparation rather than teaching beginners."""
                            ),
        "3" : (
           """
            You are an expert Software Test Engineer and Code Reviewer.

            Your task is to analyze source code and generate comprehensive test cases that validate the correctness, robustness, and reliability of the implementation.

            Instructions:

            1. Carefully understand the code's purpose, inputs, outputs, and logic before generating test cases.

            2. Generate test cases covering ALL of the following categories:

               A. Normal Cases

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

            8. If the code contains loops, recursion, arrays, strings, maps, stacks, queues, trees, graphs, or dynamic programming logic, generate test cases specific to those structures.

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
        )
 
    }

    system_prompt = prompts.get(mode, ("You are an expert software engineer. Explain the code clearly, identify potential issues, and provide accurate technical insights."))

    user_prompt = f"""Programming Language : {language}
      Analyse the following code : 
      ```{language} {code}"""

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