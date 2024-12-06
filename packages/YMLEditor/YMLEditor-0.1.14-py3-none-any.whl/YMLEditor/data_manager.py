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
#
from abc import ABC, abstractmethod
import copy
import os
from typing import List, Any, Dict, Iterator, Union


class DataManager(ABC):
    """
       Base class for managing data, providing functions for: load, save, get, set, and
       undo.

       Subclasses are created for specific file formats and must support: `_load_data` and
       `_save_data`.

       Attributes:
           _data (Union[Dict, List]): The main data structure being managed (dictionary or list).
           file_path (str): Path to the file associated with the data.
           directory (str): Directory containing the file.
           unsaved_changes (bool): Indicates if there are unsaved changes in the data.
           snapshots (List): Stack of snapshots for supporting undo functionality.
           max_snapshots (int): Maximum number of snapshots retained for undo operations.
           proxy_mapping (Dict): Maps keys to proxy files for granular build system dependencies.

        **Methods**:
       """

    def __init__(self, verbose=1):
        """Initialize """
        self.verbose = verbose
        self._data = None
        self.file_path = None
        self.directory = None
        self.unsaved_changes = False
        self.snapshots = []  # stack to store snapshots of _data for undo
        self.handler = DataHandler(verbose)  # the handler for our data type
        self.max_snapshots = 6  # Maximum number of snapshots to retain for undo
        self.proxy_mapping = {}  # Dictionary to map keys to proxy files

    @abstractmethod
    def _load_data(self, f) -> Union[Dict, List]:
        """
         Load data from a file and return as a dictionary or list.
         Subclasses must implement this method to define file-specific behavior.

         Args:
             f: File object to load data from.

         Returns:
             Union[Dict, List]: The loaded data.

         Raises:
            ValueError: If the file is empty or cannot be parsed.
         """
        raise NotImplementedError(
            f"Subclass must implement {self.__class__.__name__}._load_data()"
        )

    @abstractmethod
    def _save_data(self, f, data):
        """
        Save data to a file.
        Subclasses must implement this method to define file-specific behavior.

        Args:
            f: File object to save data to.
            data: Data to be saved.
        Raises:
            RuntimeError: If the file cannot be saved.
        """
        raise NotImplementedError(
            f"Subclass must implement {self.__class__.__name__}._save_data()"
        )

    def load(self, path):
        """
        Load data from the specified file and initialize state.
        Create an initial snapshot for undo functionality.

        Args:
            path (str): Path to the file to load.

        Returns:
            bool: True if the file was loaded successfully.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If there is an issue reading the file.
            ValueError: If the file contents are invalid.
        """
        # Clear any proxy keys
        self.proxy_mapping = {}  # Dictionary to map keys to proxy files
        self.file_path = path
        self.directory = os.path.dirname(path)

        try:
            with open(path, self.get_open_mode()) as f:
                self.init_data(self._load_data(f))
                self.unsaved_changes = False
            return True
        except FileNotFoundError:
            self.warn(f"Error: File not found: {path}")
        except IOError as e:
            self.warn(f"Error: File: {path}\n{e}")
        except ValueError as e:
            self.warn(f"Error: Invalid file contents using {self.__class__.__name__}: {path}\n{e}")
        except Exception as e:
            self.warn(f"Error loading:  {self.__class__.__name__}: {path}\n{e}")
        return False

    def get_open_mode(self, write=False):
        """
        Provides the file mode for the data file.
        Default is 'w' for write mode, 'r' for read mode.
        Override for binary or other modes.

        Args:
            write (bool): Whether the file is being opened for writing.

        Returns:
            str: 'w' for write mode, 'r' for read mode.
        """
        return 'w' if write else 'r'

    def save(self):
        """
        Save the current data to the file if it has been modified.
        Create a snapshot of the data for undo feature.

        Returns:
            bool: True if the file was saved successfully.

        Raises:
            ValueError: If the file path or data is None.
        """
        if self.file_path is None:
            raise ValueError("Save Error: File path: cannot be None")

        if self._data is None:
            raise ValueError("Save Error: Data cannot be None")

        if self.unsaved_changes:
            self.snapshot_push()  # Push the current data to snapshot stack
            try:
                with open(self.file_path, self.get_open_mode(write=True)) as f:
                    self._save_data(f, self._data)
                self.unsaved_changes = False
                return True
            except Exception as e:
                self.warn(f"Error saving: {self.file_path}\n{e}")
                return False

    def set(self, key, value):
        """
        Update the data with a new value and touch proxy file if key in proxy list.

        Args:
            key: Key for the data.
            value: New value to set.
        """
        self.unsaved_changes = True
        self.__setitem__(key, value)

        # Check if updating this key should trigger a touch to a proxy_file
        if proxy_file := self._get_proxy(key):
            touch_file(proxy_file)

    def get(self, key_or_index, default=None):
        """
        Retrieve a value from the data, returning a default if not found.

        Args:
            key_or_index: Key or index for the data.
            default: Default value to return if the key or index is not found.

        Returns:
            The value associated with the key or index, or the default.
        """
        value = self.__getitem__(key_or_index)
        return value if value is not None else default

    def __getitem__(self, key_or_index):
        """
        Retrieve a value from the data using the specified key or index.

        Args:
            key_or_index: Key or index for the data.

        Returns:
            The value associated with the specified key or index.
        """
        return self.handler.__getitem__(self._data, key_or_index)

    def __setitem__(self, key, value):
        """
        Update the data with a new value at the specified key or index.

        Args:
            key: Key or index for the data.
            value: New value to set.
        """
        self.handler.__setitem__(self._data, key, value)
        self.unsaved_changes = True

    def insert(self, key, value):
        """
        Insert a new item into the data.

        Args:
            key: Key or index for the new item.
            value: Value to insert.
        """
        self.handler.insert(self._data, key, value)
        self.unsaved_changes = True

    def delete(self, key):
        """
        Remove an item from the data.

        Args:
            key: Key or index of the item to remove.
        """
        self.handler.delete(self._data, key)
        self.unsaved_changes = True

    def snapshot_undo(self):
        """
        Restore the data to the previous state using the snapshot stack.

        The first snapshot remains in the stack to always allow undo to initial state.
        """
        if not self.snapshots:
            return

        # Pop last snapshot unless it is the only one left, always keep initial snapshot
        if len(self.snapshots) > 1:
            self._data = self.snapshots.pop()
        else:
            self._data = copy.deepcopy(self.snapshots[0])

        self.unsaved_changes = True  # Data has been modified


    def snapshot_push(self):
        """
        Push the current state of the data to snapshot stack for undo functionality.

        If the maximum number of snapshots is reached, the second-oldest snapshot is removed.
        The oldest is always retained for return to initial state.
        """
        if len(self.snapshots) >= self.max_snapshots:
            # Stack is full.  Remove the second-oldest snapshot
            self.snapshots.pop(1)

        # Create a deep copy of _data to store as a snapshot
        self.snapshots.append(copy.deepcopy(self._data))

    def __len__(self):
        """
        Get the number of items in the data.

        Returns:
            int: Number of items in the data.
        """
        if self._data:
            return len(self._data)
        else:
            return 0

    def items(self):
        """
        Get an iterator over the items in the data.

        Returns:
            Iterator: An iterator over the data items.
        """
        return self.handler.items(self._data)

    def init_data(self, data: Union[Dict[str, Any], List[Any]]):
        """
        Initialize the data

        Args:
            data (Dict[str, Any]): New data to initialize.
        """
        self.snapshots = []
        self._data = data
        self.snapshot_push()  # Save the initial state
        self.unsaved_changes = True

    def create(self, data: Dict[str, Any]):
        """
        Create a new config file with the specified data.

        Args:
            data (Dict[str, Any]): Data to save in the new file.
        """
        self.init_data(data)
        self.save()

    def add_proxy(self, proxy_file, proxy_update_keys):
        """
        Add a proxy file and its associated update keys.
        If any of these keys are updated, they will trigger a touch to this proxy_file.
        This can be used to improve the granularity of dependencies for build management systems.
        The build system can set a dependency on the proxy_file which is only updated for a subset
        of fields in the config file rather than rebuilding from any change to the config file.

        Args:
            proxy_file (str): The file to touch when any associated key is updated.
            proxy_update_keys (List[str]): List of keys that trigger a touch to this proxy_file.
        """
        for key in proxy_update_keys:
            if key in self.proxy_mapping:
                raise ValueError(
                    f"Key '{key}' is already associated with another proxy file: "
                    f"{self.proxy_mapping[key]}"
                )
            self.proxy_mapping[key] = proxy_file

    def _get_proxy(self, key):
        """
        Retrieve the proxy file associated with a given key, if set.

        Args:
            key (str): The key to look up.

        Returns:
            str or None: The proxy file associated with the key, or None if not found.
        """
        return self.proxy_mapping.get(key)

    def warn(self, message):
        if self.verbose > 0:
            print(message)


def touch_file(filename):
    """
    Set the file's modification and access time to the current time.

    Args:
        filename (str): Path to the file.
    """
    with open(filename, 'a'):
        os.utime(filename, None)


class DataHandler(ABC):
    """
    A class for managing nested dictionary and list structures with abstract methods
    for getting, setting, and iterating over elements.
    """

    def __init__(self, verbose: int = 1):
        """
        Initialize the DataHandler.

        Args:
            verbose (int): Verbosity level for logging warnings. Defaults to 1.
        """
        self.verbose = verbose

    def insert(self, data_list: list, idx: int, item: Any) -> None:
        """
        Insert an item into a list at the specified index.

        Args:
            data_list (list): The list to modify.
            idx (int): The index to insert the item.
            item (Any): The item to insert.

        Raises:
            ValueError: If the data is not a list.
            IndexError: If the index is out of range.
        """
        if not isinstance(data_list, list):
            raise ValueError("Insert operation is only supported for lists.")
        if not (0 <= idx <= len(data_list)):
            raise IndexError(f"Index {idx} is out of range for insertion.")
        data_list.insert(idx, item)


    def delete(self, data: Union[Dict, list], idx: Union[str, int]) -> None:
        """
        Delete an item from a dictionary or list.

        Args:
            data (Dict or list): The data structure to modify.
            idx (str or int): The key (for dict) or index (for list) to delete.

        Raises:
            TypeError: If the data type is unsupported.
            KeyError: If the key is not found in a dictionary.
            IndexError: If the index is out of range for a list.
        """
        if isinstance(data, dict):
            if idx in data:
                del data[idx]
            else:
                raise KeyError(f"Key '{idx}' not found in dictionary.")
        elif isinstance(data, list):
            if not isinstance(idx, int):
                raise TypeError(f"List indices must be integers, got '{type(idx).__name__}'.")
            if 0 <= idx < len(data):
                del data[idx]
            else:
                raise IndexError(f"Index {idx} out of range for list.")
        else:
            raise TypeError("Delete operation is only supported for dicts and lists.")

    def __getitem__(self, data: Union[Dict, list], key) -> Any:
        """Retrieve a value from nested data."""
        return self._access_item(data, key, set_item=False)

    def __setitem__(self, data: Union[Dict, list], key, value: Any) -> None:
        """Set a value in nested data."""
        self._access_item(data, key, value=value, set_item=True)

    def _access_item(
            self, data: Union[Dict, list], key: str, value: Any = None, set_item: bool = False
            ) -> Any:
        """
        Internal method for getting or setting values in nested data structures.
        """
        key = self.replace_indirect(data, key)

        try:
            container, final_key = self._navigate_hierarchy(data, key, create_missing=set_item)
            if isinstance(container, dict):
                if set_item:
                    container[final_key] = value
                else:
                    return container[final_key]
            elif isinstance(container, list):
                index = self._validate_index(final_key)
                if set_item:
                    while index >= len(container):
                        container.append(None)
                    container[index] = value
                else:
                    return container[index]
            else:
                raise TypeError("Unsupported container type.")
        except (KeyError, IndexError, ValueError, TypeError) as e:
            self.warn(f"Error {'setting' if set_item else 'getting'} key '{key}': {e}")
            return None

    def _navigate_hierarchy(self, data: Union[Dict, List], key: str, create_missing: bool = False):
        """
        Navigate nested hierarchies within dictionaries or lists.

        Args:
            data (Union[Dict, List]): The data structure to navigate.
            key (str): A dot-separated key path (e.g., "a.b.2.c").
            create_missing (bool): Whether to create missing intermediate nodes.

        Returns:
            Tuple[Union[Dict, List], str]: A tuple containing the target container and the last
            key or index.

        Raises:
            KeyError: If a dictionary key is missing and `create_missing` is False.
            IndexError: If a list index is out of range and `create_missing` is False.
            TypeError: If an unsupported type is encountered during navigation.
            ValueError: If a list index is not a valid integer.
        """
        if isinstance(key, str):
            keys = key.split(".")
        else:
            keys = [key]

        target = data

        for k in keys[:-1]:
            if isinstance(target, dict):
                if create_missing:
                    target = target.setdefault(k, {})
                else:
                    if k not in target:
                        raise KeyError(f"Key '{k}' not found in dictionary.")
                    target = target[k]
            elif isinstance(target, list):
                index = self._validate_index(k)
                if create_missing:
                    # Extend the list to accommodate the index if out of range
                    if index >= len(target):
                        target.extend({} for _ in range(index - len(target) + 1))
                elif index >= len(target):
                    raise IndexError(f"Index {index} out of range for list.")
                target = target[index]
            else:
                raise TypeError(f"Cannot navigate through {type(target).__name__}.")

        return target, keys[-1]


    def items(self, data: Union[Dict, list]) -> Iterator:
        """Return an iterator over key-value or index-value pairs."""
        if isinstance(data, dict):
            return iter(data.items())
        elif isinstance(data, list):
            return iter(enumerate(data))
        else:
            raise TypeError("Items method only supports dicts and lists.")

    def replace_indirect(self, data: Dict, key: str) -> Union[str, None]:
        """
        Resolve indirect key references in a string.

        Args:
            data (Dict): Dictionary containing potential indirect references.
            key (str): The key to resolve.

        Returns:
            Union[str, None]: The resolved key, or None if the reference could not be resolved.

        Notes:
            - If the key is not a string, it is returned as is.
            - If the key contains '@' for indirect references, it tries to resolve the reference.
        """
        if not isinstance(key, str):
            return key

        if "@" in key:
            try:
                main_key, indirect_ref = key.split("@", 1)
            except ValueError:
                self.warn(f"Invalid indirect key format: '{key}'")
                return None

            ref = data.get(indirect_ref)
            if ref is not None:
                return f"{main_key}{ref}"
            else:
                self.warn(f"Indirect key reference '{indirect_ref}' not found in data.")
                return None

        return key

    def _validate_index(self, key: str) -> int:
        """
        Validate and convert a key to an integer index for list access.

        Args:
            key (str): The key to validate.

        Returns:
            int: The validated integer index.

        Raises:
            ValueError: If the key is not a valid integer.
        """
        try:
            return int(key)
        except ValueError:
            raise ValueError(f"Key '{key}' is not a valid integer index for list access.")

    def warn(self, message: str) -> None:
        """Print a warning message if verbosity is enabled."""
        if self.verbose > 0:
            print(f"Warning: {message}")