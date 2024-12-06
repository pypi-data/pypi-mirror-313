def attr_get(attr: str):
    def getter(obj):
        try:
            return getattr(obj, attr)
        except AttributeError:
            return None
    return getter

class Sense:
    x = attr_get("x")
    y = attr_get("y")
    enabled = attr_get("enabled")