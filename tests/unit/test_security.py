import pytest
import os
from src.utils.security import is_path_safe

@pytest.fixture
def mock_root_dir(tmp_path):
    return tmp_path

def test_is_path_safe_within_root(mock_root_dir):
    safe_path = mock_root_dir / "subdir" / "file.txt"
    safe_path.parent.mkdir()
    safe_path.touch()
    assert is_path_safe(str(mock_root_dir), str(safe_path)) is True

def test_is_path_safe_outside_root_dot_dot(mock_root_dir):
    # Attempt to go up a directory from root
    outside_path = mock_root_dir.parent / "outside_file.txt"
    assert is_path_safe(str(mock_root_dir), str(outside_path)) is False

def test_is_path_safe_outside_root_absolute_path(mock_root_dir):
    # Attempt to access an absolute path outside root
    outside_path = "/etc/passwd"
    assert is_path_safe(str(mock_root_dir), outside_path) is False

def test_is_path_safe_symlink_within_root(mock_root_dir):
    # Symlink within root pointing to a file within root
    target_file = mock_root_dir / "target.txt"
    target_file.touch()
    symlink = mock_root_dir / "symlink_to_target.txt"
    os.symlink(target_file, symlink)
    assert is_path_safe(str(mock_root_dir), str(symlink)) is True

def test_is_path_safe_symlink_outside_root(mock_root_dir):
    # Symlink within root pointing to a file outside root
    outside_file = mock_root_dir.parent / "outside_target.txt"
    outside_file.touch()
    symlink = mock_root_dir / "symlink_to_outside.txt"
    os.symlink(outside_file, symlink)
    assert is_path_safe(str(mock_root_dir), str(symlink)) is False
