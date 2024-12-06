import os
import time
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable, List, Type
from t_bug_catcher import attach_file_to_exception
from PIL import ImageGrab


from .config import CONFIG, IS_WINDOWS_OS
from .exceptions import AppCrashException, LoginMethodNotFoundError
from .utils.logger import logger

if IS_WINDOWS_OS:
    from pywinauto.application import ProcessNotFoundError
    from pywinauto.findwindows import ElementAmbiguousError, ElementNotFoundError, WindowNotFoundError
    from pywinauto.timings import TimeoutError
else:
    logger.warning("Not in a Windows Machine, failed to import UI related libraries")


def relogin_and_retry_if_pywin_error(retries: int = 3, delay: int = 1) -> callable:
    """Decorator to relogin and retry if pywin error.

    Args:
        retries (int): Number of times to retry the function.
        delay (int): Delay in seconds between retries.

    Returns:
        Callable: The decorated function with retry logic.
    """
    if retries < 0:
        raise ValueError("Retries must be a non-negative integer.")

    default_exceptions = (
        ElementNotFoundError,
        WindowNotFoundError,
        TimeoutError,
        AppCrashException,
        OSError,
        RuntimeError,
        ProcessNotFoundError,
    )

    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(self: object, *args, **kwargs) -> callable:
            if not hasattr(self, "login") or not callable(getattr(self, "login")):
                raise LoginMethodNotFoundError("The 'login' method is not defined or not callable.")

            for attempt in range(retries + 1):
                try:
                    return func(self, *args, **kwargs)
                except default_exceptions as e:
                    logger.warning(f"Failed to process due to crash: {str(e)}. Retry attempt: {attempt + 1}")
                    if attempt < retries:
                        logger.info("Attempting to re-login.")
                        self.login()
                        time.sleep(delay)
                    else:
                        raise e

        return wrapper

    return decorator


def retry_if_pywin_error(
    retries: int = 3,
    delay: int = 1,
    close_modal: bool = False,
    exceptions: tuple[BaseException] = (),
) -> callable:
    """Decorator to be used in Apps derived classes to retry a function if specified exceptions occur.

    Args:
        retries (int): Number of times to retry the function.
        delay (int): Delay in seconds between retries.
        close_modal (bool): Whether to attempt closing modals on error.
        exceptions (Tuple[Type[BaseException], ...]): Tuple of exceptions to catch and retry on.

    Returns:
        Callable: The decorated function with retry logic.
    """
    # Default exceptions
    default_exceptions = (
        ElementNotFoundError,
        WindowNotFoundError,
        TimeoutError,
        AppCrashException,
        ProcessNotFoundError,
        RuntimeError,
    )
    if retries < 0:
        raise ValueError("Retries must be a non-negative integer.")

    exceptions = exceptions if isinstance(exceptions, tuple) else (exceptions,)
    all_exceptions = default_exceptions + exceptions

    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(self: object, *args, **kwargs) -> callable:
            last_exception = None
            for attempt in range(retries + 1):
                try:
                    result = func(self, *args, **kwargs)
                    return result
                except all_exceptions as e:
                    last_exception = e
                    logger.warning(f"Failed to process due to error: {str(e)}. Retry attempt: {attempt + 1}")
                    if close_modal:
                        if hasattr(self, "close_modal"):
                            self.close_modal()
                        else:
                            self.app.top_window().close()
                    time.sleep(delay)

            if last_exception is not None:
                raise last_exception

        return wrapper

    return decorator


def capture_screenshot_if_pywin_error(
    func: Callable = None,  # Func as default argument to allow use without parenthesis
    exceptions_to_include: List[Type[Exception]] = None,
    output: str = CONFIG.DIRECTORIES.SCREENSHOTS,
) -> Callable:
    """Decorator to capture a screenshot if specific exceptions occur.

    This decorator wraps a function and captures a screenshot when one of the
    specified exceptions is raised. The screenshot will be saved to the output
    directory, and if `ImageGrab` fails, the `RPA.Desktop` module will be used
    as a fallback (if installed).

    Args:
        func (Callable, optional): The function being decorated.
        exceptions_to_include (List[Type[Exception]], optional): A list of exception
            types to trigger the screenshot capture. Defaults to None.
        output (str, optional): Directory path where screenshots will be saved.
            Defaults to `CONFIG.DIRECTORIES.SCREENSHOTS`.

    Returns:
        Callable: The decorated function that captures a screenshot upon specific errors.

    Raises:
        Exception: Re-raises the original exception that triggered the screenshot.
    """
    default_exceptions_to_include = [
        AppCrashException,
        TimeoutError,
        ElementNotFoundError,
        WindowNotFoundError,
        AttributeError,
        IndexError,
        RuntimeError,
        ElementAmbiguousError,
    ]

    def decorator(func: Callable) -> Callable:
        exceptions_to_include_list = default_exceptions_to_include + (exceptions_to_include or [])

        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            try:
                return func(*args, **kwargs)
            except tuple(exceptions_to_include_list) as exception:
                ts = datetime.now().strftime("%H_%M_%S")
                file_name = f"{ts}_{func.__name__}.png"
                Path(output).mkdir(parents=True, exist_ok=True)
                file_path = os.path.join(output, file_name)

                try:
                    # Try to capture the screenshot
                    screenshot = ImageGrab.grab()
                    screenshot.save(file_path)
                    logger.info(f"Screenshot saved to {file_path}")
                    attach_file_to_exception(exception, file_path)
                except Exception as e:
                    try:
                        from RPA.Desktop import Desktop as RpaDesktop

                        logger.warning(f"Failed to capture screenshot using ImageGrab. Cause: {e}")
                        desktop = RpaDesktop()
                        desktop.take_screenshot(file_path)
                        logger.info(f"Screenshot saved to {file_path}")
                        attach_file_to_exception(exception, file_path)
                    except ImportError:
                        logger.warning("rpaframework not installed")
                    raise exception
                raise exception

        return wrapper

    if func is not None:
        return decorator(func)

    return decorator


def capture_screenshot_if_exception(
    func: Callable = None,  # Func as default argument to allow use without parenthesis
    output: str = CONFIG.DIRECTORIES.SCREENSHOTS,
) -> Callable:
    """Decorator to capture a screenshot if an exception occur.

    This decorator wraps a function and captures a screenshot when any exception
    is raised. The screenshot will be saved to the output
    directory, and if `ImageGrab` fails, the `RPA.Desktop` module will be used
    as a fallback (if installed).

    Args:
        func (Callable, optional): The function being decorated.
        output (str, optional): Directory path where screenshots will be saved.
            Defaults to `CONFIG.DIRECTORIES.SCREENSHOTS`.

    Returns:
        Callable: The decorated function that captures a screenshot upon specific errors.

    Raises:
        Exception: Re-raises the original exception that triggered the screenshot.
    """

    def decorator(func: Callable) -> Callable:
        """Decorator to capture screenshot if error occurs."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            try:
                return func(*args, **kwargs)
            except Exception as exception:
                ts = datetime.now().strftime("%H_%M_%S")
                file_name = f"{ts}_{func.__name__}.png"
                Path(output).mkdir(parents=True, exist_ok=True)
                file_path = os.path.join(output, file_name)

                try:
                    # Try to capture the screenshot
                    screenshot = ImageGrab.grab()
                    screenshot.save(file_path)
                    logger.info(f"Screenshot saved to {file_path}")
                    attach_file_to_exception(exception, file_path)
                except Exception as e:
                    try:
                        from RPA.Desktop import Desktop as RpaDesktop

                        logger.warning(f"Failed to capture screenshot using ImageGrab. Cause: {e}")
                        desktop = RpaDesktop()
                        desktop.take_screenshot(file_path)
                        logger.info(f"Screenshot saved to {file_path}")
                        attach_file_to_exception(exception, file_path)
                    except ImportError:
                        logger.warning("rpaframework not installed")
                    raise exception
                raise exception

        return wrapper

    if func is not None:
        return decorator(func)

    return decorator
