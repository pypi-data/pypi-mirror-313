from collections import defaultdict


def find_duplicates_of(obj, in_list, by_fields):
    groups = defaultdict(list)
    for o in [obj, *in_list]:
        key = tuple(getattr(o, field, None) for field in by_fields)
        groups[key].append(o)

    # Get duplicates for that input object
    duplicates = [group for group in groups.values() 
                  if len(group) > 1
                  and obj in group]
    
    return duplicates