class Author(dict):
    """
    The Author class represents information about an author, including their name and various optional properties.
    It inherits from the Python dictionary class, allowing for flexible storage and retrieval of author-related attributes.

    Example:
        author = Author(name="Jane Doe", email="jane.doe@example.com", affiliation="Famous University")
        print(author['name'])  # Output: Jane Doe

    See more: print(Author.__init__.__doc__)
    """
    def __init__(self, name, **kwargs):
        """
        Initializes the Author class with the author's name and additional properties.

        :param name: The name of the author as a string.
        :param kwargs: Optional keyword arguments representing author-related properties, such as:
            - 'email': The author's email address.
            - 'website': URL of the author's personal or professional website.
            - 'affiliation': The author's affiliation with an institution, organization, or publisher.
            - 'social_media': Links to the author's social media profiles (e.g., Twitter, LinkedIn).
            - 'biography': A brief description of the author's background, career, and accomplishments.
            - 'education': Details about the author's educational background, degrees, and institutions.
            - 'awards': List of awards or honors received by the author in the literary or academic field.
            - 'contact_number': The author's contact phone number.
            - 'agent': Information about the author's literary agent, if applicable.
            - 'genres': List of preferred writing genres, if applicable (e.g., fiction, non-fiction).
            - 'nationality': The author's nationality or country of origin.
            - 'birth_date': The author's birth date.
            - 'publications': List of notable publications by the author, including books, articles, etc.
            - 'pen_name': If applicable, the pseudonym used by the author.
            - 'languages': Languages the author writes in or is proficient in.
        """
        if name:
            self['name'] = name
        for k, v in kwargs.items():
            self[k] = v

    def __str__(self):
        return f"Author({', '.join(f'{k}: {v}' for k, v in self.items())})"

    def __repr__(self):
        kwargs_str = ', '.join(f"{k}={repr(v)}" for k, v in self.items() if k != 'name')
        if kwargs_str:
            return f"Author(name={repr(self.get('name'))}, {kwargs_str})"
        else:
            return f"Author(name={repr(self.get('name'))})"
