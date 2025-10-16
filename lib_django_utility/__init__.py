def get_attribute(object, name, default=None, split_by="."):
    related_names = name.split(split_by)
    obj = object
    for index, related_name in enumerate(related_names):
        obj = getattr(obj, related_name, None)
        if callable(obj) and not hasattr(obj, "get_queryset"):
            obj = obj()
        if obj is None:
            break

    if obj is None:
        return default
    return obj
