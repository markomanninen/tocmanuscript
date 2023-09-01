"""
# ToCManuscript v0.2

Manuscript Content Generation and Management in ChatGPT using Noteable Plugin and ToCManuscript Module written by Marko T. Manninen [https://github.com/markomanninen/tocmanuscript/](https://github.com/markomanninen/tocmanuscript/)

Copyright © 08/2023

Unlock the power of structured content creation with the ToCManuscript module in ChatGPT, integrated with the Noteable plugin. This tool allows you to define, manage, and generate manuscript content through a hierarchical Table of Contents (TOC), all within an interactive chat environment.

With ToCManuscript, you can:

- **Define a Hierarchical TOC**: Outline your manuscript with headings, subheadings, and descriptions in a nested tree format.
- **Set Prompts and Guidelines**: Customize the content generation process with specific prompts directives, guidelines, and constraints for each section.
- **Generate Content Iteratively**: Let ChatGPT create content for each section, one by one, guided by the prompts you have set.
- **Manage Content Progress**: Track the completion status, edit drafts, and navigate through the TOC.
- **Export to Markdown**: Save the completed manuscript to a markdown file, ready for further editing or publishing.
- **Recover**: The state of the manuscript is stored each time you make chances to it. You can restore the manuscript by initializing the main class with the correct title.

Whether you are working on a research paper, a novel, a technical manual, or any other long-form content, ToCManuscript streamlines the process, making it more creative and experimental.

Copy and paste the following wizard prompt to the ChatGPT's text input with Noteable plugin activated.


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
from tocmanuscript import ToCManuscript, Prompt, Author, docs, configure
```

d) Access the documentation for the `ToCManuscript`, `Prompt`, and `Author` classes for future reference:

```
docs(ToCManuscript, Author)
```

e) Prompt the user for the manuscript title and author details.

f) Initialize `author` and `toc_manuscript` instances using the information provided:

```
author = Author("John Doe")
toc_manuscript = ToCManuscript(title="Manuscript title", author=author)
```

If at any time, Noteable notebook kernel breaks down, you can import the main classes, initialize `toc_manuscript = ToCManuscript()` with empty arguments, and continue from where you left.


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

b) Establish general rules for LLM/GPT (Large Language Model/Generative Pre-trained Transformer) prompts. For example:

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

b) Set a title and prompt for the section:

```
toc_manuscript.set_section([1], title='Heading level one', prompt=section_1_prompt)
```

Batch initialization of sections is possible but advisable to limit to a small number, such as half a dozen, due to context window or max_token limitations. It's preferable to proceed with smaller tasks.

Note: if `prompt` is not given, then the `content` is not supposed to be generated, and `completed` parameter will automatically be `True`.

Note: When a `prompt` isn't supplied, the `content` won't be generated. For instance:

```
toc_manuscript.set_section([1], title='Heading level one', prompt=section_1_prompt)
toc_manuscript.set_section([1, 1], title='Heading level two', prompt=section_1_1_prompt)
toc_manuscript.set_section([2], title='Only heading level one')
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

If applicable, populate the manuscript schema data. To know, what meta data is collected by each section, first print out the schema:

```
print(toc_manuscript.schema.get_schema())
```

Output:

```
{
    'Keyword': {
        'Section_Title': ['list of strings']
    }
}
```

Then add items according to each subschemas:

```
# Add keywords
for keyword in ["Keyword 1", "Keyword 2"]:
    toc_manuscript.schema.add_keyword("Section Title", keyword)
```

Multiple method calls can be executed within the current section if its subschemas contains multiple items.

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

"""

from .Author import Author
from .Prompt import Prompt
from .ToCDict import ToCDict
from .Schema import Schema
from datetime import datetime
import hashlib
import pickle
import os, re

class ToCManuscript(ToCDict):
    """
    The ToCManuscript class represents a manuscript with a table of contents, content sections, author information, and other publication-related properties. It provides methods for managing the manuscript's structure, content, and metadata, and for generating a Markdown file representing the manuscript.

    Example:
        # Initialize
        author = Author(name="John Doe")
        toc_manuscript = ToCManuscript(title="Manuscript title", author=author)

        # 1. Set titles and prompts (iterative)
        toc_manuscript.set_section([1], title='Heading level one')
        toc_manuscript.set_section(
            [1, 1], 
            title='Heading level two', 
            prompt=Prompt(directives={'Question': 'How to write a best-seller?'})
        )

        # Iterate 2-3
        # 2. Set index and get prompt
        # Get and output prompt to help LLM in content generation.
        print(toc_manuscript.move_to_next_section_and_get_prompts())

        # 3. Generate content
        # a) Set variable for LLM text-generated content:
        content = "..."
        # b) Set content with completed=True|False:
        toc_manuscript.set_currently_editing_content(content, completed=True)

        # Once all sections are generated with steps 2-3:
        # 4. Check if all sections are completed
        toc_manuscript.check_complete()

        # 5. Output to the markdown text file
        toc_manuscript.generate()

    See more: print(ToCManuscript.__init__.__doc__)
    """

    # Manuscript generation directory for final output and temp files.
    _output_directory = 'text_output'

  	# Flag for objects restorage process.
    _restoring = False

    def __init__(self, title = '', subtitle = '', author = None, **kwargs):
        """
        Initializes the ToCManuscript class with the given manuscript title, author, and additional publication-related properties.

        :param title: The title of the manuscript as a string.
        :param subtitle: The subtitle of the manuscript as a string.
        :param author: An Author object representing the author of the instance.
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
            # Restore already generated manuscript by just giving a title. All other information will be restored from the pickle backup file.
            toc_manuscript = ToCManuscript(title="Manuscript title")
        """

        self.title = title
        self.output_dir = ToCManuscript._output_directory

        # Try to restore ToCManuscript instance from hash file.
        nb_file_id = os.environ.get('NTBL_FILE_ID', None)
        if not self.title and nb_file_id:
            self.title = self.retrieve_title(nb_file_id)

        if self.title:
            # Make file name safe title.
            self.safe_title = re.sub('[^a-zA-Z0-9 \n\.]', '', self.title).replace(" ", "_")
            filepath = os.path.join(self.output_dir, f'{self.safe_title}.pkl')
            if os.path.exists(filepath):
                ToCManuscript._restoring = True
                with open(filepath, 'rb') as file:
                    saved_obj = pickle.load(file)
                    # Update attributes.
                    self.__dict__.update(saved_obj.__dict__)
                    # Update the dictionary items.
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
                self.schema = Schema(
                    {
                        'Keyword': {
                            'Section_Title': ['list of strings']
                        }
                    }
                )
                # Save state.
                self.pickle()
                self._save_noteable_title()

        else:
            print("Error: Could not initialize the manuscript. Title cannot be empty!")

    def _save_noteable_title(self):
        """
        Save the title to a file if the Noteable notebook file ID is available in the environment variables.
        
        This is an internal method and should not be called directly.
        """
        nb_file_id = os.environ.get('NTBL_FILE_ID', None)
        if nb_file_id:
            self.save_title_to_file(nb_file_id, self.title)
        
    def set_title(self, title, subtitle=""):
        """
        Set the title and subtitle for the object.
        
        Parameters:
            title (str): The title to set.
            subtitle (str): The subtitle to set. Default is an empty string.
        
        Side Effects:
            - Updates the object's title, subtitle, and safe_title attributes.
            - Serializes the object using pickle.
            - Calls the internal method to save the title if applicable.
        """
        if title != "":
            self.title = title
            self.subtitle = subtitle
            self.safe_title = re.sub('[^a-zA-Z0-9 \n\.]', '', self.title).replace(" ", "_")
            self.pickle()
            self._save_noteable_title()

    def retrieve_title(self, nb_file_id):
        """
        Retrieve the title associated with a notebook file ID.
        
        Parameters:
            nb_file_id (str): The notebook file ID.
        
        Returns:
            str: The title if it exists, None otherwise.
        """
        hash_object = hashlib.sha256(nb_file_id.encode())
        hash = hash_object.hexdigest()
        filepath = os.path.join(self.output_dir, f'{hash}.title')
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                return file.read()

    def save_title_to_file(self, nb_file_id, title):
        """
        Save the title associated with a notebook file ID.
        
        Parameters:
            nb_file_id (str): The notebook file ID.
            title (str): The title to save.
        """
        hash_object = hashlib.sha256(nb_file_id.encode())
        hash = hash_object.hexdigest()
        filepath = os.path.join(self.output_dir, f'{hash}.title')
        with open(filepath, 'w') as file:
            file.write(title)

    def set_section(self, indices, **kwargs):
        """
        Set a section in the nested dictionary using indices.
        
        Parameters:
            indices (list): List of indices to navigate the nested dictionary.
            kwargs (dict): Additional keyword arguments to set in the section.
        """
        d = self
        for index in indices[:-1]:
            d = d.setdefault(index, {})
        d[indices[-1]] = ToCDict(kwargs)
    
    def get_schema(self):
        """
        Retrieves the current schema instance for this Schema or its subclass.

        Returns:
            Schema: An instance of the Schema class or its subclass that represents the current schema structure.
        """
        return self.schema

    def set_schema(self, schema):
        """
        Sets a new schema instance for this Schema or its subclass.

        Parameters:
            schema (Schema): An instance of the Schema class or its subclass to set as the new schema.

        Note:
            Typically, this is set during initialization, e.g., self.schema = StorySchema().
        """
        self.schema = schema

    def set_guidelines(self, guidelines):
        """
        Set guidelines and update the 'updated' timestamp.
        
        Parameters:
            guidelines (dict): Dictionary containing the guidelines to set.
        """
        self.guidelines = guidelines
        self['updated'] = datetime.now()
        self.pickle()

    def get_guidelines(self):
        """
        Get the current guidelines.
        
        Returns:
            dict: Dictionary containing the current guidelines.
        """
        return self.guidelines

    def set_constraints(self, constraints):
        """
        Set constraints and update the 'updated' timestamp.
        
        Parameters:
            constraints (dict): Dictionary containing the constraints to set.
        """
        self.constraints = constraints
        self['updated'] = datetime.now()
        self.pickle()

    def get_constraints(self):
        """
        Get the current constraints.
        
        Returns:
            dict: Dictionary containing the current constraints.
        """
        return self.constraints

    def __setitem__(self, key, value):
        """
        Sets the value for the specified key in the instance. If the value is of type 'ToCDict', the current state of the object is saved to a pickle file.

        Parameters:
            key (str): The key for which the value is to be set.
            value (mixed): The value to be set for the specified key. If of type 'ToCDict', the object's state is saved.
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
            filepath = os.path.join(self.output_dir, f'{self.safe_title}.pkl')
        else:
            filepath = os.path.join(f'{self.safe_title}.pkl')
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
            The returned file path will be "text_output/My_Manuscript.md".
        """
        if not self.title:
            print("Manuscript title is missing!")
            return ''
        return os.path.join(self.output_dir, f'{self.safe_title}.md')

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

        Parameters:
            content_dict (dict): A dictionary containing the content to be constructed, organized hierarchically using integer keys.
            level_str (str): A string representing the current numbering level in the hierarchy, e.g., "1.2.3.".

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

        Parameters:
            file (File): The file object to which the content will be written.
            content_dict (dict): A dictionary containing the content to be written, organized hierarchically using integer keys.
            level_str (str): A string representing the current numbering level in the hierarchy, e.g., "1.2.3.".

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

        Parameters:
            index (list): The current index in the TOC.
            toc (dict): The TOC structure.

        Returns:
            list: The index of the next available section or the first section if no next section is found.

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

        return []

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
        title = nested_dict.get("title", "")
        prompt = nested_dict.get("prompt", "")
        if title == "":
            print("Section title not found. Have you reached the end of the table of contents?")
        elif prompt == "" and title != "" and not index:
            print(f"Section title '{title}' has no prompt for the content generation. Move on to the next section?")
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

        Parameters:
            content (str): The summary to be set.
        """
        self.set_summary(summary, self.currently_editing_index)

    def set_summary(self, summary, editing_index):
        """
        Sets the summary for the given editing index.

        Parameters:
            summary (str): The summary to be set.
            editing_index (list): The index path to the location within the nested dictionary where the summary should be updated.
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

        Parameters:
            content (str): The content to be set.
            completed (bool): A flag indicating whether the content editing is completed. Defaults to False.
        """
        self.set_content(content, self.currently_editing_index, completed)

    def set_content(self, content, editing_index, completed=False):
        """
        Sets the content for the given editing index.

        Parameters:
            content (str): The content to be set.
            editing_index (list): The index path to the location within the nested dictionary where the content should be updated.
            completed (bool): A flag indicating whether the content editing is completed. Defaults to False.
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

        Parameters:
            content_dict (dict): A dictionary containing the content to be checked.
            level_str_list (list): A list of strings representing the current numbering level in the hierarchy.

        Returns:
            list: A list of dictionaries containing details about the incomplete sections.
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

            Parameters:
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

    def get_next_prompt_directives(self):
        """
        Get the directives for the next prompt based on the next index.
        
        Returns:
            dict: A dictionary containing the following keys:
                - A dictionary containing directives if available.
                - An empty string if no directives are found.
                - {"Instructions": "THE END"} if the next index is the first index, indicating the end.
        """
        # Find the next index using a separate method (not shown here)
        next_index = self.find_next_index()
        
        # Check if the next index is the first index, indicating the end
        if next_index == self.first_index:
            return {"Instructions": "THE END"}
        
        # Retrieve the next prompt using the next index
        next_prompt = self.get_prompt_by_index(next_index)
        
        # Check if the next prompt has a 'directives' attribute
        if hasattr(next_prompt, 'directives'):
            return next_prompt.directives
        
        # Check if the next prompt is a dictionary
        elif isinstance(next_prompt, dict):
            return next_prompt
        
        # Return an empty string if no directives are found
        else:
            return ""

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
                "current_index": [2],
                "current_prompt": <Prompt object>,
                "next_prompt_directives": {"Instructions": "Describe the setting"}
            }
        """
        current_index = self.move_to_next_section()
        current_prompt = self.get_currently_editing_prompt()
        
        next_prompt_directives = self.get_next_prompt_directives() if current_prompt else ""
        
        result = {
            "current_index": current_index,
            "current_prompt": current_prompt,
        }
        
        if next_prompt_directives:
            result['next_prompt_directives'] = next_prompt_directives
        
        return result

    def print_toc(self, output_summaries = True):
        """
        Print the Table of Contents (TOC) in a hierarchical tree format.

        This method iteratively traverses the nested structure of the TOC, considering various keys and levels of nesting,
        and prints the titles of the sections and subsections with appropriate indentation.

        Parameters:
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

            Parameters:
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

    @classmethod
    def configure(cls, **kwargs):
        """
        Class method to configure settings for ToCManuscript.
        
        Parameters:
            kwargs (dict): Keyword arguments to set configurations. Currently supports 'output_directory'.
        
        Usage:
            ToCManuscript.configure(output_directory='/path/to/dir')
        """
        # Check if 'output_directory' is provided in keyword arguments.
        if 'output_directory' in kwargs:
            # Set the class attribute _output_directory.
            cls._output_directory = kwargs['output_directory']
            
            # Get the absolute path and print it.
            abs_path = os.path.abspath(cls._output_directory)
            print(f'Output directory set to: {abs_path}')
        else:
            print('No settings to configure.')

# Initialize configuration function.
configure = ToCManuscript.configure
