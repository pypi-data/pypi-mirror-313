import ell
import anthropic
from .examples import simple_example,sqlite_example


client = anthropic.Anthropic()

def antrophic_generate_test_code(lua_code: str,existing_tests: str,sqlite: bool = False) -> str:
    client = anthropic.Anthropic()
    example_text = sqlite_example if sqlite else simple_example
    message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": example_text,
                },
                {
                    "type": "text",
                    "text": f"You are an expert test generator specializing in analyzing Lua code and generating corresponding TypeScript tests. Your task is to create new, comprehensive tests for handlers in the provided Lua code without duplicating existing tests.\n\nFirst, examine the following Lua code:\n\n<lua_code>\n{lua_code}\n</lua_code>\n\nNow, review the existing TypeScript tests:\n\n<existing_tests>\n{existing_tests}\n</existing_tests>\n\nYour goal is to generate new TypeScript tests for the Lua code provided. Follow these guidelines:\n\n1. Focus on testing handlers in the Lua code.\n2. Ensure tests are comprehensive but do not duplicate existing tests.\n3. Follow TypeScript and existing test patterns.\n4. Be idempotent - only add new tests for new Lua code, not for code that already has tests.\n5. Maintain the existing test file structure.\n\nGenerate only the new test code in TypeScript format. Do not include any explanations, comments, or anything other than the TypeScript test code itself. If the already provided test's are fulfilling output None.\n\nProvide your output in the following format:\n\n<new_tests>\n[Insert only the new TypeScript test code here]\n</new_tests>\n\nRemember to analyze the existing tests carefully to avoid duplication and ensure you're only adding tests for new handlers "
                }
            ]
        }
    ]
    )
    
    return message.content[0].text





@ell.simple(model='gpt-4',max_tokens=1000,temperature=0,client=client)
def openai_generate_test_code(lua_code: str,existing_tests: str,sqlite: bool = False) -> str:
    example_text = sqlite_example if sqlite else simple_example
    return [
        ell.user(example_text),
        ell.user(f"You are an expert test generator specializing in analyzing Lua code and generating corresponding TypeScript tests. Your task is to create new, comprehensive tests for handlers in the provided Lua code without duplicating existing tests.\n\nFirst, examine the following Lua code:\n\n<lua_code>\n{lua_code}\n</lua_code>\n\nNow, review the existing TypeScript tests:\n\n<existing_tests>\n{existing_tests}\n</existing_tests>\n\nYour goal is to generate new TypeScript tests for the Lua code provided. Follow these guidelines:\n\n1. Focus on testing handlers in the Lua code.\n2. Ensure tests are comprehensive but do not duplicate existing tests.\n3. Follow TypeScript and existing test patterns.\n4. Be idempotent - only add new tests for new Lua code, not for code that already has tests.\n5. Maintain the existing test file structure.\n\nGenerate only the new test code in TypeScript format. Do not include any explanations, comments, or anything other than the TypeScript test code itself. If the already provided test's are fulfilling output None.\n\nProvide your output in the following format:\n\n<new_tests>\n[Insert only the new TypeScript test code here]\n</new_tests>\n\nRemember to analyze the existing tests carefully to avoid duplication and ensure you're only adding tests for new handlers ")
    ]


# @ell.simple(model='claude-3-5-sonnet-20241022', client=client,max_tokens=2000)
# def generate_test_code(lua_code: str, existing_tests: str) -> str:
#     prompt = f"""
# Your task is to create new, comprehensive tests for handlers in the provided Lua code without duplicating existing tests. 
# You are an expert test generator specializing in analyzing Lua code and generating corresponding TypeScript tests. 
# First, examine the following Lua code:

# <lua_code>
# {lua_code}
# </lua_code>

# Now, review the existing TypeScript tests:

# <existing_tests>
# {existing_tests}
# </existing_tests>

# Your goal is to generate new TypeScript tests only for new handlers in the Lua code provided. Follow these guidelines:

# 1. Focus exclusively on testing new handlers in the Lua code that don't have corresponding tests.
# 2. Ensure new tests are comprehensive and follow TypeScript and existing test patterns.
# 3. Maintain the existing test file structure.
# 4. Do not generate any tests for handlers that already have tests.

# Before generating new tests, carefully analyze the Lua code and existing tests. Wrap your analysis in <code_analysis> tags:

# 1. List all handlers in the Lua code, numbering them.
# 2. List all handlers in the existing tests, numbering them.
# 3. Compare the two lists and identify new handlers that need testing.
# 4. For each new handler, outline its functionality and potential test cases.

# After your analysis, generate only the new test code in TypeScript format. Do not include any explanations, comments, or anything other than the TypeScript test code itself. If no new tests are needed, output "None".

# Provide your output in the following format:

# <new_tests>
# [Insert only the new TypeScript test code here, or "None" if no new tests are needed]
# </new_tests>

# Remember to analyze the existing tests carefully to avoid duplication and ensure you're only adding tests for new handlers."""

#     return prompt


