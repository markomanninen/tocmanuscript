from .core import ToCManuscript, ToCDict, Prompt, Author, StorySchema

def docs(*args):
    """ Print doc string of the main classes. """
    for cls in args:
        print(cls)
        print(cls.__doc__)
