#  Copyright (c) 2024.
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the “Software”), to deal in the
#   Software without restriction,
#   including without limitation the rights to use, copy, modify, merge, publish, distribute,
#   sublicense, and/or sell copies
#   of the Software, and to permit persons to whom the Software is furnished to do so, subject to
#   the following conditions:
#  #
#   The above copyright notice and this permission notice shall be included in all copies or
#   substantial portions of the Software.
#  #
#   THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE
#   WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO
#   EVENT SHALL THE AUTHORS OR
#   COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
#   CONTRACT, TORT OR
#   OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#  #
#   This uses QT for some components which has the primary open-source license is the GNU Lesser
#   General Public License v. 3 (“LGPL”).
#   With the LGPL license option, you can use the essential libraries and some add-on libraries
#   of Qt.
#   See https://www.qt.io/licensing/open-source-lgpl-obligations for QT details.

from functools import partial
from typing import Union, List

from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QSizePolicy, QTextEdit

from YMLEditor.structured_text import to_text, data_type, parse_text, rebuild_dict


class ItemWidget(QWidget):
    """
    A configurable widget for displaying and editing a single field from a config file.

    - Supports various widget types including editable text, combo boxes, and read-only labels.
    - All user edits are validated and synchronized with the config data.
    - Uses `structured_text` module to parse text representations of dictionaries and lists.

    Attributes:
        config(Config): The config file object.  Must support get, set, save, load.
        widget_type (str): The type of widget ("text_edit", "line_edit", "read_only", "label",
        or "combo_box").
        key (str): Key for the field in the config data.
        error_style (str):  style for indicating an error.
        rgx (str): Regex pattern for validating text fields. Set in options parameter.
        _data_type (type) : data type of the item

    **Methods**:
    """

    def __init__(
            self, config, widget_type, initial_value, combo_rgx, callback, width=50, key=None,
            text_edit_height=90, verbose=1, error_style = "color: Orange;"
    ):
        """
        Initialize

        Args:
            config(Config): Configuration handler to synchronize data.
            widget_type (str): Type of widget to create
                ("text_edit", "line_edit", "read_only", "combo", "label").
            initial_value (str): Initial value to populate the widget.
            combo_rgx (Union[List[str], str]): Dropdown options for combo boxes or
                regex for validating text fields.
            callback (callable): Function to call when the widget value changes.
            width (int, optional): Fixed width for the widget. Defaults to 50.
            key (str, optional): Key for linking the widget to the config data.
            text_edit_height (int, optional): Height for text edit widgets. Defaults to 90.
            verbose (int, optional): Verbosity level. Defaults to 1.
        """
        super().__init__()

        self.error_style = error_style
        self.rgx = None
        self.widget_type = widget_type
        self.callback = callback
        self.key = key
        self.config = config
        self._is_valid = False
        self._data_type = None
        self.verbose = verbose

        self._create_widget(widget_type, initial_value, combo_rgx, width, text_edit_height)

    def _create_widget(self, widget_type, initial_value, combo_rgx, width, text_edit_height):
        """
        Create a specific type of widget based on the provided parameters (private)

        Args:
            widget_type (str): The type of widget to create.
            initial_value (str): The initial value for the widget.
            combo_rgx (Union[List[str], str], optional): Combo options or validation regex.
            width (int): Width of the widget.
            text_edit_height (int): Height for text edit widgets.
        """
        if widget_type == "combo":
            self.widget = QComboBox()
            self.widget.addItems(combo_rgx)
            self.widget.setCurrentText(initial_value)
        elif widget_type == "text_edit":
            self.widget = QTextEdit(str(initial_value))
            self.widget.setFixedHeight(text_edit_height)
            # Disable drag-and-drop functionality
            self.widget.setAcceptDrops(False)
            self.rgx = combo_rgx
        elif widget_type == "line_edit":
            self.widget = QLineEdit(str(initial_value))
            self.widget.setAcceptDrops(False)
            self.rgx = combo_rgx
        elif widget_type == "read_only":
            self.widget = QLineEdit(str(initial_value))
            self.rgx = combo_rgx
            self.widget.setReadOnly(True)
        elif widget_type == "label":
            self.widget = QLabel()
        else:
            raise TypeError(f"Unsupported widget type: {widget_type} for {self.key}")

        if widget_type != "label":
            self.widget.setObjectName(self.key)
            if isinstance(self.widget, QComboBox):
                self.widget.currentIndexChanged.connect(
                    partial(self._on_widget_changed, self.widget)
                )
            else:
                self.widget.textChanged.connect(partial(self._on_widget_changed, self.widget))

        self.widget.setProperty("originalStyle", self.widget.styleSheet())
        if isinstance(self.widget, QLineEdit):
            self.widget.setFixedWidth(width)
        else:
            self.widget.setMinimumWidth(width)

        self.widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def display(self):
        """
        Load and display our field from the config data.
        Prints a warning if our key is not found in config data.
        """
        key, val = None, None
        try:
            if self.widget:
                key = self.widget.objectName()
                if key:
                    val = self.config.get(key) or ""
                    if not self._data_type:
                        self._data_type = data_type(val)
                    self.set_text(self.widget, val)
        except Exception as e:
            key = key or "None"
            val = val or "None"
            if self.verbose > 0:
                print(f"Warning: widget key '{key}': {e}")

    def _on_widget_changed(self, widget):
        """
        Handle changes to the widget's value: validate text. If valid,
        update the config data. Set style appropriately.

        Args:
            widget (QWidget): The widget whose value was changed.
        """
        key = widget.objectName()
        text = get_text(widget)

        # Ensure text is valid and properly formatted
        if isinstance(text, str) and self._data_type:
            text = text.strip()  # Remove surrounding whitespace
            try:
                if self._data_type == dict:
                    text = rebuild_dict(text)
                elif self._data_type == list:
                    # Add enclosing brackets if not present and content is non-empty
                    if text and (not text.startswith("[") or not text.endswith("]")):
                        text = f"[{text}]"
            except Exception as e:
                self.set_error_style(widget)
                return

        # Validate the text and parse it
        invalid, data_value = parse_text(text, self._data_type, self.rgx)

        # Update config and apply styles based on validation
        if invalid:
            self.set_error_style(widget)
        else:
            try:
                self.config.set(key, data_value)
                self.set_normal_style(widget)
                self.callback(key, text)
            except Exception as e:
                self.set_error_style(widget)

    def set_error_style(self, widget, message=None):
        """
        Apply an error style to the widget.

        Args:
            widget (QWidget): The widget to style.
            message (str, optional): Optional error message to display.
        """
        if not widget.property("originalStyle"):
            widget.setProperty("originalStyle", widget.styleSheet())
        widget.setStyleSheet(self.error_style)
        if message:
            widget.setText(message)

    def set_normal_style(self, widget):
        """
        Restore the widget's default style.

        Args:
            widget (QWidget): The widget to restore.
        """
        original_style = widget.property("originalStyle")
        widget.setStyleSheet("color: Silver;")

    def set_text(self, widget, data):
        """
        Update the widget's text with the provided value.

        Args:
            widget (QWidget): The widget to update.
            data (str or dict): The data to display in the widget.
        """
        str_value = to_text(data)

        self.widget.blockSignals(True)  # Block signals.  Don't reprocess widget update

        if isinstance(widget, QComboBox):
            widget.setCurrentText(str_value)
        elif isinstance(widget, (QLineEdit, QTextEdit)):
            # Remove enclosing braces or brackets, if present
            if str_value.startswith(("{", "[")) and str_value.endswith(("}", "]")):
                str_value = str_value[1:-1]

            if widget.isReadOnly():
                # Process key-value pairs individually
                tokens = str_value.split(",")  # Split into tokens
                processed_tokens = []

                for token in tokens:
                    token = token.strip()  # Trim whitespace
                    if ":" in token:  # Handle key-value pairs
                        key, value = map(str.strip, token.split(":", 1))

                        # Remove quotes from key
                        if key.startswith(("'", '"')) and key.endswith(("'", '"')):
                            key = key[1:-1]

                        # Process value
                        if value.startswith(("'", '"')) and value.endswith(("'", '"')):
                            inner_value = value[1:-1]
                            if inner_value:  # Non-blank value, remove enclosing quotes
                                value = inner_value  # Blank values retain their quotes (e.g., '')

                        processed_tokens.append(f"{key}: {value}")
                    else:
                        # Handle non key-value tokens (if any)
                        processed_tokens.append(token)

                str_value = ", ".join(processed_tokens)  # Reassemble tokens


            if isinstance(widget, QTextEdit):
                widget.setPlainText(str_value)
            else:
                widget.setText(str_value)
        else:
            self.widget.blockSignals(False)  # Block signals
            raise TypeError(f"Unsupported widget type for setting value: {type(widget)}")

        self.widget.blockSignals(False)  # Block signals


def get_text(widget):
    """
    Retrieve the text value from a widget.

    Args:
        widget (QWidget): The widget to retrieve the value from.

    Returns:
        str: The current text of the widget.
    """
    if isinstance(widget, QComboBox):
        return widget.currentText()
    elif isinstance(widget, QTextEdit):
        return widget.toPlainText()
    return widget.text()
