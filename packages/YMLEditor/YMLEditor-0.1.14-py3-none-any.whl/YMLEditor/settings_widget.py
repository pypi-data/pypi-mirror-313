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

#
#
from typing import List

from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QSpacerItem, QSizePolicy, QVBoxLayout

from YMLEditor.item_widget import ItemWidget


class SettingsWidget(QWidget):
    """
    Provides a configurable user interface for editing settings in a YAML config file.

    - Displays settings based on the user-supplied layout which defines:
      type of control (text field, combo box, etc.) and the key for retrieving
      each field. See project readme for a list of supported widgets and options.
    - Handles changes made to widgets by syncing the updated values back to `Config` data.
    - `Config` supports `get`, `set` data and `load`, and `save` to the YAML config file.
    - Validates user input according to provided rules (regular expressions).
    - Highlights the entry if there is an error.
    - Supports full redisplay if a specified configuration key changes.
    - Supports data fields that are lists, dictionaries, or scalar (int, string, etc.)
    - Does not support fields that are complex nested data structures.
    - Supports switching between multiple formats (e.g., "basic" vs "expert" format).

    Attributes:
        config (Config): The config file handler object.  Supports get, set, save, load.
        formats (dict): Defines display format and input validation rules for each field. See
        project readme for details.
        redisplay_keys (list of str): A list of keys that trigger a full redisplay of the UI

    **Methods**:
    """

    def __init__(self, config, formats, mode, redisplay_keys=None, verbose=1):
        """
        Initialize the settings widget.

        Args:
            config (Config): Configuration object to load, update, and store settings.
            formats (dict): Display formats for different modes.
            mode (str): Used to select between multiple layout formats.
            redisplay_keys (List): Updates to these keys will trigger a full redisplay.
            verbose (int): The verbosity level. Defaults to 1.
        """
        super().__init__()

        self.config = config
        self.verbose = verbose
        self.formats = formats
        self._mode = mode  # Select which format within formats to use
        self.validate_format(formats, mode)
        self.ignore_changes = False
        self.is_loaded = False
        self.redisplay_keys = redisplay_keys  # Keys that trigger full UI redisplay
        self.config_widgets = []

        # Set up the top-level layout once
        self.main_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)
        self._setup_ui()

    def set_layout(self, mode):
        """
        Change the current display mode and redisplay the UI.

        Args:
            mode (str): The new mode to switch to.

        Raises:
            ValueError: If the specified mode is not a valid key in `formats`.
        """
        if mode not in self.formats:
            raise ValueError(f"Invalid mode '{mode}'. Must be one of: {list(self.formats.keys())}")

        self._mode = mode
        self.format = self.formats[mode]  # Update the format based on the new mode

        self.clear_layout()
        self._setup_ui()
        self.display()

    def _setup_ui(self):
        """
        Create and arrange widgets based on the format.

        Raises:
            ValueError: If 'self.formats' is not set or is not a dictionary.
            KeyError: If the key in 'self.mode' is not found in 'self.formats'.
            Exception: If an error occurs while setting up a widget, with details on the row and key.
        """
        # Clear the grid layout without removing the top-level layout
        self.clear_layout()

        row, data_key, format_row = -1, None, None
        fmt = self.formats[self._mode]  # Get format for the current mode

        try:
            for row, (data_key, format_row) in enumerate(fmt.items()):
                label_text, widget_type, options, width = format_row

                # Create specified ConfigWidget
                config_item = ItemWidget(
                    self.config, widget_type, None, options, self.on_change, width, data_key,
                    verbose=self.verbose
                )

                self.config_widgets.append(config_item)

                # Add label to col 0
                label = QLabel(label_text)
                label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                self.grid_layout.addWidget(label, row, 0)

                # Add widget to col 1
                self.grid_layout.addWidget(config_item.widget, row, 1)

                # Add spacer item to col 2 to force items left
                h_spacer = QSpacerItem(
                    1, 1, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum
                )
                self.grid_layout.addItem(h_spacer, row, 2)

        except Exception as e:
            raise Exception(
                f"Error setting up widget at row {row} with key '{data_key}'\n"
                f"Expected a tuple of (label_text, widget_type, options, width), but got "
                f"{format_row}'.\n"
                f"{str(e)}"
            ) from e

        # Add an expanding spacer item
        v_spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.grid_layout.addItem(v_spacer, self.grid_layout.rowCount(), 0, 1, 3)

    def clear_layout(self):
        """
        Clear the current settings widget layout.
        """
        self._clear_layout(self.grid_layout)

    def _clear_layout(self, layout):
        """
        Remove all items from a layout.

        Args:
            layout (QLayout): The layout to clear.
        """
        self.config_widgets = []
        self.is_loaded = False
        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()
            if widget:
                widget.deleteLater()

            nested_layout = item.layout()
            if nested_layout:
                self._clear_layout(nested_layout)

    def display(self):
        """
        Update data from the Config data to the display widgets. Each widget's value is
        set based on the corresponding configuration key's value.
        """
        self.ignore_changes = True  # Temporarily ignore changes during synchronization
        if len(self.config_widgets) == 0:
            self._setup_ui()  # Initialize the UI if it hasn't been set up

        # Iterate over each item in the layout to update widget values from config
        for widget_item in self.config_widgets:
            widget_item.display()

        self.ignore_changes = False  # Re-enable change tracking after sync
        self.is_loaded = True  # Mark the display as loaded

    def save(self):
        """
        Save the current data to the configuration file
        """
        if self.is_loaded:
            self.config.save()

    def undo(self):
        """
        Reverts data to last snapshot and refreshes display
        """
        self.config.snapshot_undo()
        self.display()

    def on_change(self, key, value):
        """
        Do full redisplay if key is in redisplay_keys.  Called by ItemWidget
        after it has updated data from a user edit.

        Args:
            key (str): The key that changed.
            value (str): The value that changed.

        """
        # Force full redisplay if the key is in the redisplay list
        if key and self.redisplay_keys is not None:
            if key in self.redisplay_keys:
                self.display()

    def validate_format(self, formats, mode):
        """
        Validate the display format

        Args:
            formats (dict): A dictionary defining display formats.
            mode (str): Used to select between multiple layout formats

        Raises:
            ValueError: If 'formats' is not formatted properly.
            KeyError: If 'mode' is not a format in formats.
        """
        # Validate 'formats' as a non-empty dictionary
        if not formats or not isinstance(formats, dict):
            raise ValueError(
                f"'formats' must be a non-empty dictionary. Current type: {type(formats).__name__}"
            )

        # Validate format mode is in 'formats'
        if mode not in formats:
            raise KeyError(
                f"Unknown mode '{mode}' in 'formats'. Available modes: {list(formats.keys())}"
            )

        format_def = formats[mode]  # Get format for the current mode

        # Validate the entries in the format
        for row, (key, value) in enumerate(format_def.items()):
            # Validate format line
            if not isinstance(value, tuple) or len(value) != 4:
                raise ValueError(
                    f"Format for key '{key}' is invalid at row {row}. Expected tuple:  "
                    f"(label_text, widget_type, options, width), but got: {value}"
                )
