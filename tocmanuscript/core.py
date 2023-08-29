"""
# ToCManuscript v0.2

Manuscript Content Generation and Management in ChatGPT using Noteable Plugin and ToCManuscript Module written by Marko T. Manninen [https://github.com/markomanninen/tocmanuscript/](https://github.com/markomanninen/tocmanuscript/)

Copyright © 08/2023

Unlock the power of structured content creation with the ToCManuscript module in ChatGPT, integrated with the Noteable plugin. This tool allows you to define, manage, and generate manuscript content through a hierarchical Table of Contents (TOC), all within an interactive chat environment.

With ToCManuscript, you can:

- **Define a Hierarchical TOC**: Outline your manuscript with headings, subheadings, and descriptions in a nested tree format.
- **Set Prompts and Guidelines**: Customize the content generation process with specific prompt directives, guidelines, and constraints for each section.
- **Generate Content Iteratively**: Let ChatGPT create content for each section, one by one, guided by the prompts you have set.
- **Manage Content Progress**: Track the completion status, edit drafts, and navigate through the TOC.
- **Export to Markdown**: Save the completed manuscript to a markdown file, ready for further editing or publishing.
- **Recover**: The state of the manuscrit is stored each time you make shances to it. You can restore the manuscript by initializing the main class with the correct title.

Whether you're working on a research paper, a novel, a technical manual, or any other long-form content, ToCManuscript streamlines the process, making it more creative and experimental.

Copy and paste the following wizard prompt to the ChatGPT's text input with Noteable plugin activated.


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

"""

from .Author import Author
from .Prompt import Prompt
from .ToCDict import ToCDict
from .StorySchema import StorySchema
from datetime import datetime
import pickle
import os

class ToCManuscript(ToCDict):

  	# Flag for objects restorage process.
    _restoring = False

    """
    The ToCManuscript class represents a manuscript with a table of contents, content sections, author information, and other publication-related properties. It provides methods for managing the manuscript's structure, content, and metadata, and for generating a Markdown file representing the manuscript.

    Example:
        # Initialize
        author = Author(name="John Doe")
        toc_manuscript = ToCManuscript(title="Manuscript title", author=author)

        # 1. Set titles and prompts (iterative)
        toc_manuscript[1] = ToCDict({
            'title': 'Heading level one'
        })
        toc_manuscript[1][1] = ToCDict({
            'title': 'Heading level two',
            'prompt': Prompt(directives={'Question': 'How to write a best-seller?'}),
        })

        # Iterate 2-3
        # 2. Set index and get prompt
        # a) Determine index
        toc_manuscript.currently_editing_index = [1]
        # b) Get and output prompt to help LLM in content generation.
        print(toc_manuscript.get_currently_editing_prompt())

        # 3. Generate content
        # c) Placeholder for LLM text-generated content
        content = "..."
        # d) Set content with completed=True|False
        toc_manuscript.set_currently_editing_content(content, completed=True)

        # Once all sections are generated with steps 2-3:
        # 4. Check if all sections are completed
        toc_manuscript.check_complete()

        # 5. Output to .md text file
        toc_manuscript.generate()

    See more: print(ToCManuscript.__init__.__doc__)
    """
    def __init__(self, title, subtitle = '', author = None, output_dir = 'text_output', **kwargs):
        """
        Initializes the ToCManuscript class with the given manuscript title, author, and additional publication-related properties.

        :param title: The title of the manuscript as a string.
        :param subtitle: The subtitle of the manuscript as a string.
        :param author: An Author object representing the author of the instance.
        :param output_dir: Output directory name where the manuscript is stored on the generate function call.
        :param kwargs: Optional keyword arguments representing publication-related properties, such as:
            - 'publisher': The publisher's name or object.
            - 'publish_date': The date of publication.
            - 'edition': The edition of the publication.
            - 'isbn': International Standard Book Number.
            - 'genre': The genre of the publication.
            - 'language': The language in which the publication is written.
            - 'page_count': The total number of pages.
            - 'summary': A brief summary or description of the publication.
            - 'keywords': A list of keywords associated with the publication.
            - 'price': The price of the publication.

        Attributes:
            - name (str): The name of the publication.
            - author (Author): An object representing the author of the publication.
            - publication_args (dict): A dictionary containing additional publication-related properties.
            - created (datetime): The timestamp of when the instance was created.
            - modified (datetime): The timestamp of when the instance was last modified.
            - completed (bool): A flag indicating whether the publication is completed (True) or not (False).
            - currently_editing_index (list): A list of indices representing the currently editing sections or parts.

        Example:
            author = Author(name = "John Doe")
            toc_manuscript = ToCManuscript(title="Manuscript title", author=author)
            # Restore already generated manuscript by just giving a title and optionally output_dir. All other information will be restored from the pickle backup file.
            toc_manuscript = ToCManuscript(title="Manuscript title")
        """

        self.title = title
        self.output_dir = output_dir

        if self.title:
            filepath = os.path.join(self.output_dir, f'{self.title}.pkl')
            if os.path.exists(filepath):
                ToCManuscript._restoring = True
                with open(filepath, 'rb') as file:
                    saved_obj = pickle.load(file)
                    # Update attributes
                    self.__dict__.update(saved_obj.__dict__)
                    # Update the dictionary items
                    for key, value in saved_obj.items():
                        self[key] = value
                ToCManuscript._restoring = False
                print("Manuscript was restored from the previous state")
            else:
                self.subtitle = subtitle
                self.author = author
                self.publication_args = kwargs
                self['created'] = datetime.now()
                self['updated'] = datetime.now()
                self.completed = False
                self.currently_editing_index = []
                self.first_index = []
                self.directives = {}
                self.guidelines = {}
                self.constraints = {}
                self.schema = StorySchema()
                # Save state.
                self.pickle()
        else:
            print("Error: Could not initialize the manuscript. Title cannot be empty!")

    def set_schema(self, schema):
        self.schema = schema

    def set_guidelines(self, guidelines):
        self.guidelines = guidelines
        self['updated'] = datetime.now()
        self.pickle()

    def set_constraints(self, constraints):
        self.constraints = constraints
        self['updated'] = datetime.now()
        self.pickle()

    def __setitem__(self, key, value):
        """
        Sets the value for the specified key in the instance. If the value is of type 'ToCDict', the current state of the object is saved to a pickle file.

        :param key: The key for which the value is to be set.
        :param value: The value to be set for the specified key. If of type 'ToCDict', the object's state is saved.
        """

        # Object's init process we want to have a native functionality.
        if ToCManuscript._restoring:
            super().__setitem__(key, value)
            return

        # Set global references if prompt properties are not given.
        if isinstance(value, ToCDict):
            if not value.directives:
                value.directives = self.directives
            if not value.guidelines:
                value.guidelines = self.guidelines
            if not value.constraints:
                value.constraints = self.constraints
            if "prompt" in value:
                if not value["prompt"].directives:
                    value["prompt"].directives = self.directives
                if not value["prompt"].guidelines:
                    value["prompt"].guidelines = self.guidelines
                if not value["prompt"].constraints:
                    value["prompt"].constraints = self.constraints

        super().__setitem__(key, value)

        # If the value is of type 'ToCDict', execute specific logic (e.g., pickling)
        if isinstance(value, ToCDict):
            self.pickle()

    def pickle(self):
        """
        Serializes the current state of the ToCManuscript object and saves it to a pickle file.

        The method performs the following steps:
        1. Checks if the manuscript title is available. If not, prints an error message and returns.
        2. Checks if the output directory exists. If not, creates it.
        3. Constructs the filepath for the pickle file based on the title and output directory.
        4. Writes the serialized object to the pickle file.

        Note:
            The method uses Python's built-in `pickle` module for serialization.

        Raises:
            FileNotFoundError: If the output directory does not exist and cannot be created.
            PickleError: If pickling fails for any reason.

        Example:
            toc_manuscript = ToCManuscript(title="My Manuscript")
            toc_manuscript.pickle()  # Saves the object to a pickle file
        """
        if not self.title:
            print("Manuscript title is missing. Cannot save the current state of the manuscript.")
            return
        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if self.output_dir:
            filepath = os.path.join(self.output_dir, f'{self.title}.pkl')
        else:
            filepath = os.path.join(f'{self.title}.pkl')
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    def get_filepath(self):
        """
        Constructs the file path for the Markdown file based on the instance's title. The file will be named after the title and saved in the directory specified by 'self.output_dir'.

        If the title is missing, a warning message is printed, and an empty string is returned.

        Returns:
            str: The file path for the Markdown file, or an empty string if the title is missing.

        Example:
            Assuming 'self.title' is "My Manuscript" and 'self.output_dir' is "text_output":
            The returned file path will be "text_output/My Manuscript.md".
        """
        if not self.title:
            print("Manuscript title is missing!")
            return ''
        return os.path.join(self.output_dir, f'{self.title}.md')

    def get_content(self):
        """
        Generates a string containing details about the instance, including the author's information and publication arguments. The structure of the string is identical to the Markdown file generated by the 'generate' method.

        The string structure includes:
        - Title data: Contains title and subtitle strings.
        - Author section: Contains the author's name and other author-related properties.
        - Publication section: Contains the publication-related properties.
        - Content section: Delegates to a private method '_get_content_string' to construct the actual content.

        Returns:
            str: The content string representing the instance's details.

        Example String Structure:
            Title: Sub title

            Author

            Name: John Doe
            Email: john.doe@example.com
            ...

            Publication

            Publisher: ABC Publishing
            ...

            [Content Section]
        """
        content_str = ''
        title = self.title
        if self.subtitle:
            title = f'{title}: {self.subtitle}'
        content_str += f'{title}\n\n'
        if self.author:
            content_str += '_Author_\n\n'
            if "name" in self.author:
                content_str += f'Name: {self.author["name"]}\n'
            for key, value in self.author.items():
                if key != "name":
                    content_str += f'{key.capitalize()}: {value}\n'
        if self.publication_args:
            if self.author:
                content_str += '\n'
            content_str += '_Publication_\n\n'
        for key, value in self.publication_args.items():
            content_str += f'{key.capitalize()}: {value}\n'
        content_str += '\n'
        content_str += self._get_content_string(self, '')

        return content_str

    def _get_content_string(self, content_dict, level_str=''):
        """
        Recursively constructs content from a nested dictionary into a string, using integer keys as section identifiers. This method formats content in a hierarchical structure, providing section numbers, titles, and other details as required.

        :param content_dict: A dictionary containing the content to be constructed, organized hierarchically using integer keys.
        :param level_str: A string representing the current numbering level in the hierarchy, e.g., "1.2.3.".

        Returns:
            str: The content string representing the hierarchical structure of the content_dict.

        Example:
            Given a content_dict structured as:
                {
                    1: {'title': 'Introduction', 'content': 'This is the intro'},
                    2: {'title': 'Chapter 1', 'content': 'Chapter 1 content'},
                    ...
                }
            The output will be:
                # 1. Introduction

                This is the intro

                # 2. Chapter 1

                Chapter 1 content
                ...

            Sections marked as incomplete will include an "Updated" timestamp and a "Prompt" if provided.
        """
        content_str = ''
        sorted_keys = sorted([k for k in content_dict.keys() if isinstance(k, int)])

        for key in sorted_keys:
            value = content_dict[key]
            title = value.get('title', '')
            content = value.get('content', '')
            completed = value.get('completed', False)
            updated = value.get('updated', '')
            prompt = value.get('prompt', {})
            summary = value.get('summary', '')
            draft = ' (draft)' if not completed else ''
            next_level_str = level_str + str(key) + '.'
            content_str += f'%s {next_level_str} {title}{draft}\n\n' % ("#" * next_level_str.count("."))
            content_str += f'{content}\n'
            if not completed:
                content_str += f'\n\nUpdated: {updated}\n\n'
                if prompt:
                    content_str += f'Prompt: {prompt}\n\n'
                if summary:
                    content_str += f'Summary: {summary}\n\n'
            content_str += self._get_content_string(value, next_level_str)

        return content_str

    def generate(self):
        """
        Generates a Markdown file containing details about the instance, including the author's information and publication arguments. The file is named after the instance's name and is saved in the 'text_output' directory.

        The file structure includes:
        - Title data: Contains title and subtitle strings.
        - Author section: Contains the author's name and other author-related properties.
        - Publication section: Contains the publication-related properties.
        - Content section: Delegates to a private method '_write_content' to write the actual content.

        Note: If the 'text_output' directory does not exist, it will be created.

        Example File Structure:
            Title: Sub title

            Author

            Name: John Doe
            Email: john.doe@example.com
            ...

            Publication

            Publisher: ABC Publishing
            ...

            [Content Section]
        """
        output_dir = 'text_output'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        filepath = self.get_filepath()
        if not filepath:
            return ''
        with open(filepath, 'w') as file:
            title = self.title
            if self.subtitle:
                title = f'{title}: {self.subtitle}'
            file.write(f'{title}\n\n')
            if self.author:
                file.write('_Author_\n\n')
                if "name" in self.author:
                    file.write(f'Name: {self.author["name"]}\n')
                for key, value in self.author.items():
                    if key != "name":
                        file.write(f'{key.capitalize()}: {value}\n')
            if self.publication_args:
                if self.author:
                    file.write('\n')
                file.write('_Publication_\n\n')
            for key, value in self.publication_args.items():
                file.write(f'{key.capitalize()}: {value}\n')
            file.write('\n')
            self._write_content(file, self)
        with open(filepath, 'r') as file:
            return file.read()

    def _write_content(self, file, content_dict, level_str=''):
        """
        Recursively writes content from a nested dictionary into a given file, using integer keys as section identifiers. This method formats content in a hierarchical structure, providing section numbers, titles, and other details as required.

        :param file: The file object to which the content will be written.
        :param content_dict: A dictionary containing the content to be written, organized hierarchically using integer keys.
        :param level_str: A string representing the current numbering level in the hierarchy, e.g., "1.2.3.".

        Example:
            Given a content_dict structured as:
                {
                    1: {'title': 'Introduction', 'content': 'This is the intro'},
                    2: {'title': 'Chapter 1', 'content': 'Chapter 1 content'},
                    ...
                }
            The output will be:
                # 1. Introduction

                This is the intro

                # 2. Chapter 1

                Chapter 1 content
                ...

            Sections marked as incomplete will include an "Updated" timestamp and a "Prompt" if provided.
        """
        # Sorting keys ensure that the sections are processed in the correct order
        sorted_keys = sorted([k for k in content_dict.keys() if isinstance(k, int)])

        for key in sorted_keys:
            value = content_dict[key]
            title = value.get('title', '')
            content = value.get('content', '')
            completed = value.get('completed', False)
            updated = value.get('updated', '')
            prompt = value.get('prompt', {})
            summary = value.get('summary', '')

            # Mark draft sections with a label
            draft = ' (draft)' if not completed else ''

            # Construct nested numbering for hierarchical headings, such as "1.2.3."
            next_level_str = level_str + str(key) + '.'

            # Write the heading using the corresponding number of "#" symbols
            file.write(f'%s {next_level_str} {title}{draft}\n\n' % ("#" * next_level_str.count(".")))
            file.write(f'{content}\n')

            # Include additional information if the section is incomplete
            if not completed:
                file.write(f'\n\nUpdated: {updated}\n\n')
                if prompt:
                    file.write(f'Prompt: {prompt}\n\n')
                if summary:
                    file.write(f'Summary: {summary}\n\n')

            # Recurse into sub-sections if present
            self._write_content(file, value, next_level_str)

    def find_next_index(self):
        return self._find_next_index(self.currently_editing_index, self)

    def _find_next_index(self, index, toc):
        """
        Recursively find the index of the next available depth-first section in the TOC.

        Args:
            index (list): The current index in the TOC.
            toc (dict): The TOC structure.

        Returns:
            next_index (list): The index of the next available section or the first section if no next section is found.

        Example Cases:
            - Starting from an empty index: Returns the index of the first key in the TOC.
            - Starting from a section: Returns the index of the next sibling section at the same level.
            - If no sibling sections exist: Move up one level and repeat the process.
            - If no next section is found at any level: Start from the beginning of the TOC.

        """
        if not index:
            for key in toc.keys():
                if isinstance(key, int):
                    return [key]
            return []

        # Check for children at the current level
        current_level = toc
        for i in index:
            current_level = current_level[i]

        for key in current_level.keys():
            if isinstance(key, int):
                return index + [key]

        # If no children are found, try to find the next sibling section at the same level or above
        for level in range(len(index) - 1, -1, -1):
            current_level = toc
            for i in index[:level]:
                current_level = current_level[i]

            keys = list(current_level.keys())
            current_key_index = keys.index(index[level])
            for key in keys[current_key_index + 1:]:
                if isinstance(key, int):
                    return index[:level] + [key]

        # If no next section is found at any level, start from the beginning of the TOC
        return self._find_next_index([], toc)

    def get_prompt_by_index(self, index = []):
        return self.get_currently_editing_prompt(index)

    def get_currently_editing_prompt(self, index = []):
        """
        Retrieves the Prompt object associated with the content currently being edited within a nested dictionary structure. The method navigates through the nested dictionary using the indices stored in the 'currently_editing_index' attribute of the object.

        The 'currently_editing_index' attribute should be a list or iterable containing the keys or indices that define the path to the content within the nested dictionary.

        If the prompt is not found or is an empty string, a message is printed indicating that the item may not need a prompt for content generation.

        Returns:
            Prompt: The Prompt object at the location specified by 'currently_editing_index', or an empty string if no prompt is found.

        Example:
            Assuming 'self.currently_editing_index' is [0, 1] and the object's dictionary is:
            {
                0: {
                    1: {'prompt': Prompt(directives={'Instruction': 'Edit this content'}), 'title': 'Section 1'}
                }
            }
            The returned value will be:
            Prompt(directives={'Instruction': 'Edit this content'})

        See the Prompt class documentation for more details on the structure and usage of Prompt objects.
        """
        nested_dict = self
        start_index = index if index else self.currently_editing_index
        for idx in start_index:
            nested_dict = nested_dict[idx]
        prompt = nested_dict.get("prompt", "")
        if prompt == "":
            print("Item '%s' has no prompt for the content generation. Move on to the next section." % nested_dict.get("title", ""))
        return prompt

    def get_currently_editing_content(self):
        """
        Retrieves the content currently being edited within a nested dictionary structure. The method navigates through the nested dictionary using the indices stored in the 'currently_editing_index' attribute of the object.

        The 'currently_editing_index' attribute should be a list or iterable containing the keys or indices that define the path to the content within the nested dictionary.

        Returns:
            dict: The nested dictionary content at the location specified by 'currently_editing_index'. If 'currently_editing_index' is empty or does not correspond to a valid path, the entire dictionary is returned.
        """
        nested_dict = self
        for idx in self.currently_editing_index:
            nested_dict = nested_dict[idx]
        return nested_dict

    def set_currently_editing_summary(self, summary):
        """
        Sets the summary for the currently editing index.

        :param content: The summary to be set.
        """
        self.set_summary(summary, self.currently_editing_index)

    def set_summary(self, summary, editing_index):
        """
        Sets the summary for the given editing index.

        :param summary: The summary to be set.
        :param editing_index: The index path to the location within the nested dictionary where the summary should be updated.
        """
        # Get the reference to the nested dictionary using the index_path
        nested_dict = self
        for idx in editing_index:
            nested_dict = nested_dict[idx]

        # Update the content key within the nested dictionary
        nested_dict['summary'] = summary

        # Update the 'updated' datetime for the nested dictionary instance
        nested_dict['updated'] = datetime.now()

        # And the ToCManuscript
        self['updated'] = nested_dict['updated']

        # Save state.
        self.pickle()

    def set_currently_editing_content(self, content, completed=False):
        """
        Sets the content for the currently editing index.

        :param content: The content to be set.
        :param completed: A flag indicating whether the content editing is completed. Defaults to False.
        """
        self.set_content(content, self.currently_editing_index, completed)

    def set_content(self, content, editing_index, completed=False):
        """
        Sets the content for the given editing index.

        :param content: The content to be set.
        :param editing_index: The index path to the location within the nested dictionary where the content should be updated.
        :param completed: A flag indicating whether the content editing is completed. Defaults to False.
        """
        # Get the reference to the nested dictionary using the index_path
        nested_dict = self
        for idx in editing_index:
            nested_dict = nested_dict[idx]

        # Update the content key within the nested dictionary
        nested_dict['content'] = content

        # Update the 'updated' datetime for the nested dictionary instance
        nested_dict['updated'] = datetime.now()

        # Update completed flag for the nested dictionary instance
        nested_dict['completed'] = completed

        # And the ToCManuscript
        self['updated'] = nested_dict['updated']

        # Save state.
        self.pickle()

    def check_complete(self):
        """
        Checks the completion status of all sections in the manuscript. If all sections are marked as complete, the manuscript's global completion status is set to True. Otherwise, a notice is printed, and a list of all incomplete sections is provided.

        :return: None
        """
        incomplete_sections = self._check_completion_status(self, [])

        if not incomplete_sections:
            print("All sections are completed.")
            self.completed = True
            # Save state.
            self.pickle()
        else:
            print("The following sections are not completed:")
            for section in incomplete_sections:
                print(f"Section {section['level_str']} - {section['title']}")

    def _check_completion_status(self, content_dict, level_str_list):
        """
        Recursively checks the completion status of sections in the nested dictionary and returns a list of incomplete sections.

        :param content_dict: A dictionary containing the content to be checked.
        :param level_str_list: A list of strings representing the current numbering level in the hierarchy.

        :return: A list of dictionaries containing details about the incomplete sections.
        """
        incomplete_sections = []
        sorted_keys = sorted([k for k in content_dict.keys() if isinstance(k, int)])

        for key in sorted_keys:
            value = content_dict[key]
            title = value.get('title', '')
            prompt = value.get('prompt', None)
            completed = value.get('completed', False)

            # Construct the current numbering for hierarchical headings
            next_level_str_list = level_str_list + [str(key)]

            if not completed and prompt is not None:
                level_str = '.'.join(next_level_str_list) + '.'
                incomplete_sections.append({'level_str': level_str, 'title': title})

            # Recurse into sub-sections if present
            incomplete_sections += self._check_completion_status(value, next_level_str_list)

        return incomplete_sections

    def move_to_next_section(self):
        """
        Navigate to the next available section in the TOC.

        This method traverses the nested structure of the TOC, considering various keys and levels of nesting,
        and updates the currently_editing_index to point to the next available section.

        Returns:
            next_index (list): The index of the next available section.

        Example:
            toc_manuscript.move_to_next_section()  # Returns the index of the next section

            This will traverse to the next index every time method is called. If you want to keep
            a more static index and know exactly what you want, use: self.currently_editing_index = [indices...]
        """

        def find_next_index(index, toc):
            """
            Recursively find the index of the next available depth-first section in the TOC.

            Args:
                index (list): The current index in the TOC.
                toc (dict): The TOC structure.

            Returns:
                next_index (list): The index of the next available section or the first section if no next section is found.

            Example Cases:
                - Starting from an empty index: Returns the index of the first key in the TOC.
                - Starting from a section: Returns the index of the next sibling section at the same level.
                - If no sibling sections exist: Move up one level and repeat the process.
                - If no next section is found at any level: Start from the beginning of the TOC.

            """
            if not index:
                for key in toc.keys():
                    if isinstance(key, int):
                        return [key]
                return []

            # Check for children at the current level
            current_level = toc
            for i in index:
                current_level = current_level[i]

            for key in current_level.keys():
                if isinstance(key, int):
                    return index + [key]

            # If no children are found, try to find the next sibling section at the same level or above
            for level in range(len(index) - 1, -1, -1):
                current_level = toc
                for i in index[:level]:
                    current_level = current_level[i]

                keys = list(current_level.keys())
                current_key_index = keys.index(index[level])
                for key in keys[current_key_index + 1:]:
                    if isinstance(key, int):
                        return index[:level] + [key]

            # If no next section is found at any level, start from the beginning of the TOC
            return find_next_index([], toc)

        # Find the next index and update the currently_editing_index
        next_index = self._find_next_index(self.currently_editing_index, self)
        if not self.currently_editing_index and not self.first_index:
            self.first_index = next_index
        self.currently_editing_index = next_index
        # Save state.
        self.pickle()
        return next_index

    def move_to_next_section_and_get_prompts(self):
        """
        Moves to the next section in the manuscript and retrieves the prompts for the current and next sections.

        This method performs the following steps:
        1. Moves to the next section and updates the current editing index.
        2. Retrieves the prompt for the section currently being edited.
        3. Finds the index of the next section.
        4. Retrieves the directives for the next section's prompt, or sets it to "THE END" if there is no next section.

        Returns:
            dict: A dictionary containing the following keys:
                - "current_index": The index of the current section being edited.
                - "current_prompt": The prompt for the current section.
                - "next_prompt_directives": The directives for the next section's prompt, or "THE END" if there is no next section.

        Example:
            result = move_to_next_section_and_get_prompts()
            print(result)
            Output might be:
            {
                "current_index": 2,
                "current_prompt": <Prompt object>,
                "next_prompt_directives": {"Instructions": "Describe the setting"}
            }
        """
        current_index = self.move_to_next_section()
        current_prompt = self.get_currently_editing_prompt()
        next_index = self.find_next_index()
        next_prompt_directives = self.get_prompt_by_index(next_index).directives if next_index != self.first_index else {"Instructions": "THE END"}
        return {
            "current_index": current_index,
            "current_prompt": current_prompt,
    # Remove next directive if current prompt is empty, because it will misguide LLM to generatae content rather than move to the next prompt.
            "next_prompt_directives": next_prompt_directives if current_prompt else ""
        }

    def print_toc(self, output_summaries = True):
        """
        Print the Table of Contents (TOC) in a hierarchical tree format.

        This method iteratively traverses the nested structure of the TOC, considering various keys and levels of nesting,
        and prints the titles of the sections and subsections with appropriate indentation.

        Args:
            output_summaries (bool): Whether the TOC should contain summaries for each section. Default True.

        Example Output:
            - Introduction
              - The Birth of AI
              - The Perceptron: A Pioneering Concept
            - Scope of the Manuscript
              - The Perceptron: Inception, Impact, and Legacy
              - Frank Rosenblatt and the Inception of the Perceptron
            ...
        """

        def _print_toc(toc, level=0, parent=None):
            """
            Recursive inner function to print the TOC at different levels.

            Args:
                toc (dict): The TOC structure at the current level.
                level (int): The current level of indentation, allowing for a clear visual representation of the hierarchy.

            Behavior:
                - Iterates through the keys and values of the TOC at the current level.
                - If the value is a ToCDict instance, print the title with the appropriate indentation.
                - Recursively calls itself for nested levels, increasing the indentation.
            """
            # Calculate the indentation based on the current level
            indent = '  ' * level
            for key, value in toc.items():
                if isinstance(value, ToCDict):
                    title = value.get('title', '')

                    # If 'prompt' key exists, use its 'completed' status
                    if 'prompt' in value:
                        completed = ' (completed)' if value.get('completed', False) else ''
                    else:
                        # If 'prompt' key doesn't exist, check the 'completed' status of all immediate siblings under the same parent
                        if parent is not None:
                            completed = ' (completed)' if all(sibling.get('completed', False) for k, sibling in parent.items() if isinstance(sibling, ToCDict)) else ''
                        else:
                            completed = ''

                    print(f'{indent}- {title}{completed}')

                    if 'summary' in value:
                        summary = value.get('summary', '')
                        print(f'{indent}  {summary}')

                    _print_toc(value, level + 1, parent=value)

        # Start the recursive printing from the root level
        _print_toc(self)
