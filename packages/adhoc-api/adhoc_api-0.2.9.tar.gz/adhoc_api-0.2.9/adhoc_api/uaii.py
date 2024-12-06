"""Universal AI Interface (UAII) for OpenAI GPT-4 and (eventually) other AI models."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Literal, Generator
from openai import OpenAI
from google import generativeai as genai

from .utils import Logger, SimpleLogger

import pdb



"""
TODO: long term want this to be more flexible/generic
mixin classes to cover different features that LLMs may have (text, images, audio, video)
class GPT4o: ...
class GPT4Vision: ...
use __new__ to look at the model type and return the appropriate class for type hints

class OpenAIAgent:
    @overload
    def __new__(cls, model: Literal['gpt-4o', 'gpt-4o-mini'], timeout=None) -> GPT4o: ...
    @overload
    def __new__(cls, model: Literal['gpt-4v', 'gpt-4v-mini'], timeout=None) -> GPT4Vision: ...
    def __new__(cls, model: OpenAIModel, timeout=None):
        if model in ['gpt-4o', 'gpt-4o-mini']:
            return GPT4o(model, timeout)
        elif model in ['gpt-4v', 'gpt-4v-mini']:
            return GPT4Vision(model, timeout)
        elif:
            ...
"""


################## For now, only OpenAIAgent uses this ##################

class OpenAIRole(str, Enum):
    system = "system"
    assistant = "assistant"
    user = "user"

class OpenAIMessage(dict):
    def __init__(self, role: OpenAIRole, content: str):
        super().__init__(role=role.value, content=content)


#TODO: long term this should maybe be a single generic class
class OpenAIAgentBase(ABC):
    @abstractmethod
    def multishot_streaming(self, messages: list[OpenAIMessage], **kwargs) -> Generator[str, None, None]: ...

    def multishot_sync(self, messages: list[OpenAIMessage], **kwargs) -> str:
        gen = self.multishot_streaming(messages, **kwargs)
        return ''.join([*gen])

    def oneshot_streaming(self, prompt: str, query: str, **kwargs) -> Generator[str, None, None]:
        return self.multishot_streaming([
            OpenAIMessage(role=OpenAIRole.system, content=prompt),
            OpenAIMessage(role=OpenAIRole.user, content=query)
        ], **kwargs)

    def oneshot_sync(self, prompt: str, query: str, **kwargs) -> str:
        return self.multishot_sync([
            OpenAIMessage(role=OpenAIRole.system, content=prompt),
            OpenAIMessage(role=OpenAIRole.user, content=query)
        ], **kwargs)




OpenAIModel = Literal['gpt-4o', 'gpt-4o-mini', 'o1-preview', 'o1-mini', 'gpt-4', 'gpt-4-turbo']

class OpenAIAgent(OpenAIAgentBase):
    def __init__(self, model: OpenAIModel, timeout:float|None=None):
        self.model = model
        self.timeout = timeout

    def multishot_streaming(self, messages: list[OpenAIMessage], **kwargs) -> Generator[str, None, None]:
        client = OpenAI()
        gen = client.chat.completions.create(
            model=self.model,
            messages=messages,
            timeout=self.timeout,
            stream=True,
            temperature=0.0,
            **kwargs
        )
        for chunk in gen:
            try:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
            except:
                pass



################## For now, keeping gemini agent completely separate ##################

class GeminiRole(str, Enum):
    model = "model"
    user = "user"

class GeminiMessage(dict):
    def __init__(self, role: GeminiRole, parts: list[str]):
        super().__init__(role=role.value, parts=parts)


GeminiModel = Literal['gemini-1.5-flash-001', 'gemini-1.5-pro-001']


class GeminiAgent:
    def __init__(
            self,
            model: GeminiModel,
            cache_key:str|None,
            system_prompt:str,
            cache_content:str,
            ttl_seconds:int|None=None,
            logger:Logger=SimpleLogger()
        ):
        """
        Gemini agent with conversation caching

        Args:
            model (GeminiModel): The model to use for the Gemini API
            cache_key (str): The key used to retrieve the cached API chat
            system_prompt (str): The system prompt for the Gemini API chat
            cache_content (str): The content to cache for the Gemini API chat
            ttl_seconds (int, optional): The time-to-live in seconds for the Gemini API cache. Defaults to 1800 (30 minutes).
            logger (Logger, optional): The logger to use for the Gemini API chat. Defaults to SimpleLogger()
        """
        self.model = model
        self.system_prompt = system_prompt
        self.cache_key = cache_key
        self.cache_content = cache_content
        self.cache: genai.caching.CachedContent = None
        self.ttl_seconds = ttl_seconds or 1800
        self.logger = logger

    def load_cache(self):
        """Load the cache for the Gemini API chat instance. Raises an exception if unable to make/load the cache."""
        # Don't cache if cache_key is None
        if self.cache_key is None:
            raise ValueError('cache_key is None')

        # Don't need to load cache if it's already loaded
        if self.cache is not None:
            return

        caches = genai.caching.CachedContent.list()
        try:
            self.cache, = filter(lambda c: c.display_name == self.cache_key, caches)
            self.logger.info({'cache': f'found cached content for "{self.cache_key}"'})

        except ValueError:
            self.logger.info({'cache': f'No cached content found for "{self.cache_key}". pushing new instance.'})
            # this may also raise an exception if the cache content is too small
            self.cache = genai.caching.CachedContent.create(
                model=self.model,
                display_name=self.cache_key,
                system_instruction=self.system_prompt,
                contents=self.cache_content,
                ttl=self.ttl_seconds,
            )

    def multishot_streaming(self, messages: list[GeminiMessage], **kwargs) -> Generator[str, None, None]:
        try:
            self.load_cache()
            model = genai.GenerativeModel.from_cached_content(cached_content=self.cache)
        except Exception as e:
            if 'Cached content is too small' not in str(e) and 'cache_key is None' not in str(e):
                raise
            # if cache is too small, just run the model from scratch without caching
            self.logger.info({'cache': f'{e}. Running model without cache.'})
            model = genai.GenerativeModel(model_name=self.model, system_instruction=self.system_prompt, **kwargs)
            messages = [GeminiMessage(role=GeminiRole.model, parts=[self.cache_content]), *messages]

        response = model.generate_content(messages, stream=True, **kwargs)
        for chunk in response:
            try:
                yield chunk.text
            except:
                pass

    def multishot_sync(self, messages: list[GeminiMessage], **kwargs) -> str:
        return ''.join([*self.multishot_streaming(messages, **kwargs)])

    def query_streaming(self, message: str, **kwargs) -> Generator[str, None, None]:
        yield from self.multishot_streaming([GeminiMessage(role=GeminiRole.user, parts=[message])], **kwargs)

    def query_sync(self, message: str, **kwargs) -> str:
        return ''.join([*self.query_streaming(message, **kwargs)])



if __name__ == "__main__":
    from pathlib import Path
    from easyrepl import REPL
    import yaml
    here = Path(__file__).parent
    with open(here/'api_agent.yaml', 'r') as f:
        base_cache_content:str = yaml.safe_load(f)['apis']['default']['cache_body']
    gdc_docs = (here/'api_documentation/gdc.md').read_text()
    cache_contents = base_cache_content.format(additional_cache_body='', docs=gdc_docs)

    # insert the secret number into the cache
    cache_contents = f'{cache_contents[:len(cache_contents)//2]}\nthe secret number is 23\n{cache_contents[len(cache_contents)//2:]}'
    agent = GeminiAgent(
        "gemini-1.5-flash-001",
        "test_cache",
        'You are a python programmer writing code to perform API requests',
        cache_contents
    )

    messages: list[GeminiMessage] = []
    for query in REPL(history_file='.chat'):
        messages.append(GeminiMessage(role=GeminiRole.user, parts=[query]))
        chunks:list[str] = []
        for chunk in agent.multishot_streaming(messages):
            chunks.append(chunk)
            print(chunk, end="")
        messages.append(GeminiMessage(role=GeminiRole.model, parts=[''.join(chunks)]))

