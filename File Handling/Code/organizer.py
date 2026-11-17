import os
import shutil
import sys
from pathlib import Path

def organize_directory(target_dir="."):
    """
    Autonomous desktop automation utility that organizes cluttered directories
    by inspecting file extensions, creating category subfolders, and safely moving files.
    """
    target_path = Path(target_dir).resolve()
    
    if not target_path.exists():
        print(f"[Error] Directory '{target_path}' does not exist.")
        return

    # Comprehensive extension mapping dictionary
    extension_map = {
        # Documents
        '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents',
        '.txt': 'Documents', '.xlsx': 'Documents', '.xls': 'Documents',
        '.ppt': 'Documents', '.pptx': 'Documents', '.csv': 'Documents',
        # Images
        '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images',
        '.gif': 'Images', '.bmp': 'Images', '.svg': 'Images', '.webp': 'Images',
        # Videos
        '.mp4': 'Videos', '.mkv': 'Videos', '.avi': 'Videos', '.mov': 'Videos',
        # Archives
        '.zip': 'Archives', '.tar': 'Archives', '.gz': 'Archives',
        '.rar': 'Archives', '.7z': 'Archives',
        # Code & Developer files
        '.py': 'Code', '.js': 'Code', '.html': 'Code', '.css': 'Code',
        '.json': 'Code', '.cpp': 'Code', '.java': 'Code', '.sh': 'Code'
    }

    print("=" * 65)
    print("       AUTOMATED FILE ORGANIZER & CLEANUP UTILITY")
    print("=" * 65)
    print(f"Target Directory: {target_path}\n")

    stats = {
        "relocated": 0,
        "skipped_folders": 0,
        "errors": 0,
        "categories_created": set()
    }

    try:
        # Use os.scandir for high-performance directory traversal
        with os.scandir(target_path) as entries:
            for entry in entries:
                # Skip subdirectories to prevent recursive categorization loops
                if entry.is_dir():
                    stats["skipped_folders"] += 1
                    continue
                
                if entry.is_file():
                    file_path = Path(entry.path)
                    file_ext = file_path.suffix.lower()
                    
                    # Determine category, default to 'Others' for unknown extensions
                    category = extension_map.get(file_ext, 'Others')
                    dest_folder = target_path / category
                    
                    try:
                        # Dynamically create category subfolder if needed
                        if not dest_folder.exists():
                            dest_folder.mkdir(parents=True, exist_ok=True)
                        
                        stats["categories_created"].add(category)
                        dest_path = dest_folder / file_path.name
                        
                        # Handle naming collisions safely by appending an incremental counter
                        if dest_path.exists():
                            base = file_path.stem
                            ext = file_path.suffix
                            counter = 1
                            while True:
                                new_filename = f"{base}_{counter}{ext}"
                                dest_path = dest_folder / new_filename
                                if not dest_path.exists():
                                    break
                                counter += 1

                        # Relocate file safely
                        shutil.move(str(file_path), str(dest_path))
                        print(f"[Moved] '{file_path.name}' -> /{category}/")
                        stats["relocated"] += 1

                    except PermissionError:
                        print(f"[Error] Permission denied for file: {file_path.name}")
                        stats["errors"] += 1
                    except Exception as e:
                        print(f"[Error] Could not move '{file_path.name}': {e}")
                        stats["errors"] += 1

    except PermissionError:
        print(f"[Error] Permission denied to scan directory: {target_path}")
        return
    except Exception as e:
        print(f"[Error] An unexpected error occurred: {e}")
        return

    # Formatted Execution Summary
    print("\n" + "=" * 65)
    print("                      EXECUTION SUMMARY")
    print("=" * 65)
    print(f"Total Files Relocated : {stats['relocated']}")
    print(f"Categories Updated    : {', '.join(sorted(stats['categories_created'])) if stats['categories_created'] else 'None'}")
    print(f"Subdirectories Skipped: {stats['skipped_folders']}")
    print(f"Errors Encountered    : {stats['errors']}")
    print("=" * 65)

if __name__ == "__main__":
    target_directory = sys.argv[1] if len(sys.argv) > 1 else "."
    organize_directory(target_directory)