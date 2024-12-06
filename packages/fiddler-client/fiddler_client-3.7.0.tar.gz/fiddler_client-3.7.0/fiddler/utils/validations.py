from pathlib import Path


def validate_artifact_dir(artifact_dir: Path) -> None:
    """Check if artifact directory exists."""
    if not artifact_dir.is_dir():
        raise ValueError(f'{artifact_dir} is not a valid model directory')

    package_file_path = artifact_dir / 'package.py'
    if not package_file_path.is_file():
        raise ValueError(f'package.py file not found at {package_file_path}')
