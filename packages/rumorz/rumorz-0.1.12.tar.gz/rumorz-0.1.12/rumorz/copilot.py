import importlib.util
import json
import subprocess
import traceback
from textwrap import dedent

from litellm import completion
from pydantic import BaseModel, Field
from smartpy.utility import os_util


class RumorzCopilot:

    def __init__(self,
                 model):
        self.model = model

    def load_sdk_source_code(self, include_client=True, include_enums=True, include_tests=True):
        package_name = "rumorz"
        spec = importlib.util.find_spec(package_name)
        if spec and spec.origin:
            sdk_path = spec.origin.replace('__init__.py', '')
        else:
            raise Exception(f"Package {package_name} not found")

        client_content = enums_content = test_content = ""

        if include_client:
            client_path = sdk_path + 'client.py'
            with open(client_path, 'r') as file:
                client_content = f"<RUMORZ SDK SOURCE CODE>\nfile_path: {client_path}\n{file.read()}\n"

        if include_enums:
            enums_path = sdk_path + 'enums.py'
            with open(enums_path, 'r') as file:
                enums_content = f"<ENUMS>\nfile_path: {enums_path}\n{file.read()}\n"

        if include_tests:
            test_path = sdk_path + 'tests/test_sdk.py'
            with open(test_path, 'r') as file:
                test_content = f"<TESTS>\nfile_path: {test_path}\n{file.read()}\n"

        docs = dedent(f"{client_content}{enums_content}{test_content}")
        return docs


    def run_script(self, script_path):
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        return result

    def create_file(self,
                    file_description,
                    output_path,
                    include_client=True,
                    include_enums=True,
                    include_tests=True):

        source_code = self.load_sdk_source_code(include_client, include_enums, include_tests)

        class SDKCopilotResponse(BaseModel):
            reasoning: str = Field(...,
                                   description="Write a complete reasoning and planning on requirements and steps to write the script based on the documentation and the provided script description")
            file_content: str = Field(..., description="The content of the file to create")


        response = completion(
            model=self.model,
            response_format=SDKCopilotResponse,
            messages=[
                {"role": "system", "content": f"""
ROLE:
You are an expert in Programming and the Rumorz Python SDK. Rumorz provides Financial markets AI intelligence through
the Graph and an Agent. The Graph gives access to entities (tokens, people, companies, etc.) and their posts, sentiment
etc. The Agent provides summaries and insights on entities. 

TASK
You are tasked to create a fully working Python script based on user input. The script must use the Rumorz Python SDK. 
Your output will be in json

GUIDELINES
- Minimize the number of API queries.
- If you hesitate, tell the user to ask again with specific improvements to make in his query
- Your script should always print a success message with details at the end of the execution

DOCUMENTATION
Use the following documentation and Enums to build working queries:
<SOURCE CODE>
{source_code}
<SOURCE CODE>
"""},
                {"role": "user",
                 "content": f"""The user message to describe the script required:
Description:\n{file_description}
"""
                 }
            ],

        )
        class RumorzCopilotException(Exception):
            pass

        try:
            script_code = json.loads(response.choices[0].message.content)['file_content']
            script_code = script_code.replace('```yaml', '').replace('```', '')
            with open(output_path, 'w') as f:
                f.write(script_code)
        except Exception as e:
            raise RumorzCopilotException("Error while parsing LLM response ", traceback.format_exc())
