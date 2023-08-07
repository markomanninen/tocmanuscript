# ToCManuscript v0.1

Manuscript Content Generation and Management in ChatGPT using Noteable Plugin and ToCManuscript Module written by Marko T. Manninen [https://github.com/markomanninen/tocmanuscript/](https://github.com/markomanninen/tocmanuscript/)

Copyright © 08/2023

Unlock the power of structured content creation with the ToCManuscript module in ChatGPT, seamlessly integrated with the Noteable plugin. This tool allows you to define, manage, and generate manuscript content through a hierarchical Table of Contents (TOC), all within an interactive chat environment.

With ToCManuscript, you can:

- **Define a Hierarchical TOC**: Outline your manuscript with headings, subheadings, and descriptions in a nested tree format.
- **Set Prompts and Guidelines**: Customize the content generation process with specific prompts, guidelines, and constraints for each section.
- **Generate Content Iteratively**: Let ChatGPT create content for each section, one by one, guided by the prompts you've set.
- **Manage Content Progress**: Track the completion status, edit drafts, and navigate through the TOC with ease.
- **Export to Markdown**: Save the completed manuscript to a markdown file, ready for further editing or publishing.

Whether you're working on a research paper, a novel, a technical manual, or any other long-form content, ToCManuscript streamlines the process, making it more creative, productive, and enjoyable.

Get started with ToCManuscript and transform the way you write!

# START WIZARD

This step by step procedure will help user to generate manuscript content by using ChatGPT and Noteable plugin. This procedure will use custom classes, initialize them, ask TOC titles and prompts, generate content, and save the completed manuscript to the `.md` text file.

All steps are stored to the notebook cells for running them independently at any time. The associated ChatGPT conversation can be shared to show how it was used to generate the manuscript.

Download module from github, if it is not available in th Noteable project, or if user wants to replace the file with appended option: `-O tocmanuscript.py`:

```
!wget https://raw.githubusercontent.com/markomanninen/tocmanuscript/main/tocmanuscript.py
```

a) Start a new Noteable notebook (or use a given one) to import classes:

```
from tocmanuscript import ToCDict, ToCManuscript, Prompt, Author, docs
```

b) Read ToCManuscript, Prompt, Author, and ToCDict class documentation for later reference:

```
docs(ToCManuscript, Prompt, Author, ToCDict)
```

c) Ask manuscript title and author information from the user.

d) Init author and toc_manuscript instances with the given information:

```
author = Author("John Doe")
toc_manuscript = ToCManuscript(title="Manuscript title", author=author)
```

# STEP 1

User must give a table of contents (TOC) with optional descriptions in a hierarchical tree format:

```
Heading 1 [Description]
 - Heading 2
   - Heading 3
Heading 1
...
```

Ask user to provide TOC or help user to create one.

# STEP 2

Set general guidelines for LLM prompts:

```
guidelines={'Role': '', 'Style': '', 'Format': '', 'Context': '', ...}
```

This can be used as a global system prompt for LLM. But it can be overriden at any spesific section prompt.

# STEP 3 (iterative)

a) Generate prompts for each section, one by one, to guide the future content creation in step 4:

```
section_1_prompt = Prompt(
    # Based on the current section title
    directive={'Instruction': '...'},
    # Use general guidelines or extend it
    guidelines=guidelines,
    # Optionally use restrictive definitions for prompt
    restrictions={...}
)
```

See more help: `print(Prompt.__init__.__doc__)`

b) Create title and prompt entry for the section. Value must be `ToCDict` type:

```
toc_manuscript[1] = ToCDict({'title': 'Heading level one', prompt: section_1_prompt})
```

You may initialize a group of sections, like one chapter in one cell, but possibly half a dozen sections at most, because the generated text will be limited by length. Proceeding with smaller tasks is best.

```
toc_manuscript[1][1] = ToCDict({'title': 'Heading level two', prompt: section_1_1_prompt})
```

Repeat step 3. Ask user for permission to proceed to the next item(s).

After the step 3 final iteration, you can call `toc_manuscript.print_toc()` to see the intended table of contents in plain text format.

# STEP 4 (iterative)

Once all titles and prompts are set, let Noteable + ChatGPT generate a content cell for each item in TOC, one by one.

a) Call `next_index = toc_manuscript.move_to_next_section()` to shift currently_editing_index to the next section.

b) Get prompt data: `next_prompt = toc_manuscript.get_currently_editing_prompt()`

```
print(next_index, next_prompt)
```

Wait for a user's permission to proceed to the next steps c) and d).

c) Let LLM generate content to the variable:

```
content = "..."
```

d) Set content and completition state (`True`|`False`), `True` means complete, `False` means draft:

```
toc_manuscript.set_currently_editing_content(content, completed=True)
```

Repeat step 4. Ask user for permission to proceed to the next item(s).

# STEP 5

a) Use `toc_manuscript.check_complete()` to see the current state of completed sections.

If content has been marked with `completed = False`, it will be denoted by (draft) mark in the heading and appended prompt information.

b) Once all contents are set, store the generated content to the text directory and `.md` file:

```
toc_manuscript.generate()
```
