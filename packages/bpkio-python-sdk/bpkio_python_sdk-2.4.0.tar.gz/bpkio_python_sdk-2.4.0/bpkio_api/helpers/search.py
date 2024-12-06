import re
from enum import Enum
from typing import Any, List, Tuple


class SearchMethod(Enum):
    STRICT = "strict"
    STRING_MATCH = "string"
    STRING_SUB = "partial"


def search_array_with_filters(
    arr: List,
    filters: List[Tuple[str, str | None, SearchMethod]] | None = None,
) -> List:
    results = arr

    # Define a helper function for the different search methods
    def match_search_method(value: Any, target: Any, method: SearchMethod) -> bool:
        if method == SearchMethod.STRICT:
            return value == target
        elif method == SearchMethod.STRING_MATCH:
            tgt = target.value if isinstance(target, Enum) else str(target)
            return str(value).lower() == tgt.lower()
        elif method == SearchMethod.STRING_SUB:
            return re.search(str(value), str(target), flags=re.IGNORECASE) is not None
        else:
            return False

    # Iterate through search filters
    for value, field, method in filters:
        # TODO - support other methods
        results = [
            i
            for i in results
            if (
                field
                and hasattr(i, field)
                and match_search_method(value, getattr(i, field), method)
            )
            or (
                not field
                and any(
                    match_search_method(value, getattr(i, f), method) for f in i.dict()
                )
            )
        ]

    return results
