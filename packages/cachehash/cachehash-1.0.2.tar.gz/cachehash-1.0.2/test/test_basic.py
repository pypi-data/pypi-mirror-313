import os
import datetime
import tempfile
from pathlib import Path
from time import sleep

from cachehash.main import Cache


def test_basics():
    test_db = Path("test.db")
    assert not test_db.exists(), "Test DB exists"
    cache = Cache("test.db")
    now = str(datetime.datetime.now())
    sleep(0.1)
    this_file = os.path.abspath(__file__)
    cache.set(this_file, {"now": now})
    sleep(0.1)
    new_now = cache.get(this_file)["now"]

    assert test_db.exists(), "Test DB not created"
    assert now == new_now, "Invalid 'now"
    os.remove(test_db)
    assert not test_db.exists(), "Test DB not removed"


def test_directory_hash():
    # Clean up any leftover test DB from previous runs
    test_db = Path("test_dir.db")
    if test_db.exists():
        os.remove(test_db)

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test DB
        assert not test_db.exists(), "Test DB exists"
        cache = Cache("test_dir.db")

        # Create some test files
        (temp_path / "file1.txt").write_text("content1")
        (temp_path / "file2.txt").write_text("content2")
        subdir = temp_path / "subdir"
        subdir.mkdir()
        (subdir / "file3.txt").write_text("content3")

        # Test initial cache
        now = str(datetime.datetime.now())
        cache.set(temp_path, {"now": now})
        cached_value = cache.get(temp_path)
        assert cached_value["now"] == now, "Initial cache failed"

        # Modify a file and verify cache invalidation
        sleep(0.1)  # Ensure modification time changes
        (temp_path / "file1.txt").write_text("modified content")
        cached_value = cache.get(temp_path)
        assert cached_value is None, (
            "Cache should be invalid after file modification"
        )

        os.remove(test_db)
        assert not test_db.exists(), "Test DB not removed"
