import os

import h5py
import numpy as np
import pandas as pd
import six

from cosmic_toolbox import file_utils, logger

LOGGER = logger.get_logger(__file__)


def view_fields(rec, names):
    """
    `rec` must be a numpy structured array.
    `names` is the collection of field names to keep.

    Returns a view of the array `a` (not a copy).
    """
    dt = rec.dtype
    formats = [dt.fields[name][0] for name in names]
    offsets = [dt.fields[name][1] for name in names]
    itemsize = rec.dtype.itemsize
    newdt = np.dtype(
        dict(names=names, formats=formats, offsets=offsets, itemsize=itemsize)
    )
    rec_view = rec.view(newdt)
    return rec_view


def delete_cols(rec, col_names):
    """
    Delete columns from a numpy recarray.

    :param rec: numpy recarray
    :param col_names: list of names of the columns to delete
    :return: numpy recarray
    """
    col_names_all = list(rec.dtype.names)

    for col_name in col_names:
        if col_name in col_names_all:
            col_names_all.remove(col_name)

    if not col_names_all:
        # If no columns are left, return an empty recarray with an empty dtype
        return np.array([], dtype=[])

    return rec[col_names_all].copy()


def delete_columns(rec, col_names):
    """
    Delete columns from a numpy recarray. (alias for delete_cols for backwards compatibility)

    :param rec: numpy recarray
    :param col_names: list of names of the columns to delete
    """
    return delete_cols(rec, col_names)


def add_cols(rec, names, shapes=None, data=0, dtype=None):
    """
    Add columns to a numpy recarray. By default, the new columns are filled with zeros.
    If `data` is a numpy array, it is used to fill the new columns. If each column should
    should be filled with different data, `data` should be a list of numpy arrays or an
    array of shape (n_cols, n_rows).

    :param rec: numpy recarray
    :param names: list of names for the columns
    :param shapes: list of shapes for the columns
    :param data: data to fill the columns with
    :param dtype: dtype of the columns
    :return: numpy recarray
    """

    # check if new data should be sliced
    slice_data = isinstance(data, np.ndarray) and data.ndim == 2

    # create new recarray
    names = [str(name) for name in names]
    extra_dtype = get_dtype(names, shapes=shapes, main=dtype)
    newdtype = np.dtype(rec.dtype.descr + extra_dtype.descr)
    newrec = np.empty(rec.shape, dtype=newdtype)

    # add data to new recarray
    for field in rec.dtype.fields:
        newrec[field] = rec[field]
    for ni, name in enumerate(extra_dtype.fields):
        if slice_data:
            newrec[name] = data[ni]
        else:
            newrec[name] = np.array(data).astype(dtype)

    return newrec


def ensure_cols(rec, names, shapes=None, data=0):
    # find columns to add
    names = [str(name) for name in names]
    new_names = []
    for name in names:
        if get_dtype([name]).names[0] not in rec.dtype.names:
            new_names.append(name)

    # exit if no new cols
    if len(new_names) == 0:
        return rec

    # add new columns
    newrec = add_cols(rec, new_names, shapes=shapes, data=data)

    return newrec


def arr2rec(arr, names):
    """
    Convert a numpy array to a numpy structured array.

    :param arr: numpy array
    :param names: list of names for the columns
    :return: numpy structured array
    """
    arr = np.atleast_2d(arr)
    n_arr, n_params = arr.shape
    dtype = dict(formats=[], names=names)
    for i in range(n_params):
        dtype["formats"].append(arr[:, i].dtype)
    rec = np.zeros(n_arr, dtype=dtype)
    for i, name in enumerate(names):
        rec[name] = arr[:, i]
    return rec


def rec2arr(rec, return_names=False):
    """
    Convert a numpy structured array to a numpy array.

    :param rec: numpy structured array
    :param return_names: if True, also return the names of the columns
    :return: numpy array

    Example
    -------
    >>> rec = np.array([(1, 4), (2, 4), (3, 4)],
            dtype=[('a', '<i8'), ('b', '<i8')])
    >>> arr = rec2arr(rec)
    >>> arr
    array([[1, 4], [2, 4], [3, 4]])
    >>> arr, names = rec2arr(rec, return_names=True)
    >>> arr
    array([[1, 4], [2, 4], [3, 4]])
    >>> names
    ['a', 'b']
    """
    arr = np.array([rec[par] for par in rec.dtype.names]).T
    if return_names:
        return arr, rec.dtype.names
    else:
        return arr


def dict2rec(d):
    """
    Convert a dictionary of arrays/lists to a numpy structured array.

    :param d: Dictionary with arrays/lists as values
    :return: numpy structured array
    """

    # Convert lists/values to numpy arrays
    d = {
        k: np.array(v) if hasattr(v, "__iter__") and not isinstance(v, str) else v
        for k, v in d.items()
    }

    # Get first dimension size from array values
    array_sizes = [v.shape[0] for v in d.values() if hasattr(v, "shape")]
    if not array_sizes:
        raise ValueError("At least one array value required")
    size = array_sizes[0]

    # Create dtype with proper shapes
    dtype_list = []
    for key, val in d.items():
        if hasattr(val, "dtype"):
            if val.ndim > 1:
                dtype_list.append((key, val.dtype, val.shape[1:]))
            else:
                dtype_list.append((key, val.dtype))
        else:
            # For scalar values
            dtype_list.append((key, np.array(val).dtype))

    # Create empty structured array
    rec = np.empty(size, dtype=dtype_list)

    # Fill array
    for key, val in d.items():
        if hasattr(val, "shape"):
            rec[key] = val
        else:
            rec[key] = np.full(size, val)

    return rec


def rec2dict(rec):
    """
    Convert a numpy structured array to a dictionary.

    :param rec: numpy structured array
    :return: dictionary

    Example
    -------
    >>> rec = np.array([(1, 4), (2, 4), (3, 4)],
            dtype=[('a', '<i8'), ('b', '<i8')])
    >>> d = rec2dict(rec)
    >>> d
    {'a': array([1, 2, 3]), 'b': array([4, 4, 4])}
    """
    keys = rec.dtype.names
    d = {}
    for key in keys:
        d[key] = rec[key]
    return d


def dict2class(d):
    """
    Convert a dictionary to a class.

    :param d: dictionary
    :return: class

    Example
    -------
    >>> d = {'a': [1, 2, 3], 'b': 4}
    >>> c = dict2class(d)
    >>> c.a
    [1, 2, 3]
    >>> c.b
    4
    """

    class C:
        pass

    c = C()
    for key in d.keys():
        setattr(c, key, d[key])
    return c


def rec2class(rec):
    """
    Convert a numpy structured array to a class.

    :param rec: numpy structured array
    :return: class
    """
    return dict2class(rec2dict(rec))


def class2dict(c):
    """
    Convert a class to a dictionary.

    :param c: class
    :return: dictionary
    """

    return vars(c)


def class2rec(c):
    """
    Convert a class to a numpy structured array.

    :param c: class
    :return: numpy structured array
    """
    return dict2rec(class2dict(c))


def pd2rec(df):
    """
    Convert a pandas dataframe to a numpy structured array.

    :param df: pandas dataframe
    :return: numpy structured array
    """
    return df.to_records(index=False)


def rec2pd(rec):
    data_dict = {}
    for name in rec.dtype.names:
        if rec.dtype[name].shape:
            for i in range(rec.dtype[name].shape[0]):
                data_dict[f"{name}_{i}"] = rec[name][:, i]
        else:
            # Otherwise, just add it as a regular column
            data_dict[name] = rec[name]
    df = pd.DataFrame(data_dict)
    return df


def get_nan_mask(rec):
    """
    Get a mask for rows with NaNs in a numpy structured array.

    :param rec: numpy structured array
    :return: numpy structured array
    """
    nan_mask = np.zeros(len(rec), dtype=bool)
    for name in rec.dtype.names:
        nan_mask |= np.isnan(rec[name])
    return nan_mask


def remove_nans(rec):
    """
    Remove rows with NaNs from a numpy structured array.

    :param rec: numpy structured array
    :return: numpy structured array
    """
    nan_mask = get_nan_mask(rec)
    return rec[~nan_mask]


def get_inf_mask(rec):
    """
    Get a mask for rows with infs in a numpy structured array.

    :param rec: numpy structured array
    :return: numpy structured array
    """
    inf_mask = np.zeros(len(rec), dtype=bool)
    for name in rec.dtype.names:
        inf_mask |= np.isinf(rec[name])
    return inf_mask


def remove_infs(rec):
    """
    Remove rows with infs from a numpy structured array.

    :param rec: numpy structured array
    :return: numpy structured array
    """
    inf_mask = get_inf_mask(rec)
    return rec[~inf_mask]


def get_finite_mask(rec):
    """
    Get a mask for finite rows (i.e., rows without NaNs or infs) in a numpy structured array.

    :param rec: numpy structured array
    :return: numpy structured array
    """
    inf_mask = get_inf_mask(rec)
    nan_mask = get_nan_mask(rec)
    return ~(inf_mask | nan_mask)


def select_finite(rec):
    """
    Remove rows with NaNs or infs from a numpy structured array.

    :param rec: numpy structured array
    :return: numpy structured array
    """
    return remove_infs(remove_nans(rec))


def arr_to_rec(arr, dtype):
    """
    Convert a numpy array to a numpy structured array given its dtype.

    :param arr: numpy array
    :param dtype: dtype of the structured array
    :return: numpy structured array
    """
    newrecarray = np.core.records.fromarrays(np.array(arr).transpose(), dtype=dtype)
    return newrecarray


def get_dtype_of_list(lst):
    # Convert the list to a NumPy array
    arr = np.array(lst)

    # Get the data type of the first element in the array
    dtype = arr[0].dtype
    if len(arr) == 1:
        return dtype

    # Check if the data type of every other element is the same as the first element
    all_the_same = True
    for element in arr[1:]:
        if element.dtype != dtype:
            all_the_same = False

    assert all_the_same, "Not all entries of the list have the same dtype"

    return dtype


def new_array(n_rows, columns, ints=[], float_dtype=np.float64, int_dtype=np.int64):
    n_columns = len(columns)
    formats = [None] * n_columns
    for ic in range(n_columns):
        if columns[ic] in ints:
            formats[ic] = int_dtype
        else:
            formats[ic] = float_dtype
    newrec = np.zeros(n_rows, dtype=np.dtype(zip(columns, formats)))
    return newrec


def get_dtype(columns, main="f8", shapes=None):
    if main is None:
        main = "f8"
    elif isinstance(main, type):
        main = main.__name__
    list_name = []
    list_dtype = []

    if shapes is None:
        shapes = [() for _ in columns]

    for col in columns:
        if ":" in col:
            name, dtype = col.split(":")
        else:
            name, dtype = col, main

        list_name.append(str(name))
        list_dtype.append(str(dtype))

    dtype = np.dtype(list(zip(list_name, list_dtype, shapes)))

    return dtype


def get_storing_dtypes(dtype_list):
    if six.PY2:
        dtypes = [(str(dt[0]), str(dt[1])) + dt[2:] for dt in dtype_list]

    else:
        dtypes = [(dt[0], dt[1].replace("<U", "|S")) + dt[2:] for dt in dtype_list]

    return dtypes


def get_loading_dtypes(dtype_list):
    if six.PY2:
        dtypes = [(str(dt[0]), str(dt[1])) + dt[2:] for dt in dtype_list]

    else:
        dtypes = []
        # handling for h5py>=2.10.0
        for dt in dtype_list:
            if isinstance(dt[1], tuple):
                dtypes.append((dt[0], dt[1][0].replace("|S", "<U")) + dt[2:])
            else:
                dtypes.append((dt[0], dt[1].replace("|S", "<U")) + dt[2:])

    return dtypes


def set_storing_dtypes(arr):
    if six.PY2:
        return arr

    # numpy array
    elif hasattr(arr, "dtype"):
        dtype = arr.dtype

        # ndarray
        if len(dtype) == 0:
            dtypes_store = arr.dtype.str.replace("<U", "|S")

        # recarray
        else:
            dtypes_store = get_storing_dtypes(arr.dtype.descr)

        return arr.astype(dtypes_store)

    # string
    elif isinstance(arr, str):
        return arr.encode("utf-8")

    else:
        # list or tuple
        try:
            arr_fixed = [None] * len(arr)

            for i, x in enumerate(arr):
                if isinstance(x, str):
                    arr_fixed[i] = x.encode("utf-8")
                else:
                    arr_fixed[i] = x

            return arr_fixed

        # single number
        except Exception:
            return arr


def set_loading_dtypes(arr):
    if six.PY2:
        return arr

    # numpy array
    elif hasattr(arr, "dtype"):
        dtype = arr.dtype

        # ndarray
        if len(dtype) == 0:
            dtypes_load = arr.dtype.str.replace("|S", "<U").replace("|O", "<U")

        # recarray
        else:
            dtypes_load = get_loading_dtypes(arr.dtype.descr)

        return arr.astype(dtypes_load)

    # bytes
    elif isinstance(arr, bytes):
        return arr.decode("utf-8")

    else:
        # list or tuple
        try:
            arr_fixed = [None] * len(arr)

            for i, x in enumerate(arr):
                if isinstance(x, bytes):
                    arr_fixed[i] = x.decode("utf-8")
                else:
                    arr_fixed[i] = x

            return arr_fixed

        # single number
        except Exception:
            return arr


def save_hdf(filename, arr, **kwargs):
    f5 = h5py.File(name=filename, mode="a")

    try:
        f5.clear()

    except Exception:
        for datasetname in f5.keys():
            del f5[datasetname]

    arr_store = set_storing_dtypes(arr)
    f5.create_dataset(name="data", data=arr_store, **kwargs)
    f5.close()
    LOGGER.info("saved {}".format(filename))


def write_to_hdf(filename, arr, name="data", compression="lzf", shuffle=True, **kwargs):
    """
    Write a recarray to a hdf file.

    :param filename: filename of the hdf file
    :param arr: numpy recarray
    :param name: name of the dataset
    :param compression: compression method
    :param shuffle: shuffle data before compression
    :param kwargs: keyword arguments for h5py.File.create_dataset
    """
    with h5py.File(filename, "w") as fh5:
        fh5.create_dataset(
            name=name, data=arr, compression=compression, shuffle=shuffle, **kwargs
        )


def load_hdf(filename, first_row=-1, last_row=-1):
    f5 = h5py.File(name=filename, mode="r")

    if (first_row > -1) & (last_row > -1) & (first_row < last_row):
        if first_row < last_row:
            data = np.array(f5["data"][first_row:last_row])

        else:
            raise Exception(
                "first_row ({}) should be smaller " "than last_row ({})".format(
                    first_row, last_row
                )
            )
    else:
        data = np.array(f5["data"])

    f5.close()

    safe_dtypes = get_loading_dtypes(data.dtype.descr)
    data = data.astype(safe_dtypes, copy=False)

    LOGGER.debug("loaded {}".format(filename))

    return data


def save_hdf_cols(filename, arr, compression=None, resizable=False):
    if compression is None:
        kwargs = {}
    else:
        if isinstance(compression, dict):
            kwargs = compression
        else:
            kwargs = {"compression": compression}

    dtypes_store = get_storing_dtypes(arr.dtype.descr)

    with h5py.File(filename, "w") as fh5:
        for dt in dtypes_store:
            col = dt[0]
            dtype = dt[1]
            extra_dims = dt[2:]

            if col in fh5:
                del fh5[col]

            if resizable:
                kwargs["maxshape"] = (None,) + extra_dims

            fh5.create_dataset(
                name=col, data=arr[col].astype(dtype, copy=False), **kwargs
            )

    LOGGER.info("saved hdf file {} with {} rows".format(filename, len(arr)))


def load_hdf_cols_from_file(
    filename,
    columns="all",
    first_row=0,
    last_row=-1,
    cols_to_add=(),
    selectors=None,
    verb=True,
):
    """
    Loads all columns of an hdf file into one recarray.

    :param filename: path to hdf file
    :param columns: list of columns to load, "all" to load all columns
    :param first_row: first row to load
    :param last_row: last row to load
    :param cols_to_add: list of columns to add to the recarray
    :param selectors: dictionary of selection masks for columns
    :param verb: if True, print information
    :return: recarray
    """
    with h5py.File(filename, mode="r") as fh5:
        # Infer columns to load
        if columns == "all":
            columns = list(fh5.keys())

        # Infer size of data to load
        if last_row is not None:
            if last_row > 0:
                size = last_row - first_row
            else:
                size = len(fh5[columns[0]]) + last_row
                last_row = size

                if size < 0 or last_row < first_row:
                    raise Exception(
                        "Combination first_row={}, last_row={} " "invalid".format(
                            first_row, last_row
                        )
                    )
        else:
            size = len(fh5[columns[0]])
            last_row = size

        # Get boolean mask in case any selectors were specified
        if selectors is not None and len(selectors) > 0:
            select = np.ones(size, dtype=np.bool)

            for cols in selectors:
                select_fun = selectors[cols]

                if isinstance(cols, str):
                    cols = (cols,)

                select &= select_fun(*[fh5[c][first_row:last_row] for c in cols])

            size = np.count_nonzero(select)

            if verb:
                LOGGER.info(
                    "masking {} / {} rows while " "loading {}".format(
                        select.size - size, select.size, filename
                    )
                )

        else:
            select = np.s_[:size]

        # Create array holding loaded data
        dtype_list = [(col, fh5[col].dtype.str, fh5[col].shape[1:]) for col in columns]
        dtypes_load = get_loading_dtypes(dtype_list)
        dtypes_load += [(col, np.float32) for col in cols_to_add]
        arr = np.empty(size, dtype=dtypes_load)

        for col in columns:
            arr[col] = fh5[col][first_row:last_row][select]

    for col in cols_to_add:
        arr[col] = 0.0

    return arr


def col_name_to_path(dirname, colname):
    return os.path.join(dirname, colname + ".h5")


def get_hdf_col_names(path):
    # file
    if os.path.isfile(path):
        with h5py.File(path, mode="r") as fh5:
            columns = list(fh5.keys())

    # directory
    columns = [
        name for name, ext in map(os.path.splitext, os.listdir(path)) if ext == ".h5"
    ]

    return columns


def load_hdf_cols_from_directory(
    dirname,
    columns="all",
    first_row=0,
    last_row=-1,
    copy_local=False,
    dirname_parent=None,
    allow_nonexisting=False,
    cols_to_add=(),
    selectors=None,
    verb=True,
    copy_editor=None,
):
    """
    Loads columns that are stored as individual files in a directory into one recarray.
    """
    if selectors is None:
        selectors = dict()

    if copy_editor is None:
        copy_editor = lambda p: p  # noqa

    # Infer columns to load
    columns_all = []
    if not allow_nonexisting or os.path.exists(dirname):
        columns_all += [
            name
            for name, ext in map(os.path.splitext, os.listdir(dirname))
            if ext == ".h5"
        ]
    if dirname_parent is not None:
        columns_all += [
            name
            for name, ext in map(os.path.splitext, os.listdir(dirname_parent))
            if ext == ".h5"
        ]
    columns_all = list(set(columns_all))

    if columns == "all":
        columns = columns_all
    else:
        columns = list(columns)

    # Get filename
    # (for all columns s.t. one can also use selectors
    # using columns that are not loaded)
    dict_filename_cols = {}
    for col in set(columns_all + columns + list(selectors.keys())):
        # get the filename from the right folder
        filename_col = col_name_to_path(dirname, col)

        if not os.path.isfile(filename_col) and dirname_parent is not None:
            filename_col = col_name_to_path(dirname_parent, col)

        dict_filename_cols[col] = filename_col

    # Infer size of data to load
    if last_row is not None:
        if last_row > 0:
            size = last_row - first_row
        else:
            with h5py.File(dict_filename_cols[columns[0]], mode="r") as fh5:
                size = len(fh5[columns[0]]) + last_row
                last_row = size

                if size < 0 or last_row < first_row:
                    raise Exception(
                        "Combination first_row={}, last_row={} invalid".format(
                            first_row, last_row
                        )
                    )
    else:
        with h5py.File(dict_filename_cols[columns[0]], mode="r") as fh5:
            size = len(fh5[columns[0]])
            last_row = size

    # Get boolean mask in case any selectors were specified
    columns_copied = {}

    if len(selectors) > 0:
        select = np.ones(size, dtype=np.bool)

        for cols in selectors:
            select_fun = selectors[cols]

            if isinstance(cols, str):
                cols = (cols,)

            data_select = [None] * len(cols)

            for ic, c in enumerate(cols):
                filename_col = dict_filename_cols[c]

                if copy_local:
                    if c not in columns_copied:
                        path_local = os.path.join(
                            os.getcwd(), os.path.basename(filename_col)
                        )
                        file_utils.robust_copy(
                            copy_editor(filename_col),
                            path_local,
                            use_copyfile=True,
                        )
                        path_load = path_local
                        columns_copied[c] = path_load
                    else:
                        path_load = columns_copied[c]

                else:
                    path_load = filename_col

                with h5py.File(path_load, mode="r") as fh5:
                    data_select[ic] = fh5[c][first_row:last_row]

            select &= select_fun(*data_select)

        size = np.count_nonzero(select)
        del data_select

        if verb:
            LOGGER.info(
                "masking {} / {} rows while loading " "{}".format(
                    select.size - size, select.size, dirname
                )
            )

    else:
        select = np.s_[:size]

    # Create array holding loaded data
    dtypes_list = [None] * len(columns)

    for i, col in enumerate(columns):
        with h5py.File(dict_filename_cols[col], mode="r") as fh5:
            dtypes_list[i] = (col, fh5[col].dtype.str, fh5[col].shape[1:])

    dtypes_load = get_loading_dtypes(dtypes_list)
    dtypes_load += [(col, np.float32) for col in cols_to_add]
    arr = np.empty(size, dtype=dtypes_load)

    # Now copy files one by one and read data
    for col in columns:
        filename_col = dict_filename_cols[col]

        if copy_local:
            if col in columns_copied:
                path_local = columns_copied[col]

            else:
                path_local = os.path.join(os.getcwd(), os.path.basename(filename_col))
                file_utils.robust_copy(
                    copy_editor(filename_col), path_local, use_copyfile=True
                )
                columns_copied[col] = path_local

            path_load = path_local

        else:
            path_load = filename_col

        with h5py.File(path_load, mode="r") as fh5:
            arr[col] = fh5[col][first_row:last_row][select]

        if copy_local:
            os.remove(path_load)
            del columns_copied[col]

    # Remove remaining columns (columns used for selecting only)
    for path_local in columns_copied.values():
        os.remove(path_local)

    # Set newly added columns to zero
    for col in cols_to_add:
        arr[col] = 0.0

    return arr


def load_hdf_cols(
    filename,
    columns="all",
    first_row=0,
    last_row=None,
    verb=True,
    copy_local=True,
    filename_parent=None,
    allow_nonexisting=False,
    cols_to_add=(),
    selectors=None,
    copy_editor=None,
):
    if last_row is not None:
        if (last_row > 0) & (first_row >= last_row):
            raise Exception(
                "first_row {} should be smaller than " "last_row {}".format(
                    first_row, last_row
                )
            )

    if os.path.isfile(filename):
        arr = load_hdf_cols_from_file(
            filename,
            columns=columns,
            first_row=first_row,
            last_row=last_row,
            cols_to_add=cols_to_add,
            selectors=selectors,
            verb=verb,
        )

    else:
        arr = load_hdf_cols_from_directory(
            filename,
            columns=columns,
            first_row=first_row,
            last_row=last_row,
            copy_local=copy_local,
            dirname_parent=filename_parent,
            allow_nonexisting=allow_nonexisting,
            cols_to_add=cols_to_add,
            selectors=selectors,
            verb=verb,
            copy_editor=copy_editor,
        )

    if verb:
        LOGGER.info("loaded {} with n_rows={}".format(filename, len(arr)))

    return arr


def append_rows_to_h5dset(dset, array):
    nr_dset, nr_array = dset.shape[0], array.shape[0]
    nr_new = nr_dset + nr_array
    dset.resize(nr_new, axis=0)
    dset[nr_dset:] = set_storing_dtypes(array)


def replace_hdf5_dataset(fobj, name, data, **kwargs):
    if name in fobj:
        del fobj[name]
    fobj.create_dataset(name=name, data=set_storing_dtypes(data), **kwargs)


def overwrite_hdf5_column(path, name, data, **kwargs):
    if os.path.isdir(path):
        path_col = col_name_to_path(path, name)

    else:
        path_col = path

    with h5py.File(path_col) as fh5:
        replace_hdf5_dataset(fh5, name, set_storing_dtypes(data), **kwargs)


def check_hdf_column(filename, column_name):
    if os.path.isfile(filename):
        with h5py.File(filename, mode="r") as fh5:
            col_found = column_name in fh5.keys()

    else:
        filename_col = col_name_to_path(filename, column_name)
        col_found = os.path.isfile(filename_col)

    return col_found


def rec_float64_to_float32(cat):
    list_new_dtype = []

    all_ok = True

    for i in range(len(cat.dtype)):
        if cat.dtype[i] == np.float64:
            list_new_dtype.append(np.float32)
            all_ok = False

        else:
            list_new_dtype.append(cat.dtype[i])

    if all_ok:
        return cat

    else:
        new_dtype = np.dtype(dict(formats=list_new_dtype, names=cat.dtype.names))
        cat_new = cat.astype(new_dtype)
        return cat_new


def save_dict_to_hdf5(filename, data_dict, kw_compress={}):
    kw_compress.setdefault("compression", "lzf")
    kw_compress.setdefault("shuffle", True)

    f = h5py.File(filename, "w")
    for grp_name in data_dict:
        grp = f.create_group(grp_name)
        for dset_name in data_dict[grp_name]:
            grp.create_dataset(
                dset_name, data=data_dict[grp_name][dset_name], **kw_compress
            )
    f.close()


def nanequal(a, b):
    return (np.isnan(b) & np.isnan(a)) | (a == b)
