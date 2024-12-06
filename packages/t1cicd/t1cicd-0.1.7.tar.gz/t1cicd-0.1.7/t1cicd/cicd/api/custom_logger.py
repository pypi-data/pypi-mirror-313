"""
Custom Logger
=============

This module provides a thread-safe logging utility to collect and manage logs in memory.

Classes:
    - CustomLogger: A thread-safe logger that stores logs in a shared list.
"""

import threading


class CustomLogger:
    """
    A thread-safe logger for storing and retrieving logs in memory.

    Attributes:
        logs (list): A shared list that stores log messages.
        lock (threading.Lock): A lock to ensure thread-safe access to the `logs` list.

    Methods:
        add(message): Adds a new log message to the logger.
        reset(): Clears all log messages.
        get(): Retrieves all log messages as a single string.
    """

    logs = []
    lock = threading.Lock()

    @staticmethod
    def add(message: str):
        """
        Adds a new log message to the logger.

        This method is thread-safe and uses a lock to ensure that concurrent writes
        do not cause data corruption.

        Args:
            message (str): The log message to add.
        """
        with CustomLogger.lock:
            CustomLogger.logs.append(message)

    @staticmethod
    def reset():
        """
        Clears all log messages.

        This method is thread-safe and uses a lock to ensure that concurrent writes
        are handled correctly.
        """
        with CustomLogger.lock:
            CustomLogger.logs = []

    @staticmethod
    def get():
        """
        Retrieves all log messages as a single string.

        This method is thread-safe and uses a lock to ensure that the logs are read
        consistently.

        Returns:
            str: All log messages joined by newline characters.
        """
        with CustomLogger.lock:
            return "\n".join(CustomLogger.logs)
