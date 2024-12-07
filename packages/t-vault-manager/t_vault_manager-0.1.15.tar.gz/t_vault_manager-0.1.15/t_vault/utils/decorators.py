def singleton(cls):
    """Creates a singleton pattern for a class.

    Returns:
        The singleton instance of the class.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
