from .Schema import Schema

class StorySchema(Schema):

    schema = {
        'Character': {
            'Name': {
                'Role': 'String',
                'Traits': ['List of Strings'],
                'Arc': 'String',
                'History': 'String',
                'Persona': 'String'
            },
        },
        'Scene': {
            'Chapter_Title': [
                {
                    'Section_Title': 'String',
                    'Setting': 'String',
                    'Characters': ['List of Strings'],
                    'Places': ['List of Strings'],
                    'Objects': ['List of Strings'],
                    'Symbols': ['List of Strings'],
                    'Key Elements': ['List of Strings']
                },
            ],
        },
        'Place': [
            {
                'Name': 'String',
                'Description': 'String',
                'Significance': 'String'
            }
        ],
		'Timeline': [
            {
                'Time': 'String',
				'Event': 'String',
				'Type': 'Normal/Dream/TimeTravel',
                'Significance': 'String'
            }
        ],
        'Object': [
            {
                'Name': 'String',
                'Description': 'String',
                'Significance': 'String',
                'Material': 'String',
                'Age': 'String'
            }
        ],
        'Symbol': [
            {
                'Name': 'String',
                'Description': 'String',
                'Significance': 'String'
            }
        ],
        'Directive': {
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


class MysterySchema(StorySchema):
    genre_schema = {
        'Suspect': {
            'Name': {
                'Motive': 'String',
                'Alibi': 'String',
                'Relationship': 'String'
            }
        },
        'Detective': {
            'Name': {
                'Skills': ['List of Strings'],
                'Background': 'String'
            }
        },
        'Clue': [
            {
                'Type': 'String',
                'Location': 'String',
                'Significance': 'String'
            }
        ],
        'Red_Herring': [
            {
                'Type': 'String',
                'Source': 'String'
            }
        ]
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema)

class FantasySchema(StorySchema):
    genre_schema = {
        'Magic_System': {
            'Name': {
                'Rules': 'String',
                'Limitations': 'String',
                'Source': 'String'
            }
        },
        'Creature': {
            'Name': {
                'Abilities': ['List of Strings'],
                'Weaknesses': ['List of Strings'],
                'Habitat': 'String'
            }
        },
        'Kingdom': {
            'Name': {
                'Ruler': 'String',
                'Culture': 'String',
                'Geography': 'String'
            }
        },
        'Artifact': {
            'Name': {
                'Powers': 'String',
                'Origin': 'String',
                'Custodian': 'String'
            }
        }
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema)

class RomanceSchema(StorySchema):
    genre_schema = {
        'Relationship': {
            'Pairing': {
                'Dynamics': 'String',
                'Status': 'String',
                'History': 'String'
            }
        },
        'Conflict': [
			{
            	'Type': 'String',
            	'Resolution': 'String'
			}
        ],
        'Milestone': [
			{
            	'Event': 'String',
	            'Significance': 'String',
	            'Time': 'String'
			}
        ],
        'Setting': {
            'Location': {
                'Atmosphere': 'String',
                'Significance': 'String'
            }
        }
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema)

class SciFiSchema(StorySchema):
    genre_schema = {
        'Technology': [
			{
            	'Name': 'String',
                'Function': 'String',
                'Limitations': 'String',
                'Origin': 'String'
            }
        ],
        'Planet': {
            'Name': {
                'Climate': 'String',
                'Inhabitants': 'String',
                'Role': 'String'
            }
        },
        'Organization': {
            'Name': {
                'Purpose': 'String',
                'Hierarchy': 'String',
                'Influence': 'String'
            }
        },
        'Phenomenon': [
            {
				'Name': 'String',
                'Explanation': 'String',
                'Impact': 'String'
            }
        ]
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema, {'Phenomenon': 'Phenomena'})


class HorrorSchema(StorySchema):
    genre_schema = {
        'Fear': [
		    {
	            'Type': 'String',
	            'Trigger': 'String'
			}
        ],
        'Haunting': {
            'Location': {
                'Entity': 'String',
                'History': 'String'
            }
        },
        'Monster': {
            'Name': {
                'Abilities': ['List of Strings'],
                'Weaknesses': ['List of Strings']
            }
        },
        'Survival_Tactic': [
			{
	            'Strategy': 'String',
	            'Effectiveness': 'String'
			}
        ]
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema)


class BiographySchema(StorySchema):
    genre_schema = {
        'Life_Event': [
			{
            	'Name': 'String',
                'Time': 'String',
                'Significance': 'String'
            }
        ],
        'Achievement': [
			{
            	'Name': 'String',
                'Type': 'String',
                'Details': 'String'
            }
        ],
        'Challenge': [
            {
                'Type': 'String',
                'Outcome': 'String'
            }
        ],
        'Influence': [
            {
                'Impact': 'String',
                'Duration': 'String'
            }
        ]
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema)


class AdventureSchema(StorySchema):
    genre_schema = {
        'Quest': {
            'Name': {
                'Objective': 'String',
                'Antagonist': 'String',
                'Reward': 'String'
            }
        },
        'Obstacle': [
			{
	            'Type': 'String',
	            'Difficulty': 'String'
	        }
		],
        'Reward': {
            'Name': {
                'Value': 'String',
                'Significance': 'String'
            }
        },
        'Travel': [
			{
	            'Mode': 'String',
	            'Duration': 'String'
	        }
		]
    }
    def __init__(self):
        combined_schema = {**self.schema, **self.genre_schema}
        super().__init__(combined_schema)
