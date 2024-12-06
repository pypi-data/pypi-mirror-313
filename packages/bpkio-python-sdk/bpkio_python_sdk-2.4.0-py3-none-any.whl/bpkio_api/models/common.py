import inspect
from typing import Any, Dict, Optional

from pydantic import BaseModel


class NamedModel(BaseModel):
    name: str


class BaseResource(BaseModel):
    id: int

    @property
    def summary(self):
        return summary(self, True)


class WithDescription(BaseModel):
    description: Optional[str] = None


class PropertyMixin:
    def get_all_fields_and_properties(self) -> Dict[str, Any]:
        all_data = self.dict()

        for name, attribute in inspect.getmembers(self.__class__):
            if isinstance(attribute, property):
                all_data[name] = getattr(self, name)

        return all_data


def summary(model: BaseModel, with_class=False):
    id_parts = []
    if with_class:
        id_parts.append(model.__class__.__name__)
    if hasattr(model, "id"):
        id_parts.append(str(model.id))

    return "({}) {}".format(".".join(id_parts), getattr(model, "name", ""))
