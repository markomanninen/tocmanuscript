from .Schema import Schema

class StorySchema(Schema):
	
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
        super().__init__(self.schema)
