from typing import List

from pydantic import BaseModel

from drax_sdk.utils.timestamp import unix_timestamp


class Value(BaseModel):
    name: str
    value: str


class BaseValueObject(BaseModel):
    values: List[Value] = []

    def all_names(self):
        return [value.name for value in self.values]

    def all_values(self):
        return self.values

    def get_value(self, name: str):
        for value in self.values:
            if value.name == name:
                return value.value
        return None

    def set_value(self, name: str, value: str):
        for val in self.values:
            if val.name == name:
                val.value = value
                return
        self.values.append(Value(name=name, value=value))

    def remove_value(self, name: str):
        self.values = [value for value in self.values if value.name != name]

    def clear_values(self):
        self.values.clear()

    @classmethod
    def from_dict(cls, map: dict):
        return cls(
            timestamp=unix_timestamp(),
            values=[Value(name=k, value=str(v)) for k, v in map.items()],
        )

    def to_dict(self):
        return {value.name: value.value for value in self.values}

    @staticmethod
    def merge(*measures):
        merged = BaseValueObject(values=[])
        for measure in measures:
            if measure is not None:
                for value in measure.values:
                    merged.set_value(value.name, value.value)
        return merged


class NodeEntry(BaseValueObject):
    node_id: str | None = None
    timestamp: int | None = None
