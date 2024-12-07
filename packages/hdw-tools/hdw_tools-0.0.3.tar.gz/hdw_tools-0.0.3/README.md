#  🔎 Horizon Data Wave Tools 

`Horizon Data Wave Tools` is a collection of tools for integrating with `llamaindex` and `crewai`. This library provides endpoints to fetch data from LinkedIn via the **HorizonDataWave** data provider. You can use `hdw_tools` to easily integrate LinkedIn data queries into projects using `llamaindex` and `crewai`.

## Python Version Requirement
HDW tools requires Python 3.12 or higher.

## Installation

Install using pip:

```bash
pip install hdw_tools
```
##  Environment Variables
To use this project, you need to set the following environment variables:

**HDW_API_KEY**: The API key required for authentication. You can obtain this key by visiting [Horizon Data Wave](https://www.horizondatawave.ai/).

Make sure to add these variables to your environment configuration before running the project.

## Examples

Using with LlamaIndex
```python
from hdw_tools.tools.llama_linkedin import LinkedInToolSpec
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI

agent = OpenAIAgent.from_tools(
    [tool for sublist in [LinkedInToolSpec().to_tool_list()] for tool in sublist],
    llm=OpenAI(model="gpt-4", temperature=0.1),
    verbose=True,
    system_prompt="You are an AI assistant helping users with LinkedIn searches",
)
```
Using with CrewAI
```python
from crewai import Task
from hdw_tools.tools import crewai_linkedin

find_user_data = Task(
    description=(
        "Analyze {user_request}. Define provided data and tasks. Create plan to use existing tools to find information "
        "in requred sources based on provided information and tasks. And execute this plan."
    ),
    expected_output="Provide results in markdown format.",
    tools=[
        crewai_linkedin.GetLinkedInCompany(),
        crewai_linkedin.GetLinkedInUser(),
        crewai_linkedin.GetLinkedInPost()
    ]
)
```

##  License
This project is licensed under the MIT License. See the LICENSE file for more information.