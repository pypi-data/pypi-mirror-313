def dataclass_from_dict(klass, dikt):
    """Convert dictionary to dataclass."""
    try:
        field_types = klass.__annotations__
        return klass(**{f: dataclass_from_dict(field_types[f], dikt[f]) for f in dikt})
    except AttributeError:
        if isinstance(dikt, tuple | list):
            return [dataclass_from_dict(klass.__args__[0], f) for f in dikt]
        return dikt
