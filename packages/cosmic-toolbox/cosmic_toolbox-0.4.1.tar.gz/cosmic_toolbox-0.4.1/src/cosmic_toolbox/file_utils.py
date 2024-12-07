# Copyright (C) 2017 ETH Zurich
# Cosmology Research Group
# Author: Joerg Herbel


import distutils.dir_util
import os
import pickle
import shlex
import shutil
import stat
import subprocess

import copy_guardian
import h5py
import yaml

from cosmic_toolbox.logger import get_logger

DEFAULT_ROOT_PATH = ""
LOGGER = get_logger(__file__)


def robust_remove(path):
    """
    Remove a file or directory.

    :param path: Path to the file or directory.
    """
    if is_remote(path):
        LOGGER.info("Removing remote directory {}".format(path))
        host, path = path.split(":")
        cmd = 'ssh {} "rm -rf {}"'.format(host, path)
        subprocess.call(shlex.split(cmd))

    else:
        if os.path.isfile(path):
            os.remove(path)

        elif os.path.isdir(path):
            shutil.rmtree(path)

        else:
            LOGGER.warning(f"Cannot remove {path} because it does not exist")


def write_to_pickle(filepath, obj, compression="none"):
    """
    Write an object to a pickle file.

    :param filepath: Path to the pickle file.
    :param obj: Object to write.
    :param compression: Compression method to use. Can be "none", "lzf" or "bz2".
    """
    if compression.lower() == "none":
        with open(filepath, "wb") as f:
            pickle.dump(obj, f)
    elif compression.lower() == "lzf":
        import lzf

        with lzf.open(filepath, "wb") as f:
            pickle.dump(obj, f)
    elif compression.lower() == "bz2":
        import bz2

        with bz2.open(filepath, "wb") as f:
            pickle.dump(obj, f)

    else:
        raise Exception(f"uknown compression {compression} [none, lzf, bz2]")


def read_from_pickle(filepath, compression="none"):
    """
    Read an object from a pickle file.

    :param filepath: Path to the pickle file.
    :param compression: Compression method to use. Can be "none", "lzf" or "bz2".
    :return: Object read from the pickle file.
    """
    if compression.lower() == "none":
        with open(filepath, "rb") as f:
            obj = pickle.load(f)
    elif compression.lower() == "lzf":
        import lzf

        with lzf.open(filepath, "rb") as f:
            obj = pickle.load(f)
    elif compression.lower() == "bz2":
        import bz2

        with bz2.open(filepath, "rb") as f:
            obj = pickle.load(f)

    else:
        raise Exception(f"uknown compression {compression} [none, lzf, bz2]")

    return obj


def write_to_hdf(filepath, obj, name="data", **kwargs):
    """
    Write an object to an hdf5 file.

    :param filepath: Path to the hdf5 file.
    :param obj: Object to write.
    :param name: Name of the dataset.
    :param kwargs: Additional arguments passed to h5py.File.create_dataset.
    """

    with h5py.File(filepath, "w") as f:
        f.create_dataset(name, data=obj, **kwargs)


def read_from_hdf(filepath, name="data"):
    """
    Read an object from an hdf5 file.

    :param filepath: Path to the hdf5 file.
    :param name: Name of the dataset.
    :return: Object read from the hdf5 file.
    """

    with h5py.File(filepath, "r") as f:
        obj = f[name][:]

    return obj


def load_from_hdf5(file_name, hdf5_keys, hdf5_path="", root_path=DEFAULT_ROOT_PATH):
    """
    Load data stored in a HDF5-file.
    :param file_name: Name of the file.
    :param hdf5_keys: Keys of arrays to be loaded.
    :param hdf5_path: Path within HDF5-file appended to all keys.
    :param root_path: Relative or absolute root path.
    :return: Loaded arrays.
    """

    if str(hdf5_keys) == hdf5_keys:
        hdf5_keys = [hdf5_keys]
        return_null_entry = True
    else:
        return_null_entry = False

    hdf5_keys = [hdf5_path + hdf5_key for hdf5_key in hdf5_keys]

    path = get_abs_path(file_name, root_path=root_path)

    with h5py.File(path, mode="r") as hdf5_file:
        hdf5_data = [hdf5_file[hdf5_key][...] for hdf5_key in hdf5_keys]

    if return_null_entry:
        hdf5_data = hdf5_data[0]

    return hdf5_data


def get_abs_path(path):
    if "@" in path and ":/" in path:
        abs_path = path

    elif os.path.isabs(path):
        abs_path = path

    else:
        if "SUBMIT_DIR" in os.environ:
            parent = os.environ["SUBMIT_DIR"]
        else:
            parent = os.getcwd()

        abs_path = os.path.join(parent, path)

    return abs_path


def robust_makedirs(path):
    if is_remote(path):
        LOGGER.info("Creating remote directory {}".format(path))
        host, path = path.split(":")
        cmd = 'ssh {} "mkdir -p {}"'.format(host, path)
        subprocess.call(shlex.split(cmd))

    elif not os.path.isdir(path):
        os.makedirs(path)
        LOGGER.info("Created directory {}".format(path))


def robust_copy(
    src,
    dst,
    n_max_connect=50,
    method="CopyGuardian",
    folder_with_many_files=False,
    **kwargs,
):
    """
    Copy files/directories using the specified method.

    :param src: Source file/directory.
    :param dst: Destination file/directory.
    :param n_max_connect: Maximum number of simultaneous connections.
    :param method: Method to use for copying. Can be "CopyGuardian" or "system_cp".
    :param folder_with_many_files: If True, the source is a folder with many files (only for CopyGuardian).
    :param kwargs: Additional arguments passed to the copy method.
    """
    src = _ensure_list(src)
    if str(dst) != dst:
        raise ValueError(
            "Destination {} not supported. Multiple destinations for "
            "multiple sources not implemented.".format(dst)
        )

    # In case of a remote destination, rsync will create the directory itself
    if not is_remote(dst):
        robust_makedirs(os.path.dirname(dst))

    if method == "CopyGuardian":
        copy_with_copy_guardian(
            src,
            dst,
            n_max_connect=n_max_connect,
            folder_with_many_files=folder_with_many_files,
        )

    elif method == "system_cp":
        system_copy(sources=src, dest=dst, **kwargs)

    else:
        raise Exception(f"Unknown copy method {method}")


def _ensure_list(obj):
    if not isinstance(obj, list):
        return [obj]
    return obj


def copy_with_copy_guardian(
    sources,
    destination,
    n_max_connect=10,
    timeout=1000,
    folder_with_many_files=False,
):
    """
    Copy files/directories using the CopyGuardian.

    :param sources: List of source files/directories.
    :param destination: Destination directory.
    :param n_max_connect: Maximum number of simultaneous connections.
    :param timeout: time in seconds to wait for a connection to become available
    :param folder_with_many_files: If True, the source is a folder with many files
    """
    with copy_guardian.BoundedSemaphore(n_max_connect, timeout=timeout):
        for src in sources:
            LOGGER.info("Copying locally: {} -> {}".format(src, destination))
            if os.path.isdir(src):
                if folder_with_many_files:
                    LOGGER.debug("Copying folder with many files")
                    # robust_makedirs(destination)
                    copy_guardian.copy_utils.copy_local_folder(src, destination)
                else:
                    distutils.dir_util.copy_tree(src, destination)
            elif os.path.isdir(destination):
                shutil.copy(src, destination)
            else:
                shutil.copyfile(src, destination)


def system_copy(sources, dest, args_str_cp=""):
    cmd = "cp -r " + args_str_cp
    for f in sources:
        cmd += f" {f} "
    cmd += " {}".format(dest)
    LOGGER.debug("Copying {} files to {}".format(len(sources), dest))
    LOGGER.debug(cmd)
    os.system(cmd)


def is_remote(path):
    return "@" in path and ":/" in path


def read_yaml(filename):
    with open(filename) as f:
        file = yaml.load(f, Loader=yaml.Loader)
    return file


def ensure_permissions(path, verb=False):
    val = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    os.chmod(path, val)
    if verb:
        LOGGER.debug("Changed permissions for {} to {}".format(path, oct(val)))
