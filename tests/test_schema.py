
import unittest
from tocmanuscript.Schema import Schema

class TestSchema(unittest.TestCase):

    def setUp(self):
        self.schema = Schema({
            'Character': {
                'Name': {
                    'Role': 'String',
                    'Traits': ['List of Strings']
                }
            },
            'Scene': {
                'Chapter_Title': [
                    {
                        'Section_Title': 'String',
                        'Setting': 'String',
                        'Characters': ['List of Strings']
                    }
                ]
            },
            'Place': [
                {
                    'Place': 'String',
                    'Description': 'String',
                    'Significance': 'String'
                }
            ]
        })


    def test_add_character(self):
        self.schema.add_character('Alice', {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})
        self.assertEqual(self.schema.get_character('Alice'), {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})

    def test_get_character(self):
        self.schema.add_character('Alice', {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})
        self.assertEqual(self.schema.get_character('Alice'), {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})

    def test_get_characters(self):
        self.schema.add_character('Alice', {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})
        self.assertEqual(self.schema.get_characters(), {'Alice': {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']}})

    def test_remove_character(self):
        self.schema.add_character('Alice', {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})
        self.schema.add_character('Bob', {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})
        self.schema.remove_character('Alice')
        self.assertEqual(self.schema.get_character('Alice'), {})
        self.assertEqual(self.schema.get_character('Bob'), {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})

    def test_add_scene(self):
        self.schema.add_scene('Chapter 1', {'Section_Title': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']})
        self.assertEqual(self.schema.get_scene('Chapter 1'), [{'Section_Title': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']}])

    def test_get_scene_by_index(self):
        self.schema.add_scene('Chapter 1', {'Section_Title': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']})
        self.assertEqual(self.schema.get_scene('Chapter 1', 0), {'Section_Title': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']})

    def test_remove_scene(self):
        self.schema.add_scene('Chapter 1', {'Section_Title': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']})
        self.schema.remove_scene('Chapter 1', 0)
        self.assertEqual(self.schema.get_scene('Chapter 1'), [])
        self.assertEqual(self.schema.get_scene('Chapter 1', 0), None)
        self.assertEqual(self.schema.get_scenes(), {'Chapter 1': []})

    def test_remove_root_scene(self):
        self.schema.add_scene('Chapter 1', {'Section_Title1': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']})
        self.schema.add_scene('Chapter 2', {'Section_Title2': 'Intro', 'Setting': 'Forest', 'Characters': ['Bob']})
        self.schema.remove_scene('Chapter 1')
        self.assertEqual(self.schema.get_scene('Chapter 1'), None)
        self.assertEqual(self.schema.get_scene('Chapter 1', 0), None)
        self.assertEqual(self.schema.get_scenes(), {'Chapter 2': [{'Section_Title2': 'Intro', 'Setting': 'Forest', 'Characters': ['Bob']}]})
        self.schema.remove_scene('Chapter 2')
        self.assertEqual(self.schema.get_scenes(), {})

    def test_remove_all_scenes(self):
        self.schema.add_scene('Chapter 1', {'Section1_Title': 'Intro1', 'Setting': 'Forest', 'Characters': ['Alice']})
        self.schema.add_scene('Chapter 1', {'Section2_Title': 'Intro2', 'Setting': 'Forest', 'Characters': ['Bob']})
        self.schema.add_scene('Chapter 2', {'Section3_Title': 'Intro3', 'Setting': 'Forest', 'Characters': ['Charles']})
        scenes = self.schema.get_scenes().items()
        for chapter, scene_list in scenes:
            for i in range(len(scene_list)):
                # remove always the first item from the list as long as there are items
                self.schema.remove_scene(chapter, 0)
        self.assertEqual(self.schema.get_scene('Chapter 1'), [])
        self.assertEqual(self.schema.get_scene('Chapter 1', 0), None)
        self.assertEqual(self.schema.get_scene('Chapter 2'), [])
        self.assertEqual(self.schema.get_scenes(), {'Chapter 1': [], 'Chapter 2': []})

    def test_add_place(self):
        self.schema.add_place({'Place': 'Forest', 'Description': 'Dark and spooky', 'Significance': 'Initial setting'})
        self.assertEqual(self.schema.get_place(), [{'Place': 'Forest', 'Description': 'Dark and spooky', 'Significance': 'Initial setting'}])

    def test_get_place(self):
        self.schema.add_place({'Place': 'Forest', 'Description': 'Dark and spooky', 'Significance': 'Initial setting'})
        self.assertEqual(self.schema.get_place(0), {'Place': 'Forest', 'Description': 'Dark and spooky', 'Significance': 'Initial setting'})

    def test_remove_place(self):
        self.schema.add_place({'Place': 'Forest', 'Description': 'Dark and spooky', 'Significance': 'Initial setting'})
        self.schema.remove_place(0)
        self.assertEqual(self.schema.get_place(0), None)

    def test_get_schema(self):
        self.assertEqual(self.schema.get_schema(), {
            'Character': {
                'Name': {
                    'Role': 'String',
                    'Traits': ['List of Strings']
                }
            },
            'Scene': {
                'Chapter_Title': [
                    {
                        'Section_Title': 'String',
                        'Setting': 'String',
                        'Characters': ['List of Strings']
                    }
                ]
            },
            'Place': [
                {
                    'Place': 'String',
                    'Description': 'String',
                    'Significance': 'String'
                }
            ]
        })

if __name__ == '__main__':
    unittest.main()
