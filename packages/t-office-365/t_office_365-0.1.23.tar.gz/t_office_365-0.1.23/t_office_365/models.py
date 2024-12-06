"""Models for the Excel file."""
from openpyxl.utils import get_column_letter


class Cell:
    """Cell model."""

    def __init__(self, column_name, data_type, value, row_num, col_num):
        """Initialize the cell model."""
        self.column_name: str = column_name
        self.data_type: str = data_type
        self.value: str = value
        self.column_number = col_num
        self.row_number = row_num
        self.address = f"{get_column_letter(col_num)}{row_num}"

    def __str__(self):
        """Return the string representation of the cell."""
        return self.value

    def __repr__(self):
        """Return the representation of the cell."""
        return f"{self.column_name} - {self.data_type} - {self.value}"
