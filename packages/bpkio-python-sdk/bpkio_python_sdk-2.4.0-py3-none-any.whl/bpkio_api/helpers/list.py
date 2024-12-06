from typing import Callable, List


def get_all_with_pagination(get_fn: Callable, **kwargs):
    """Convenience function to retrieve all resources from an endpoint that supports pagination.

    Args:
        get_fn (Callable): The function that retrieves a page of items.
            It must have parameters `offset` and `limit`

    Returns:
        List: the full list of resources
    """
    items = []

    offset = 0
    limit = 50

    while True:
        page = get_fn(offset=offset, limit=limit, **kwargs)  # type: ignore
        items.extend(page)
        if len(page) < limit:
            return items
        else:
            offset = offset + limit


def collect_from_ids(ids: List[int], get_fn: Callable):
    arr = []
    for id in ids:
        resource = get_fn(id)
        arr.append(resource)
    return arr

