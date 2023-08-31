
import unittest
from tocmanuscript.StorySchema import StorySchema

class TestSchema(unittest.TestCase):

    def setUp(self):
        self.schema = StorySchema()

    def test_add_character(self):
        self.schema.add_character('Alice', {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})
        self.assertEqual(self.schema.get_character('Alice'), {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})

    def test_add_scene(self):
        scene_data = {
            'Section_Title': 'Introduction',
            'Setting': 'Forest',
            'Characters': ['Alice', 'Rabbit'],
            'Places': ['Forest'],
            'Objects': ['Amulet'],
            'Symbols': ['Ouroboros'],
            'Key Elements': ['Rabbit Hole']
        }
        self.schema.add_scene('Chapter 1', scene_data)
        self.assertEqual(self.schema.get_scene('Chapter 1'), [scene_data])

    def test_add_place(self):
        place_data = {
            'Name': 'Wonderland',
            'Description': 'Magical',
            'Significance': 'Central location'
        }
        self.schema.add_place(place_data)
        self.assertEqual(self.schema.get_place(), [place_data])

    def test_add_timeline(self):
        event_data = {
            'Time': 'String',
            'Event': 'String',
            'Type': 'Normal/Dream/TimeTravel',
            'Significance': 'String'
        }
        self.schema.add_timeline(event_data)
        self.assertEqual(self.schema.get_timeline(0), event_data)
        self.assertEqual(self.schema.get_timelines(), [event_data])

    """
    def test_add_timeline_event(self):
        event_data = {
            'Event': 'Alice falls',
            'Type': 'Normal',
            'Sub_Episodes': [
                {
                    'Episode': 'Alice lands',
                    'Type': 'Normal'
                }
            ]
        }
        self.schema.add_timeline('2023', {'August': {'30': [event_data]}})
        #self.assertEqual(self.schema.get_timeline('2023', 'August', '30', event_data))
        self.assertEqual(self.schema.get_timeline('2023', 'August'), {'30': [event_data]})
        self.assertEqual(self.schema.get_timeline('2023'), {'August': {'30': [event_data]}})
        self.assertEqual(self.schema.get_timeline(), {'2023': {'August': {'30': [event_data]}}})
        self.assertEqual(self.schema.get_timelines(), {'2023': {'August': {'30': [event_data]}}})
    """

    def test_add_object(self):
        object_data = {
            'Name': 'Pocket Watch',
            'Description': 'Golden',
            'Significance': 'Timekeeping',
            'Material': 'Gold',
            'Age': 'Ancient'
        }
        self.schema.add_object(object_data)
        self.assertEqual(self.schema.get_object(), [object_data])

    def test_add_directive(self):
        directive_data = {
            'Objective': 'Introduce Alice',
            'KeyEvents': ['Alice wakes up'],
            'CharactersInvolved': ['Alice'],
            'Setting': 'Bedroom',
            'Mood': 'Curious',
            'Conflict': 'None',
            'Resolution': 'Alice decides to explore',
            'Foreshadowing': 'Clock ticking',
            'KeyDialogues': ['Where am I?'],
            'Time': 'Morning',
            'SpecialInstructions': 'None'
        }
        self.schema.add_directive('Introduction', directive_data)
        self.assertEqual(self.schema.get_directive('Introduction'), directive_data)

if __name__ == '__main__':
    unittest.main()
