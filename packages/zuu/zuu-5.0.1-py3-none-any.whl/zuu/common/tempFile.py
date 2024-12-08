import functools
import tempfile
import shutil
import os
import glob

def temp(paths=None, capture=None, chcwd : bool = True, err_copy_over : bool = True):
    """
    Decorator that creates a temporary directory and manages file operations.
    
    Args:
        paths (list, optional): List of paths/patterns to copy to temp directory
        capture (list, optional): List of paths/patterns to copy back from temp directory
    
    Returns:
        callable: Decorated function that handles temporary directory operations
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    # Copy files to temp directory
                    if paths:
                        for path in paths:
                            for file in glob.glob(path):
                                if os.path.isfile(file):
                                    shutil.copy2(file, temp_dir)
                    
                    # Execute the wrapped function
                    currCwd = os.getcwd()
                    if chcwd:
                        os.chdir(temp_dir)

                    result = func(*args, **kwargs)
                    if chcwd:
                        os.chdir(currCwd)

                    # Copy files back from temp directory
                    if capture:
                        for pattern in capture:
                            for file in glob.glob(os.path.join(temp_dir, pattern)):
                                if os.path.isfile(file):
                                    shutil.copy2(file, os.getcwd())
                    
                    return result
                except Exception as e:
                    os.chdir(currCwd)
                    os.makedirs("debug", exist_ok=True)
                    if err_copy_over:
                        # move temporary folder contents to a folder called debug
                        shutil.copytree(temp_dir, os.path.join(os.getcwd(), "debug"))
                    raise e
        
        return wrapper
    return decorator