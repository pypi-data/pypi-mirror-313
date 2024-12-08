"""Serialization utilities."""

from typing import Any, Protocol, TypeVar, runtime_checkable


@runtime_checkable
class Serializable(Protocol):
    """Protocol for serializable objects."""

    def to_dict(self) -> dict[str, Any]:
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Serializable":
        ...


T = TypeVar("T", bound=Serializable)


def serialize(obj: Any) -> dict[str, Any]:
    """Serialize object to dictionary.

    Args:
        obj: Object to serialize

    Returns:
        Serialized object
    """
    data: dict[str, Any] = {}

    if hasattr(obj, "__dict__"):
        data.update(obj.__dict__)
    elif hasattr(obj, "to_dict"):
        data.update(obj.to_dict())  # type: ignore
    else:
        data = {"value": obj}

    return data


def deserialize(data: dict[str, Any], cls: type[T]) -> T:
    """Deserialize dictionary to object.

    Args:
        data: Dictionary to deserialize
        cls: Target class that implements Serializable protocol

    Returns:
        Deserialized object

    Raises:
        TypeError: If cls doesn't implement Serializable protocol
    """
    if not hasattr(cls, "from_dict"):
        raise TypeError(f"Class {cls.__name__} must implement from_dict method")

    return cls.from_dict(data)  # type: ignore
