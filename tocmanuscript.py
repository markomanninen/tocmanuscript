"""
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

---

Start with the first step!

"""

from datetime import datetime
import pickle
import os

def docs(*args):
    """ Print doc string of the main classes. """
    for cls in args:
        print(cls)
        print(cls.__doc__)

class ToCDict(dict):
    """
    A specialized dictionary class that extends the built-in dict type to manage a table of contents (ToC) structure.
    The ToCDict class provides custom handling for setting items, ensuring that the values adhere to a specific structure
    with attributes like 'prompt', 'title', 'created', 'modified', and 'completed'.

    The __setitem__ method is overridden to enforce these constraints and manage timestamps for 'created' and 'modified',
    as well as the 'completed' attribute.

    Usage:
        a = ToCDict({})
        a[1] = ToCDict({'title': 'title 1'})
        # This is the right way to setting a new index/subsection.
        a[1][1] = ToCDict({'title': 'title 1.1'})
        # This is the wrong way. Title 2.1 is not going to reach __setitem__.
        a[2] = ToCDict({'title': 'title 2', 1: ToCDict({'title': 'title 2.1'})})
    """
    def __setitem__(self, key, value):
        """
        ToCDict __setitem__ overrides the default behavior for setting an item's value. Ensures that the value is a dictionary and contains specific keys like 'prompt' and 'title'. Also manages timestamps for 'created' and 'modified' and sets the 'completed' attribute.

        :param key: The key for which the value needs to be set.
        :param value: The value to be set. Must be a dictionary and contain specific keys and objects:
            - 'prompt': (Optional) A Prompt object.
            - 'title': The title associated with the key.
            - 'modified': (Automatically set) The timestamp when the value was last modified.
            - 'created': (Automatically set if not provided) The timestamp when the value was created.
            - 'completed': (Automatically set to False if not provided) A flag indicating whether the task associated with the key is completed.
                           If a prompt has not been given, then the title is printed without content, and completed is automatically True.

        :raises ValueError: If the value is not a dictionary, if 'prompt' is not a Prompt object, or 'title' is not given.
        """
        if type(value) == ToCDict:
            if 'prompt' in value and type(value['prompt']) != Prompt:
                raise ValueError('Prompt must be an object.')
            if 'title' not in value:
                raise ValueError('Title must be given.')
            value['modified'] = datetime.now()
            self['modified'] = value['modified']
            if 'created' not in value:
                value['created'] = value['modified']
            if 'completed' not in value:
                value['completed'] = False
            if 'prompt' not in value:
                value['completed'] = True
        super().__setitem__(key, value)

class ToCManuscript(ToCDict):

    _restoring = False  # Class-level attribute

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
        """

        self.title = title
        self.output_dir = output_dir

        if self.title:
            filepath = os.path.join(self.output_dir, f'{self.title}.pkl')
            if os.path.exists(filepath):
                ToCManuscript._restoring = True
                with open(filepath, 'rb') as file:
                    saved_obj = pickle.load(file)
                    super(ToCManuscript, self).__dict__.update(saved_obj.__dict__)
                ToCManuscript._restoring = True
            else:
                self.subtitle = subtitle
                self.author = author
                self.publication_args = kwargs
                self.created = datetime.now()
                self.modified = datetime.now()
                self.completed = False
                self.currently_editing_index = []
                self.directives = {}
                self.guidelines = {}
                self.constraints = {}

    def __setitem__(self, key, value):
        """
        Sets the value for the specified key in the instance. If the value is of type 'ToCDict', the current state of the object is saved to a pickle file.

        :param key: The key for which the value is to be set.
        :param value: The value to be set for the specified key. If of type 'ToCDict', the object's state is saved.
        """

        if ToCManuscript._restoring:
            super().__setitem__(key, value)
            return

        # Set global references if prompt properties are not given.
        if isinstance(value, ToCDict):
            if "directives" not in value:
                value["directives"] = self.directives
            if "guidelines" not in value:
                value["guidelines"] = self.guidelines
            if "constraints" not in value:
                value["constraints"] = self.constraints

        super().__setitem__(key, value)

        # If the value is of type 'ToCDict', execute specific logic (e.g., pickling)
        if isinstance(value, ToCDict):
            if not self.title:
                print("Manuscript title is missing. Cannot save the current state of the manuscript.")
                return
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            filepath = os.path.join(self.output_dir, f'{self.title}.pkl')
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

    def get_currently_editing_prompt(self):
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
        for idx in self.currently_editing_index:
            nested_dict = nested_dict[idx]
        prompt = nested_dict.get("prompt", "")
        if prompt == "":
            print("Item '%s' may not need prompt for content generation. Move on to the next section." % nested_dict.get("title", ""))
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

    def check_complete(self):
        """
        Checks the completion status of all sections in the manuscript. If all sections are marked as complete, the manuscript's global completion status is set to True. Otherwise, a notice is printed, and a list of all incomplete sections is provided.

        :return: None
        """
        incomplete_sections = self._check_completion_status(self, [])

        if not incomplete_sections:
            print("All sections are completed.")
            self.completed = True
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
        next_index = find_next_index(self.currently_editing_index, self)
        self.currently_editing_index = next_index
        return next_index

    def print_toc(self):
        """
        Print the Table of Contents (TOC) in a hierarchical tree format.

        This method iteratively traverses the nested structure of the TOC, considering various keys and levels of nesting,
        and prints the titles of the sections and subsections with appropriate indentation.

        Example Output:
            - Introduction
              - The Birth of AI
              - The Perceptron: A Pioneering Concept
            - Scope of the Manuscript
              - The Perceptron: Inception, Impact, and Legacy
              - Frank Rosenblatt and the Inception of the Perceptron
            ...
        """

        def _print_toc(toc, level=0):
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
                # Check if the value is a ToCDict instance (i.e., a section)
                if isinstance(value, ToCDict):
                     # Get the title and print with indentation
                    title = value.get('title', '')
                    completed = ' (completed)' if value.get('completed', False) else ''
                    print(f'{indent}- {title}{completed}')
                    # Recursive call for nested levels, increasing the indentation
                    _print_toc(value, level + 1)

        # Start the recursive printing from the root level
        _print_toc(self)

class Author(dict):
    """
    The Author class represents information about an author, including their name and various optional properties.
    It inherits from the Python dictionary class, allowing for flexible storage and retrieval of author-related attributes.

    Example:
        author = Author(name="Jane Doe", email="jane.doe@example.com", affiliation="Famous University")
        print(author['name'])  # Output: Jane Doe
        print(author['email']) # Output: jane.doe@example.com

    See more: print(Author.__init__.__doc__)
    """
    def __init__(self, name, **kwargs):
        """
        Initializes the Author class with the author's name and additional properties.

        :param name: The name of the author as a string.
        :param kwargs: Optional keyword arguments representing author-related properties, such as:
            - 'email': The author's email address.
            - 'website': URL of the author's personal or professional website.
            - 'affiliation': The author's affiliation with an institution, organization, or publisher.
            - 'social_media': Links to the author's social media profiles (e.g., Twitter, LinkedIn).
            - 'biography': A brief description of the author's background, career, and accomplishments.
            - 'education': Details about the author's educational background, degrees, and institutions.
            - 'awards': List of awards or honors received by the author in the literary or academic field.
            - 'contact_number': The author's contact phone number.
            - 'agent': Information about the author's literary agent, if applicable.
            - 'genres': List of preferred writing genres, if applicable (e.g., fiction, non-fiction).
            - 'nationality': The author's nationality or country of origin.
            - 'birth_date': The author's birth date.
            - 'publications': List of notable publications by the author, including books, articles, etc.
            - 'pen_name': If applicable, the pseudonym used by the author.
            - 'languages': Languages the author writes in or is proficient in.
        """
        if name:
            self['name'] = name
        for k, v in kwargs.items():
            self[k] = v

    def __str__(self):
        return f"Author({', '.join(f'{k}: {v}' for k, v in self.items())})"

    def __repr__(self):
        kwargs_str = ', '.join(f"{k}={repr(v)}" for k, v in self.items() if k != 'name')
        return f"Author(name={repr(self.get('name'))}, {kwargs_str})"

class Prompt:
    """
    The Prompt class is designed to encapsulate directives, guidelines, and constraints for guiding a large language model's response. Consider the following writing tips:

    1. Target Audience, 2. Message and Theme, 3. Purpose, 4. Style and Tone, 5. Structuring and Organization, 6. Main Characters/Concepts, 7. Evidence/Background Research, and

    8. Textual Devices and Language Usage:

        Fiction:
            Metaphors and Similes: Creating vivid imagery.
            Dialogue: Revealing the character's personality.
            Foreshadowing: Building suspense.
            Alliteration and Assonance: Enhancing rhythm.
            Point of View: Controlling narration.
        Non-Fiction:
            Clarity and Precision: Ensuring understanding.
            Data Visualization: Enhancing comprehension.
            Rhetorical Questions: Engaging readers.
            Anecdotes and Case Studies: Humanizing concepts.
            Citation and Referencing: Establishing credibility.
        Both:
            Tone and Voice: Creating mood and connection.
            Active vs. Passive Voice: Controlling focus.
            Transitional Phrases: Ensuring smooth flow.

    Here's a summary of the Prompt class parameters that encapsulate all the user-given definitions:

    Directives: These are the core instructions that guide the model's response. They can include various subcategories like questions, statements, instructions, creative requests, analytical questions, hypothetical scenarios, debates, dialogues, step-by-step, and more.

    Guidelines: These shape the tone, structure, and context of the response. They can include aspects like role, style, format, context, audience awareness, cultural sensitivity, accessibility considerations, and multimodal instructions.

    Constraints: These set limitations or boundaries for the response, including length constraints, content restrictions, time, ethics, language, accessibility, legal or regulatory, domain-specific, sensitivity, and multimodal constraints.

    Example:
        guidelines = {
            'Style': 'Formal',
            'Format': 'Essay',
            'Audience Awareness': 'Academic Readers'
        }
        constraints = {
            'Length Constraints': '1000 words',
            'Content Restrictions': 'Exclude slang or colloquial language'
        }

        # Create a Prompt object for section 1
        section_1_prompt = Prompt(
            directives={'Instruction': 'Write an introduction to the topic of artificial intelligence.'},
            guidelines=guidelines,
            constraints=constraints
        )

    See more: print(Prompt.__init__.__doc__)
    """
    def __init__(self,
                 directives={},
                 guidelines={},
                 constraints={}):
        """
        Initializes the Prompt class with directives, guidelines, and constraints.

        :param directives: The core instruction that guides the model's response. Can include subcategories like:
            - Question: Asking for specific information.
            - Statement: Providing information to elicit a response.
            - Instruction: Giving a command or request.
            - QA/Debate Interaction: Structuring a question-and-answer or debate format.
            - Informational Query: Asking for factual information or explanations.
            - Creative Request: Asking the model to generate creative content like poetry, stories, etc.
            - Analytical Question: Requesting analysis, comparison, or evaluation.
            - Instructional Command: Providing step-by-step instructions or guidance.
            - Hypothetical Scenario: Posing a hypothetical situation or question.
            - Debate or Argumentation: Asking the model to take a stance or debate a topic.
            - Interactive Dialogue: Engaging in a back-and-forth dialogue or conversation.
            - Multimodal Interaction: Including non-textual elements like images, audio, etc.
            - Conditional Request: Making a request based on certain conditions or criteria.
            - Emotional Engagement: Asking the model to respond with empathy, humor, etc.
            Example:
                {
                    'Question': 'How to lose weight?',
                    ...
                }

        :param guidelines: Shapes the tone, structure, and context of the response. Can include subcategories like:
            - Role: Defining a persona or scenario.
            - Style: Guiding the language or tone.
            - Format: Specifying the structure or layout.
            - Context: Providing background information.
            - N-Shot Learning: Providing examples to guide the model's understanding.
            - Audience Awareness: Tailoring the response to a specific audience or demographic.
            - Cultural Sensitivity: Considering cultural norms, values, or customs.
            - Accessibility Considerations: Ensuring the response is accessible to all users, including those with disabilities.
            - Multimodal Instructions: Including non-textual elements or instructions, like visual, auditory, or other sensory instructions.
            Example:
                {
                    'Role': 'You are a personal trainer',
                    'Style': 'Explain in layman\'s terms',
                    ...
                }

        :param constraints: Sets limitations or boundaries for the response. Can include subcategories like:
            - Length Constraints: Limiting the response to a specific length, such as word or character count.
            - Content Restrictions: Avoiding certain words, topics, or content.
            - Time Constraints: Requiring a response within a specific time frame or historical period.
            - Ethical Constraints: Adhering to ethical guidelines, such as privacy or bias considerations.
            - Language Constraints: Specifying the language or dialect to be used.
            - Accessibility Constraints: Ensuring the content is suitable for all users, including those with disabilities.
            - Legal or Regulatory Constraints: Complying with legal or regulatory requirements.
            - Domain-Specific Constraints: Staying within a specific domain or field of knowledge.
            - Sensitivity Constraints: Avoiding content that might be considered offensive or inappropriate.
            - Multimodal Constraints: Limitations related to non-textual elements, like images or audio.
            Example:
                {
                    'Length Constraints': '100 words',
                    'Content Restrictions': 'Exclude diet, starving, heavy-weight lifting keywords',
                    ...
                }
        """
        self.directives = directives
        self.guidelines = guidelines
        self.constraints = constraints

    def __repr__(self):
        return f"Prompt(directives={self.directives}, guidelines={self.guidelines}, constraints={self.constraints})"

    def __str__(self):
        return f"Prompt(directives: {self.directives}, guidelines: {self.guidelines}, constraints: {self.constraints})"
