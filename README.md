# ToCManuscript v0.2

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

d) Read `ToCManuscript`, `Prompt`, `Author`, and `ToCDict` class documentation for later reference:

```
docs(ToCManuscript, Author)
```

e) Ask manuscript title and author information from the user.

f) Init `author` and `toc_manuscript` instances with the given information:

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


## STEP 3 (a-b)

a) Read prompt class documentation to guide through this step: `docs(Prompt)`

b) Set general rules for LLM prompts, for example:

```
guidelines={'Role': '{role}', 'Style': '{style}', 'Format': '{format}', 'Context': '{context}', }

constraints={'Content': 'Emit main heading/title in the beginning; Emit the conclusive part at the end of the text; Exclude slang or colloquial language; Do not consume topics and content from the future chapters and sections; Avoid fragmented structures with lots of subtitles', }
```

These can be used as a global system prompt for LLM:

```
toc_manuscript.set_guidelines(guidelines)
toc_manuscript.set_constraints(constraints)
```

General rules can be overridden at any specific section prompt.


## STEP 4 (a-b, iterative)

These definitions will guide the future content creation in STEP 5.

a) Generate prompts for each section:

```
section_1_prompt = Prompt(
    # Based on the current section title
    directives = {'Instruction': '{instruction}'}
)
```

If you want to override global system content creation rules, set specific guidelines and restrictions for the prompt either in the previous `prompt` initialization step, or with separate assignments:

```
section_1_prompt.guidelines = {}
section_1_prompt.constraints = {}
```

See more help about different prompt parameter options and examples: `print(Prompt.__init__.__doc__)`

b) Create a title and prompt entry for the section. The value must be `ToCDict` type:

```
toc_manuscript[1] = ToCDict({'title': 'Heading level one', 'prompt': section_1_prompt})
```

You may initialize a group of sections, but possibly half a dozen sections at most because the generated text will be limited by context window/max_tokens length of LLM. Proceeding with smaller tasks is best.

Note: if `prompt` is not given, then the `content` is not supposed to be generated, and `completed` parameter will automatically be `True`.

For example:

```
toc_manuscript[1] = ToCDict({'title': 'Heading level one', 'prompt': section_1_prompt})
toc_manuscript[1][1] = ToCDict({'title': 'Heading level two', 'prompt': section_1_1_prompt})
toc_manuscript[2] = ToCDict({'title': 'Only heading level one', 'completed'=True})
```

Repeat STEP 4.


## STEP 5 (a-h, iterative)

After the last item in the STEP 4 iteration, call `toc_manuscript.print_toc()` to see the intended table of contents in a plain text format.

Once all titles and prompts are set, let Noteable + ChatGPT generate a content for each item in TOC, one by one:

a) `move_to_next_section_and_get_prompts()` is used to shift internal pointer to the next section, see the section index, and the rules and instructions for the content generation and give an idea plus what is coming after this section.

```
instructions = toc_manuscript.move_to_next_section_and_get_prompts()
```

The instructions dictionary contain the following keys:

- current_index: The index of the current section being edited.
- current_prompt: The prompt for the current section.
- next_prompt_directives: The directives for the next section's prompt, or "THE END" if there is no next section.

The `next_prompt_directives` is meant to prevent LLM from telling/revealing the forthcoming details of the sections in the current section content generation. This ensure a natural flow and continuation without repeating the same material.

Note: If `current_prompt` is empty, call `move_to_next_section_and_get_prompts()` again to move to the next section.

If `next_prompt_directives` is `THE END`, it indicates that the manuscript is reaching the end after the current iteration.

Wait for a user's permission to proceed to the next phases, b - h. It is important to stop at this phase and let LLM read and comprehend the last output about the instructions by printing them on the user chat interface.

b) Generate content with maximum length/tokens as a string with double line breaks indicating paragraphs:

```
section_content = '''
LLM generated content...
'''
```

Output content for a user review.

Note: You do not need to create redundant placeholders and variables for the content. There is no content generation method in `ToCManuscript` class. It needs to be generated by LLM (ChatGPT).

c) Examine, analyze, and give a critical review of the generated content. Investigate textual devices and techniques utilized in it. Confirm that general guidelines and constraints are properly considered. Give a list of improvements.

d) Address the suggestions and regenerate the content with maximum length/tokens.

e) Set final revised content and completion state (`True`|`False`). Boolean `True` means complete, `False` means a draft, which is the default value:

```
toc_manuscript.set_currently_editing_content(content, completed=False)
```

f) Summarize the previous section content so that the next content generation will not repeat the same:

```
toc_manuscript.set_currently_editing_summary('{summary}')
```

g) Optionally, populate story schema, replacing the example data and following the next method calls:

```
# Add a character(s)
toc_manuscript.schema.add_character("Alice", {'Role': 'Protagonist', 'Traits': ['Curious', 'Brave'], 'Arc': 'Growth', 'History': 'Orphan', 'Persona': 'Adventurous'})

# Add a scene(s)
toc_manuscript.schema.add_scene("Chapter 1", [{'Section Title': 'Introduction', 'Setting': 'Forest', 'Characters': ['Alice'], 'Key Elements': ['Mysterious Door']}])

# Add a place(s) or location(s)
toc_manuscript.schema.add_place_or_location("Chapter 1", [{'Place': 'Forest Clearing', 'Description': 'A clearing filled with flowers', 'Significance': 'First major setting'}])

# Add to the timeline(s). Year, month and day can be any main epoch, sub-epoch and sub-sub-epochs. Sub episodes are for the flashbacks, or other parallel shifts in a timetine.
toc_manuscript.schema.add_timeline("2023", {'August': {'29': [{'Event': 'Alice finds a door', 'Type': 'Normal', 'Sub_Episodes': [{'Episode': 'Door opens', 'Type': 'Normal'}]}]}})

# Add an object(s) or symbol(s)
toc_manuscript.schema.add_object_or_symbol("Chapter 1", [{'Object': 'Mysterious Door', 'Description': 'An intricately carved door standing alone', 'Significance': 'Gateway to another world', 'Material': 'Wood', 'Age': 'Ancient'}])
```

You may call method multiple times, if the currenct section has multiple items.

h) Finally, if `next_prompt_directives` is THE END, then jump to STEP 6. Else repeat STEP 5.


## STEP 6 (a-c)

a) Use `toc_manuscript.check_complete()` to see the current state of completed sections.

b) Once all contents are set, store the generated content in the text directory to the markdown file:

```
manuscript_content = toc_manuscript.generate()
filepath = toc_manuscript.get_filepath()
```

If content has been marked with `completed = False`, it will be denoted by (draft) mark in the heading and appended by prompt information.

c) You can also just output the content without storing it:

```
manuscript_content = toc_manuscript.get_content()
```

---

Start with the first step!
