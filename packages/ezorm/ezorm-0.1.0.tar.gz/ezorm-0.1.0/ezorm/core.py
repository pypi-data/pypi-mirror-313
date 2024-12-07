from pydantic import BaseModel
from typing import Any

# Define a custom metaclass to handle field registration and validation
class ModelMeta(type(BaseModel)):  # Inherit from the BaseModel's metaclass
    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)

        # Store fields and their types in the class, using annotations
        fields = {}
        for key, value in dct.get('__annotations__', {}).items():
            # fields[key] = value # this is original code looks like
            fields[key] = key # manually fixing this to key because I want to use the functionality in the ORM class
        new_class._fields = fields
        
        # Also store field types on the class itself
        for field in fields:
            setattr(new_class, field, fields[field])

        return new_class

# Extended BaseModel to handle dynamic behavior for field access
class EzORM(BaseModel, metaclass=ModelMeta):
    __table__:str = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Set the table name to the lowercase name of the class
        cls.__table__ = cls.__name__.lower()
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initialize as per Pydantic's logic
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, item: str) -> Any:
        # Return the type of the field if accessed at class level
        if item in self._fields:
            if isinstance(self, type(self)):  # Class-level access
                return self._fields[item]  # Return field type
            else:  # Instance-level access
                return getattr(self, item, None)  # Return the field value
        
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")