"""
Papai-specific functions and data schema.
"""

import datetime
import io
import os
import warnings
from collections.abc import Iterator
from io import TextIOWrapper
from typing import TypeAlias, TypedDict

import pandas as pd
from fsspec.spec import AbstractBufferedFile
from google.oauth2 import service_account

from papai_unified_storage.storage import Storage, filesystem
from papai_unified_storage.utils import (
    dummy_fn,
    generate_temporary_filename,
    get_one_of,
    joinpath,
)

GlobPath: TypeAlias = str
PathPattern: TypeAlias = str | list[str] | GlobPath | list[GlobPath]


class Parquet(TypedDict):
    bucket_name: str
    """
    workspace bucket name.
    """
    step_name: str
    """
    friendly parquet name.
    """
    object_name: str
    """
    path to the parquet file.
    """


class Bucket(TypedDict):
    bucket_name: str
    """
    workspace bucket name.
    """
    step_name: str
    """
    friendly folder name that we consider being the bucket.
    """
    settings: dict
    """
    store connection settings to external buckets.
    """


class Registry(TypedDict):
    bucket_name: str
    """
    workspace bucket name.
    """
    artefacts_path: str
    """
    path to the artefact folder.
    """
    registry_name: str
    """
    friendly registry name.
    """


def _get_io_config(key: str, match_value: str, list_io: list, io_name: str) -> dict:
    for io_ in list_io:
        if io_[key] == match_value:
            return io_
    raise ValueError(f"Could not find {io_name} with name {match_value}")


def _get_bucket_fs(
    bucket_name: str, papai_fs: Storage, list_buckets: list[Bucket]
) -> tuple[Storage, str]:
    """Get a filesystem to interact with a specific bucket.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to interact with.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    list_buckets : list[Bucket]
        List of all bucket configurations.

    Returns
    -------
    filesystem, path_prefix : tuple[Storage, str]
        Filesystem that allows interaction with the bucket.
        Path prefix to be used in papai internal bucket. If you are using an
        external bucket, this will be an empty string.
    """
    bucket = _get_io_config("step_name", bucket_name, list_buckets, "bucket")
    settings = bucket["settings"]

    if "virtual_bucket_path" in settings:
        return papai_fs, bucket["bucket_name"] + "/" + settings["virtual_bucket_path"]

    available_protocols = {
        "AZURE_OBJECT_STORAGE_SETTINGS": _get_abfs,
        "S3_OBJECT_STORAGE_SETTINGS": _get_s3fs,
        "GC_OBJECT_STORAGE_SETTINGS": _get_gcsfs,
    }
    protocol = available_protocols[settings["kind"]]

    return filesystem(protocol, settings["storage_options"]), bucket["bucket_name"]


def _get_abfs(settings: dict) -> Storage:
    account_name = settings["account_name"]
    account_key = settings["account_key"]
    return filesystem("abfs", account_name=account_name, account_key=account_key)


def _get_gcsfs(settings: dict) -> Storage:
    credentials_dict = {
        "type": "service_account",
        "private_key_id": settings["private_key_id"],
        "private_key": settings["private_key"],
        "client_email": settings["client_email"],
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    credentials = service_account.Credentials.from_service_account_info(
        credentials_dict
    )
    return filesystem("gcsfs", token=credentials)


def _get_s3fs(settings: dict) -> Storage:
    endpoint = settings["endpoint"]
    access_key = settings["access_key"]
    secret_key = settings["secret_key"]
    return filesystem("s3fs", key=access_key, secret=secret_key, endpoint=endpoint)


def _get_bucket_fs_with_prefix(
    bucket_name: str, papai_fs: Storage, list_buckets: list[Bucket]
) -> tuple[Storage, str]:
    fs, path_prefix = _get_bucket_fs(bucket_name, papai_fs, list_buckets)

    return fs, path_prefix


def list_bucket_objects(
    bucket_name: str,
    path: str,
    list_buckets: list[Bucket],
    papai_fs: Storage,
    recursive: bool = True,
):
    """List bucket objects with name starting with `path`.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to list in.
    path : str
        List all objects that starts with `path`.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    recursive : bool, optional
        Whether to list objects that are deeper than `path`, by default True.
    """
    fs, bucket_name = _get_bucket_fs_with_prefix(bucket_name, papai_fs, list_buckets)
    full_path = joinpath(bucket_name, path)
    return fs.list_files(full_path, recursive)


def glob_bucket_objects(
    bucket_name: str,
    pattern: str,
    list_buckets: list[Bucket],
    papai_fs: Storage,
):
    """List files in a remote directory that match a pattern.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to list in.
    pattern : str
        List all objects that starts with `pattern`.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    """
    fs, bucket_name = _get_bucket_fs_with_prefix(bucket_name, papai_fs, list_buckets)
    full_path = joinpath(bucket_name, pattern)
    return fs.glob_files(full_path)


def read_from_bucket_to_file(
    bucket_name: str,
    object_name: str,
    list_buckets: list[Bucket],
    papai_fs: Storage,
    destination_directory: str | None = None,
) -> str:
    warnings.warn(
        "read_from_bucket_to_file is deprecated, use get_from_bucket instead",
        DeprecationWarning,
    )
    return get_from_bucket(
        bucket_name,
        object_name,
        list_buckets,
        papai_fs,
        destination_directory=destination_directory,
    )


def get_from_bucket(
    bucket_name: str,
    remote_paths: PathPattern,
    list_buckets: list[Bucket],
    papai_fs: Storage,
    destination_directory: str | None = None,
) -> str:
    """Download files or folders from a bucket to the local file system.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to download from.
    remote_paths : PathPattern
        Path to the objects to download. It can be a glob pattern or a list of
        patterns.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    destination_directory : str|None
        Directory in which to save the downloaded file. By default None.

    Returns
    -------
    str
        If you download a single file, the path to the downloaded file.
        If you download multiple files, the path to the directory containing
        the downloaded files.
    """
    fs, bucket_name = _get_bucket_fs_with_prefix(bucket_name, papai_fs, list_buckets)
    paths = joinpath(bucket_name, remote_paths)

    tmp_dir = generate_temporary_filename(destination_directory)
    fs.get(paths, tmp_dir)

    return tmp_dir


def put_to_bucket(
    bucket_name: str,
    local_paths: PathPattern,
    remote_paths: PathPattern,
    list_buckets: list[Bucket],
    papai_fs: Storage,
):
    """Upload files / folders to a bucket.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to upload to.
    local_paths : PathPattern
        Path to the objects to upload. It can be a glob pattern or a list of
        patterns.
    remote_paths : PathPattern
        Path(s) to upload to in the bucket. If it is a list, it must have the
        same length as `local_object_names`.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    """
    fs, bucket_name = _get_bucket_fs_with_prefix(bucket_name, papai_fs, list_buckets)
    destination = joinpath(bucket_name, remote_paths)
    fs.put(local_paths, destination)


def put_to_bucket_with_versionning(
    bucket_name: str,
    local_paths: PathPattern,
    base_versionned_path: str,
    remote_path: PathPattern,
    list_buckets: list[Bucket],
    papai_fs: Storage,
    version_generator: Iterator[int | str] = range(int(10e10)),
) -> str:
    """Upload files / folders to a bucket. If the remote path already exists,
    a suffix will be added to remote_path so that the destination is not
    overridden.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to upload to.
    local_paths : PathPattern
        Path to the objects to upload. It can be a glob pattern or a list of
        patterns.
    base_versionned_path : str
        Base path that will be versionned with a suffix.
    remote_path : PathPattern
        Path(s) to upload to in the base_versionned_path. If it is a list, it
        must have the same length as `local_paths`.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    version_generator : Iterator[int | str], optional
        Generator of version numbers/string to try. You can customize this
        to change how the versionned named will be generated. By default
        range(10e10).

    Returns
    -------
    str
        Path to base_versionned_path with the version added.
    """

    def build_versionned_path(base_versionned_path: str, version: int | str):
        return base_versionned_path + f"_{version}"

    fs, bucket_name = _get_bucket_fs_with_prefix(bucket_name, papai_fs, list_buckets)
    destination = joinpath(bucket_name, base_versionned_path)

    for version in version_generator:
        versionned_path = build_versionned_path(destination, version)
        if not fs.exists(versionned_path):
            break

    fs.put(local_paths, joinpath(versionned_path, remote_path))

    return versionned_path


def write_to_file_in_bucket(
    bucket_name: str,
    file_name: str,
    data: io.BytesIO | str,
    list_buckets: list[Bucket],
    papai_fs: Storage,
):
    """Upload a file to a bucket / Write data in a bucket.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to write in.
    file_name : str
        Path to which the data will be written.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    data : io.BytesIO | str
        Data to write to the file
    """
    fs, bucket_name = _get_bucket_fs_with_prefix(bucket_name, papai_fs, list_buckets)
    path = joinpath(bucket_name, file_name)

    fs.write_to_file(path, content=data)


def write_file_in_bucket(
    bucket_name: str,
    file_name: str,
    list_buckets: list[Bucket],
    papai_fs: Storage,
    data: io.BytesIO | str | None = None,
    file_path: str | bytes | os.PathLike | None = None,
):
    if file_path is not None:
        warnings.warn(
            "write_file_in_bucket with `file_path` argument is deprecated, use put_to_bucket instead",
            DeprecationWarning,
        )
        put_to_bucket(bucket_name, file_name, list_buckets, papai_fs, file_path)

    if data is not None:
        warnings.warn(
            "write_file_in_bucket with `data` argument is deprecated, use write_to_file_in_bucket instead",
            DeprecationWarning,
        )
        write_to_file_in_bucket(bucket_name, file_name, list_buckets, papai_fs, data)

    raise ValueError("You must provide either data or a file_path")


def import_dataset(
    dataset_name: str, list_parquets: list[Parquet], papai_fs: Storage
) -> pd.DataFrame:
    """Load a pandas DataFrame from a parquet file in the papai bucket.

    Parameters
    ----------
    dataset_name : str
        Name of the dataset to load.
    list_parquets : list[Parquet]
        List of all parquet configurations.
    papai_fs : Storage
        Papai filesystem in which to find the dataset.

    Returns
    -------
    pd.DataFrame
    """
    parquet = _get_io_config("step_name", dataset_name, list_parquets, "dataset")
    parquet_path = joinpath(parquet["bucket_name"], parquet["object_name"])
    return papai_fs.read_dataset_from_parquet(parquet_path)


def export_dataset(
    dataset: pd.DataFrame,
    dataset_name: str,
    list_parquets: list[Parquet],
    papai_fs: Storage,
):
    """Write a pandas DataFrame to a parquet file in the papai bucket.

    Parameters
    ----------
    dataset : pd.DataFrame
        Pandas DataFrame to write to the bucket.
    dataset_name : str
        Name of the dataset to write to.
    list_parquets : list[Parquet]
        List of all parquet configurations.
    papai_fs : Storage
        Papai filesystem in which to find the dataset.
    """
    parquet = _get_io_config("step_name", dataset_name, list_parquets, "dataset")
    parquet_path = joinpath(parquet["bucket_name"], parquet["object_name"])
    papai_fs.write_dataframe_to_parquet(parquet_path, dataset)


def _get_artefacts_folder_path(
    registry_name: str,
    list_registries: list[Registry],
    run_uuid: str | None = None,
) -> str:
    """
    Get the path to the artefacts folder in the papai filesystem. If a run_uuid
    is provided, the default run_uuid will be replaced by the provided one.
    """
    registry = _get_io_config(
        "registry_name", registry_name, list_registries, "registry"
    )
    artefacts_folder_path = joinpath(
        registry["bucket_name"], registry["artefacts_path"]
    )

    if run_uuid is not None:
        # Replace the default run_uuid by the provided one
        artefacts_folder_path = artefacts_folder_path.rsplit("/", 1)[0] + "/" + run_uuid

    return artefacts_folder_path


def get_model_artefacts(
    registry_name: str,
    remote_paths: PathPattern,
    registry_inputs: list[Registry],
    papai_fs: Storage,
    run_uuid: str | None = None,
    destination_directory: str | None = None,
) -> str:
    """Download a model artefact(s) from the papai filesystem.

    Parameters
    ----------
    registry_name : str
        Name of the registry to get the artefact from.
    remote_paths : str
        Path to the artefact(s) to download. It can be a glob pattern or a list
        of patterns.
    registry_inputs : list[Registry]
        List of all registry configurations.
    papai_fs : Storage
        PapAI filesystem to interact with the bucket.
    run_uuid : str | None
        The UUID of the run you want to save artefacts to. If None, it will
        be automatically be the activated run. By default None.
    destination_directory : str | None
        Directory in which to save the downloaded file. By default None.

    Returns
    -------
    str
        Local path to the folder that contains the downloaded artefacts.
    """
    artefacts_folder_path = _get_artefacts_folder_path(
        registry_name, registry_inputs, run_uuid
    )
    artefact_full_path = joinpath(artefacts_folder_path, remote_paths)

    tmp_file = generate_temporary_filename(destination_directory) + "/"
    papai_fs.get(artefact_full_path, tmp_file)

    return tmp_file


def save_model_artefact(
    data,
    registry_name: str,
    artefact_path: str,
    registry_inputs: list[Registry],
    papai_fs: Storage,
    run_uuid: str | None = None,
):
    """Upload an artefact to the papai filesystem.

    Parameters
    ----------
    data: str | bytes
        Data to write to the file.
    registry_name : str
        Name of the registry to save the artefact to.
    artefact_path : str
        Path to the artefact.
    registry_inputs : list[Registry]
        List of all registry configurations.
    papai_fs : Storage
        PapAI filesystem to interact with the bucket.
    run_uuid : str | None
        The UUID of the run you want to save artefacts to. If None, it will
        be automatically be the activated run. By default None.
    """
    artefacts_folder_path = _get_artefacts_folder_path(
        registry_name, registry_inputs, run_uuid
    )
    artefact_full_path = joinpath(artefacts_folder_path, artefact_path)

    papai_fs.write_to_file(artefact_full_path, data)


def set_verbose(papai_fs: Storage, verbose: bool):
    """
    Set the verbosity level of the papai filesystem.

    Parameters
    ----------
    verbose : bool
        Whether to print logs from the filesystem.
    """
    papai_fs.log_fn = print if verbose else dummy_fn


def delete_old_files(
    bucket_name: str,
    remote_path: str,
    date_threshold: datetime.datetime,
    list_buckets: list[Bucket],
    papai_fs: Storage,
    recursive: bool = False,
    only_print_files_to_delete: bool = False,
):
    """Delete files in a bucket that are older than a given date.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to delete files from.
    remote_path : str
        Path to the files to delete.
    date_threshold : datetime.datetime
        Date threshold to delete files older than.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    recursive : bool, optional
        Whether to delete files recursively in `remote_path`, by default
        False.
    only_print_files_to_delete : bool, optional
        If True, disables the deletion of files and only prints the path to
        files that would be deleted, by default False.
    """
    fs, bucket_name = _get_bucket_fs_with_prefix(bucket_name, papai_fs, list_buckets)
    full_path = joinpath(bucket_name, remote_path)
    files = fs.list_files(full_path, recursive=recursive, detail=True)

    for file_details in files.values():
        last_modified_ts = get_one_of(file_details, ("LastModified", "mtime"))
        if last_modified_ts < date_threshold.timestamp():
            if only_print_files_to_delete:
                last_modified_date = datetime.datetime.fromtimestamp(last_modified_ts)
                print(
                    f"Would delete {file_details['name']} (Last modified: {last_modified_date})"
                )
            else:
                fs.remove_files(file_details["name"])


def delete_large_files(
    bucket_name: str,
    remote_path: str,
    size_threshold: int,
    list_buckets: list[Bucket],
    papai_fs: Storage,
    recursive: bool = False,
    only_print_files_to_delete: bool = False,
):
    """Delete files in a bucket that are larger than a threshold.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to delete files from.
    remote_path : str
        Path to the files to delete.
    size_threshold : int
        Number of bytes above which files will be deleted.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    recursive : bool, optional
        Whether to delete files recursively in `remote_path`, by default
        False.
    only_print_files_to_delete : bool, optional
        If True, disables the deletion of files and only prints the path to
        files that would be deleted, by default False.
    """
    fs, bucket_name = _get_bucket_fs_with_prefix(bucket_name, papai_fs, list_buckets)
    full_path = joinpath(bucket_name, remote_path)
    files = fs.list_files(full_path, recursive=recursive, detail=True)

    for file_details in files.values():
        file_size = get_one_of(file_details, ("Size", "size"))
        if file_size > size_threshold:
            if only_print_files_to_delete:
                print(f"Would delete {file_details['name']} ({file_size} bytes)")
            else:
                fs.remove_files(file_details["name"])


def open_bucket_file(
    bucket_name: str,
    file_path: str,
    mode: str,
    list_buckets: list[Bucket],
    papai_fs: Storage,
    **kwargs,
) -> TextIOWrapper | AbstractBufferedFile:
    """Open a file.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to delete files from.
    file_path : str
        Path to the file to open.
    mode : str
        Mode in which to open the file. See builtin `open()`.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    kwargs
        Additional arguments (such as encoding, errors, newline) to pass to the
        filesystem and/or to the TextIOWrapper if file is opened in text mode.

    Returns
    -------
    TextIOWrapper | fsspec.AbstractBufferedFile
        File object.
    """
    fs, bucket_name = _get_bucket_fs_with_prefix(bucket_name, papai_fs, list_buckets)
    full_path = joinpath(bucket_name, file_path)
    return fs.open(full_path, mode=mode, **kwargs)
