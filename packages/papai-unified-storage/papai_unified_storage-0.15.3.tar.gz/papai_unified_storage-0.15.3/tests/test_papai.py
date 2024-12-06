import datetime
import os
from tempfile import TemporaryDirectory

import fsspec
import pandas as pd
import pytest

from papai_unified_storage.papai import (
    Parquet,
    Registry,
    delete_large_files,
    delete_old_files,
    export_dataset,
    get_from_bucket,
    get_model_artefacts,
    glob_bucket_objects,
    import_dataset,
    list_bucket_objects,
    open_bucket_file,
    put_to_bucket,
    put_to_bucket_with_versionning,
    save_model_artefact,
    set_verbose,
    write_to_file_in_bucket,
)
from papai_unified_storage.storage import filesystem
from papai_unified_storage.utils import dummy_fn, ensure_in_list, joinpath
from tests.utils import create_files


@pytest.fixture
def tmp_directories():
    with TemporaryDirectory() as remote:
        with TemporaryDirectory() as local:
            yield remote, local


@pytest.fixture
def path_to_create():
    return ["file1", "dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"]


@pytest.fixture
def mock_bucket_config_with_tmp_dir(mocker, tmp_directories):
    remote, local = tmp_directories
    mocker.patch(
        "papai_unified_storage.papai._get_bucket_fs_with_prefix",
        return_value=(
            filesystem("file", logging_function=print),
            remote,
        ),
    )
    return remote, local


@pytest.fixture(
    params=(
        (
            "",
            True,
            ["file1", "dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"],
        ),
        (
            "dir1",
            False,
            ["dir1/file1", "dir1/file2", "dir1/file3"],
        ),
        (
            "dir1",
            True,
            ["dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"],
        ),
    )
)
def data_test_list_bucket_objects(request):
    return request.param


def test_list_bucket_objects(
    mock_bucket_config_with_tmp_dir, path_to_create, data_test_list_bucket_objects
):
    remote_dir, _ = mock_bucket_config_with_tmp_dir
    (
        list_bucket_path,
        list_bucket_recursive,
        expected_existing_files,
    ) = data_test_list_bucket_objects

    create_files(joinpath(remote_dir, path_to_create))

    files = list_bucket_objects(
        "",
        list_bucket_path,
        [],
        fsspec.filesystem("file"),
        recursive=list_bucket_recursive,
    )
    assert set(files) == set(joinpath(remote_dir, expected_existing_files))


@pytest.fixture(
    params=(
        (
            "file1",
            ["file1"],
        ),
        (
            "**/file1",
            ["file1", "dir1/file1", "dir1/dir2/file1"],
        ),
    )
)
def data_test_glob_bucket_objects(request):
    return request.param


def test_glob_bucket_objects(
    mock_bucket_config_with_tmp_dir, path_to_create, data_test_glob_bucket_objects
):
    remote_dir, _ = mock_bucket_config_with_tmp_dir
    (
        list_bucket_pattern,
        expected_existing_files,
    ) = data_test_glob_bucket_objects

    create_files(joinpath(remote_dir, path_to_create))

    files = glob_bucket_objects(
        "",
        list_bucket_pattern,
        [],
        fsspec.filesystem("file"),
    )

    assert set(files) == set(
        ensure_in_list(joinpath(remote_dir, expected_existing_files))
    )


@pytest.fixture(
    params=(
        (
            "file1",
            [""],  # `destination` is actually the file
        ),
        (
            "**/file1",
            ["file1", "dir1/file1", "dir1/dir2/file1"],
        ),
    )
)
def data_test_get_from_bucket(request):
    return request.param


def test_get_from_bucket(
    mock_bucket_config_with_tmp_dir, path_to_create, data_test_get_from_bucket
):
    remote_dir, local_dir = mock_bucket_config_with_tmp_dir
    (
        object_names,
        expected_existing_files,
    ) = data_test_get_from_bucket
    create_files(joinpath(remote_dir, path_to_create))

    destination = get_from_bucket(
        "",
        object_names,
        [],
        fsspec.filesystem("file"),
        local_dir,
    )

    files_downloaded = set(fsspec.filesystem("file").find(destination))
    expected_files = set(ensure_in_list(joinpath(destination, expected_existing_files)))

    assert files_downloaded == expected_files


@pytest.fixture(
    params=(
        (
            "file1",
            "",
            ["file1"],
        ),
        (
            "**/file1",
            "",
            ["file1", "dir1/file1", "dir1/dir2/file1"],
        ),
        (
            ["file1", "dir1/file1"],
            ["file1", "dir1/file1"],
            ["file1", "dir1/file1"],
        ),
    )
)
def data_test_put_to_bucket(request):
    return request.param


def test_put_to_bucket(
    mock_bucket_config_with_tmp_dir, path_to_create, data_test_put_to_bucket
):
    remote_dir, local_dir = mock_bucket_config_with_tmp_dir
    (
        local_object_names,
        remote_object_names,
        expected_existing_remote_files,
    ) = data_test_put_to_bucket
    create_files(joinpath(local_dir, path_to_create))

    put_to_bucket(
        "",
        joinpath(local_dir, local_object_names),
        remote_object_names,
        [],
        fsspec.filesystem("file"),
    )

    files_uploaded = set(fsspec.filesystem("file").find(remote_dir))
    expected_files = set(
        ensure_in_list(joinpath(remote_dir, expected_existing_remote_files))
    )

    assert files_uploaded == expected_files


@pytest.fixture(
    params=(
        (
            "file1",
            "file",
            "",
            2,
            "",  # `base_versionned_path` is actually the file
        ),
        (
            "**/file1",
            "",
            "",
            3,
            ["file1", "dir1/file1", "dir1/dir2/file1"],
        ),
        (
            ["file1", "dir1/file1"],
            "",
            ["file1", "dir1/file1"],
            4,
            ["file1", "dir1/file1"],
        ),
    )
)
def data_test_put_to_bucket_with_versionning(request):
    return request.param


def test_put_to_bucket_with_versionning(
    mock_bucket_config_with_tmp_dir,
    path_to_create,
    data_test_put_to_bucket_with_versionning,
):
    remote_dir, local_dir = mock_bucket_config_with_tmp_dir
    create_files(joinpath(local_dir, path_to_create))

    (
        local_object_names,
        base_versionned_path,
        remote_object_names,
        n_uploads,
        expected_existing_remote_files,
    ) = data_test_put_to_bucket_with_versionning

    for expected_version in range(n_uploads):
        version = put_to_bucket_with_versionning(
            "",
            joinpath(local_dir, local_object_names),
            base_versionned_path,
            remote_object_names,
            [],
            fsspec.filesystem("file"),
        )
        assert joinpath(
            remote_dir, base_versionned_path
        ) + f"_{expected_version}" == str(version)

    for i in range(n_uploads):
        files_uploaded = set(
            fsspec.filesystem("file").find(
                joinpath(remote_dir, base_versionned_path) + f"_{i}"
            )
        )
        expected_files = set(
            ensure_in_list(
                joinpath(
                    joinpath(remote_dir, base_versionned_path) + f"_{i}",
                    expected_existing_remote_files,
                )
            )
        )
        assert files_uploaded == expected_files


@pytest.fixture(
    params=(
        ("file1", "content", "file1", "content"),
        ("file1", b"hey", "file1", b"hey"),
    )
)
def data_test_write_to_file_in_bucket(request):
    return request.param


def test_write_to_file_in_bucket(
    mock_bucket_config_with_tmp_dir, data_test_write_to_file_in_bucket
):
    remote_dir, _ = mock_bucket_config_with_tmp_dir
    (
        file_name,
        data,
        expected_remote_file,
        expected_content,
    ) = data_test_write_to_file_in_bucket

    write_to_file_in_bucket(
        "",
        file_name,
        data,
        [],
        fsspec.filesystem("file"),
    )

    mode = "rb" if isinstance(data, bytes) else "r"

    with fsspec.filesystem("file").open(
        joinpath(remote_dir, expected_remote_file), mode=mode
    ) as f:
        content = f.read()
        assert content == expected_content


def test_import_dataset(mock_bucket_config_with_tmp_dir):
    remote_dir, _ = mock_bucket_config_with_tmp_dir
    parquet_configs = [
        Parquet(
            bucket_name="",
            object_name=joinpath(remote_dir, "object.parquet"),
            step_name="michel",
        )
    ]

    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df.to_parquet(joinpath(remote_dir, "object.parquet"))

    df_imported = import_dataset("michel", parquet_configs, filesystem("file"))

    assert df.equals(df_imported)


def test_export_dataset(mock_bucket_config_with_tmp_dir):
    remote_dir, _ = mock_bucket_config_with_tmp_dir
    parquet_configs = [
        Parquet(
            bucket_name="",
            object_name=joinpath(remote_dir, "object.parquet"),
            step_name="michel",
        )
    ]

    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    export_dataset(df, "michel", parquet_configs, filesystem("file"))

    df_exported = pd.read_parquet(joinpath(remote_dir, "object.parquet"))

    assert df.equals(df_exported)


def test_get_model_artefacts(mock_bucket_config_with_tmp_dir):
    remote_dir, local_dir = mock_bucket_config_with_tmp_dir
    model_artefacts = [
        "config.lol",
        "model.json",
        "info",
        "img.png",
        "model.weights",
    ]
    create_files(joinpath(remote_dir, "run_uuid", model_artefacts))

    registry_configs = [
        Registry(
            bucket_name="",
            artefacts_path=joinpath(remote_dir, "default_run_uuid"),
            registry_name="michel",
        )
    ]

    model_artefacts_downloaded = get_model_artefacts(
        "michel",
        "model*",
        registry_configs,
        filesystem("file"),
        "run_uuid",
        destination_directory=local_dir,
    )

    file_downloaded = set(fsspec.filesystem("file").find(local_dir))
    expected_file = set(
        ensure_in_list(
            joinpath(model_artefacts_downloaded, ["model.weights", "model.json"])
        )
    )
    assert file_downloaded == expected_file


def test_save_model_artefact(mock_bucket_config_with_tmp_dir):
    remote_dir, _ = mock_bucket_config_with_tmp_dir

    registry_configs = [
        Registry(
            bucket_name="",
            artefacts_path=joinpath(remote_dir, "default_run_uuid"),
            registry_name="michel",
        )
    ]

    save_model_artefact(
        b"hello, i'm an artefact",
        "michel",
        "super.artefact",
        registry_configs,
        filesystem("file"),
        "run_uuid",
    )

    file_downloaded = set(fsspec.filesystem("file").find(remote_dir))
    expected_file = set(ensure_in_list(joinpath(remote_dir, "run_uuid/super.artefact")))
    assert file_downloaded == expected_file


def test_set_verbose():
    fs = filesystem("file")

    set_verbose(fs, True)
    assert fs.log_fn == print

    set_verbose(fs, False)
    assert fs.log_fn == dummy_fn


@pytest.fixture(
    params=(
        (
            [(0, 0), (None, None), (0, 0), (None, None), (0, 0)],
            datetime.datetime(2000, 7, 9),
            "dir1",
            False,
            ["file1", "dir1/file1", "dir1/file3", "dir1/dir2/file1"],
        ),
        (
            [(0, 0), (None, None), (0, 0), (None, None), (0, 0)],
            datetime.datetime(2000, 7, 9),
            "dir1",
            True,
            ["file1", "dir1/file1", "dir1/file3"],
        ),
    )
)
def data_test_remove_old_files(request):
    return request.param


def test_remove_old_files(
    mock_bucket_config_with_tmp_dir, path_to_create, data_test_remove_old_files
):
    remote_dir, _ = mock_bucket_config_with_tmp_dir
    create_files(joinpath(remote_dir, path_to_create))

    (
        files_utime,
        datetime_threshold,
        remote_path_to_delete_from,
        recursive,
        expected_remaining_files,
    ) = data_test_remove_old_files

    for file, utime in zip(path_to_create, files_utime):
        if utime[0] is not None:
            os.utime(joinpath(remote_dir, file), utime)

    delete_old_files(
        "",
        remote_path_to_delete_from,
        datetime_threshold,
        [],
        fsspec.filesystem("file"),
        recursive=recursive,
    )

    files_not_deleted = set(fsspec.filesystem("file").find(remote_dir))
    expected_files = set(ensure_in_list(joinpath(remote_dir, expected_remaining_files)))
    assert files_not_deleted == expected_files


@pytest.fixture(
    params=(
        (
            [10, 50, 100, 500, 1000],
            400,
            "dir1",
            False,
            ["file1", "dir1/file1", "dir1/file2", "dir1/dir2/file1"],
        ),
        (
            [10, 50, 100, 500, 1000],
            50,
            "dir1",
            True,
            ["file1", "dir1/file1"],
        ),
    )
)
def data_test_remove_large_files(request):
    return request.param


def test_remove_large_files(
    mock_bucket_config_with_tmp_dir, path_to_create, data_test_remove_large_files
):
    remote_dir, _ = mock_bucket_config_with_tmp_dir
    create_files(joinpath(remote_dir, path_to_create))

    (
        files_size,
        size_threshold,
        remote_path_to_delete_from,
        recursive,
        expected_remaining_files,
    ) = data_test_remove_large_files

    for file, size in zip(path_to_create, files_size):
        with open(joinpath(remote_dir, file), "wb") as f:
            f.write(b"0" * size)

    delete_large_files(
        "",
        remote_path_to_delete_from,
        size_threshold,
        [],
        fsspec.filesystem("file"),
        recursive=recursive,
    )

    files_not_deleted = set(fsspec.filesystem("file").find(remote_dir))
    expected_files = set(ensure_in_list(joinpath(remote_dir, expected_remaining_files)))
    assert files_not_deleted == expected_files


@pytest.fixture(
    params=(
        ("file1", "w"),
        ("file1", "wb"),
    )
)
def data_test_open_bucket_file_writing(request):
    return request.param


def test_test_open_bucket_file_writing(
    mock_bucket_config_with_tmp_dir, data_test_open_bucket_file_writing
):
    remote_dir, _ = mock_bucket_config_with_tmp_dir
    (
        file_name,
        open_mode,
    ) = data_test_open_bucket_file_writing

    remote_fs = fsspec.filesystem("file")
    with open_bucket_file("", file_name, open_mode, [], remote_fs) as f:
        if open_mode == "w":
            f.write("content🙂")
        else:
            f.write(b"content")

    mode = "rb" if open_mode == "wb" else "r"
    with remote_fs.open(joinpath(remote_dir, file_name), mode=mode) as f:
        content = f.read()
        assert content == b"content" if open_mode == "wb" else "content🙂"


@pytest.fixture(
    params=(
        ("file1", "r"),
        ("file1", "rb"),
    )
)
def data_test_open_bucket_file_reading(request):
    return request.param


def test_test_open_bucket_file_reading(
    mock_bucket_config_with_tmp_dir, data_test_open_bucket_file_reading
):
    remote_dir, _ = mock_bucket_config_with_tmp_dir
    (
        file_name,
        open_mode,
    ) = data_test_open_bucket_file_reading

    remote_fs = fsspec.filesystem("file")

    mode = "wb" if open_mode == "rb" else "w"
    with remote_fs.open(joinpath(remote_dir, file_name), mode=mode) as f:
        f.write(b"content" if mode == "wb" else "content🙂")

    with open_bucket_file("", file_name, open_mode, [], remote_fs) as f:
        if open_mode == "r":
            assert f.read() == "content🙂"
        else:
            assert f.read() == b"content"
