import os  # For operating system interactions and path manipulations
import glob  # For file pattern matching
import shutil  # For file operations like moving

def get_latest_mp4(subdirectory):
    """
    Finds and returns the most recent MP4 file in the specified subdirectory
    based on the numerical index in the filename.
    
    The function searches for files matching the pattern 'input_*.mp4' in the
    specified subdirectory of the user's home directory. Files are sorted by
    their numerical index to determine the most recent one.
    
    Args:
        subdirectory (str): The subdirectory to search within the user's home directory
                           (e.g., 'inputs' would search in ~/inputs/)
    
    Returns:
        str: Full path to the most recent MP4 file, or None if:
             - Directory doesn't exist
             - No matching files found
             - Filename parsing fails
    
    Example:
        >>> get_latest_mp4('inputs')
        '/home/user/inputs/input_5.mp4'
    """
    # Get the user's home directory for cross-platform compatibility
    home_directory = os.path.expanduser("~")
    
    # Construct full path by joining home directory with subdirectory
    directory = os.path.join(home_directory, subdirectory)
    
    # Debugging output to verify directory existence
    print(f"Checking if directory exists: {directory}")
    if not os.path.exists(directory):
        print("ERROR: Directory does not exist.")
        return None
    
    # Search for all MP4 files with the expected naming pattern
    print(f"Searching for MP4 files in: {directory}")
    files = glob.glob(os.path.join(directory, "input_*.mp4"))
    
    if not files:
        print("No MP4 files found.")
        return None
    
    print(f"Found {len(files)} files: {files}")
    
    try:
        # Sort files by extracting the numerical index from filenames
        # Expected format: input_<number>.mp4
        files.sort(key=lambda x: int(os.path.basename(x).split("_")[1].split(".")[0]))
    except ValueError as e:
        print(f"ERROR: Failed to parse filenames. {e}")
        return None
    
    # The last file in the sorted list is the most recent
    latest_file = files[-1]
    print(f"Latest file found: {latest_file}")
    
    return latest_file

def move_file(old_path, new_path):
    """
    Moves a file from old_path to a new location within the user's home directory,
    creating the destination directory if it doesn't exist.
    
    Args:
        old_path (str): Absolute path to the source file
        new_path (str): Relative path (from home directory) for the destination
    
    Returns:
        str: The full path where the file was moved, or raises exception on failure
    
    Example:
        >>> move_file('/home/user/videos/file.mp4', 'processed_videos')
        '/home/user/processed_videos/file.mp4'
    """
    # Construct the full destination path by joining with home directory
    destination_folder = os.path.join(os.path.expanduser("~"), new_path)
    
    # Create destination directory (including parent directories) if needed
    os.makedirs(destination_folder, exist_ok=True)
    
    # Extract filename from old path and construct new full path
    file_name = os.path.basename(old_path)
    destination_path = os.path.join(destination_folder, file_name)
    
    # Perform the actual file move operation
    shutil.move(old_path, destination_path)
    
    return destination_path