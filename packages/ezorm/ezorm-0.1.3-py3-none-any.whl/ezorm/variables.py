from pydantic import BaseModel, Field
from typing import Optional, Type, get_args
from ezorm.utils import data_mapping, print_table

def get_dtype_from_annotation(annotation):
    if str(Optional) in str(annotation):
        return get_args(annotation)[0]
    return annotation

class EzORMMeta(type(BaseModel)):
    """This is a metaclass to create __table__ that will be used in later step
    Args:
        name (str) : the input class name
        bases (any) : abc
        dct (dict) : this is the annotation of pydantic BaseModel
        table (str) : a specified table name

    Note:
        This will be inspected and debugged later.
    """
    def __new__(cls, name:str, bases, dct:dict, table:str=None):
        new_class = super().__new__(cls, name, bases, dct)
        setattr(new_class, "__table__", table if table else name.lower())
        return new_class

class EzORM(BaseModel, metaclass=EzORMMeta):
    """This is a base class for EzORM"""
    @classmethod
    def to_prompt(cls):
        dtypes = data_mapping(engine='prompt')
        table = cls.__table__
        table_description = cls.__doc__

        prompt = []
        prompt.append(f"Table: {table}")
        prompt.append(f"Description: {table_description}")
        prompt.append(f"Columns:")
        for name, detail in cls.model_fields.items():
            annotation = detail.annotation
            dtype = get_dtype_from_annotation(annotation)
            column_description = detail.description
            prompt.append(f"\t- {name} ({dtypes[dtype]}): {column_description}")

        return "\n".join(prompt)
    
    @classmethod
    def data_dict(cls):
        table_name = cls.__table__
        table_description = cls.__doc__ or "Unspecified"
        headers = ["column", "dtype", "description"]
        rows = []
        columns = []
        for name, detail in cls.model_fields.items():
            dtypes = data_mapping(engine="duck")
            annotation = detail.annotation
            dtype = get_dtype_from_annotation(annotation)
            description = detail.description
            rows.append([name, dtypes[dtype], description])
            columns.append({
                "name":name,
                "dtype":dtypes[dtype],
                "description": description
            })

        _ = print_table(table_name, table_description, headers, rows)
        
        return {
            "table": table_name,
            "description": table_description,
            "columns": columns
        }
    
def EzField(description, default=None, default_factory=None):
    """
    Note:
        It will have features for create ez table:
            pk, fk, mandatory, validate value, default value in the future
    """
    inputs = {
        "description": description,
        "default": default,
        "default_factory": default_factory,
    }
    return Field(**inputs)