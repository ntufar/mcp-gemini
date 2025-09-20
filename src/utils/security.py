import os

def is_path_safe(base_dir: str, target_path: str) -> bool:
    # Resolve to absolute paths to handle '..' and symlinks
    base_dir = os.path.abspath(base_dir)
    
    # Resolve the real path of the target, following symlinks
    real_target_path = os.path.realpath(target_path)

    # Check if the real target path starts with the base directory
    return real_target_path.startswith(base_dir)

