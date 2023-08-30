from .core import ToCManuscript, ToCDict, Prompt, Author
from .Schema import Schema
from .StorySchema import StorySchema
from .ResearchSchema import ResearchSchema

def docs(*args):
    """ Print doc string of the main classes. """
    for cls in args:
        print(cls)
        print(cls.__doc__)
