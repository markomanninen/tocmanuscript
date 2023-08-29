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

This step-by-step procedure facilitates manuscript generation using ChatGPT and the Noteable plugin. The process involves downloading the `tocmanuscript` module, importing the required classes, accessing documentation, initializing class instances, collecting table of contents (TOC) titles and prompts, iteratively generating content section by section, and ultimately saving the completed manuscript as a markdown text file. Each step is stored in notebook cells, allowing for independent execution at any time. For paid v4 users, the associated ChatGPT conversation can be shared to demonstrate the manuscript's creation process.


## STEP 1 (a-f)

a) Start with a new or existing project and notebook.

b) If the module is not present in your Noteable project or if you wish to replace the existing file, download it from GitHub using the following command with the `-O tocmanuscript.py` option:

```
!wget https://raw.githubusercontent.com/markomanninen/tocmanuscript/main/tocmanuscript.py
```

c) Import the necessary classes:

```
from tocmanuscript import ToCDict, ToCManuscript, Prompt, Author, docs
```

d) Access the documentation for the `ToCManuscript`, `Prompt`, `Author`, and `ToCDict` classes for future reference:

```
docs(ToCManuscript, Author)
```

e) Prompt the user for the manuscript title and author details.

f) Initialize `author` and `toc_manuscript` instances using the information provided:

```
author = Author("John Doe")
toc_manuscript = ToCManuscript(title="Manuscript title", author=author)
```

If at any time, Noteable notebook kernel breaks down, you can import the main classes, initialize `TocManuscript` with empty arguments, and continue from where you left.


## STEP 2

In this stage, the user should supply the TOC, optionally including descriptions, formatted as a hierarchical tree:

```
Heading 1 [Description]
 - Heading 2
   - Heading 3
Heading 1
...
```

Either request the TOC from the user or assist in crafting one.


## STEP 3 (a-b)

a) Consult the documentation of the `Prompt` class for guidance on this step: `docs(Prompt)`

b) Establish general rules for LLM prompts. For example:

```
guidelines = {'Role': 'Author', 'Style': 'Formal', 'Format': 'Essay', 'Context': 'Academic Research'}
constraints = {'Content': 'Start with the main heading/title; Conclude with a summary at the end; Exclude slang or colloquial language; Refrain from covering topics from future chapters and sections; Avoid fragmented structures with excessive subtitles'}
```

Apply these as the global system prompt for LLM:

```
toc_manuscript.set_guidelines(guidelines)
toc_manuscript.set_constraints(constraints)
```

Remember, these general rules can be overridden for any specific section prompt.


## STEP 4 (a-b, iterative)

These definitions will guide the future content creation in STEP 5.

a) Formulate prompts for individual sections:

```
section_1_prompt = Prompt(
    directives = {'Instruction': '...'}
)
```

To override global guidelines and constraints, specify them either during the `prompt` initialization or later through separate assignments:

```
section_1_prompt.guidelines = {}
section_1_prompt.constraints = {}
```

For more information on prompt parameters and examples, consult: `print(Prompt.__init__.__doc__)`

b) CDefine a title and prompt for the section, making sure the value is of `ToCDict` type:

```
toc_manuscript[1] = ToCDict({'title': 'Heading level one', 'prompt': section_1_prompt})
```

Batch initialization of sections is possible but advisable to limit to a small number, such as half a dozen, due to context window or max_token limitations. It's preferable to proceed with smaller tasks.

Note: if `prompt` is not given, then the `content` is not supposed to be generated, and `completed` parameter will automatically be `True`.

Note: When a `prompt` isn't supplied, the `content` won't be generated. For instance:

```
toc_manuscript[1] = ToCDict({'title': 'Heading level one', 'prompt': section_1_prompt})
toc_manuscript[1][1] = ToCDict({'title': 'Heading level two', 'prompt': section_1_1_prompt})
toc_manuscript[2] = ToCDict({'title': 'Only heading level one'})
```

Repeat STEP 4 for additional sections.


## STEP 5 (a-h, iterative)

After completing the last iteration in STEP 4, run `toc_manuscript.print_toc()` to display the planned table of contents as plain text.

Now, with all titles and prompts in place, use Noteable + ChatGPT to sequentially generate content for each item in the TOC.

### STEP 5a

Utilize `move_to_next_section_and_get_prompts()` to advance the internal pointer to the forthcoming section. This will reveal the section index as well as the governing rules and directives for generating its content. Additionally, this provides insight into subsequent sections.

```
print(toc_manuscript.move_to_next_section_and_get_prompts())
```

__Additional Information for STEP 5a__

`move_to_next_section_and_get_prompts()` returns the `instructions` dictionary which includes:

- `current_index`: Denotes the section currently under consideration.
- `current_prompt`: Provides the prompt allocated for this specific section.
- `next_prompt_directives`: Outlines the directives for the succeeding section's prompt. If no further sections exist, this key will read "THE END."

The `next_prompt_directives` key serves a specific function: to prevent LLM from divulging information about future sections during current content generation. This ensures continuity and avoids repetitive content.

Note: If `current_prompt` returns empty, it's an indication to invoke `move_to_next_section_and_get_prompts()` once more to skip to the succeeding section.

Reaching "THE END" in `next_prompt_directives` implies that the manuscript generation will soon conclude.

Before advancing to the next phases, b-h, seek user authorization. Pausing at this juncture allows LLM to digest the latest instructions, displayed on the user chat interface.

### STEP 5b

Generate the section's content, adhering to token or length limitations. Use double line breaks to signify new paragraphs:

```
section_content = '''
LLM generated content...
'''
```

Display the generated content for user review.

Note: Refrain from using extraneous placeholders or variables for this content. `ToCManuscript` class does not feature a method for content generation; this task is solely handled by LLM (ChatGPT).

### STEP 5c

Scrutinize the generated text, evaluating its literary elements and techniques. Ensure compliance with the initial guidelines and constraints. Identify areas for refinement.

### STEP 5d

Incorporate the identified improvements and produce a revised version of the content, still observing token or length limits.

### STEP 5e

Store the finalized content and its completion status, which can be either `True` for complete or `False` for a draft. By default, the state is set to `False`:

```
toc_manuscript.set_currently_editing_content(section_content, completed=True)
```

### STEP 5f

Condense the essence of the previously generated content to avoid repetition in future content generation:

```
toc_manuscript.set_currently_editing_summary('...')
```

### STEP 5g

If applicable, fill in the story schema by substituting example data in subsequent method calls:

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

Multiple method calls can be executed within the current section if its sub schema contains multiple items.

### STEP 5h

If `next_prompt_directives` reads "THE END," proceed to STEP 6. Otherwise, loop back to STEP 5.


## STEP 6 (a-c)

a) Determine the completion status of various sections using `toc_manuscript.check_complete()`.

b) When all sections are populated, save the assembled content to a markdown file in the text directory:

```
manuscript_content = toc_manuscript.generate()
filepath = toc_manuscript.get_filepath()
```

Sections flagged with `completed = False` will feature a (draft) label in the heading and will also show the associated prompt information.

c) Alternatively, simply retrieve the manuscript content without storing it:

```
manuscript_content = toc_manuscript.get_content()
```

---

Initiate the procedure with the first step!
