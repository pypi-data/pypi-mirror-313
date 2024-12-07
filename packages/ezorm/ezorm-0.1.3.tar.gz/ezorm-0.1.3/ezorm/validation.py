from ezorm.variables import EzORM
from typing import Type, Any

def isinstance_ezorm(obj:Type[EzORM]):
    if not isinstance(obj, EzORM):
        raise ValueError(f"Expected a subclass of EzORM, but got {obj}")
    
def issubclass_ezorm(obj:Type[EzORM]):
    if not issubclass(obj, EzORM):
        raise ValueError(f"Expected a subclass of EzORM, but got {obj}")