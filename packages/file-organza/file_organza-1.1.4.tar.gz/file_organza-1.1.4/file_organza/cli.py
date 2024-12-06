import argparse
from file_organza.organizer import FileOrganizer


def main():
    parser = argparse.ArgumentParser(description="Organize your files!")
    parser.add_argument('directory', type=str, help="Directory to organize")
    parser.add_argument('--by-type', action='store_true', help="Organize by file type")
    parser.add_argument('--by-date', action='store_true', help="Organize by file creation date")

    args = parser.parse_args()

    organizer = FileOrganizer(args.directory)

    if args.by_type:
        organizer.organize_by_type()
    elif args.by_date:
        organizer.organize_by_date()
    else:
        print("Please specify how to organize files (by type or by date).")


if __name__ == "__main__":
    main()
