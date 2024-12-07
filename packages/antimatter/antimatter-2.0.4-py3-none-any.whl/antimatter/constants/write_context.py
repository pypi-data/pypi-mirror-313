from enum import Enum


class WriteContextHookMode(str, Enum):
    """
    Class representing the mode of the WriteContextHook.
    """

    Sync = "sync"
    Async = "async"
