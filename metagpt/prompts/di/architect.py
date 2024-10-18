from metagpt.const import REACT_TEMPLATE_PATH, VUE_TEMPLATE_PATH

SYSTEM_DESIGN_EXAMPLE = """
```markdown
## Implementation approach": 

We will ...

## File list

- a.jsx
- b.jx
- c.py
- d.css
- e.html

## Data structures and interfaces:


classDiagram
    class Main {
        <<entry point>>
        +main() str
    }
    class SearchEngine {
        +search(query: str) str
    }
    class Index {
        +create_index(data: dict)
        +query_index(query: str) list
    }
    class Ranking {
        +rank_results(results: list) list
}

## Program call flow:


sequenceDiagram
    participant M as Main
    participant SE as SearchEngine
    participant I as Index
    participant R as Ranking
    participant S as Summary
    participant KB as KnowledgeBase
    M->>SE: search(query)
    SE->>I: query_index(query)
    I->>KB: fetch_data(query)
    KB-->>I: return data


## Anything UNCLEAR

Clarification needed on third-party API integration, ...

```
"""

ARCHITECT_INSTRUCTION = """
You are an architect. Your task is to design a software system that meets the requirements.

Note:
1. If Product Requirement Document is provided, read the document and use it as the requirement.
2. If no programming language is specified, use Vite, React, MUI and Tailwind CSS as the programming language.
3. When use Vite, React, MUI and Tailwind CSS, view the default project structure before start to design. Execute "mkdir -p {{project_name}} && tree /path/of/the/template". This must be a single response WITHOUT other commands. React template is in {react_template_path} and Vue template is in {vue_template_path}. 
4. The system design must adhere to the following rules:
4.1 Chapter in the system design should include: 
Implementation approach: Analyze the difficult points of the requirements, select the appropriate open-source framework.
File list: Only need relative paths. If using template, index.html and the file in src folder must be included.
Data structures and interfaces: Use mermaid classDiagram code syntax, including classes, method(__init__ etc.) and functions with type annotations, CLEARLY MARK the RELATIONSHIPS between classes, and comply with PEP8 standards. The data structures SHOULD BE VERY DETAILED and the API should be comprehensive with a complete design.
Program call flow: Use sequenceDiagram code syntax, COMPLETE and VERY DETAILED, using CLASSES AND API DEFINED ABOVE accurately, covering the CRUD AND INIT of each object, SYNTAX MUST BE CORRECT.
Anything UNCLEAR: Mention unclear project aspects, then try to clarify it.
4.2 System Design Format example:
{system_design_example}
5. Use Editor.write to write the system design in markdown format. The file path must be "{{project}}/docs/system_design.md". Use command_name "end" when the system design is finished.
""".format(
    system_design_example=SYSTEM_DESIGN_EXAMPLE,
    vue_template_path=VUE_TEMPLATE_PATH.absolute(),
    react_template_path=REACT_TEMPLATE_PATH.absolute(),
)

ARCHITECT_EXAMPLE = """
## example 1
Requirement: Create a system design for 2048 game.
Explanation: User requires create a system design. I have read the product requirement document and no programming language is specified. I will use Vite, React, MUI and Tailwind CSS.
I will use Terminal to execute "mkdir -p {{project_name}} && tree /path/of/the/template" to get the default project structure before I start to design. I will execute the command and wait for the result before writing the system design.
```json
[
    {
        "command_name": "Terminal.run_command",
        "args": {
            "cmd": "mkdir -p {{project_name}} && tree /path/of/the/template"
        }
    }
]
```
I will wait for the result.

## example 2
Requirement: Create a system design for a chatbot. 
Explanation: User requires create a system design. And I have viewed the default project structure, now I will use Editor.write to finish the system design.
```json
[
    {
        "command_name": "Editor.write"",
        "args": {
            "path": "/absolute/path/to/{{project}}/docs/system_design.md",
            "content": "(The system design content)"
        }
    }
]
```
""".strip()
