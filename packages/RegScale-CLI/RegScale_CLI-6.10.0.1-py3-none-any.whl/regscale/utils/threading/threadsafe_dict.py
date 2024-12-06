"""
This module contains the ThreadSafeDict class, which is a thread-safe dictionary.
"""

from threading import RLock
from typing import Any, Optional, List, Callable, Iterator


class ThreadSafeDict:
    """
    ThreadSafeDict class to create a thread-safe dictionary.
    """

    def __init__(self):
        self._dict: dict = {}
        self._lock = RLock()

    def __getitem__(self, key: Any) -> Any:
        """
        Get a value from the thread-safe dictionary

        :param Any key: Key to get the value for
        :return: The value from the dictionary
        :rtype: Any
        """
        with self._lock:
            return self._dict[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set a key-value pair in the thread-safe dictionary

        :param Any key: Key to set
        :param Any value: Value to set
        :rtype: None
        """
        with self._lock:
            self._dict[key] = value

    def __delitem__(self, key: Any) -> None:
        """
        Delete a key from the thread-safe dictionary

        :param Any key: Key to delete
        :rtype: None
        """
        with self._lock:
            del self._dict[key]

    def get(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        """
        Get a value from the thread-safe dictionary

        :param Any key: Key to get the value for
        :param Optional[Any] default: Default value to return if the key is not in the dictionary, defaults to None
        :return: The value from the dictionary, if found or the default value
        :rtype: Optional[Any]
        """
        with self._lock:
            return self._dict.get(key, default)

    def pop(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        """
        Pop a value from the thread-safe dictionary

        :param Any key: Key to pop the value for
        :param Optional[Any] default: Default value to return if the key is not in the dictionary, defaults to None
        :return: The value from the dictionary, if found or the default value
        :rtype: Optional[Any]
        """
        with self._lock:
            return self._dict.pop(key, default)

    def __contains__(self, key: Any) -> bool:
        """
        Check if a key is in the thread-safe dictionary

        :param Any key: Key to check in the dictionary
        :return: Whether the key is in the dictionary
        :rtype: bool
        """
        with self._lock:
            return key in self._dict

    def keys(self) -> List[Any]:
        """
        Get a list of keys from the thread-safe dictionary

        :return: A list of keys
        :rtype: List[Any]
        """
        with self._lock:
            return list(self._dict.keys())

    def values(self) -> List[Any]:
        """
        Get a list of values from the thread-safe dictionary

        :return: A list of values
        :rtype: List[Any]
        """
        with self._lock:
            return list(self._dict.values())

    def items(self) -> List[tuple]:
        """
        Get a list of items from the thread-safe dictionary

        :return: A list of items
        :rtype: List[Any]
        """
        with self._lock:
            return list(self._dict.items())

    def clear(self) -> None:
        """
        Clear the thread-safe dictionary

        :rtype: None
        """
        with self._lock:
            self._dict.clear()

    def update(self, other_dict: dict) -> None:
        """
        Update the thread-safe dictionary with another dictionary

        :param dict other_dict: Dictionary to update the thread-safe dictionary with
        :rtype: None
        """
        with self._lock:
            self._dict.update(other_dict)

    def __len__(self) -> int:
        """
        Get the length of the thread-safe dictionary

        :return: The length of the dictionary
        :rtype: int
        """
        with self._lock:
            return len(self._dict)

    def __iter__(self) -> Iterator[Any]:
        """
        Return an iterator over the keys of the dictionary.

        :return: An iterator over the keys of the dictionary
        :rtype: Iterator[Any]
        """
        with self._lock:
            # Create a copy of the keys to prevent issues during iteration
            return iter(self._dict.copy())

    def setdefault(self, key: Any, default: Any = None) -> Any:
        with self._lock:
            return self._dict.setdefault(key, default)


class ThreadSafeDefaultDict(ThreadSafeDict):
    """
    ThreadSafeDefaultDict class to create a thread-safe defaultdict.
    """

    def __init__(self, default_factory: Optional[Callable[[], Any]] = None):
        """
        Initialize a ThreadSafeDefaultDict.

        :param Optional[Callable[[], Any]] default_factory: A callable that returns the default value for missing keys
        """
        super().__init__()
        if default_factory is not None and not callable(default_factory):
            raise TypeError("default_factory must be callable")
        self.default_factory: Optional[Callable[[], Any]] = default_factory

    def __getitem__(self, key: Any) -> Any:
        """
        Get an item from the dictionary, using the default_factory if the key is missing.

        :param Any key: The key to look up
        :return: The value associated with the key or the default value
        :rtype: Any
        """
        with self._lock:
            try:
                return self._dict[key]
            except KeyError:
                if self.default_factory is None:
                    raise
                else:
                    value = self.default_factory()
                    self._dict[key] = value
                    return value

    def get(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        """
        Get an item from the dictionary, using the default_factory or provided default if the key is missing.

        :param Any key: The key to look up
        :param Optional[Any] default: The default value to return if the key is not found and default_factory is None
        :return: The value associated with the key or the default value
        :rtype: Optional[Any]
        """
        with self._lock:
            if key in self._dict:
                return self._dict[key]
            elif self.default_factory is not None:
                value = self.default_factory()
                self._dict[key] = value
                return value
            else:
                return default

    def setdefault(self, key: Any, default: Optional[Any] = None) -> Any:
        """
        Insert key with a value of default if key is not in the dictionary.

        :param Any key: The key to insert if it doesn't exist
        :param Optional[Any] default: The value to set if the key doesn't exist
        :return: The value for key if key is in the dictionary, else default
        :rtype: Any
        """
        with self._lock:
            if key in self._dict:
                return self._dict[key]
            else:
                if default is None and self.default_factory is not None:
                    default = self.default_factory()
                self._dict[key] = default
                return default

    def __repr__(self) -> str:
        """
        Return a string representation of the ThreadSafeDefaultDict.

        :return: A string representation of the object
        :rtype: str
        """
        return f"{self.__class__.__name__}({self.default_factory}, {self._dict})"
