import os
import shutil
from datetime import datetime

class FileOrganizer:
    def __init__(self, directory: str):
        self.directory = directory

    def organize_by_type(self):
        """Move files into folders based on their type."""
        for filename in os.listdir(self.directory):
            filepath = os.path.join(self.directory, filename)
            if os.path.isfile(filepath):
                filetype = filename.split('.')[-1]
                target_dir = os.path.join(self.directory, filetype)
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(filepath, os.path.join(target_dir, filename))

    def organize_by_date(self):
        """Move files into folders based on their creation date."""
        for filename in os.listdir(self.directory):
            filepath = os.path.join(self.directory, filename)
            if os.path.isfile(filepath):
                timestamp = os.path.getmtime(filepath)
                date_folder = datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d')
                target_dir = os.path.join(self.directory, date_folder)
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(filepath, os.path.join(target_dir, filename))
