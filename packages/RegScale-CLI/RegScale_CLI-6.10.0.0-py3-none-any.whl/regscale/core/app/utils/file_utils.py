import os
from pathlib import Path
from typing import Union, List, Iterator
from datetime import datetime


def is_s3_path(path: Union[str, Path]) -> bool:
    """
    Check if the given path is an S3 URI.

    :param Union[str, Path] path: The path to check
    :return: True if the path is an S3 URI, False otherwise
    :rtype: bool
    """
    return isinstance(path, str) and path.startswith("s3://")


def read_file(file_path: Union[str, Path]) -> str:
    """
    Read a file from local filesystem or S3.

    :param Union[str, Path] file_path: Path to the file or S3 URI
    :return: Content of the file
    :rtype: str
    """
    import smart_open  # type: ignore # Optimize import performance

    with smart_open.open(str(file_path), "r") as f:
        return f.read()


def find_files(path: Union[str, Path], pattern: str) -> List[Union[Path, str]]:
    """
    Find all files matching the pattern in the given path, including S3.

    :param Union[str, Path] path: Path to a file, a folder, or an S3 URI
    :param str pattern: File pattern to match (e.g., "*.nessus")
    :return: List of Path objects for matching files or S3 URIs
    :rtype: List[Union[Path, str]]
    """
    import boto3  # type: ignore # Optimize import performance

    if is_s3_path(path):
        s3_parts = path[5:].split("/", 1)
        bucket = s3_parts[0]
        prefix = s3_parts[1] if len(s3_parts) > 1 else ""

        s3 = boto3.client("s3")
        paginator = s3.get_paginator("list_objects_v2")

        files: List[Union[Path, str]] = []
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                if obj["Key"].endswith(pattern.lstrip("*")):
                    files.append(f"s3://{bucket}/{obj['Key']}")
        return files

    file_path = Path(path)
    if file_path.is_file():
        return [file_path] if file_path.match(pattern) else []
    return list(file_path.glob(pattern))


def move_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
    """
    Move a file from src to dst. Works with local files and S3.

    :param Union[str, Path] src: Source file path or S3 URI
    :param Union[str, Path] dst: Destination file path or S3 URI
    """
    import smart_open  # type: ignore # Optimize import performance

    if is_s3_path(src):
        import boto3  # type: ignore # Optimize import performance

        # S3 to S3 move
        if is_s3_path(dst):
            s3 = boto3.client("s3")
            src_parts = src[5:].split("/", 1)
            dst_parts = dst[5:].split("/", 1)
            s3.copy_object(
                CopySource={"Bucket": src_parts[0], "Key": src_parts[1]}, Bucket=dst_parts[0], Key=dst_parts[1]
            )
            s3.delete_object(Bucket=src_parts[0], Key=src_parts[1])
        else:
            # S3 to local
            with smart_open.open(src, "rb") as s_file, smart_open.open(dst, "wb") as d_file:
                d_file.write(s_file.read())
            s3 = boto3.client("s3")
            src_parts = src[5:].split("/", 1)
            s3.delete_object(Bucket=src_parts[0], Key=src_parts[1])
    else:
        # Local to local or local to S3
        with smart_open.open(src, "rb") as s_file, smart_open.open(dst, "wb") as d_file:
            d_file.write(s_file.read())
        if not isinstance(dst, str) or not dst.startswith("s3://"):
            os.remove(src)


def iterate_files(file_collection: List[Union[Path, str]]) -> Iterator[Union[Path, str]]:
    """
    Iterate over a collection of files, yielding each file path.

    :param List[Union[Path, str]] file_collection: List of file paths or S3 URIs
    :yield: Each file path or S3 URI
    :rtype: Iterator[Union[Path, str]]
    """
    for file in file_collection:
        yield file


def get_processed_file_path(file_path: Union[str, Path], processed_folder: str = "processed") -> Union[str, Path]:
    """
    Generate a path for the processed file, handling both local and S3 paths.

    :param Union[str, Path] file_path: Original file path or S3 URI
    :param str processed_folder: Name of the folder for processed files (default: "processed")
    :return: Path or S3 URI for the processed file
    :rtype: Union[str, Path]
    """
    if is_s3_path(file_path):
        s3_parts = file_path[5:].split("/")  # type: ignore  # is_s3_path ensures string
        bucket = s3_parts[0]
        key = "/".join(s3_parts[1:])
        new_key = f"processed/{os.path.basename(key)}"
        return f"s3://{bucket}/{new_key}"
    else:
        file_path = Path(file_path)
        timestamp = datetime.now().strftime("%Y%m%d-%I%M%S%p")
        new_filename = f"{file_path.stem}_{timestamp}{file_path.suffix}".replace(" ", "_")
        new_path = file_path.parent / processed_folder / new_filename
        os.makedirs(new_path.parent, exist_ok=True)
        return new_path
