"""
This module contains the ThreadSafeList class, which is a thread-safe list.
"""

from threading import Lock
from typing import Any


class ThreadSafeList:
    """
    ThreadSafeList class to create a thread-safe list.
    """

    def __init__(self):
        self._list = list()
        self._lock = Lock()

    def __getitem__(self, item: int) -> Any:
        """
        Get an item from the list

        :param int item: Index of the item to get
        :return: The item from the list
        :rtype: Any
        """
        with self._lock:
            return self._list[item]

    def __len__(self) -> int:
        """
        Get the length of the list

        :return: The length of the list
        :rtype: int
        """
        with self._lock:
            return len(self._list)

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Set an item in the list

        :param int index: Index of the item to set
        :param Any value: Value to set
        :rtype: None
        """
        with self._lock:
            self._list[index] = value

    def append(self, value: Any) -> None:
        """
        Append a value to the list

        :param Any value: Value to append to the list
        :rtype: None
        """
        with self._lock:
            self._list.append(value)

    def pop(self) -> Any:
        """
        Pop a value from the list

        :return: The value from the list
        :rtype: Any
        """
        with self._lock:
            return self._list.pop()

    def get(self, index: int) -> Any:
        """
        Get a value from the list with the given index

        :param int index: Index of the value to get
        :return: The value from the list
        :rtype: Any
        """
        return self.__getitem__(index)

    def length(self) -> int:
        """
        Get the length of the list

        :return: The length of the list
        :rtype: int
        """
        return self.__len__()
