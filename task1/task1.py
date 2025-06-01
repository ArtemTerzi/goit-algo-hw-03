import argparse
import shutil
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description="Copies files in a subdirectory by extension.")
    parser.add_argument("source", type=Path, help="Path to the source directory")
    parser.add_argument("destination", type=Path, nargs="?", default=Path("dist"), help="Path to the destination directory (default: dist)")
    return parser.parse_args()

def copy_files_by_type(src: Path, dst: Path) -> None:
    try:
        if not src.exists():
            print(f"The source directory does not exist: {src}")
            return
        for item in src.iterdir():
            if item.is_dir():
                copy_files_by_type(item, dst)
            elif item.is_file():
                try:
                    extension = item.suffix[1:] if item.suffix else "no_extension"
                    target_dir = dst / extension
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target_dir / item.name)
                    print(f"Copied: {item} → {target_dir / item.name}")
                except (OSError, shutil.Error) as e:
                    print(f"Copy error {item}: {e}")
    except PermissionError as e:
        print(f"Access denied: {src} - {e}")
    except Exception as e:
        print(f"An error occurred while copying files from the {src} directory: {e}")

def main():
    args = parse_arguments()
    source_dir = args.source.resolve()
    destination_dir = args.destination.resolve()

    print(f"Source folder: {source_dir}")
    print(f"Destination folder: {destination_dir}")

    copy_files_by_type(source_dir, destination_dir)


if __name__ == "__main__":
    main()