
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
            'Key Elements': ['Rabbit Hole']
        }
        self.schema.add_scene('Chapter 1', scene_data)
        self.assertEqual(self.schema.get_scene('Chapter 1'), [scene_data])

    def test_add_place(self):
        place_data = {
            'Place': 'Wonderland',
            'Description': 'Magical',
            'Significance': 'Central location'
        }
        self.schema.add_place('Chapter 1', place_data)
        self.assertEqual(self.schema.get_place('Chapter 1'), [place_data])

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

    def test_add_object(self):
        object_data = {
            'Object': 'Pocket Watch',
            'Description': 'Golden',
            'Significance': 'Timekeeping',
            'Material': 'Gold',
            'Age': 'Ancient'
        }
        self.schema.add_object('Chapter 1', object_data)
        self.assertEqual(self.schema.get_object('Chapter 1'), [object_data])

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
