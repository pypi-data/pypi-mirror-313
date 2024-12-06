# Ad-Hoc API
An [Archytas](https://github.com/jataware/archytas) tool that uses LLMs to interact with APIs given documentation. User explains what they want in plain english, and then the agent (using the APIs docs for context) writes python code to complete the task.

## Installation
```bash
pip install adhoc-api
```

## Usage

This is designed to be paired with an Archytas agent. You may omit the python tool, and the agent should instead return the source code to you rather than running it.

Here is a complete example of grabbing the HTML content of an API documentation page, converting it to markdown, and then having the adhoc-api tool interact with the API using the generated markdown documentation (see [examples/jokes.py](examples/jokes.py) for reference):

```python
from archytas.react import ReActAgent, FailedTaskError
from archytas.tools import PythonTool
from easyrepl import REPL
from adhoc_api.tool import AdhocApi, APISpec

from bs4 import BeautifulSoup
import requests
from markdownify import markdownify


def main():    
    # set up the API spec for the JokeAPI
    gdc_api: APISpec = {
        'name': "JokesAPI",
        'description': 'JokeAPI is a REST API that serves uniformly and well formatted jokes.',
        'documentation': get_joke_api_documentation(),
    }

    # set up the tools and agent
    adhoc_api = AdhocApi(
        apis=[gdc_api],
        drafter_config={'model': 'gemini-1.5-flash-001'},
        finalizer_config={'model': 'gpt-4o'}
    )
    python = PythonTool()
    agent = ReActAgent(model='gpt-4o', tools=[adhoc_api, python], verbose=True)

    # REPL to interact with agent
    for query in REPL(history_file='.chat'):
        try:
            answer = agent.react(query)
            print(answer)
        except FailedTaskError as e:
            print(f"Error: {e}")


def get_joke_api_documentation() -> str:
    """Download the HTML of the joke API documentation page with soup and convert it to markdown."""
    url = 'https://sv443.net/jokeapi/v2/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    markdown = markdownify(str(soup))
    
    return markdown


if __name__ == "__main__":
    main()
```

Then you can run the script and interact with the agent in the REPL:

```
$ python example.py

>>> Can you tell me what apis are available?
The available API is JokesAPI, which is a REST API that serves uniformly and well formatted jokes.

>>> Can you fetch a safe joke?
Here is a safe joke from the JokesAPI:

Category: Pun
Type: Two-part
Setup: What kind of doctor is Dr. Pepper?
Delivery: He's a fizzician.
```