"""Dropdown element module."""

from ..base.ui_element import UIElement


class DropdownElement(UIElement):
    """Standard dropdown element."""

    def __init__(self, *args, option_tag: str = "li", **kwargs):
        """Initialise dropdown element."""
        super().__init__(*args, **kwargs)
        self.option_tag = option_tag

    def type_and_enter(self, *text_to_enter) -> None:
        """Selects an option from the dropdown list based on the provided text.

        The text is input into the dropdown list input and the Enter key is pressed to select the option.

        Args:
            text_to_enter (str): The text/s of the option to be selected from the dropdown list.
            option_tag (str): The tag used for the different options. Defaults to 'li'.

        Returns:
            None
        """
        text_to_enter = tuple(text_to_enter)
        for text in text_to_enter:
            self.input_text(text)
            self.press_key(r"\13")

    def click_and_select_option(self, text_to_find: str) -> None:
        """Selects an option from the dropdown list based on the provided text.

        The dropdown list is clicked to open the list and the option is selected.

        Args:
            text_to_find (str): The text of the option to be selected from the dropdown list.
            option_tag (str, optional): The tag of the option to be selected from the dropdown list. Defaults to 'li'.

        Returns:
            None
        """
        self.click_element_when_visible()
        self.browser.get_webelement(f"{self.xpath}//{self.option_tag}[text()='{text_to_find}']").click()

    def get_selected_option(self, by="value") -> str:
        """Gets the selected option."""
        if by == "text":
            value = self.find_element().text
        else:
            value = self.find_element().get_attribute(by)
        return value
