"""Contains the BasePage class which is the parent class for all page objects in the project."""

import copy
import datetime
from selenium.webdriver.remote.webelement import WebElement
from SeleniumLibrary.errors import ElementNotFound  # type: ignore
from ..selenium_manager import SeleniumManager
from RPA.Browser.Selenium import Selenium  # type: ignore
from .ui_element import UIElement
from typing import Optional
from abc import ABC
from ..exceptions import NoVerificationElement, NoURL


class BasePage(ABC):
    """Base page class for all page objects in the project."""

    browser: Selenium = Selenium
    url: str = ""
    verification_element: Optional[UIElement] = None

    def __init__(self):
        """Base Page."""
        # Get the Selenium instance based on the portal name (if provided)
        self.browser = SeleniumManager.get_instance()
        if not self.verification_element:
            raise NoVerificationElement("Verification element not set for page.")
        if not self.url:
            raise NoURL("URL not set for page.")

    def __deepcopy__(self):
        """Custom deepcopy to avoid copying the Selenium browser instance."""
        new_copy = copy.copy(self)  # Perform shallow copy
        new_copy.browser = self.browser  # Prevent deep copying the Selenium instance
        return new_copy

    def visit(self) -> None:
        """Navigate to the base page URL."""
        self.browser.go_to(self.url)
        self.wait_page_load()

    def wait_page_load(self, timeout=None) -> None:
        """Wait for the page to load by waiting for the verification element to load.

        timeout: The maximum time to wait for the element to be present, in seconds.
        """
        if timeout and self.verification_element:
            self.verification_element.wait_element_load(timeout)
        elif self.verification_element:
            self.verification_element.wait_element_load()

    def wait_for_new_window_and_switch(self, old_window_handles: list) -> None:
        """Function for waiting and switching to new window.

        Args:
            old_window_handles: The list of window handles before the new window is opened.

        Returns:
            The new window handle.
        """
        timeout = datetime.datetime.now() + datetime.timedelta(seconds=30)
        while datetime.datetime.now() < timeout:
            currents_window_handles = self.browser.get_window_handles()
            if len(currents_window_handles) > len(old_window_handles):
                window = [window for window in currents_window_handles if window not in old_window_handles][0]
                return self.browser.switch_window(window)
        else:
            raise TimeoutError("New window was not opened")

    def get_element_from_shadow_roots(self, *roots, element_css: str) -> WebElement:
        """Get element from nested shadow roots.

        Args:
            roots: The css locators of the shadow root elements, in hierarchal order.
            element_css: The css locator of the element to find.

        Returns:
            The WebElement of the element found.
        """
        javascript_code = (
            "return document"
            + "".join([f".querySelector('{x}').shadowRoot" for x in roots])
            + f".querySelector('{element_css}')"
        )
        element = self.browser.execute_javascript(javascript_code)
        if not isinstance(element, WebElement):
            raise ElementNotFound(f"Element not found in shadow root: {element_css}")
        return element
