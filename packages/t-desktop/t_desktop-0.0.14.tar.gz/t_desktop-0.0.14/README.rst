======================
t-desktop
======================

This Python library provides functionality for interacting with desktop
applications via UI automation on Windows OS using ``pywinauto``. It
includes methods to manage application lifecycles, interact with UI
elements, and handle alerts.

--------------

Classes
-------

``DesktopApp``
~~~~~~~~~~~~~~

The main class, ``DesktopApp``, is an abstract base class designed to
manage desktop applications, providing methods to start, connect, and
interact with app elements.

--------------

Class Documentation
-------------------

Initialization

.. code:: python

   DesktopApp(app_path: str)

Initializes the desktop application instance.

- **Parameters**

  - ``app_path`` (``str``): Path to the application executable.

--------------

Methods
-------

``dialog`` (property)
~~~~~~~~~~~~~~~~~~~~~

The main point of interaction with the App Window.

**Returns**: - ``WindowSpecification``: The top-level window of the
application.

--------------

``connect_to_app``
~~~~~~~~~~~~~~~~~~

Connect to the application.

.. code:: python

   def connect_to_app(app_path: str = None, title: str = None, timeout: int = None, **kwargs) -> Application

- **Parameters**

  - ``app_path`` (``str``, optional): Location of the application.
  - ``title`` (``str``, optional): Window title.
  - ``timeout`` (``int``, optional): Max wait time for connection.

- **Returns**:

  - ``Application``: Connected application object.

--------------

``start_app``
~~~~~~~~~~~~~

Starts the application.

.. code:: python

   def start_app(app_path: str, app_folder: str, sleep_seconds: int = 2) -> None

- **Parameters**

  - ``app_path`` (``str``): Application path.
  - ``app_folder`` (``str``): Application folder.
  - ``sleep_seconds`` (``int``): Pause time after startup.

--------------

``close_alerts``
~~~~~~~~~~~~~~~~

Closes application alerts.

.. code:: python

   def close_alerts(expected_window_title: str, max_attempts: int = 3, sleep_seconds: int = 1, ignored_titles: list[str] = []) -> None

- **Parameters**

  - ``expected_window_title`` (``str``): Title of the expected window.
  - ``max_attempts`` (``int``): Max attempts to check for the window.
  - ``sleep_seconds`` (``int``): Time between attempts.
  - ``ignored_titles`` (``list[str]``): Titles to ignore.

- **Raises**:

  - ``ElementNotFoundError``: If the expected window is not visible.

--------------

``get_element``
~~~~~~~~~~~~~~~

Retrieves a UI element.

.. code:: python

   def get_element(control_type: str, title: str | None = None, auto_id: str | None = None, dialog: WindowSpecification = None, **kwargs) -> WindowSpecification

- **Parameters**

  - ``control_type`` (``str``): Control type of the element.
  - ``title`` (``str``, optional): Title of the element.
  - ``auto_id`` (``str``, optional): Automation ID.

- **Returns**:

  - ``WindowSpecification``: Matching UI element.

--------------

``invoke_button``
~~~~~~~~~~~~~~~~~

Invokes a button.

.. code:: python

   def invoke_button(auto_id: str = None, title: str = None, dialog: WindowSpecification | None = None, **kwargs) -> None

- **Parameters**

  - ``auto_id`` (``str``, optional): Automation ID of the button.
  - ``title`` (``str``, optional): Title of the button.

--------------

``set_input_text``
~~~~~~~~~~~~~~~~~~

Sets text in an input field.

.. code:: python

   def set_input_text(text: str, auto_id: str = None, title: str = None, dialog: WindowSpecification | None = None) -> None

- **Parameters**

  - ``text`` (``str``): Text to set.
  - ``auto_id`` (``str``, optional): ID of the input field.
  - ``title`` (``str``, optional): Title of the input field.

--------------

``mouse_click_element``
~~~~~~~~~~~~~~~~~~~~~~~

Performs a mouse click on a specified element.

.. code:: python

   def mouse_click_element(element: WindowSpecification, button: str = "left", offset_x: int = 0, offset_y: int = 0) -> None

- **Parameters**

  - ``element`` (``WindowSpecification``): Element to click.
  - ``button`` (``str``): Mouse button.
  - ``offset_x`` (``int``): Horizontal offset.
  - ``offset_y`` (``int``): Vertical offset.

--------------

``mouse_double_click_element``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Performs a mouse double-click on a specified element.

.. code:: python

   def mouse_double_click_element(element: WindowSpecification, button: str = "left", set_focus: bool = False) -> None

- **Parameters**

  - ``element`` (``WindowSpecification``): Element to double-click.
  - ``button`` (``str``): Mouse button.
  - ``set_focus`` (``bool``): Set focus before clicking.

--------------

``select_dropdown_item``
~~~~~~~~~~~~~~~~~~~~~~~~

Selects an item from a dropdown.

.. code:: python

   def select_dropdown_item(auto_id: str, dropdown_item: str) -> None

- **Parameters**

  - ``auto_id`` (``str``): Dropdown ID.
  - ``dropdown_item`` (``str``): Dropdown item to select.

--------------

``wait_to_disappear``
~~~~~~~~~~~~~~~~~~~~~

Waits for an element to disappear.

.. code:: python

   def wait_to_disappear(control_type: str, auto_id: str = None, title: str = None, max_attempts: int = 3, timeout: int = 1) -> None

- **Parameters**

  - ``control_type`` (``str``): Element control type.
  - ``auto_id`` (``str``, optional): Element ID.
  - ``title`` (``str``, optional): Element title.

- **Raises**:

  - ``AssertionError``: If the element is still present after all
    attempts.

Here’s the documentation for the new methods and the ``dialog``
attribute:

--------------

``click_input``
~~~~~~~~~~~~~~~

Click element based on provided kwargs.

.. code:: python

   def click_input(
           self,
           control_type: str,
           auto_id: str | None = None,
           title: str | None = None,
           dialog: WindowSpecification | None = None,
           **kwargs,
       ) -> None

**Args**: - ``control_type`` (str): The control type of the element
(required). - ``auto_id`` (str, optional): The automation ID of the
button. Defaults to None. - ``title`` (str, optional): The title of the
button. Defaults to None. - ``dialog`` (WindowSpecification, optional):
The dialog to operate on. Defaults to self.dialog. - ``**kwargs``:
Additional keyword arguments for identifying a child window element.

--------------

``right_click_empty_space``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Right clicks in the blank space after a list of elements.

.. code:: python

   def right_click_empty_space(self, element: WindowSpecification, sleep_seconds: int = 2) -> None

**Args**: - ``element`` (WindowSpecification): The element to operate
on. - ``sleep_seconds`` (int): Time to sleep after right-clicking to
allow the dropdown to appear.

--------------

``get_element_coordinates``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Retrieves the coordinates of an element.

.. code:: python

   def get_element_coordinates(element: WindowSpecification) -> tuple

**Args**: - ``element`` (WindowSpecification): The element whose
coordinates are retrieved.

**Returns**: - ``tuple``: The coordinates of the element.

**Raises**: - ``AssertionError``: If the coordinates cannot be
retrieved.

--------------

``wait_until_element_visible``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Waits for an element to become visible in the dialog window.

.. code:: python

   def wait_until_element_visible(
           self, control_type: str, title: str = None, auto_id: str = None, timeout: int = 5
       ) -> bool

**Args**: - ``control_type`` (str): The control type of the element
(required). - ``title`` (str, optional): The title of the element.
Defaults to None. - ``auto_id`` (str, optional): The automation ID of
the element. Defaults to None. - ``timeout`` (int, optional): The
maximum wait time for the element to become visible. Defaults to 5
seconds.

**Raises**: - ``ValueError``: If neither ‘title’ nor ‘auto_id’ is
provided. - ``TimeoutError``: If the element does not become visible
within the timeout.

**Returns**: - ``bool``: True if the element becomes visible within the
allowed time.

--------------

``kill_app``
~~~~~~~~~~~~

Closes the app if it remains open after the session ends.

.. code:: python

   def kill_app(self, process: str, app_path: str) -> None

**Args**: - ``process`` (str): The name of the application process. -
``app_path`` (str): The path of the application executable.

**Raises**: - ``UsernameNotFoundError``: If the username is missing.

--------------

``get_app_session_if_running``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns the current session ID if the app is running.

.. code:: python

   def get_app_session_if_running(self, app_path: str) -> str | None

**Args**: - ``app_path`` (str): The system path of the application
executable.

**Returns**: - ``None | str``: None if the app is not running, otherwise
the tasklist output.

**Raises**: - ``UsernameNotFoundError``: If the username is missing.

--------------

Utilities
---------

``relogin_and_retry_if_pywin_error``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decorator to relogin and retry a function if a specified PyWin error
occurs.

**Args**: - ``retries`` (int): Number of times to retry the function.
Defaults to 3. - ``delay`` (int): Delay in seconds between retries.
Defaults to 1.

**Returns**: - ``Callable``: The decorated function with retry and
relogin logic.

**Raises**: - ``LoginMethodNotFoundError``: If the ``login`` method is
not defined or not callable on the class.

--------------

``retry_if_pywin_error``
~~~~~~~~~~~~~~~~~~~~~~~~

Decorator for retrying a function in Apps derived classes if specified
exceptions are encountered.

**Args**: - ``retries`` (int): Number of times to retry the function.
Defaults to 3. - ``delay`` (int): Delay in seconds between retries.
Defaults to 1. - ``close_modal`` (bool): Whether to attempt closing
modal dialogs on error. Defaults to False. - ``exceptions``
(tuple[Type[BaseException], …]): Additional exceptions to catch and
retry on.

**Returns**: - ``Callable``: The decorated function with retry logic for
specified exceptions.

**Raises**: - The last caught exception if all retry attempts fail.

--------------

``capture_screenshot_if_pywin_error``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decorator to capture a screenshot if specified exceptions occur during
the execution of a function.

**Args**: - ``func`` (Callable, optional): The function being decorated.
- ``exceptions_to_include`` (List[Type[Exception]], optional): List of
exceptions to trigger screenshot capture. Defaults to a predefined list.
- ``output`` (str): Directory path where screenshots will be saved.
Defaults to ``CONFIG.DIRECTORIES.SCREENSHOTS``.

**Returns**: - ``Callable``: The decorated function that captures a
screenshot upon specific errors.

**Raises**: - The original exception that triggered the screenshot
capture if a failure occurs.
