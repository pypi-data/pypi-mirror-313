from importlib.metadata import version


def get_user_agent() -> str:
    """
    Get the user agent for the python client API requests.
    """
    return f"antimatter/python-client/{version('antimatter')}"
