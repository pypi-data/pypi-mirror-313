import inspect
import sys

from bpkio_api.models import *
from graphviz import Digraph
from pydantic import BaseModel

# Collect all Pydantic models in the module
models = [
    obj
    for name, obj in inspect.getmembers(sys.modules[__name__])
    if inspect.isclass(obj) and issubclass(obj, BaseModel)  # and obj != BaseModel
]


def get_inherited_fields(model):
    inherited_fields = set()
    for base in model.__bases__:
        if issubclass(base, BaseModel):
            inherited_fields |= set(base.__fields__.keys())
            inherited_fields |= get_inherited_fields(base)
    return inherited_fields


# Create a directed graph
graph = Digraph(
    "Pydantic Models", node_attr={"shape": "plaintext"}, graph_attr={"rankdir": "BT"}
)

# Add nodes for each model with fields and their types
for model in models:
    inherited_fields = get_inherited_fields(model)
    added_fields = set(model.__fields__.keys()) - inherited_fields
    fields_label = ""
    for field, field_info in model.__fields__.items():
        field_type = field_info.outer_type_.__name__
        if field in added_fields:
            fields_label += f'+ <b>{field}</b>: <i>{field_type}</i><br align="left" />'
        else:
            fields_label += f'{field}: <i>{field_type}</i><br align="left" />'

    model_label = f'<<table border="0" cellborder="1" cellspacing="0"><tr><td><b>{model.__name__}</b></td></tr><tr><td align="text">{fields_label}<br align="left" /></td></tr></table>>'
    graph.node(model.__name__, label=model_label)

# Add edges for model inheritance
for model in models:
    for base in model.__bases__:
        if base in models:
            graph.edge(model.__name__, base.__name__)

# Add edges with a dotted line for field types that are Pydantic models
for model in models:
    for field, field_info in model.__fields__.items():
        field_type = field_info.outer_type_
        if field_type in models:
            graph.edge(
                model.__name__, field_type.__name__, _attributes={"style": "dotted"}
            )


# Save or render the graph
graph.render("models_graph_with_fields_and_types", format="png", cleanup=True)
