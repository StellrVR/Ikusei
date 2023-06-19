from __future__ import annotations
from typing import Optional, TypeVar

T = TypeVar('T')

def unwrap(x: Optional[T]) -> T:
    if x is None:
        raise ValueError("Found none.")
    return x