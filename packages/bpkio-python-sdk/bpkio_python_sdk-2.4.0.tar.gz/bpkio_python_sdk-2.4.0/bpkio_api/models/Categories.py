from typing import List

from bpkio_api.models.common import BaseResource, NamedModel
from pydantic import BaseModel


class SubCategory(BaseModel):
    key: str
    value: str


class CategoryIn(NamedModel):
    subcategories: List[SubCategory] = []

    @property
    def subcategories_list(self):
        return ", ".join(f"{sc.key}:{sc.value}" for sc in self.subcategories)


class Category(BaseResource, CategoryIn):
    pass
