from datetime import datetime

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.directives = {}
        self.guidelines = {}
        self.constraints = {}

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
            if 'prompt' in value:
                if type(value['prompt']) != Prompt:
                    raise ValueError('Prompt must be an object.')
                if not value["prompt"].directives:
                    value["prompt"].directives = self.directives
                if not value["prompt"].guidelines:
                    value["prompt"].guidelines = self.guidelines
                if not value["prompt"].constraints:
                    value["prompt"].constraints = self.constraints
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
