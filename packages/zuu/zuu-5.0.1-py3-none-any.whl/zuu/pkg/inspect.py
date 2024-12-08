import typing
import inspect
import os


def typing_literal_generator(*args: typing.Tuple[str]):
    """
    Generate a typing.Literal type from the provided arguments.

    This function takes a variable number of string arguments and generates a
    typing.Literal type that represents the union of those string literals.
    It is a convenient way to create a Literal type without having to manually
    enumerate all the possible values.

    Args:
        *args: A variable number of string arguments to include in the Literal type.

    Returns:
        A typing.Literal type that represents the union of the provided string arguments.
    """
    oneliner = ",".join(f'"{arg}"' for arg in args)

    local = {"typing": typing}
    exec(f"x = typing.Literal[{oneliner}]", local, local)

    return local["x"]


def get_self_name() -> str:
    """
    Get the name of the calling function.

    This function uses the `inspect` module to get the name of the function that called the current function. It is useful for logging or debugging purposes, where you want to know the name of the function that is currently being executed.

    Returns:
        str: The name of the calling function.
    """

    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    calname = calframe[1][3]
    return calname


def get_caller_info() -> dict:
    """
    Get the name of the caller function, including the file, class, instance, and function name.

    Returns:
        dict: A dictionary representing the caller's file, class (if any), instance (if any), and function name.
    """
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)

    # Get the caller's frame
    caller_frame = calframe[2].frame

    # Get the caller's function name
    caller_func_name = caller_frame.f_code.co_name

    # Get the caller's file name (without the full path)
    caller_file_name = os.path.basename(caller_frame.f_code.co_filename)

    caller_info = {"file": caller_file_name, "class": None, "method": caller_func_name}

    # Check for 'self' (instance method) or 'cls' (class method)
    if "self" in caller_frame.f_locals:
        caller_info["class"] = caller_frame.f_locals["self"].__class__.__name__
    elif "cls" in caller_frame.f_locals:
        caller_info["class"] = caller_frame.f_locals["cls"].__name__

    # Check for static method by looking at the globals for a class name
    if caller_info["class"] is None:
        for name, obj in caller_frame.f_globals.items():
            if isinstance(obj, type) and caller_func_name in obj.__dict__:
                caller_info["class"] = name
                break

    return caller_info


def get_caller_instance():
    """
    Get the instance or module that called this function based on get_caller_info.
    """
    caller_info = get_caller_info()
    caller_frame = inspect.currentframe().f_back.f_back

    # Check for 'self' (instance method) or 'cls' (class method)
    if "self" in caller_frame.f_locals:
        return caller_frame.f_locals["self"]
    elif "cls" in caller_frame.f_locals:
        return caller_frame.f_locals["cls"]

    # Check for module-level function
    if caller_info["class"] is None:
        for name, obj in caller_frame.f_globals.items():
            if isinstance(obj, type) and caller_info["method"] in obj.__dict__:
                return obj

    return None


__all__ = [
    "typing_literal_generator",
    "get_self_name",
    "get_caller_info",
    "get_caller_instance",
]
