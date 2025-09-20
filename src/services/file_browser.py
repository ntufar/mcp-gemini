import os
import datetime
from src.utils.security import is_path_safe
import base64

class PermissionDeniedError(Exception):
    """Custom exception for permission denied errors."""
    pass

class FileBrowser:
    def __init__(self, root_dir: str):
        self.root_dir = os.path.abspath(root_dir)

    def _resolve_path(self, path: str) -> str:
        full_path = os.path.abspath(os.path.join(self.root_dir, path))
        if not is_path_safe(self.root_dir, full_path):
            raise ValueError("Attempted to access path outside root directory")
        return full_path

    def list_directory(self, path: str):
        full_path = self._resolve_path(path)
        if not os.path.isdir(full_path):
            raise FileNotFoundError(f"Directory not found: {path}")

        files = []
        directories = []

        try:
            with os.scandir(full_path) as entries:
                for entry in entries:
                    entry_path = os.path.join(path, entry.name)
                    if entry.is_file():
                        stat = entry.stat()
                        files.append({
                            "name": entry.name,
                            "path": entry_path,
                            "size": stat.st_size,
                            "modified_date": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat() + "Z"
                        })
                    elif entry.is_dir():
                        directories.append({
                            "name": entry.name,
                            "path": entry_path
                        })
            return {"files": files, "directories": directories}
        except PermissionError:
            raise PermissionDeniedError(f"Permission denied to list directory: {path}")

    def read_file(self, path: str):
        full_path = self._resolve_path(path)
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"File not found: {path}")
        
        file_size = os.path.getsize(full_path)
        if file_size > 10 * 1024 * 1024:  # 10 MB limit
            raise ValueError(f"File size exceeds the 10MB limit: {path}")

        try:
            with open(full_path, "rb") as f:
                content_bytes = f.read()
        except PermissionError:
            raise PermissionDeniedError(f"Permission denied to read file: {path}")

        try:
            # Attempt to decode as UTF-8. If it fails, treat as binary.
            content = content_bytes.decode("utf-8")
            return content
        except UnicodeDecodeError:
            # If decoding fails, base64 encode the bytes
            return base64.b64encode(content_bytes).decode("utf-8")
