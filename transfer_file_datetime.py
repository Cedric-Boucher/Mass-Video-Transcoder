import os
import win32_setctime
from tqdm import tqdm
import argparse

def transfer_file_datetime(source_file_path: str, destination_file_path: str) -> None:
    """
    Will try to get the source modification, creation, and accessed time,
    and set the destination modification, creation, and accessed time to match.
    If any of those steps fail, the remaining steps are still attempted, but the last
    caught exception is raised before returning
    """
    exception: Exception | None = None

    try:
        source_modification_time: float = os.path.getmtime(source_file_path)
        source_accessed_time: float = os.path.getatime(source_file_path)
        os.utime(destination_file_path, (source_accessed_time, source_modification_time))
    except Exception as e:
        exception = e

    try:
        source_creation_time: float = os.path.getctime(source_file_path)
        win32_setctime.setctime(destination_file_path, source_creation_time)
    except Exception as e:
        exception = e

    if exception is not None:
        raise exception

def transfer_all_file_datetimes(source_directory_path: str, destination_directory_path: str) -> list[Exception]:
    """
    For each file in the source directory (recursive),
    look for a file with a matching name (extension is excluded) in the destination directory (also recursive).
    If there is a match, get the source file modification, creation, and accessed time,
    and set the destination modification, creation, and accessed time to match.
    If any of the steps fail at any time, exceptions are caught and kept in a list,
    and that list is returned to be handled by the caller
    """
    exceptions: list[Exception] = list()
    destination_file_paths: dict[str, list[str]] = dict() # {file_name_no_extension: [file_paths]} for O(1) search
    for directory_path, _, file_names in tqdm(os.walk(destination_directory_path), desc="Recursively Scanning Destination Directory"):
        for file_name in file_names:
            file_name_no_extension: str = os.path.splitext(file_name)[0]
            file_path: str = os.path.join(directory_path, file_name)
            try:
                destination_file_paths[file_name_no_extension].append(file_path)
            except:
                destination_file_paths[file_name_no_extension] = [file_path]

    for directory_path, _, file_names in tqdm(os.walk(source_directory_path), desc="Recursively Scanning Source Directory and Applying Datetime Transfers to Destination Matches"):
        for file_name in file_names:
            file_name_no_extension: str = os.path.splitext(file_name)[0]
            destination_match: list[str] | None = destination_file_paths.get(file_name_no_extension)
            if destination_match is None:
                continue
            source_file_path: str = os.path.join(directory_path, file_name)
            for destination_file_path in destination_match:
                try:
                    transfer_file_datetime(source_file_path, destination_file_path)
                except Exception as e:
                    exceptions.append(e)

    return exceptions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transfer File Datetime")
    parser.add_argument('--source', '-src', required=True, type=str, help="Source Directory Path")
    parser.add_argument('--destination', '-dst', required=True, type=str, help="Destination Directory Path")
    args = parser.parse_args()
    source_directory_path: str = args.source
    destination_directory_path: str = args.destination

    transfer_all_file_datetimes(source_directory_path, destination_directory_path)
