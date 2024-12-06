#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thread handler to create and start threads"""

from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from typing import Any, Callable, List, Tuple


class ThreadManager:
    """
    Class to manage threads and tasks
    """

    def __init__(self, max_workers: int = 20):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.futures = []

    def submit_task(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        """
        Submit a task to the executor

        :param Callable func: Function to execute
        :param Any args: Arguments to pass to the function
        :param Any kwargs: Keyword arguments to pass to the function
        :rtype: None
        """
        future = self.executor.submit(func, *args, **kwargs)
        self.futures.append(future)

    def submit_tasks_from_list(self, func: Callable, items: List[Any], *args: Any, **kwargs: Any) -> None:
        """
        Submit multiple tasks to the executor, used for a list of items

        :param Callable func: Function to execute
        :param List[Any] items: List of items to process
        :param Any args: Arguments to pass to the function
        :param Any kwargs: Keyword arguments to pass to the function
        :rtype: None
        """
        for item in items:
            self.submit_task(func, item, *args, **kwargs)

    def execute_and_verify(
        self, timeout: int = None, check_for_failures: bool = True, terminate_after: bool = False
    ) -> List[Tuple[bool, Any]]:
        """
        Execute the tasks and verify if they were successful

        :param int timeout: Timeout for the tasks
        :param bool check_for_failures: Whether to check for failures, default True
        :return: List of tuples with a boolean indicating success and the result
        :rtype: List[Tuple[bool, Any]]
        """
        results = []
        try:
            for future in as_completed(self.futures, timeout=timeout):
                try:
                    result = future.result()
                    results.append((True, result))
                except TimeoutError:
                    results.append((False, "Task timed out"))
                except Exception as e:
                    results.append((False, str(e)))
        finally:
            if terminate_after:
                self.shutdown()
        if check_for_failures:
            import logging

            logger = logging.getLogger(__name__)
            for success, result in results:
                if not success:
                    logger.error(f"Task failed with error: {result}")
        return results

    def shutdown(self, wait: bool = True) -> None:
        """
        Shutdown the executor

        :param bool wait: Whether to wait for the tasks to complete
        :rtype: None
        """
        self.executor.shutdown(wait=wait)


def create_threads(process: Callable, args: Tuple, thread_count: int) -> None:
    """
    Function to create x threads using ThreadPoolExecutor

    :param Callable process: function for the threads to execute
    :param Tuple args: args for the provided process
    :param int thread_count: # of threads needed
    :rtype: None
    """
    # set max threads
    from regscale.core.app.application import Application

    app = Application()
    max_threads = app.config["maxThreads"]
    if threads := min(thread_count, max_threads):
        # start the threads with the number of threads allowed
        with ThreadPoolExecutor(max_workers=threads) as executor:
            # iterate and start the threads that were requested
            for thread in range(threads):
                # assign each thread the passed process and args along with the thread number
                executor.submit(process, args, thread)


def thread_assignment(thread: int, total_items: int) -> list:
    """
    Function to iterate through items and returns a list the
    provided thread should be assigned and use during its execution

    :param int thread: current thread number
    :param int total_items: Total # of items to process with threads
    :return: List of items to process for the given thread
    :rtype: list
    """
    from regscale.core.app.application import Application

    app = Application()
    # set max threads
    max_threads = app.config["maxThreads"]

    return [x for x in range(total_items) if x % max_threads == thread]
