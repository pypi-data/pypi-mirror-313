"""
These tests, as beautiful as they might be, are not perfect. The biggest
limitation is that the file sotrage tested can only be the local one since
tempfile is used. It relies on OS specification to create and remove
temporary files / folders. Unfortunately, it cannot be extended to every
file system support in fsspec.

Tests of read/write methods are not isolated, and they rely on each other
to pass. If the tests fails, one of them (or both) is the culprit.
"""

import os
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from papai_unified_storage.storage import filesystem
from papai_unified_storage.utils import joinpath
from tests.utils import create_files


@pytest.fixture()
def fs():
    return filesystem("file", auto_mkdir=False)


def test_dataframe_read_parquet(fs):
    import pandas as pd

    df = pd.DataFrame(
        {
            "one": [-1, 1, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )
    with TemporaryDirectory() as d:
        df.to_parquet(f"{d}/test.parquet")

        df_wrote_read = fs.read_dataset_from_parquet(f"{d}/test.parquet")

    assert df.equals(df_wrote_read)


def test_read_dataset_from_parquet_decimal(fs):
    from decimal import Decimal
    from random import random

    import numpy as np
    from pyarrow import Table, parquet

    ar_deci_1 = [Decimal(random()) for _ in range(100)]
    ar_deci_2 = [Decimal(random() * 10) for _ in range(100)]
    ar_float = [random() * 100 for _ in range(100)]
    ar_string = ["moi" for _ in range(100)]

    table = Table.from_arrays(
        [ar_deci_1, ar_deci_2, ar_float, ar_string],
        names=["ar_deci_1", "ar_deci_2", "ar_float", "ar_string"],
    )
    with TemporaryDirectory() as d:
        parquet.write_table(table, f"{d}/test.parquet")

        df_read = fs.read_dataset_from_parquet(f"{d}/test.parquet")

    assert isinstance(df_read["ar_deci_1"].dtype, type(np.dtype("float64")))
    assert isinstance(df_read["ar_deci_2"].dtype, type(np.dtype("float64")))
    assert isinstance(df_read["ar_float"].dtype, type(np.dtype("float64")))
    assert isinstance(df_read["ar_string"].dtype, type(np.dtype("object")))


def test_dataframe_write_parquet(fs):
    import pandas as pd

    df = pd.DataFrame(
        {
            "one": [-1, 1, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )

    with TemporaryDirectory() as d:
        fs.write_dataframe_to_parquet(f"{d}/test.parquet", df)

        df_wrote_read = pd.read_parquet(f"{d}/test.parquet")

        assert df.equals(df_wrote_read)


@pytest.fixture
def tmp_directories():
    with TemporaryDirectory() as remote:
        with TemporaryDirectory() as local:
            yield remote, local


@pytest.fixture(
    params=(
        (
            ["f1", "d/f2", "d/f3", "d/d/g1"],
            ["f1", "d/f2"],
            "",
            ["f1", "f2"],
            {"recursive": False},
        ),
        (
            ["f1", "d/f1", "d/f2", "d/f3", "d/d/g1"],
            ["d/f*"],
            "",
            ["f1", "f2", "f3"],
            {"recursive": False},
        ),
        (
            ["f1", "d/f1", "d/f2", "d/f3", "d/d/g1"],
            ["d/**"],
            "",
            ["f1", "f2", "f3"],
            {"recursive": False},
        ),
        (
            ["file1", "dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"],
            ["file1", "dir1/dir2/file1"],
            ["download/file1", "download/file2"],
            ["download/file1", "download/file2"],
            {"recursive": False},
        ),
        (
            ["file1", "dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"],
            ["file1", "dir1/"],
            "download",
            [
                "download/file1",
                "download/file2",
                "download/file3",
            ],
            {"recursive": True},
        ),
        # You can't download a folders at a different locations than the rest
        (
            ["file1", "dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"],
            ["file1", "dir1/"],
            ["download1/file1", "download2/"],
            [
                "download1/file1",
                "download2/",
            ],
            {"recursive": True},
        ),
    )
)
def data_test_get(request):
    return request.param


def test_get(
    fs,
    tmp_directories,
    data_test_get,
):
    remote_dir, local_dir = tmp_directories
    (
        remote_paths_to_create,
        get_rpaths,
        get_lpath,
        expected_existing_files,
        get_kwargs,
    ) = data_test_get

    create_files(joinpath(remote_dir, remote_paths_to_create))

    fs.get(
        joinpath(remote_dir, get_rpaths), joinpath(local_dir, get_lpath), **get_kwargs
    )

    for file in expected_existing_files:
        assert os.path.exists(joinpath(local_dir, file))


@pytest.fixture(
    params=(
        (
            ["file1", "dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"],
            "file1",
            "upload/file1",
            ["upload/file1"],
            {"recursive": False},
        ),
        (
            ["file1", "dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"],
            "dir1/**",
            "upload/",
            [
                "upload/file1",
                "upload/file2",
                "upload/file3",
                "upload/dir2/file1",
            ],
            {"recursive": False},
        ),
        (
            ["file1", "dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"],
            "dir1",
            "upload/",
            [
                "upload/dir1/file1",
                "upload/dir1/file2",
                "upload/dir1/file3",
                "upload/dir1/dir2/file1",
            ],
            {"recursive": True},
        ),
        (
            ["file1", "dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"],
            ["file1", "dir1/dir2/file1"],
            ["upload/file1", "upload/file2"],
            ["upload/file1", "upload/file2"],
            {"recursive": False},
        ),
        (
            ["file1", "dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"],
            ["file1", "dir1/"],
            "upload",
            [
                "upload/file1",
                "upload/file2",
                "upload/file3",
            ],
            {"recursive": True},
        ),
        # You can't upload a folders at a different locations than the rest
        (
            ["file1", "dir1/file1", "dir1/file2", "dir1/file3", "dir1/dir2/file1"],
            ["file1", "dir1/"],
            ["upload1/file1", "upload2/"],
            [
                "upload1/file1",
                "upload2/",
            ],
            {"recursive": True},
        ),
    )
)
def data_test_put(request):
    return request.param


def test_put(
    fs,
    tmp_directories,
    data_test_put,
):
    remote_dir, local_dir = tmp_directories
    (
        local_paths_to_create,
        put_lpath,
        put_rpaths,
        expected_existing_files,
        put_kwargs,
    ) = data_test_put

    create_files(joinpath(local_dir, local_paths_to_create))

    fs.put(
        joinpath(local_dir, put_lpath), joinpath(remote_dir, put_rpaths), **put_kwargs
    )

    for file in expected_existing_files:
        assert os.path.exists(joinpath(remote_dir, file))


def test_list_files(fs):
    with TemporaryDirectory() as d:
        create_files([f"{d}/f1", f"{d}/d/f2"])

        assert set(fs.list_files(d, recursive=True)) == {f"{d}/f1", f"{d}/d/f2"}
        assert set(fs.list_files(d)) == {f"{d}/f1"}


def test_list_files_with_details(fs):
    with TemporaryDirectory() as d:
        create_files([f"{d}/f1", f"{d}/d/f2"])

        list_files = fs.list_files(d, recursive=True, detail=True)
        assert len(list_files) == 2
        for file_detail, file_name, file_size in zip(
            list_files.values(), [f"{d}/d/f2", f"{d}/f1"], [65, 63]
        ):
            assert file_detail["name"] == file_name
            assert file_detail["size"] == file_size


def test_glob_files_with_details(fs):
    with TemporaryDirectory() as d:
        create_files([f"{d}/f1", f"{d}/d/f1", f"{d}/d/f2", f"{d}/d/f3"])

        list_files = fs.glob_files(f"{d}/d/f*", detail=True)
        assert len(list_files) == 3
        for file_detail, file_name, file_size in zip(
            list_files.values(), [f"{d}/d/f1", f"{d}/d/f2", f"{d}/d/f3"], [65, 65, 65]
        ):
            assert file_detail["name"] == file_name
            assert file_detail["size"] == file_size


def test_list_files_without_root_folder_name(fs):
    with TemporaryDirectory() as d:
        create_files([f"{d}/f1", f"{d}/d/f2"])

        d_without_root = d.strip("/").split("/", 1)[1]

        assert set(fs.list_files(d, recursive=True, remove_root_folder=True)) == {
            f"{d_without_root}/f1",
            f"{d_without_root}/d/f2",
        }

        root_folder = d.strip("/").split("/", 1)[0]
        root_folder_with_sep = fs.sep + root_folder + fs.sep
        assert set(
            fs.list_files(d, recursive=True, remove_prefix=root_folder_with_sep)
        ) == {
            f"{d_without_root}/f1",
            f"{d_without_root}/d/f2",
        }


def test_list_files_without_root_folder_name_and_remove_prefix(fs):
    with TemporaryDirectory() as d:
        first_folder_name = d.split("/", 2)[1] + fs.sep
        d_without_root_nor_first_folder = d.split("/", 2)[2]

        create_files([f"{d}/f1", f"{d}/d/f2"])

        assert set(
            fs.list_files(
                d,
                recursive=True,
                remove_root_folder=True,
                remove_prefix=first_folder_name,
            )
        ) == {
            f"{d_without_root_nor_first_folder}/f1",
            f"{d_without_root_nor_first_folder}/d/f2",
        }


def test_remove_files(fs):
    with TemporaryDirectory() as d:
        create_files([f"{d}/f1", f"{d}/d/f2"])

        fs.remove_files([f"{d}/f1", f"{d}/d/f2"])

        assert not os.path.exists(f"{d}/f1")
        assert not os.path.exists(f"{d}/d/f2")


def test_open_read_write(fs):
    with NamedTemporaryFile(mode="wb+") as file:
        with fs.open_for_writing(file.name) as f:
            f.write(b"content")

        with fs.open_for_reading(file.name) as f:
            assert f.read() == b"content"


def test_move(fs):
    with TemporaryDirectory() as d:
        # create a file
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        fs.move(f"{d}/f1", f"{d}/f2")

        assert not os.path.exists(f"{d}/f1")
        assert os.path.exists(f"{d}/f2")


def test_bytes_to_file(fs):
    with TemporaryDirectory() as d:
        file_path = f"{d}/file"
        fs.write_to_file(file_path, b"content")

        with open(file_path, "rb") as f:
            assert f.read() == b"content"


def test_str_to_file(fs):
    with TemporaryDirectory() as d:
        file_path = f"{d}/file"
        fs.write_to_file(file_path, "content")

        with open(file_path) as f:
            assert f.read() == "content"


@pytest.fixture
def json_data():
    return {"a": 1, "b": 2, "c": 3}


def test_loader(fs, json_data: dict):
    import json

    with TemporaryDirectory() as d:
        with open(f"{d}/json", "w") as file:
            json.dump(json_data, file)

        out_model: dict = fs.loader(file.name, json.load, text=True)

        for key_item_1, key_item_2 in zip(json_data.items(), out_model.items()):
            if key_item_1[1] != key_item_2[1]:
                assert False
