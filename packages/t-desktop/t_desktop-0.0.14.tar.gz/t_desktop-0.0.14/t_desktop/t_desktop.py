"""Main module."""
import contextlib
import os
import subprocess
import time
from abc import ABC
from typing import Union
import _ctypes


from t_desktop.config import CONFIG, IS_WINDOWS_OS
from t_desktop.decorators import retry_if_pywin_error
from t_desktop.exceptions import UsernameNotFoundError
from t_desktop.utils.logger import logger

if IS_WINDOWS_OS:
    from pywinauto import Application, WindowSpecification, mouse
    from pywinauto.application import ProcessNotFoundError
    from pywinauto.timings import TimeoutError as PywinTimeout
    from pywinauto.findwindows import ElementNotFoundError
else:
    logger.warning("Not in a Windows Machine, failed to import UI related libraries")


class DesktopApp(ABC):
    """This class is the base class for all Desktop classes."""

    def __init__(self, app_path: str):
        """Initializes the Apps class."""
        self.app: Application = None
        self.app_path = app_path

    @retry_if_pywin_error(retries=3)  # type: ignore[misc]
    def _dialog(self) -> WindowSpecification:
        try:
            return self.app.top_window()
        except RuntimeError as e:
            if (
                "No windows for that process could be found" in str(e)
                and self.get_app_session_if_running(self.app_path) is not None
            ):
                time.sleep(5)
                self.app = self.connect_to_app(self.app_path)
                return self.app.top_window()
            raise e

    @property
    def dialog(self) -> WindowSpecification:
        """The main point of interaction with the App Window."""
        return self._dialog()

    def set_focus(self) -> None:
        """Ste focus to 'self.dialog'."""
        with contextlib.suppress(_ctypes.COMError):
            self.dialog.set_focus()

    @retry_if_pywin_error(exceptions=(OSError, RuntimeError), delay=3, retries=2)  # type: ignore[misc]
    def close_alerts(
        self, expected_window_title: str, max_attempts: int = 3, sleep_seconds: int = 1, ignored_titles: list[str] = []
    ) -> None:
        """Close alerts until the expected window exists or the timeout is reached.

        Args:
            expected_window_title (str): The title of the expected window.
            max_attempts (int): Maximum number of attempts to check for the expected window and close alerts.
            sleep_seconds (int): Time to sleep between each search for modal
            ignored_titles (list[str]): List of window titles to ignore during the search. Defaults to an empty list.
        """
        with contextlib.suppress(_ctypes.COMError, OSError):
            attempts = 0
            while attempts < max_attempts:
                current_top_title = self.dialog.child_window(control_type="Window", found_index=0).window_text()
                if current_top_title == expected_window_title:
                    break

                alerts = self.dialog.children(control_type="Window")
                for alert in alerts:
                    if alert.window_text() not in [expected_window_title] + ignored_titles:
                        logger.debug(f"Closing Alert with title: {alert.window_text()}.")
                        alert.close()

                attempts += 1
                time.sleep(sleep_seconds)
            else:
                raise ElementNotFoundError(f"Window {expected_window_title} not visible")

    def connect_to_app(self, app_path: str = None, title: str = None, timeout: int = None, **kwargs) -> Application:
        """Connect to the application using optional parameters for the app path, title, and timeout.

        This method connects to an application using the provided keyword arguments. Only the
        arguments with values will be passed to the `connect` method, allowing for flexible
        connections to applications.

        Args:
            app_path (str, optional): The location of the application on the system.
            title (str, optional): The title of the application window to connect to.
            timeout (int, optional): The maximum time (in seconds) to wait for the connection.
            **kwargs: Additional keyword arguments for connecting to the application.

        Returns:
            Application: The connected Application object.
        """
        connect_args = {
            k: v for k, v in {"path": app_path, "title": title, "timeout": timeout}.items() if v is not None
        }
        return Application(backend="uia").connect(**connect_args, **kwargs)

    @retry_if_pywin_error(exceptions=(ProcessNotFoundError,), delay=5, retries=3)  # type: ignore[misc]
    def start_app(self, app_path: str, app_folder: str, sleep_seconds: int = 2) -> None:
        """Start the App.

        Args:
            app_path (str): the location of the app on the system
            app_folder (str): the location of the folder that contains the app
            sleep_seconds (int): Time to sleep after open the app
        """
        Application().start(app_path, work_dir=app_folder)
        self.app = self.connect_to_app(path=app_path, timeout=120)
        time.sleep(sleep_seconds)

    def get_app_session_if_running(self, app_path: str) -> Union[str, None]:
        """Return current session ID if app is running.

        Args:
            app_name (str): The name of the application executable.

        Returns:
            Union[str, None]: None if the app is not running, otherwise the tasklist output.
        """
        if not CONFIG.username:
            raise UsernameNotFoundError("Username is empty for this server")
        tasklist_cmd = (
            f'tasklist /fi "imagename eq {os.path.basename(app_path)}" /fi "username eq {CONFIG.username}" /fo csv'
        )
        tasklist_result = subprocess.run(tasklist_cmd, shell=True, capture_output=True, text=True, check=True)
        tasklist_output = tasklist_result.stdout.strip()
        if "INFO: No tasks are running which match the specified criteria." in tasklist_output:
            return None
        return tasklist_output

    def kill_app(self, process: str, app_path: str) -> None:
        """Close the app if it is still open after closing the session.

        Args:
            process (str): The process name of the application.
            app_path (str): The system path of the application executable.

        Returns:
            None
        """
        app_name = os.path.basename(app_path)
        try:
            if not process:
                logger.warning(f"No running process found for {app_name}.")
                return
            if not CONFIG.username:
                raise UsernameNotFoundError("Username is empty for this server")
            process_id = next(
                int(line.split(",")[1].replace('"', "").strip()) for line in process.split("\n") if app_name in line
            )
            taskkill_cmd = f'taskkill /f /pid {process_id} /fi "username eq {CONFIG.username}"'
            subprocess.run(taskkill_cmd, shell=True, check=True)
            logger.info(f"Process {app_name} terminated for user {CONFIG.username}")
            time.sleep(2)
        except StopIteration:
            logger.warning(f"No running process found for {app_name}.")

    def get_element(
        self,
        control_type: str,
        title: Union[str, None] = None,
        auto_id: Union[str, None] = None,
        dialog: WindowSpecification = None,
        **kwargs,
    ):
        """Retrieve an element from the dialog using either 'title' or 'auto_id'.

        Args:
            control_type (str): The control type of the element (required).
            title (str, optional): The title of the element.
            auto_id (str, optional): The automation ID of the element.
            dialog (WindowSpecification, optional): The dialog to operate on. Defaults to self.dialog.

        Raises:
            ValueError: If neither 'title' nor 'auto_id' is provided.

        Returns:
            WindowSpecification: The matching element.
        """
        if dialog is None:
            dialog = self.dialog

        # Add non-None elements to kwargs
        if title is not None:
            kwargs["title"] = title
        if auto_id is not None:
            kwargs["auto_id"] = auto_id

        return dialog.child_window(control_type=control_type, **kwargs)

    def set_input_text(
        self, text: str, auto_id: str = None, title: str = None, dialog: Union[WindowSpecification, None] = None
    ) -> None:
        """Set the text of an input field in the dialog window.

        Args:
            text (str): The text to set in the input field.
            auto_id (str, optional): The automation ID of the input field. Defaults to None.
            title (str, optional): The title of the input field. Defaults to None.
            dialog (WindowSpecification, optional): The dialog to operate on. Defaults to self.dialog.

        Raises:
            ValueError: If neither 'auto_id' nor 'title' is provided.

        Note:
            This method suppresses `_ctypes.COMError` and `OSError` exceptions.
        """
        with contextlib.suppress(_ctypes.COMError, OSError):
            element = self.get_element(control_type="Edit", auto_id=auto_id, title=title, dialog=dialog)
            element.set_edit_text(text)

    def invoke_button(
        self, auto_id: str = None, title: str = None, dialog: Union[WindowSpecification, None] = None, **kargs
    ) -> None:
        """Invoke a button in the dialog window.

        Args:
            auto_id (str, optional): The automation ID of the button. Defaults to None.
            title (str, optional): The title of the button. Defaults to None.
            dialog (WindowSpecification, optional): The dialog to operate on. Defaults to self.dialog.
            **kargs: Additional keyword arguments passed to the child_window method.

        Raises:
            ValueError: If neither 'auto_id' nor 'title' is provided.
        """
        with contextlib.suppress(_ctypes.COMError, OSError):
            element = self.get_element(control_type="Button", auto_id=auto_id, title=title, dialog=dialog, **kargs)
            element.invoke()

    def wait_until_element_visible(
        self,
        control_type: str,
        title: str = None,
        auto_id: str = None,
        timeout: int = 5,
        retries=3,
        raise_ex: bool = True,
        **kwargs,
    ) -> bool:
        """Waits for an element to become visible in the dialog window.

        Args:
            control_type (str): The control type of the element (required).
            title (str, optional): The title of the element. Defaults to None.
            auto_id (str, optional): The automation ID of the element. Defaults to None.
            timeout (int, optional): The maximum time to wait for the element to become visible. Defaults to 5 seconds.
            raise_ex (bool, optional): If you wanna suppress the exception and receive boolean instead.
            **kwargs: Accept all keyword arguments that can be used to identify a child window element
        Raises:
            ValueError: If neither 'title' nor 'auto_id' is provided.
            TimeoutError: If the element does not become visible within the timeout.

        Returns:
            bool: Returns True if the element becomes visible within the allowed time.
        """
        retry = 0
        while retry < retries:
            element = self.get_element(control_type=control_type, title=title, auto_id=auto_id, **kwargs)
            try:
                element.wait("visible", timeout)
            except PywinTimeout:
                retry += 1
                continue
            return True
        if raise_ex:
            raise PywinTimeout("Element was not visible in the max timeout")
        else:
            return False

    @staticmethod  # type: ignore[misc]
    @retry_if_pywin_error(exceptions=(AssertionError,), delay=5, retries=2)  # type: ignore[misc]
    def get_element_coordinates(element: WindowSpecification) -> tuple:
        """This method gets the element coordinates.

        Args:
            element (UIAWrapper): element
        Returns:
            tuple: element coordinates
        """
        point = None
        with contextlib.suppress(_ctypes.COMError, OSError):
            point = element.rectangle().mid_point()
        if not point:
            raise AssertionError("Failed to retrieve coordinates.")
        return point

    def mouse_click_element(
        self, element: WindowSpecification, button: str = "left", offset_x: int = 0, offset_y: int = 0
    ) -> None:
        """This method performs a mouse click at a specified offset within a given element's location.

        Args:
            element (WindowSpecification): The UI element to click.
            button (str): The mouse button to click (left/right). Defaults to "left".
            offset_x (int): The horizontal offset from the element's top-left corner. Defaults to 0.
            offset_y (int): The vertical offset from the element's top-left corner. Defaults to 0.
        """
        coords = self.get_element_coordinates(element)
        click_x = coords[0] + offset_x
        click_y = coords[1] + offset_y
        element_rec = element.rectangle()

        # Ensure the point is within the bounds of the element
        click_x = min(max(click_x, element_rec.left), element_rec.right - 1)
        click_y = min(max(click_y, element_rec.top), element_rec.bottom - 1)

        mouse.click(button=button, coords=(click_x, click_y))

    def mouse_double_click_element(
        self, element: WindowSpecification, button: str = "left", set_focus: bool = False
    ) -> None:
        """This method double click with mouse in a given element's location.

        Args:
            element (UIAWrapper): element
            button (str): Mouse Button to be clicked (left/right)
            set_focus (bool): If True, calls set_focus() on the element
        """
        if set_focus:
            element.set_focus()

        mouse.double_click(button=button, coords=self.get_element_coordinates(element))

    def select_dropdown_item(self, auto_id: str, dropdown_item: str) -> None:
        """Select the required item from the dropdown list.

        Args:
            auto_id (str): the name ID the dropdown.
            dropdown_item (str): the name of the dropdown item to be selected.
        """
        with contextlib.suppress(_ctypes.COMError):
            self.dialog.child_window(auto_id=auto_id).select(dropdown_item)

    @retry_if_pywin_error()  # type: ignore[misc]
    def right_click_empty_space(self, element: WindowSpecification, sleep_seconds: int = 2) -> None:
        """This method right clicks in the blank space after a list of elements.

        Args:
            element (WindowSpecification): element
            sleep_seconds (int): time to sleep after right clicking, to wait dropdown to appear.
        """
        last_child_coords = self.get_element_coordinates(element.descendants()[-1])
        parent_rect = element.rectangle()

        # Calculate a point slightly beyond the last child but within the parent
        click_x = last_child_coords[0]
        click_y = last_child_coords[1] + 30

        # Ensure the point is within the bounds of the parent
        if click_x > parent_rect.right:
            click_x = parent_rect.right - 1
        if click_y > parent_rect.bottom:
            click_y = parent_rect.bottom - 1

        mouse.click(button="right", coords=(click_x, click_y))
        time.sleep(sleep_seconds)

    def wait_to_disappear(
        self, control_type: str, auto_id: str = None, title: str = None, max_attempts: int = 3, timeout: int = 1
    ) -> None:
        """Wait for an element to disappear and raise an AssertionError if the element is still present.

        Args:
            control_type (str): The control type of the element (required).
            auto_id (str, optional): The automation ID of the element to wait for. Defaults to None.
            title (str, optional): The title of the element to wait for. Defaults to None.
            max_attempts (int, optional): The maximum number of attempts to check. Defaults to 3.
            timeout (int, optional): The time to wait between attempts in seconds. Defaults to 1 second.

        Raises:
            ValueError: If neither 'auto_id' nor 'title' is provided, or if both are provided.
            AssertionError: If the element is still present after all attempts.
        """
        attempts = 0
        while attempts < max_attempts:
            try:
                element = self.get_element(control_type=control_type, auto_id=auto_id, title=title)
                if not element.exists():
                    return  # Element disappeared
            except (TimeoutError, ElementNotFoundError):
                return  # Element already gone or not found

            time.sleep(timeout)
            attempts += 1

        raise AssertionError(f"Element is still present after {max_attempts} attempts.")

    def click_input(
        self,
        control_type: str,
        auto_id: Union[str, None] = None,
        title: Union[str, None] = None,
        dialog: Union[WindowSpecification, None] = None,
        **kwargs,
    ) -> None:
        """Click element with based on provided kwargs.

        Args:
            control_type (str): The control type of the element (required).
            auto_id (str, optional): The automation ID of the button. Defaults to None.
            title (str, optional): The title of the button. Defaults to None.
            dialog (WindowSpecification, optional): The dialog to operate on. Defaults to self.dialog.
            **kwargs: Accept all keyword arguments that can be used to identify a child window element
        """
        with contextlib.suppress(_ctypes.COMError):
            element = self.get_element(control_type=control_type, auto_id=auto_id, title=title, dialog=dialog, **kwargs)
            element.click_input()
