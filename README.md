# ToCManuscript v0.1

Manuscript Content Generation and Management in ChatGPT using Noteable Plugin and ToCManuscript Module written by Marko T. Manninen [https://github.com/markomanninen/tocmanuscript/](https://github.com/markomanninen/tocmanuscript/)

Copyright © 08/2023

Unlock the power of structured content creation with the ToCManuscript module in ChatGPT, integrated with the Noteable plugin. This tool allows you to define, manage, and generate manuscript content through a hierarchical Table of Contents (TOC), all within an interactive chat environment.

With ToCManuscript, you can:

- **Define a Hierarchical TOC**: Outline your manuscript with headings, subheadings, and descriptions in a nested tree format.
- **Set Prompts and Guidelines**: Customize the content generation process with specific prompts, guidelines, and constraints for each section.
- **Generate Content Iteratively**: Let ChatGPT create content for each section, one by one, guided by the prompts you've set.
- **Manage Content Progress**: Track the completion status, edit drafts, and navigate through the TOC.
- **Export to Markdown**: Save the completed manuscript to a markdown file, ready for further editing or publishing.

Whether you're working on a research paper, a novel, a technical manual, or any other long-form content, ToCManuscript streamlines the process, making it more creative and experimental.

Copy and paste the following wizard prompt to the ChatGPT's text input with Noteable plugin activated.

# SHORT PROMPT

Download Python module:

```
!wget https://raw.githubusercontent.com/markomanninen/tocmanuscript/main/tocmanuscript.py
```

Display documentation:

```
from IPython.display import Markdown, display
import tocmanuscript
display(Markdown(tocmanuscript.__doc__))
```

Follow the instructions given in the documentation.

# LONG PROMPT

# START WIZARD

This step-by-step procedure will help user to generate manuscript content by using ChatGPT and the Noteable plugin. This procedure will download tocmanuscript module, import necessary classes, get documentation, initialize instances of the classes, ask TOC titles and prompts, generate content iteratively section by section, and save the completed manuscript to the `.md` text file.

Steps are stored in the notebook cells for running them independently at any time. The associated ChatGPT conversation can be shared (for paid v4 users) to show how it was used to generate the manuscript.

## STEP 1 (a-f)

a) Create a new project and notebook, or use current ones.

b) Download the module from GitHub if it is not available in the Noteable project or if the user wants to replace the file with appended option: `-O tocmanuscript.py`:

```
!wget https://raw.githubusercontent.com/markomanninen/tocmanuscript/main/tocmanuscript.py
```

c) Import classes:

```
from tocmanuscript import ToCDict, ToCManuscript, Prompt, Author, docs
```

d) Read ToCManuscript, Prompt, Author, and ToCDict class documentation for later reference:

```
docs(ToCManuscript, Author)
```

e) Ask manuscript title and author information from the user.

f) Init author and toc_manuscript instances with the given information:

```
author = Author("John Doe")
toc_manuscript = ToCManuscript(title="Manuscript title", author=author)
```


## STEP 2

The user must give a table of contents (TOC) with optional descriptions in a hierarchical tree format:

```
Heading 1 [Description]
 - Heading 2
   - Heading 3
Heading 1
...
```

Ask the user to provide TOC or help the user to create one.

Store toc as string in a variable so that we can refer to it at any time in the future: `toc_text = '...'`


## STEP 3 (a-b)

a) Read prompt class documentation to guide through this step: `docs(Prompt)`

b) Set general guidelines for LLM prompts:

```
guidelines={'Role': '', 'Style': '', 'Format': '', 'Context': '', ...}
constraints={'Content': 'Emit main heading/title in the beginning; Emit the conclusive part at the end of the text; Exclude slang or colloquial language; Do not consume topics and content from the future chapters and sections; Avoid fragmented structures with lots of subtitles', ...}
```

These can be used kind of a global system prompt for LLM. But they can be overridden at any specific section prompt.


## STEP 4 (a-b, iterative)

These definitions will guide the future content creation in step 5.

a) Generate prompts for each section:

```
section_1_prompt = Prompt(
    # Based on the current section title
    directives={'Instruction': '...'},
    # Use general guidelines or extend it
    guidelines=guidelines,
    # Restrictive definitions for prompt
    constraints=constraints
)
```

See more help about different prompt parameter options and examples: `print(Prompt.__init__.__doc__)`

b) Create a title and prompt entry for the section. The value must be `ToCDict` type:

```
toc_manuscript[1] = ToCDict({'title': 'Heading level one', 'prompt': section_1_prompt})
```

You may initialize a group of sections, like one chapter in one cell, but possibly half a dozen sections at most because the generated text will be limited by length. Proceeding with smaller tasks is best. Note: if `prompt` is not given, then the `content` is not supposed to follow the `title`, and `completed` parameter will automatically be `True`.

For example:

```
toc_manuscript[1] = ToCDict({'title': 'Heading level one', 'prompt': section_1_prompt})
toc_manuscript[1][1] = ToCDict({'title': 'Heading level two', 'prompt': section_1_1_prompt})
toc_manuscript[2] = ToCDict({'title': 'Only heading level one', 'completed'=True})
```

Repeat STEP 4.

## STEP 5 (a-b, c-d, iterative)

After the last item in the STEP 4 iteration, you can call `toc_manuscript.print_toc()` to see the intended table of contents in plain text format.

Once all titles and prompts are set, let Noteable + ChatGPT generate a content cell for each item in TOC, one by one.

a) Call `next_index = toc_manuscript.move_to_next_section()` to shift currently_editing_index to the next section.

b) Get prompt data and print them:

```
next_prompt = toc_manuscript.get_currently_editing_prompt()
print(next_index, next_prompt)
```

Wait for a user's permission to proceed to the next phases, c) and d). It is important to stop at this phase and let LLM read the output of the last print. It will guide LLM to generate sophisticated content.

If `next_prompt` is empty, it may indicate that the section has only a title and no content generation intended. Call `move_to_next_section()` again in that case to move to the next index.

c) Let LLM generate content for the variable:

```
content = "..."
```

d) Set content and completion state (`True`|`False`), `True` means complete, `False` means a draft, which is the default value:

```
toc_manuscript.set_currently_editing_content(content, completed=bool)
```

Repeat STEP 5. Ask the user for permission to proceed to the next item(s).


## STEP 6 (a-b)

a) Use `toc_manuscript.check_complete()` to see the current state of completed sections.

If content has been marked with `completed = False`, it will be denoted by (draft) mark in the heading and appended prompt information.

b) Once all contents are set, store the generated content in the text directory to the `.md` file:

```
manuscript_content = toc_manuscript.generate()
```
