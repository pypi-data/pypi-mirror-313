from archytas.tool_utils import tool
from typing import Callable, Any, TypedDict
from typing_extensions import Annotated, NotRequired

from .utils import Logger, SimpleLogger, get_code, set_openai_api_key, set_gemini_api_key
from .uaii import GeminiModel, OpenAIModel, OpenAIAgent, GeminiAgent


import pdb


# configuration for agents that the user passes in
class DrafterConfig(TypedDict):
    api_key: NotRequired[Annotated[str, 'The API key for the Gemini API']]
    model: Annotated[GeminiModel, 'The model to use for the Gemini API']
    ttl_seconds: NotRequired[Annotated[int, "The time-to-live in seconds for the Gemini API cache"]]

# drafter_config_defaults = {
#     'ttl_seconds': 1800
# }

class FinalizerConfig(TypedDict):
    api_key: NotRequired[Annotated[str, 'The API key for the OpenAI API']]
    model: Annotated[OpenAIModel, 'The model to use for the OpenAI API']

class APISpec(TypedDict):
    name: Annotated[str, 'The name of the API']
    cache_key: NotRequired[Annotated[str, 'The key used to retrieve the cached API chat. If not provided, caching will be disabled.']]
    description: Annotated[str, 'A description of the API']
    documentation: Annotated[str, "The raw extracted text of the API's documentation"]
    proofread_instructions: NotRequired[Annotated[str, 'Additional information related to writing request code for the API. e.g. lists of valid values to use for certain fields, etc.']]



# newer prompt to try
# 'You are a python programmer writing code to perform API requests. You will be provided with the raw API documentation, and your job is to draft a python script that will perform the user-specified task.',
DRAFTER_SYSTEM_PROMPT = '''\
You are an assistant who will help me query the {name} API. 
You should write clean python code to solve specific queries I pose. 
You should write it as though it will be executed directly as a python script.
Do not include backticks ``` or the word "python" at the top of the code block.
Do not provide any other explanation. Your only output should be the raw code, ready to be run. 
Assume pandas is installed and is imported with `import pandas as pd`. 
Also assume `requests`, `json`, and `os` are imported properly.
'''
DRAFTER_ASK_ABOUT_API_PROMPT = '''\
You are an assistant who is helping users to write code to interact with the {name} API.
You will be provided with the raw API documentation, and your job is to answer questions about the API.
You should not write any large blocks of code, but rather provide in words comprehensive and concise answers to the questions posed.
Any necessary code examples you want to provide should be short and inline with the text of your response.
'''

# DRAFTER_PRELUDE_CODE = '''\
# import pandas as pd
# import os
# import json
# import requests
# '''

class Drafter:
    def __init__(self, model:GeminiModel, cache_key:str|None, system_prompt:str, api_docs:str, ttl_seconds:int, logger: Logger=SimpleLogger()):
        self.agent = GeminiAgent(model, cache_key, system_prompt, api_docs, ttl_seconds, logger)
    
    def draft_request(self, query: str) -> str:
        """
        Have gemini produce a draft of code to perform a request to the API
        Returns a string containing the draft code. Strips out instances of markdown syntax wrapping the code (i.e. ```python  ```)
        If multiple markdown code blocks are present, they will be combined into a single source code output.

        Args:
            query (str): The description of what the request should do in plain English

        Returns:
            str: The draft code produced by the agent
        """
        # generate draft
        draft = self.agent.query_sync(query)

        # remove any markdown syntax
        code = get_code(draft)

        return code



FINALIZER_SYSTEM_PROMPT = '''\
You are a python code proofreader. Your job is to look at the following code and make sure it doesn't have any errors, such as
- syntax errors
- logical errors
- missing imports
- missing function definitions
- uncommented commentary
- erroneously included markdown block syntax (e.g. ```python  ```)
- etc.
The code should be ready to run directly as a python script.
Do not include markdown block syntax (e.g. ```python  ```) or the word "python" at the top of the code block.
Please output the corrected code without any other explanation or commentary.
'''
FINALIZER_EXTRA_PROMPT = '''\
Additionally, for this specific code, the following notes are provided:
{notes}
'''


class Finalizer:
    def __init__(self, model:OpenAIModel, logger:Logger=SimpleLogger()):
        self.logger = logger
        self.agent = OpenAIAgent(model=model)
    
    def proofread_code(self, code: str, extra_instructions:str|None=None) -> str:
        """
        Apply fixes to draft code so that it is ready to run as a python script.
        Uses a set of default fixes, and may include additional instructions specific to the current code.

        Args:
            code (str): The code to proofread
            extra_instructions (str, optional): Additional notes to provide to the proofreader, relevant to the current code. Defaults to None.
        """
        prompt = FINALIZER_SYSTEM_PROMPT
        if extra_instructions is not None:
            prompt += FINALIZER_EXTRA_PROMPT.format(notes=extra_instructions)

        # have agent revise the code
        fixed_code = self.agent.oneshot_sync(prompt, code)

        # strip off any markdown syntax
        final_code = get_code(fixed_code)

        return final_code


class AdhocApi:
    """
    Toolset for interacting with external APIs in an flexible manner. 
    These tools can be used to draft code to perform requests to APIs given some goal in plain English.
    Common usage is to first list APIs to determine which to use, then draft code to perform a specific task.
    If proofread instructions are present for a given API, ensure that you are consistent with them if you modify the code yourself.
    """
    def __init__(self, *,
        apis: list[APISpec],
        drafter_config: DrafterConfig,
        finalizer_config: FinalizerConfig,
        run_code: Callable[[str], Any]|None=None,
        logger: Logger=SimpleLogger()
    ):
        """
        Create a new AdhocApi instance.

        Args:
            apis (list[APISpec]): A list of APIs available to the tool
            drafter_config_base (DrafterConfigBase): The base configuration for the drafter agent
            finalizer_config_base (FinalizerConfigBase): The base configuration for the finalizer agent
            run_code (Callable[[str], Any], optional): An optional function that runs the code generated by the finalizer. 
                If None, the tool will return generated code as a string, otherwise it will attempt to call
                `result = run_code(generated_code)` and return the result or an error. Defaults to None.
        """
        self.logger = logger
        self.apis = {api['name']: api for api in apis}
        self.drafter_config = drafter_config
        self.finalizer_config = finalizer_config
        # lambda is necessary here because if run_code is an @tool, it would
        # pollute the prompt description of this class's @tool method
        self.run_code = (lambda: run_code) if run_code is not None else None

        # ensure api keys are set
        set_gemini_api_key(drafter_config.get('api_key', None))
        set_openai_api_key(finalizer_config.get('api_key', None))

    
    @tool
    def list_apis(self) -> dict:
        """
        This tool lists all the APIs available to you.

        Returns:
            dict: A dict mapping from API names to their descriptions
        """
        # make a new dict that is name: {description, proofread_instructions}
        subset_keys = ['description']#, 'proofread_instructions'] #TODO: proofread instructions can be too long to include, and pollute the context...
        return {
            name: {
                key: api[key] for key in subset_keys if key in api
            }
            for name, api in self.apis.items()
        }
    
    @tool
    def ask_api(self, api: str, query: str) -> str:
        """
        Ask a question about the API to get more information.

        Args:
            api (str): The name of the API to ask about
            query (str): The question to ask

        Returns:
            str: The response to the query
        """
        api_spec = self.apis.get(api)
        if api_spec is None:
            return f"API {api} not found. Please consult the list of available APIs: {[*self.apis.keys()]}"

        agent = GeminiAgent(
            model=self.drafter_config['model'],
            cache_key=api_spec.get('cache_key', None),
            system_prompt=DRAFTER_ASK_ABOUT_API_PROMPT.format(name=api),
            cache_content=api_spec['documentation'],
            ttl_seconds=self.drafter_config.get('ttl_seconds', None),
            logger=self.logger
        )

        return agent.query_sync(query)


    @tool
    def use_api(self, api: str, goal: str) -> str:
        """
        Draft python code for an API request given some goal in plain English.

        Args:
            api (str): The name of the API to use
            goal (str): The task to be performed by the API request (in plain English)

        Returns:
            str: Depending on the user defined configuration will do one of two things.
                 Either A) return the raw generated code. Or B) Will attempt to run the code and return the result or
                 any errors that occurred (along with the original code). if an error is returned, you may consider
                 trying to fix the code yourself rather than reusing the tool.
        """
        api_spec = self.apis.get(api)
        if api_spec is None:
            return f"API {api} not found. Please consult the list of available APIs."
        
        # Collect the API documentation and any additional proofread instructions
        api_docs = api_spec["documentation"]
        proofread_instructions = api_spec.get('proofread_instructions', None)
        if proofread_instructions is not None:
            api_docs += f'\n\n# Additional instructions:\n{proofread_instructions}'

        drafter = Drafter(
            model=self.drafter_config['model'],
            cache_key=api_spec.get('cache_key', None),
            system_prompt=DRAFTER_SYSTEM_PROMPT.format(name=api),
            api_docs=api_docs,
            ttl_seconds=self.drafter_config.get('ttl_seconds', None),
            logger=self.logger
        )
        finalizer = Finalizer(self.finalizer_config['model'], logger=self.logger)

        self.logger.info({'api': api, 'goal': goal})
        draft_code = drafter.draft_request(goal)
        self.logger.info({'draft_code': draft_code})
        fixed_code = finalizer.proofread_code(draft_code, proofread_instructions)
        self.logger.info({'fixed_code': fixed_code})

        # return code directly if no run_code function is provided
        if self.run_code is None:
            self.logger.info({'info': 'directly returning code'})
            return fixed_code

        # attempt to run the code
        try:
            self.logger.info({'info': 'running code'})
            # TODO: this doesn't necessarily return str. perhaps adjust the function signature
            result = self.run_code()(fixed_code)
            return result
        except Exception as e:
            import traceback
            traceback_str = traceback.format_exc()
            self.logger.error({'error': str(e), 'traceback': traceback_str})
            return f'Encountered an error while running the code "{e}". The original code is provided below:\n\n{fixed_code}\n'


import subprocess
import tempfile
import os

class PythonTool:
    """Tool for running python code. If the user asks you to write code, you can run it here."""
    def __init__(self, sideeffect:Callable[[str, str, str, int], Any]=lambda x: None):
        """
        Set up a PythonTool instance.

        Args:
            sideeffect (Callable[[str], Any], optional): A side effect function to run when the tool is used. Defaults to do nothing.
        """
        self.sideeffect = sideeffect

    @tool
    def run(self, code: str) -> tuple[str, str, int]:
        """
        Runs python code in a python subprocess.

        The environment is not persistent between runs, so any variables created will not be available in subsequent runs.
        The only visible effects of this tool are from output to stdout/stderr. If you want to view a result, you MUST print it.

        Args:
            code (str): The code to run

        Returns:
            tuple: The stdout, stderr, and returncode from executing the code
        """

        # make a temporary file to run the code
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w+') as f:
            f.write(code)
            f.flush()
            f.seek(0)

            # run the file in a separate Python process and capture the output
            try:
                result = subprocess.run(['python', f.name], capture_output=True, text=True, cwd=os.getcwd())
                stdout = result.stdout
                stderr = result.stderr or (f'No error output available. Process returned non-zero error code {result.returncode}' if result.returncode != 0 else '')
                returncode = result.returncode
            except Exception as e:
                stdout, stderr, returncode = "", str(e), 1
        
        # perform side effect
        self.sideeffect(code, stdout, stderr, returncode)


        return stdout, stderr, returncode


from .files import tree
from pathlib import Path

@tool
def view_filesystem(max_depth:int=-1, max_similar: int=25, ignore: list[str] = []) -> str:
    """
    View files and directories in the current working directory, displayed in a tree structure.

    Args:
        max_depth (int, optional): The maximum depth to traverse. Set to negative for infinite depth.
        max_similar (int, optional): The maximum number of similar files to display. When too many similar files are found, further matches will be elided. Defaults to 25.
        ignore (list, optional): List of unix filename pattern strings (e.g. '*.py', 'file?.txt', 'file[!a-c]*.txt', etc.) to skip including in output. Defaults to [].

    Returns:
        str: A string representation of the tree structure of the current working directory.
    """
    return tree(Path('.'), ignore=ignore, max_depth=max_depth, max_similar=max_similar)