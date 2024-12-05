import hashlib
import os
import shutil
import stat
import tarfile
import zipfile
from pathlib import Path


def ensure_folder(path):
    if isinstance(path, Path):
        path = str(path)

    os.makedirs(path, exist_ok=True)
    return path


def clear_folder(path, mkdir_if_not_exist=True):
    """
    Given a folder, remove files and sub folders to make it empty.
    The given folder itself will not be deleted.

    :param path: The folder to be cleared.
    :param mkdir_if_not_exist: Whether to make directory if the folder doesn't exist.
    :return: The folder itself.
    """
    if isinstance(path, Path):
        path = str(path)

    if not os.path.exists(path):
        if mkdir_if_not_exist:
            return ensure_folder(path)
        return

    # Handle files which are readonly
    def on_rm_error(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    shutil.rmtree(path, onerror=on_rm_error)
    ensure_folder(path)
    return path


def _validate_overwrite(save_to: str, overwrite_if_exists: bool):
    """Raise Exception if save_to exists, and overwrite_if_exists=False

    :param save_to: file system path
    :param overwrite_if_exists: bool
    :return: None
    """
    if os.path.exists(save_to) and not overwrite_if_exists:
        raise FileExistsError(f"Save destination path {save_to} exists. "
                              f"Please set overwrite_if_exists=True if you want to overwrite it.")


def make_file_name(base_name, extension):
    return f"{base_name}.{extension}"


def make_full_path(parent_folder, base_name, extension):
    file_name_with_extension = make_file_name(base_name, extension)
    return os.path.join(parent_folder, file_name_with_extension)


def get_file_name(full_path):
    from pathlib import Path
    return Path(full_path).name


def iter_files(path, recursive=True, predicate=lambda _: True):
    """
    Given a path, iterate all files inside it.

    :param path: The folder from with to find files from.
    :param recursive: Find sub folders if True, else find only given folder.
    :param predicate: Find files only when this function evaluates `True` when file full path as the param.
    :return: A generator generates the files which file name meets `predicate`.
    """
    if isinstance(path, Path):
        path = str(path)

    for cur_dir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(cur_dir, file)
            if predicate(full_path):
                yield full_path

        # break if non recursive
        if not recursive:
            break


def write_text_to_path(path: Path, text: str, verify_content_if_exists=False):
    """Write given text to the given file.

    :param path: The file to be written to.
    :param text: The text to be written.
    :param verify_content_if_exists: When specified, If file already exists,
           an error will be raised if the existing content is not identical with the text to be written.
    """
    if path.is_dir():
        raise ValueError(f"'path' should be a file, not a folder.")

    if path.is_file():
        if verify_content_if_exists:
            old_text = path.read_text()
            if old_text != text:
                raise ValueError(f"File {path} already exists but with a different content, " f"unable to overwrite.")
            else:
                # Do nothing, return as succeed
                return

    # Write the text to file
    ensure_folder(path.parent)
    path.write_text(text)


def make_zipfile(zip_file_path, folder_or_file_to_zip, exclude_function=None):
    """Create an archive with exclusive files or directories. Adapted from shutil._make_zipfile.

    :param zip_file_path: Path of zip file to create.
    :param folder_or_file_to_zip: Directory or file that will be zipped.
    :param exclude_function: Function of exclude files or directories
    """
    with zipfile.ZipFile(zip_file_path, "w") as zf:
        if os.path.isfile(folder_or_file_to_zip):
            zf.write(folder_or_file_to_zip, os.path.basename(folder_or_file_to_zip))
        else:
            for dirpath, dirnames, filenames in os.walk(folder_or_file_to_zip):
                relative_dirpath = os.path.relpath(dirpath, folder_or_file_to_zip)
                for name in sorted(dirnames):
                    full_path = os.path.normpath(os.path.join(dirpath, name))
                    relative_path = os.path.normpath(os.path.join(relative_dirpath, name))
                    if exclude_function and exclude_function(full_path):
                        continue
                    zf.write(full_path, relative_path)
                for name in filenames:
                    full_path = os.path.normpath(os.path.join(dirpath, name))
                    relative_path = os.path.normpath(os.path.join(relative_dirpath, name))
                    if exclude_function and exclude_function(full_path):
                        continue
                    if os.path.isfile(full_path):
                        zf.write(full_path, relative_path)


def make_tarfile(tar_file_path, folder_or_file_to_tar, mode="w"):
    tar = tarfile.open(tar_file_path, mode=mode)
    for root, dir, files in os.walk(folder_or_file_to_tar):
        for file in files:
            fullpath = os.path.join(root, file)
            tar.add(fullpath)

    tar.close()


def md5_file(f):
    h = hashlib.md5()
    with open(f, 'rb') as fin:
        h.update(fin.read())
    return h.hexdigest()


def is_xml_file(path):
    _, extension = os.path.splitext(path)
    return extension.lower() == '.xml'


def is_json_file(path):
    _, extension = os.path.splitext(path)
    return extension.lower() == '.json'


def iter_xml_files(path, recursive=True):
    yield from iter_files(path, recursive=recursive, predicate=is_xml_file)


def iter_json_files(path, recursive=True):
    yield from iter_files(path, recursive=recursive, predicate=is_json_file)


def unzip_dir(zip_file_path, dst_dir_path, overwrite_if_exists=True):
    """unzip zip_file_path to dst_dir_path

    :param zip_file_path: path to zip file
    :param dst_dir_path: destination directory path
    :param overwrite_if_exists: whether or not overwrite dst_dir_path if it exists
    :return: None
    """
    _validate_overwrite(dst_dir_path, overwrite_if_exists)
    clear_folder(dst_dir_path)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        zip_file.extractall(dst_dir_path)


class ExecuteInDirectory:
    def __init__(self, file_path, is_directory=False):
        # The reason that explicitly pass a is_directory bool parameter
        # is os.path.isfile/os.path.isdir simply does't work well on Windows
        if is_directory:
            self.target_dir = file_path
            self.target_file_name = None
        else:
            self.target_dir = os.path.dirname(file_path)
            self.target_file_name = os.path.basename(file_path)

    def __enter__(self):
        self.backup_cwd = os.getcwd()
        os.chdir(self.target_dir)

        if self.target_file_name:
            return self.target_file_name

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.backup_cwd)
