from bpkio_api.models.common import BaseResource
from pydantic import BaseModel


def edit_property(resource: BaseModel, property_key: str, value: object):
    """A function that allows changing the value of a single property in a pydantic object, possibly nested.
    Dot notation can be used to define the path to the property.

    Special features:
    - Fuzzy matching applies to the property names.
    - If the property is inside a nested object that does not exist, we attempt to create it.
    - If the property is a BaseResource, we assume the value is the ID of the resource to link to.
    """
    previous_value = None
    anchor_property_for_new_model = None
    new_model_flag = False

    def _fuzzy_search_through_properties(o, key):
        model_properties = o.__fields__
        # fuzzy search through the keys
        search_term = key.lower()
        matching_keys = [k for k in model_properties.keys() if search_term in k.lower()]

        if not len(matching_keys):
            raise KeyError(f"Property '{property_key}' not found")
        if len(matching_keys) > 1:
            raise KeyError(
                f"Ambiguous property '{property_key}': matches {', '.join(matching_keys)}"
            )
        # TODO - what if multiple match?
        return matching_keys[0], model_properties[matching_keys[0]].type_

    # traverse the model to the property to modify
    keys = property_key.split(".")
    o = resource
    traversed_models = [resource]
    property_path = []
    for i, key in enumerate(keys[:-1]):
        traversed_models.append(o)
        matching_key, model_type = _fuzzy_search_through_properties(o, key)
        property_path.append(matching_key)
        o = getattr(o, matching_key)

        if not issubclass(model_type, BaseModel):
            raise KeyError(
                f"Property '{property_key}' cannot be updated (not a Pydantic object)"
            )

        # Create model for null properties that should contain models
        if o is None:
            new_model_flag = True
            anchor_property_for_new_model = traversed_models[-1]

            new_model_data_root = {}
            new_model_data_next_level = new_model_data_root
            new_model_construct = model_type.construct({})
            # we loop through the remaining keys to build the skeleton of the subobjects
            for k in keys[i + 1 :]:
                sub_k, sub_type = _fuzzy_search_through_properties(
                    new_model_construct, k
                )
                if issubclass(sub_type, BaseModel):
                    new_model_data_next_level[sub_k] = {}
                    # and in case it's the last key, but it's a BaseResource, we assume the value is the ID
                    if (
                        k == keys[-1]
                        and issubclass(sub_type, BaseResource)
                        and value != "__NULL__"
                    ):
                        new_model_data_next_level[sub_k] = {"id": int(value)}

                    new_model_construct = sub_type.construct({})
                    new_model_data_next_level = new_model_data_next_level[sub_k]
                else:
                    new_model_data_next_level[sub_k] = sub_type(value)

            # Then we attempt to build it and add it
            o = model_type.parse_obj(new_model_data_root)
            setattr(anchor_property_for_new_model, property_path[-1], o)

    # retrieve the leaf property
    matching_key, property_type = _fuzzy_search_through_properties(o, keys[-1])
    property_path.append(matching_key)

    # special situation: if property is a nested object with id, attempt to use the value as id
    if issubclass(property_type, BaseResource):
        parent = o
        o = getattr(o, matching_key, None)
        # if it doesn't exist, we create it
        if o is None:
            o = property_type(id=int(value))
            setattr(parent, property_path[-1], o)

        matching_key = "id"
        property_path.append("id")
        property_type = int

    previous_value = getattr(o, matching_key, None) if not new_model_flag else "(empty)"

    if value == "__NULL__" or value == "null" or value == "None":
        setattr(o, matching_key, None)
        print(
            f"Removed {'.'.join(property_path)} (set to null)\n  previous value: {previous_value}",
        )
    else:
        # Cast the value to the appropriate type
        try:
            if issubclass(property_type, BaseModel):
                value = property_type.parse_obj(value)
            else:
                value = property_type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Cannot cast value '{value}' to type {property_type}: {e}"
            )

        # modify the property
        # if not o and isinstance(o, BaseModel):
        setattr(o, matching_key, value)
        print(
            f"Updated property '{'.'.join(property_path)}' to {value}\n - previously: {previous_value}",
        )

    return resource
