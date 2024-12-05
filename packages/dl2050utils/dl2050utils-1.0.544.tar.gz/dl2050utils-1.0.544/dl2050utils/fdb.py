import hashlib
import pathlib
from pathlib import Path
import numpy as np
from dl2050utils.common import pickle_save, pickle_load

class FileDB():
    """
    A class for managing file-based storage using a structured directory hierarchy,
    with an optional hashing mechanism for non-integer keys.
    Attributes:
        base_path (Path): The root directory for storing files.
        max_value (int): The maximum range for hashed values to avoid excessive directory depth.
    Methods:
        get_dir(key): Generates a directory path based on the hash or integer representation of the key.
        get_name(key, pre='', ext=''): Generates a file name based on the key, with optional prefix and extension.
        save(key, data, pre='', ext='', save_f=pickle_save): Saves data to a file in the appropriate directory.
        load(key, pre='', ext='', load_f=pickle_load): Loads data from a file based on the key, prefix, and extension.
    """

    def __init__(self, base_path, max_value=10**12):
        """
        Initializes FileDB with a specified base path and maximum hash value.
        Args:
            base_path (str or Path): The root directory where files will be stored.
            max_value (int, optional): Limits the hash range for directory distribution. Defaults to 10^12.
        """
        self.base_path,self.max_value = Path(base_path),max_value
        self.base_path.mkdir(parents=True, exist_ok=True)

    def get_dir(self, key):
        """
        Generates a nested directory path for a given key.
        Args:
            key (int or str): The unique identifier for the file. If a string, it is hashed using MD5.
        Returns:
            Path: A directory path within the base path, structured in 3-levels based on the key hash.
        """
        if type(key)==int:
            seq = key
        else:
            key = str(key)
            hash_object = hashlib.md5(key.encode('utf-8'))
            seq = int(hash_object.hexdigest(), 16)
        seq = seq % self.max_value
        s = f'{seq:012}'
        dir_path = Path(f'{self.base_path}/{s[:3]}/{s[3:6]}/{s[6:9]}')
        return dir_path
    
    def get_name(self, key, pre='', ext=''):
        """
        Generates a file name using the key, with optional prefix and extension.
        Args:
            key (int or str): The unique identifier for the file.
            pre (str, optional): A prefix for the file name.
            ext (str, optional): A file extension.
        Returns:
            str: The generated file name.
        """
        return f'{pre}{key}{ext}'
    
    def save(self, key, data, pre='', ext='', save_f=pickle_save, allow_pickle=False):
        """
        Saves data to a file in the directory corresponding to the key.
        Args:
            key (int or str): The unique identifier for the file.
            data (any): The data to be saved.
            pre (str, optional): A prefix for the file name.
            ext (str, optional): The file extension. Use '.npy' for NumPy arrays.
            save_f (callable, optional): The save function to use (defaults to pickle_save).
        Returns 0 if all goes well, 1 otherwise.
        """
        dir_path = Path(self.get_dir(key))
        dir_path.mkdir(parents=True, exist_ok=True)
        file_name = self.get_name(key, pre=pre, ext=ext)
        p = dir_path/file_name
        try:
            if ext=='.npy':
                np.save(p, data, allow_pickle=allow_pickle)
            else:
                save_f(p, data)
            return 0
        except Exception as exc:
            print(f'FileDB save Exception: {exc}')
            return 1

    def load(self, key, pre='', ext='', load_f=pickle_load, allow_pickle=False):
        """
        Loads data from a file based on the key, prefix, and extension.
        Args:
            key (int or str): The unique identifier for the file.
            pre (str, optional): A prefix for the file name.
            ext (str, optional): The file extension. Use '.npy' for NumPy arrays.
            load_f (callable, optional): The load function to use (defaults to pickle_load).
        Returns:
            any: The loaded data or None if the load failed.
        """
        dir_path = Path(self.get_dir(key))
        file_name = self.get_name(key, pre=pre, ext=ext)
        p = dir_path/file_name
        try:
            if ext=='.npy': return np.load(p, allow_pickle=allow_pickle)
            return load_f(p)
        except Exception as exc:
            print(f'FileDB load Exception: {exc}')
            return None
    
    def delete(self, key, pre='', ext=''):
        """
        Deletes file based on the key, prefix, and extension.
        Args:
            key (int or str): The unique identifier for the file.
            pre (str, optional): A prefix for the file name.
            ext (str, optional): The file extension. Use '.npy' for NumPy arrays.
        Returns 0 if all goes well, 1 otherwise.
        """
        dir_path = Path(self.get_dir(key))
        file_name = self.get_name(key, pre=pre, ext=ext)
        p = dir_path/file_name
        try:
            p.unlink()
            return 0
        except Exception as exc:
            print(f'FileDB delete Exception: {exc}')
            return 1
