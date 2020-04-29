import collections
from typing import List
from pydantic import validator

from .basemodel import BaseModel

def find_dup_items(values: List) -> List:
    """Find duplicate items in a list."""
    dup = [t for t, c in collections.Counter(values).items() if c > 1]
    return dup

class IOItem(BaseModel):

    name: str


class IOBase(BaseModel):

    parameters: List[IOItem]

    artifacts: List[IOItem]

    @classmethod
    @validator('parameters', 'artifacts')
    def parameter_unique_names(cls, v):
        names = [value.name for value in v]
        duplicates = find_dup_items(names)
        if len(duplicates) != 0:
            raise ValueError(f'Duplicate names: {duplicates}')
        return v

    @staticmethod
    def _by_name(
        input_list: list,
        name: str, 
    ):
        res = list(filter(lambda x: x.name == name, input_list))
        if res == []:
            raise KeyError(f'no input with name {name} exists')
        
        return res[0]

    def artifact_by_name(self, name: str):
        return self._by_name(self.artifacts, name)

    def parameter_by_name(self, name: str):
        return self._by_name(self.parameters, name)