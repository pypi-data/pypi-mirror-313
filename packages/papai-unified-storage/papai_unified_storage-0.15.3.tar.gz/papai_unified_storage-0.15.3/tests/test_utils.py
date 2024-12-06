import os
from tempfile import TemporaryDirectory

import fsspec
import pytest


@pytest.mark.parametrize(
    "paths_pieces, expected_result",
    (
        (["a", "b", "c"], "a/b/c"),
        (["a", "", "c"], "a/c"),
        (["a/", "/b/", "//c"], "a/b/c"),
        (["a/", "/b/", "//c/"], "a/b/c/"),
        (["a", ["b", "c"]], ["a/b", "a/c"]),
        (
            [["a", "b"], ["c", "d"]],
            ["a/c", "a/d", "b/c", "b/d"],
        ),
        (["a", ["b", "c"], "d"], ["a/b/d", "a/c/d"]),
        ([["a", "", "b"], ["c", "d"], "e"], ["a/c/e", "a/d/e", "b/c/e", "b/d/e"]),
        ([["a", "b", "c"], ["", ""], "e"], ["a/e", "b/e", "c/e"]),
        ([["", ""], ["a", "b", "c"], "e"], ["a/e", "b/e", "c/e"]),
    ),
)
def test_joinpath(paths_pieces, expected_result):
    from papai_unified_storage import joinpath

    assert joinpath(*paths_pieces) == expected_result


def test_create_local_dir_tree_folder():
    from papai_unified_storage.utils import create_dir_tree

    with TemporaryDirectory() as d:
        create_dir_tree(fsspec.filesystem("file"), f"{d}/a/b/c/")

        assert os.path.exists(f"{d}/a/b/c/")
