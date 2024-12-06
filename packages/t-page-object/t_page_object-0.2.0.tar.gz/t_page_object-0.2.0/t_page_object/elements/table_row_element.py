"""Table Row element module."""

from ..base.ui_element import UIElement


class TableRowElement(UIElement):
    """Class for TextElement element model."""

    def get_row_values(self) -> list[str]:
        """Get Element value."""
        row_cells = self.find_elements()

        return [cell.text for cell in row_cells]
