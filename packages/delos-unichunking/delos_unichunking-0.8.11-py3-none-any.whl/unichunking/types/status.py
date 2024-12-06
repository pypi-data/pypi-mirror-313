"""Surveil the status of a file processing task."""

from typing import Any

from unichunking.utils import logger


class TaskStatus:
    """Data class for storing task status information."""

    def __init__(
        self: "TaskStatus",
        task: str,
        progress: int = 0,
    ) -> None:
        """Initializes the TaskStatus object."""
        self.task = task
        self.progress = progress

    async def update_status(
        self: "TaskStatus",
        progress: int,
        start: int = 0,
        end: int = 100,
    ) -> None:
        """Update the progress of a TaskStatus object with a logging statement."""
        self.progress = (
            start if end == start else int(start + (progress / 100) * (end - start))
        )
        logger.debug(f'Task "{self.task}" updated progress to {self.progress}.')


class StatusManager:
    """Data class to handle status management."""

    def __init__(
        self: "StatusManager",
        status: Any = None,
        update_status_function: Any = None,
        task: str = "",
        start: int = 0,
        end: int = 100,
    ) -> None:
        """Initializes the StatusManager object."""
        if status and update_status_function:
            self.status = status
            self.update_status = update_status_function
        else:
            self.status = TaskStatus(task)
            self.update_status = self.status.update_status
        self.start = start
        self.end = end
