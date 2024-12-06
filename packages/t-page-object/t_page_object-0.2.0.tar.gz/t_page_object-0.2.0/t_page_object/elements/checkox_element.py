"""Checkbox element module."""

from ..base.ui_element import UIElement


class CheckboxElement(UIElement):
    """Checkbox element."""

    def select(self) -> None:
        """Selects the checkbox element."""
        self.click_element_when_visible()
