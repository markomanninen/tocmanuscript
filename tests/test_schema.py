
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

    def test_remove_character(self):
        self.schema.add_character('Alice', {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})
        self.schema.remove_character('Alice')
        self.assertEqual(self.schema.get_character('Alice'), {})

    def test_add_scene(self):
        self.schema.add_scene('Chapter 1', {'Section_Title': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']})
        self.assertEqual(self.schema.get_scene('Chapter 1'), {'Section_Title': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']})

    def test_get_scene(self):
        self.schema.add_scene('Chapter 1', {'Section_Title': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']})
        self.assertEqual(self.schema.get_scene('Chapter 1'), {'Section_Title': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']})

    def test_remove_scene(self):
        self.schema.add_scene('Chapter 1', {'Section_Title': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']})
        self.schema.remove_scene('Chapter 1')
        self.assertEqual(self.schema.get_scene('Chapter 1'), {})

    def test_add_place(self):
        self.schema.add_place(None, {'Place': 'Forest', 'Description': 'Dark and spooky', 'Significance': 'Initial setting'})
        self.assertEqual(self.schema.get_place(0), {'Place': 'Forest', 'Description': 'Dark and spooky', 'Significance': 'Initial setting'})

    def test_get_place(self):
        self.schema.add_place(None, {'Place': 'Forest', 'Description': 'Dark and spooky', 'Significance': 'Initial setting'})
        self.assertEqual(self.schema.get_place(0), {'Place': 'Forest', 'Description': 'Dark and spooky', 'Significance': 'Initial setting'})

    def test_remove_place(self):
        self.schema.add_place(None, {'Place': 'Forest', 'Description': 'Dark and spooky', 'Significance': 'Initial setting'})
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
