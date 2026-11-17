import os
import shutil
import logging
from pathlib import Path

file_categories = {
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".csv": "Documents",
    ".xlsx": "Documents",
    ".pptx": "Documents",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".svg": "Images",

    # Videos
    ".mp4": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",
    ".mkv": "Videos",

    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",

    # Code
    ".py": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".html": "Code",
    ".css": "Code",
    ".js": "Code",
    ".php": "Code"
}

logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_unique_path(destination):
    original = destination
    counter = 1

    while destination.exists():
        destination = original.with_name(
            f"{original.stem}_{counter}{original.suffix}"
        )
        counter += 1

    return destination

def organize_files(folder_path):

    folder = Path(folder_path)

    if not folder.is_dir():
        print("Invalid directory!")
        return

    moved = 0
    skipped = 0
    failed = 0

    for entry in os.scandir(folder):

        if not entry.is_file():
            continue

        source = Path(entry.path)

        # Ignore the organizer script itself
        if source.name == "organizer.py":
            skipped += 1
            continue

        extension = source.suffix.lower()

        # Find the category
        category = file_categories.get(extension)

        if category is None:
            print(f"Skipped: {source.name} (Unknown file type)")
            skipped += 1
            continue

        # Create the category folder
        destination_folder = folder / category

        try:
            destination_folder.mkdir(exist_ok=True)

            # Avoid filename collisions
            destination = get_unique_path(
                destination_folder / source.name
            )

            # Move the file
            shutil.move(str(source), str(destination))

            print(f"Moved: {source.name} -> {category}")
            logging.info(f"Moved {source.name} to {category}")

            moved += 1

        except PermissionError:
            print(f"Permission denied: {source.name}")
            logging.error(f"Permission denied: {source.name}")
            failed += 1

        except FileExistsError:
            print(f"File already exists: {source.name}")
            logging.error(f"File already exists: {source.name}")
            failed += 1

        except OSError as error:
            print(f"Error moving {source.name}: {error}")
            logging.error(f"Error moving {source.name}: {error}")
            failed += 1

    # Execution summary
    print("\n========== ORGANIZATION SUMMARY ==========")
    print(f"Files successfully moved : {moved}")
    print(f"Files skipped            : {skipped}")
    print(f"Files failed             : {failed}")
    print("==========================================")

    logging.info(
        f"Organization completed. Moved: {moved}, "
        f"Skipped: {skipped}, Failed: {failed}"
    )

if __name__ == "__main__":
    print("===== AUTOMATIC FILE ORGANIZER =====")

    folder_path = input("Enter the directory path to organize: ")

    organize_files(folder_path)