class StorySchema():
    """
    The StorySchema class provides a structure for organizing various elements of a story.
    It allows for the addition of characters, scenes, places, timelines, and objects or symbols.

    Class Attributes:
        schema (dict): A dictionary that describes the expected structure for each element in the story.

    Instance Attributes:
        data (dict): A dictionary that holds the actual data for the story elements.

    Methods:
        add_character(character_name, character_dict): Adds a character to the 'Characters' subsection.
        add_scene(chapter_title, scene_dict): Adds a scene to the 'Scenes' subsection.
        add_place_or_location(chapter_title, place_dict): Adds a place or location to the 'Places_and_Locations' subsection.
        add_timeline(year, timeline_dict): Adds a timeline event to the 'Timeline' subsection.
        add_object_or_symbol(chapter_title, object_dict): Adds an object or symbol to the 'Objects_and_Symbols' subsection.
        get_schema(subschema_key=None): Retrieves the original schema structure or a specific subschema.

    Usage:
        # Create an instance
        story_schema = StorySchema()

        # Add a character
        story_schema.add_character("Alice", {'Role': 'Protagonist', 'Traits': ['Curious', 'Brave'], 'Arc': 'Growth', 'History': 'Orphan', 'Persona': 'Adventurous'})

        # Add a scene
        story_schema.add_scene("Chapter 1", [{'Section Title': 'Introduction', 'Setting': 'Forest', 'Characters': ['Alice'], 'Key Elements': ['Mysterious Door']}])

        # Add a place or location
        story_schema.add_place_or_location("Chapter 1", [{'Place': 'Forest Clearing', 'Description': 'A clearing filled with flowers', 'Significance': 'First major setting'}])

        # Add to the timeline
        story_schema.add_timeline("2023", {'August': {'29': [{'Event': 'Alice finds a door', 'Type': 'Normal', 'Sub_Episodes': [{'Episode': 'Door opens', 'Type': 'Normal'}]}]}})

        # Add an object or symbol
        story_schema.add_object_or_symbol("Chapter 1", [{'Object': 'Mysterious Door', 'Description': 'An intricately carved door standing alone', 'Significance': 'Gateway to another world', 'Material': 'Wood', 'Age': 'Ancient'}])

        # Retrieve the entire schema
    print(story_schema.get_schema())

    # Retrieve a specific subschema, e.g., 'Characters'
    print(story_schema.get_schema('Characters'))
    """
    schema = {
        'Characters': {
            'Character_Name': {
                'Role': 'String',
                'Traits': ['List of Strings'],
                'Arc': 'String',
                'History': 'String',
                'Persona': 'String'
            },
        },
        'Scenes': {
            'Chapter_Title': [
                {
                    'Section_Title': 'String',
                    'Setting': 'String',
                    'Characters': ['List of Strings'],
                    'Key Elements': ['List of Strings']
                },
            ],
        },
        'Places_and_Locations': {
            'Chapter_Title': [
                {
                    'Place': 'String',
                    'Description': 'String',
                    'Significance': 'String'
                },
            ],
        },
        'Timeline': {
            'Year': {
                'Month': {
                    'Day': [
                        {
                            'Event': 'String',
                            'Type': 'Normal/Dream/Time Travel',
                            'Sub_Episodes': [
                                {
                                    'Episode': 'String',
                                    'Type': 'Normal/Dream/TimeTravel'
                                },
                            ]
                        },
                    ]
                },
            },
        },
        'Objects_and_Symbols': {
            'Chapter_Title': [
                {
                    'Object': 'String',
                    'Description': 'String',
                    'Significance': 'String',
                    'Material': 'String',
                    'Age': 'String'
                },
            ],
        },
        'Directives': {
            'Section_Title': {
                'Objective': 'String',
                'KeyEvents': ['List of Strings'],
                'CharactersInvolved': ['List of Strings'],
                'Setting': 'String',
                'Mood': 'String',
                'Conflict': 'String',
                'Resolution': 'String',
                'Foreshadowing': 'String',
                'KeyDialogues': ['List of Strings'],
                'Time': 'String',
                'SpecialInstructions': 'String'
            },
        }
    }

    def __init__(self):
        self.data = {
            'Characters': {},
            'Scenes': {},
            'Places_and_Locations': {},
            'Timeline': {},
            'Objects_and_Symbols': {}
        }

    def add_character(self, character_name, character_dict):
        self.data['Characters'].update({character_name: character_dict})

    def add_scene(self, chapter_title, scene_dict):
        self.data['Scenes'].update({chapter_title: scene_dict})

    def add_place_or_location(self, chapter_title, place_dict):
        self.data['Places_and_Locations'].update({chapter_title: place_dict})

    def add_timeline(self, chapter_title, timeline_dict):
        self.data['Timeline'].update({chapter_title: timeline_dict})

    def add_object_or_symbol(self, chapter_title, object_dict):
        self.data['Objects_and_Symbols'].update({chapter_title: object_dict})

    @classmethod
    def get_schema(cls, subschema_key=None):
        """
        Retrieve the original schema structure or a specific subschema.

            Parameters:
                subschema_key (str, optional): The key for the subschema to retrieve.
                                              If None, the entire schema is returned.

            Returns:
                dict: The entire schema or the specified subschema.
                      Returns "Subschema not found." if the key doesn't exist.
        """
        if subschema_key:
            return cls.schema.get(subschema_key, "Subschema not found.")
        else:
            return cls.schema
