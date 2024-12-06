from typing import Any

def get_properties_dict(instance) -> dict[str: Any]:
    """Provide a class instance and receive its property (not attribute) names & values.
    Useful because __dict__ only returns attribute names & values"""
    cls = type(instance)
    properties = {name: getattr(instance, name) for name, value in cls.__dict__.items() if isinstance(value, property)}
    return properties

def get_attrs_and_props(instance) -> dict[str: Any]:
    return instance.__dict__ | get_properties_dict(instance)