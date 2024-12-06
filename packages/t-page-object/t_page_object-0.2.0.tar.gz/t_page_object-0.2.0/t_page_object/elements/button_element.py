"""Button element module."""

from .. import logger
from ..bot_config import BotConfig
from ..base.ui_element import UIElement


class ButtonElement(UIElement):
    """Standard button element."""

    def __init__(
        self,
        xpath: str,
        dev_safe_sensitive: bool = False,
        wait: bool = True,
        timeout: int = 10,
    ):
        """
        Initializes a button element with specified parameters.

        Args:
            xpath (str): The XPath expression used to locate the button element.
            dev_safe_sensitive (bool, optional): Indicates whether the button is
            sensitive to development-safe operations. Defaults to False.
            wait (bool, optional): Whether to wait for the button element to be present. Defaults to True.

        Returns:
            None
        """
        super().__init__(xpath=xpath, wait=wait, timeout=timeout)
        self.dev_safe_sensitive = dev_safe_sensitive

    def click(self) -> None:
        """Main click method for button element.

        Checks if button is dev_save_sensitive and if dev_safe_mode is enabled.
        """
        if self.dev_safe_sensitive and BotConfig.dev_safe_mode:
            logger.debug("Button not clicked: The element is dev safe sensitive, and DEV_SAFE_MODE is enabled")
        else:
            super().__getattr__("click_element_if_visible")()
            logger.debug("Button clicked: DEV_SAFE_MODE is disabled")

    def click_button(self) -> None:
        """Redirects to click method."""
        self.click()

    def click_button_when_visible(self) -> None:
        """Redirects to click method."""
        self.click()

    def click_button_if_visible(self) -> None:
        """Redirects to click method."""
        self.click()

    def click_element(self) -> None:
        """Redirects to click method."""
        self.click()

    def click_element_if_visible(self) -> None:
        """Redirects to click method."""
        self.click()

    def click_element_when_visible(self) -> None:
        """Redirects to click method."""
        self.click()

    def click_element_when_clickable(self) -> None:
        """Redirects to click method."""
        self.click()
