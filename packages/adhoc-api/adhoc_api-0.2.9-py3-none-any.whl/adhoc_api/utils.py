from typing import Protocol, Any, Generator
import os
from google import generativeai as genai
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager


class Logger(Protocol):
    def info(self, message: Any) -> None: ...
    def error(self, message: Any) -> None: ...

class SimpleLogger:
    def info(self, message: Any) -> None:
        print('INFO', message)
    def error(self, message: Any) -> None:
        print('ERROR', message)


def extract_code_blocks(text: str) -> list[str]:
    """
    Extracts code blocks from a string of text
    Code blocks will be a between a pair of triple backticks ``` with optional language specifier after the first set
    """
    blocks = []
    in_block = False
    block = []
    for line in text.split('\n'):
        if line.startswith('```'):
            if in_block:
                blocks.append('\n'.join(block))
                block = []
            in_block = not in_block
        elif in_block:
            block.append(line)
    return blocks


def get_code(text: str, allow_multiple:bool=True) -> str:
    """
    Extracts raw code from any markdown code blocks in the text if present
    If multiple code blocks are present, they will be combined into a single source code output.
    If no code blocks are present, the original text will be returned as is.

    Args:
        text (str): The text to extract code from
        allow_multiple (bool): If False, will raise an error if multiple code blocks are found. Default is True.

    Returns:
        str: The extracted code as a string
    """
    code_blocks = extract_code_blocks(text)
    if len(code_blocks) == 0:
        return text
    if len(code_blocks) == 1:
        return code_blocks[0]
    if not allow_multiple:
        raise ValueError(f'Multiple code blocks found in text, but expected only one. Raw text:\n{text}')
    return '\n\n'.join(code_blocks)



def set_openai_api_key(api_key:str|None=None):
    """
    Set the OpenAI API key for the OpenAI API. If no key provided, uses the environment variable OPENAI_API_KEY
    """
    # overwrite the environment variable if a key is provided
    if api_key is not None:
        os.environ['OPENAI_API_KEY'] = api_key

    # ensure that a key is set
    if os.environ.get('OPENAI_API_KEY') is None:
        raise ValueError('OpenAI API key not provided or set in environment variable OPENAI_API_KEY')

    # openai just looks at the environment key, or expects you to pass it in with the client.
    # it does not have a global way to set it anymore

def set_gemini_api_key(api_key:str|None=None):
    """
    Set the Gemini API key for the Gemini API. If no key provided, uses the environment variable GEMINI_API_KEY
    """
    if api_key is None:
        api_key = os.environ.get('GEMINI_API_KEY')
    if api_key is None:
        raise ValueError('Gemini API key not provided or set in environment variable GEMINI_API_KEY')
    genai.configure(api_key=api_key)


@contextmanager
def move_to_isolated_dir(prefix:str='workdir_') -> Generator[None, None, None]:
    """
    Context to create a unique isolated directory for working in, and move cd into it (and exit on context end)

    Args:
        prefix (str): Prefix for the directory name. A timestamp will be appended to this prefix.
    """
    original_dir = Path.cwd()
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        isolated_dir = Path(f'{prefix}{timestamp}')
        isolated_dir.mkdir(exist_ok=True)
        os.chdir(isolated_dir)
        yield
    finally:
        os.chdir(original_dir)
        # Optionally, remove the isolated directory if empty
        if not os.listdir(isolated_dir):
            os.rmdir(isolated_dir)