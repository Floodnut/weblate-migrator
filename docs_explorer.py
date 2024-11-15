import os

from typing import List
from metadata import File
from pathlib import Path


def find_all_doc_files(project: str, path: str) -> List[File]:
    """Find all doc files in the given path and return a list of File objects.
    
    If the template file(.po) does not exist, create it from the doc file.
    """
    
    root_path = Path(path)

    files: List[File] = []
    for file in root_path.rglob('*.po'):
        if file.is_file():
            po_file = File.from_path(project, file.as_posix())
            files.append(po_file)
    
    return list(set(files))
    

def find_all_project_name_from_dirs(base_path: str="./") -> List[str]:
    """Find all project names from the given path and return a list of project names."""
    
    directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    return directories
