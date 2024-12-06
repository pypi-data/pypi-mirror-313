"""Contains the UIElement class."""

import datetime

from ..bot_config import BotConfig
from .. import logger
from retry import retry
from selenium.common import (  # type: ignore
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)

from RPA.Browser.Selenium import Selenium  # type: ignore
from ..bug_catcher_meta import BugCatcherMeta
from ..selenium_manager import SeleniumManager
from typing import Callable, TypeVar, Optional, Any
from time import sleep
import re


T = TypeVar("T", bound="UIElement")


class UIElement(metaclass=BugCatcherMeta):
    """This is an UI Element used to build each Page."""

    def __init__(self, xpath: str, wait: bool = True, id: str = "", timeout: Optional[int] = None) -> None:
        """
        Initializes a base element with specified parameters.

        Args:
            xpath (str): The XPath expression used to locate the element,
                could also be a formattable string for dynamic XPaths.
            wait (bool, optional): Wait for the element to be present. Defaults to True.
            id (str, optional): An optional identifier for the element. Defaults to None.
            timeout (int, optional): The maximum time to wait for the element to be present, in seconds.

        """
        self.xpath = xpath
        self.wait = wait
        self.id = id
        self.timeout = timeout
        self.original_xpath = xpath
        self.browser: Selenium = SeleniumManager.get_instance()

        self.name_in_page = None
        self.page_name = None

    def __set_name__(self, owner, name):
        """Called when the attribute is set in the class.

        Args:
            owner: The class where this descriptor is defined.
            name: The name of the attribute.
        """
        self.name_in_page = name
        self.page_name = owner.__name__

    @retry(
        exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
            NoSuchElementException,
            ElementNotInteractableException,
            AssertionError,
            TimeoutException,
        ),
        tries=2,
        delay=1,
    )
    def format_xpath(self, *args: list, **kwargs: dict) -> None:
        """If using a dynamic xpath, this method formats the xpath string.

        Args:
            *args (list): The arguments to be used to format the xpath.
            **kwargs (dict): The keyword arguments to be used to format the
        """
        self.xpath = self.original_xpath.format(*args, **kwargs)

    def __getattr__(self, name: str) -> Callable[..., Any]:
        """Delegate method calls not found in this class to the Selenium instance."""
        if self.browser.get_browser_ids():
            self._handle_alert()
            if not self.wait_element_load():
                logger.info(f"Element not found: {self.xpath}. Wait is set to False. Doing nothing")
                return lambda *args, **kwargs: None
            return lambda *args, **kwargs: self._selenium_method(name, *args, **kwargs)
        return None  # type: ignore

    def _selenium_method(self, name: str, *args, **kwargs) -> Callable:
        """Executing self.browser.name(*args,**kwargs) method.

        For example: self.browser.click_element(self.xpath)
        """
        method = getattr(self.browser, name, None)
        if method:
            try:
                return method(self.xpath, *args, **kwargs)
            except ElementClickInterceptedException as e:
                if BotConfig.close_modals:
                    logger.info("Element click intercepted. Attempting to close modal window...")
                    self._close_modal(str(e))
                    try:
                        return method(self.xpath, *args, **kwargs)
                    except ElementClickInterceptedException as ex:
                        logger.info("Element click intercepted. Attempting to remove covering element...")
                        self._remove_covering_element(str(ex))
                        return method(self.xpath, *args, **kwargs)
                else:
                    raise e
        else:
            raise AttributeError(f"Method '{name}' not found in Selenium instance.")

    @retry(
        exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
            NoSuchElementException,
            ElementNotInteractableException,
            AssertionError,
            TimeoutException,
        ),
        tries=2,
        delay=1,
    )
    def wait_element_load(self, timeout: Optional[int] = None) -> bool:
        """
        Wait for element to load.

        Args:
            timeout (int, optional): The maximum time to wait for the element to be present, in seconds.
                Defaults to None. Overwrites apps inherent timeout if set.

        Returns:
            bool: True if element is visible, False not found and wait is False otherwise.

        Raises:
            AssertionError: If element is not visible and wait is True.
        """
        timeout = timeout if timeout else self.timeout if self.timeout else BotConfig.default_timeout
        is_success = False
        timer = datetime.datetime.now() + datetime.timedelta(0, timeout)

        while not is_success and timer > datetime.datetime.now():
            if self.browser.does_page_contain_element(self.xpath):
                try:
                    elem = self.browser.find_element(self.xpath)
                    is_success = elem.is_displayed()
                except Exception:
                    sleep(1)

        if not is_success:
            if self.wait:
                raise AssertionError(f"Element '{self.xpath}' not visible.")
            return False
        return True

    def _handle_alert(self):
        """Handle alert if present."""
        try:
            self.browser.alert_should_not_be_present(BotConfig.alert_handling_option)
        except AssertionError:
            logger.info(f"Alert detected. Handling with option: {BotConfig.alert_handling_option}")

    def _get_element_from_message(self, exception_message: str) -> tuple[str, str, str]:
        """Get element from exception message.

        Args:
            exception_message (str): The exception message.
        """
        match = re.search(r"Other element would receive the click: <(.+?)>", exception_message)
        if match:
            blocking_element_html = match.group(1)
            logger.info(f"Blocking element: {blocking_element_html}")
            tag_match = re.match(r"(\w+)", blocking_element_html)
            tag = tag_match.group(1) if tag_match else ""

            id_match = re.search(r'id="([^"]+)"', blocking_element_html)
            if id_match:
                locator = "id"
                locator_value = id_match.group(1)
            else:
                attr_matches = re.findall(r'(\w+)="([^"]+)"', blocking_element_html)
                for attr_name, attr_value in attr_matches:
                    if attr_name != "style":
                        locator = attr_name
                        locator_value = attr_value
                        break
                else:
                    locator = ""
                    locator_value = ""
            return tag, locator, locator_value
        return "", "", ""

    def _close_modal(self, exception_message: str) -> None:
        """Attempt to accept or close modal."""
        tag, locator, locator_value = self._get_element_from_message(exception_message)

        if tag and locator and locator_value:
            if BotConfig.modal_button:
                elements = self.browser.find_elements(
                    f"//{tag}[@{locator}='{locator_value}']//button[text()='{BotConfig.modal_button}']"
                )
                if elements:
                    element = elements[0]
                    logger.info(f"Clicking on the blocking element: {element.get_attribute('outerHTML')}")
                    element.click()
                    return
            elements = self.browser.find_elements(f"//{tag}[@{locator}='{locator_value}']//button[text()='Close']")
            if elements:
                element = elements[0]
                logger.info(f"Clicking on the blocking element: {element.get_attribute('outerHTML')}")
                element.click()
                return
            elements = self.browser.find_elements(f"//{tag}[@{locator}='{locator_value}']//button")
            if elements:
                logger.info(f"Clicking on the blocking element: {elements[-1].get_attribute('outerHTML')}")
                elements[-1].click()
            else:
                elements = self.browser.find_elements(f"//{tag}[@{locator}='{locator_value}']//input")
                if elements:
                    logger.info(f"Clicking on the blocking element: {elements[-1].get_attribute('outerHTML')}")
                    elements[-1].click()

    def _remove_covering_element(self, exception_message: str) -> None:
        """Remove covering element."""
        tag, locator, locator_value = self._get_element_from_message(exception_message)
        js_script = f"""document.querySelector('{tag}[{locator}="{locator_value}"]').style.display = 'none';"""
        self.browser.execute_javascript(js_script)
