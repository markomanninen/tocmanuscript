
from functools import partial

class SchemaValidator:
    """
    The SchemaValidator class serves as a utility for validating schema structures.
    It provides methods to check if a given schema conforms to expected rules and structures.

    Methods:
        validate(schema: dict) -> bool: Validates the provided schema against predefined rules.

    Usage:
        # Create an instance of SchemaValidator
        validator = SchemaValidator()

        # Validate a schema
        is_valid = validator.validate({
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

        if is_valid:
            print("The schema is valid.")
        else:
            print("The schema is invalid.")
    """
    def validate(self, schema):
        if not isinstance(schema, dict):
            raise TypeError("Schema must be a dictionary.")

        for key, value in schema.items():
            if not isinstance(key, str):
                raise TypeError(f"Schema key '{key}' must be a string.")

            if isinstance(value, dict):
                self.validate(value)

            elif isinstance(value, list):
                if len(value) != 1:
                    raise TypeError(f"Schema key '{key}' must contain a list with one element.")

                if isinstance(value[0], dict):
                    self.validate(value[0])
                elif isinstance(value[0], str):
                    """
                    if value[0].lower() not in ['string', 'list of strings']:
                        raise ValueError(f"Schema key '{key}' has an unsupported type '{value[0]}'.")
                    """
                    pass

            elif isinstance(value, str):
                """
                if value.lower() not in ['string', 'list of strings']:
                    raise ValueError(f"Schema key '{key}' has an unsupported type '{value}'.")
                """
                pass

            else:
                raise TypeError(f"Schema key '{key}' has an unsupported type '{type(value).__name__}'.")

class Schema(SchemaValidator):
    """
    The Schema class serves as a generic superclass for organizing structured data.
    It dynamically generates methods for adding, retrieving, and removing data based on the provided schema.

    Class Attributes:
        schema (dict): A dictionary that describes the expected structure for each element in the schema.

    Instance Attributes:
        data (dict): A dictionary that holds the actual data for the schema elements.

    Dynamically Generated Methods:
        add_{subschema}(key, item_dict): Adds a data item to the specified subschema.
        get_{subschema}(key): Retrieves a data item from the specified subschema by its key.
        get_{subschema}s(): Retrieves all data items from the specified subschema.
        remove_{subschema}(key): Removes a data item from the specified subschema by its key.
        get_{subschema}_schema(): Retrieves the schema for the specified subschema.

    Methods:
        _add_to_subschema(subschema_key, item_key=None, item_dict=None, index=None): Internal method to add an item to a subschema.
        _get_from_subschema(subschema_key, item_key=None, index=None): Internal method to get items from a subschema.
        _remove_from_subschema(subschema_key, item_key, index=None): Internal method to remove items from a subschema.
        get_schema(subschema_key=None): Retrieves the original schema structure or a specific subschema.

    Usage:
        # Create a subclass with a specific schema for Character, Scene, and Place
        class MySchema(Schema):
            schema = {
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
            }

            def __init__(self):
                super().__init__(self.schema)

        # Create an instance
        schema = MySchema()

        # Character Handlers
        schema.add_character('Alice', {'Role': 'Protagonist', 'Traits': ['Brave', 'Curious']})
        print(schema.get_character('Alice'))
        print(schema.get_characters())
        schema.remove_character('Alice')

        # Scene Handlers
        schema.add_scene('Chapter 1', {'Section_Title': 'Intro', 'Setting': 'Forest', 'Characters': ['Alice']})
        print(schema.get_scene('Chapter 1'))
        print(schema.get_scenes())
        schema.remove_scene('Chapter 1')

        # Place Handlers
        schema.add_place(None, {'Place': 'Forest', 'Description': 'Dark and spooky', 'Significance': 'Initial setting'})
        print(schema.get_place(0))
        print(schema.get_places())
        schema.remove_place(0)

        # Retrieve the entire schema
        print(schema.get_schema())

        # Retrieve a specific subschema, e.g., 'Character'
        print(schema.get_character_schema())
    """
    def __init__(self, schema, plural_names=None):
        """
        Initializes the Schema class with a given schema structure.

        Parameters:
            schema (dict, optional): A dictionary that describes the expected structure for each element in the schema.
            plural_names (dict, optional): A dictionary that maps singular schema keys to their plural forms.

        Attributes:
            schema (dict): Stores the provided schema structure.
            data (dict): Initializes an empty dictionary to hold the actual data for the schema elements.

        Dynamically Generated Methods:
            add_{subschema}(key, item_dict): Adds an item to the specified subschema.
            get_{subschema}(key): Retrieves an item from the specified subschema by its key.
            get_{subschema}s(): Retrieves all items from the specified subschema.
            get_{subschema}_schema(): Retrieves the specified subschema.
            remove_{subschema}(key): Removes an item from the specified subschema by its key.

        Raises:
            ValueError: If the schema is not provided or is empty.

        Example:
            # Initialize Schema with Character, Scene, and Place subschemas
            my_schema = Schema({
                'Character': {
                    'Name': {'Role': 'String', 'Traits': ['List of Strings']}
                },
                'Scene': {
                    'Chapter_Title': [
                        {'Section_Title': 'String', 'Setting': 'String'}
                    ]
                },
                'Place': [
                    {'Place': 'String', 'Description': 'String', 'Significance': 'String'}
                ]
            })

            # Character Handlers
            # - add_character(key, item_dict)
            # - get_character(key)
            # - get_characters()
            # - remove_character(key)
            # - get_character_schema()

            # Scene Handlers
            # - add_scene(key, item_dict)
            # - get_scene(key, index)  # Optional index for list-based subschema
            # - get_scenes()
            # - remove_scene(key, index)  # Optional index for list-based subschema
            # - get_scene_schema()

            # Place Handlers
            # - add_place(item_dict)  # Note: No key is needed as it's a list
            # - get_place(index)
            # - get_places()
            # - remove_place(index)
            # - get_place_schema()
        """
        try:
            self.validate(schema)
        except (TypeError, ValueError) as e:
            raise ValueError(f"{e} Provided data does not conform to schema. Please refer to Schema.__docs__.")

        self.schema = schema

        self.data = {}
        for key, value in self.schema.items():
            if isinstance(value, list):
                self.data[key] = []
            elif isinstance(value, dict):
                self.data[key] = {}

        if plural_names is None:
            plural_names = {}

        plural_names = {key: plural_names.get(key, key + "s") for key in self.schema.keys()}

        for subschema in self.schema.keys():
            # Specific schema getter
            setattr(self, f'get_{subschema.lower()}_schema', partial(self.get_schema, subschema))

            # Singular getter
            setattr(self, f'get_{subschema.lower()}', partial(self._get_from_subschema, subschema))

            # Plural getter
            plural = plural_names.get(subschema, subschema + "s")
            setattr(self, f'get_{plural.lower()}', partial(self._get_from_subschema, subschema))

            # Adder
            setattr(self, f'add_{subschema.lower()}', partial(self._add_to_subschema, subschema))

            # Remover
            if isinstance(self.schema[subschema], dict):
                setattr(self, f'remove_{subschema.lower()}', partial(self._remove_from_subschema, subschema))
            elif isinstance(self.schema[subschema], list):
                setattr(self, f'remove_{subschema.lower()}', partial(self._remove_from_subschema, subschema))


    def _add_to_subschema(self, subschema_key, item_key=None, item_dict=None, index=None):
        """
        Private method to add or update an item in a specific subschema.

        Parameters:
            subschema_key (str): The key for the subschema to add the item to.
            item_key (str): The key for the item to add or update.
            item_dict (dict): The dictionary containing the item's data.

        Returns:
            None

        Examples:
            # For a subschema 'Character' that expects a dictionary
            _add_to_subschema('Character', 'John Doe', {'Role': 'Protagonist', 'Traits': ['Brave', 'Smart']})
            # Result: self.data['Character']['John Doe'] = {'Role': 'Protagonist', 'Traits': ['Brave', 'Smart']}

            # For a subschema 'Scene' -> 'Chapter 1' that expects a list
            _add_to_subschema('Scene', 'Chapter 1', {'Section_Title': 'Introduction', 'Setting': 'Forest', 'Characters': ['John Doe']})
            # Result: self.data['Scene']['Chapter 1'].append({'Section_Title': 'Introduction', 'Setting': 'Forest', 'Characters': ['John Doe']})

            # For a subschema 'Place' that expects a list
            _add_to_subschema('Place', {'Place': 'Castle', 'Description': 'Large and foreboding', 'Significance': 'Main setting'})
            # Result: self.data['Place'].append({'Place': 'Castle', 'Description': 'Large and foreboding', 'Significance': 'Main setting'})
        """
        schema_type = self.schema.get(subschema_key)

        if subschema_key not in self.data:
            if isinstance(schema_type, list):
                self.data[subschema_key] = []
            elif isinstance(schema_type, dict):
                self.data[subschema_key] = {}

        current_data = self.data[subschema_key]

        if isinstance(schema_type, list):
            if item_key is None:
                if index is not None:
                    current_data.insert(index, item_dict)
                else:
                    current_data.append(item_dict)
            else:
                if index is not None:
                    current_data.insert(index, {item_key: item_dict})
                else:
                    current_data.append(item_key)
        elif isinstance(schema_type, dict):

            def check_first_item_is_list(my_dict):
                first_key = list(my_dict.keys())[0]
                return isinstance(my_dict[first_key], list)

            if check_first_item_is_list(schema_type):
                if item_key not in current_data:
                    current_data[item_key] = []
                current_data[item_key].append(item_dict)
            else:
                if item_key is not None:
                    if item_key in current_data:
                        current_data[item_key].update(item_dict)
                    else:
                        current_data[item_key] = item_dict

    def _get_from_subschema(self, subschema_key, item_key=None, index=None):
        """
        Retrieves data from a specific subschema. This method is intended for internal use
        and is dynamically called by the getter methods created in the constructor.

        Parameters:
            subschema_key (str): The key for the subschema from which to retrieve data.
            item_key (str, optional): The key for the specific item within the subschema.
                                      If not provided, the entire subschema data is returned.
            index (int, optional): The index of the item in a list-based subschema.
                                    Only applicable if the subschema data is a list.

        Returns:
            dict or list or any: The requested data. If `item_key` is provided, returns the data
                                 for that specific item. If `index` is provided for a list-based
                                 subschema, returns the item at that index. Otherwise, returns
                                 the entire subschema data.

        Examples:
            # Retrieve a specific character as a dictionary
            self._get_from_subschema('Character', 'Alice')

            # Retrieve all characters in a dictionary
            self._get_from_subschema('Character')

            # Retrieve list of scenes in 'Chapter 1'
            self._get_from_subschema('Scene', 'Chapter 1')

            # Retrieve a specific scene from a list of scenes by index
            self._get_from_subschema('Scene', 'Chapter 1', 0)

            # Retrieve a specific place from a list of places by index
            self._get_from_subschema('Place', 0)

            # Retrieve a list all places
            self._get_from_subschema('Place')
        """
        schema_type = self.schema.get(subschema_key)

        current_data = self.data[subschema_key]

        if isinstance(schema_type, dict):
            def check_first_item_is_list(my_dict):
                first_key = list(my_dict.keys())[0]
                return isinstance(my_dict[first_key], list)

            if item_key and index is not None:
                try:
                    subdata = current_data[item_key]
                    return subdata[index]
                except (KeyError, IndexError):
                    return None
            else:
                if check_first_item_is_list(schema_type):
                    return current_data.get(item_key, None) if item_key else current_data
                else:
                	return current_data.get(item_key, {}) if item_key else current_data
        elif isinstance(schema_type, list):
            if item_key is not None:
                try:
                    return current_data[item_key]
                except IndexError:
                    return None
            else:
                return current_data

    def _remove_from_subschema(self, subschema_key, item_key, index=None):
        """
        Private method to remove an item from a specific subschema.

        Parameters:
            subschema_key (str): The key for the subschema to remove the item from.
            item_key (str): The key for the item to remove.
            index (int, optional): The index of the item to remove in a list-based subschema.
                                    Only applicable if the subschema data is a list.

        Returns:
            None

        Raises:
            KeyError: If the item_key does not exist in a dictionary-based subschema.
            IndexError: If the index is out of range in a list-based subschema.

        Notes:
            - If the item_key does not exist in a dictionary-based subschema, a KeyError is raised.
            - If the index is out of range in a list-based subschema, an IndexError is raised.
            - If the item_key does not exist in a list-based subschema, the list remains unchanged (fails silently)

        Examples:
            # For a subschema 'Character' that expects a dictionary
            _remove_from_subschema('Character', 'John Doe')
            # Result: Removes the entry with the key 'John Doe' from self.data['Character']

            # For a subschema 'Scene' that expects a list
            _remove_from_subschema('Scene', 'Chapter 1', 0)
            # Result: Removes the first entry with the key 'Chapter 1' from the list self.data['Scene']['Chapter 1']

            # For a subschema 'Place' that expects a list
            _remove_from_subschema('Place', 0)
            # Result: Removes the first entry from the list self.data['Place']
        """
        if isinstance(self.data[subschema_key], dict):
            if item_key and index is not None:
                self.data[subschema_key][item_key].pop(index)
            else:
                if item_key in self.data[subschema_key]:
                    del self.data[subschema_key][item_key]
        elif isinstance(self.data[subschema_key], list):
            self.data[subschema_key] = [item for i, item in enumerate(self.data[subschema_key]) if i != item_key]


    def get_schema(self, subschema_key=None):
        """
        Retrieves the original schema structure or a specific subschema.

        Parameters:
            subschema_key (str, optional): The key for the subschema to retrieve.
                                           If None, the entire schema is returned.

        Returns:
            dict: The entire schema or the specified subschema.
                  Returns "Subschema not found." if the key doesn't exist.

        Examples:
            get_schema('Character')  # Retrieve the 'Character' subschema
            get_schema()  # Retrieve the entire schema

        Dynamically Generated Examples:
            get_character_schema()  # Retrieve the 'Character' subschema
            get_scene_schema()  # Retrieve the 'Scene' subschema
            get_place_schema()  # Retrieve the 'Place' subschema
        """
        if subschema_key:
            return self.schema.get(subschema_key, "Subschema not found.")
        else:
            return self.schema
