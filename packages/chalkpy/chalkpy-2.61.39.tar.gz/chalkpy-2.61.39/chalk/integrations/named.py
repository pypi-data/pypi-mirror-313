import json
import os
from typing import Any, Callable, Optional, TypeVar, overload

T = TypeVar("T")


def has_integration(integration_name: str) -> bool:
    encoded = os.getenv("_CHALK_AVAILABLE_INTEGRATIONS")
    if encoded is not None:
        available = set(json.loads(encoded))
        return integration_name in available
    return False


@overload
def load_integration_variable(
    name: str,
    integration_name: Optional[str],
) -> Optional[str]:
    ...


@overload
def load_integration_variable(name: str, integration_name: Optional[str], parser: Callable[[str], T]) -> Optional[T]:
    ...


def load_integration_variable(
    name: str,
    integration_name: Optional[str],
    parser: Callable[[str], Any] = str,
) -> Optional[Any]:
    value = None
    if integration_name is None:
        value = os.getenv(name)
    else:
        value = os.getenv(f"{integration_name}_{name}")

    return parser(value) if value is not None else None
