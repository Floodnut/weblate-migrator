import os

from typing import List
from metadata import File
from pathlib import Path


def _po_to_pot(po_file_path: str, pot_file_path: str):
    with open(po_file_path, 'r', encoding='utf-8') as po_file:
        lines = po_file.readlines()
    
    pot_lines = []
    in_msgid_block = False
    
    for line in lines:

        if line.startswith('msgid'):
            in_msgid_block = True
            pot_lines.append(line)

        elif line.startswith('msgstr'):
            if in_msgid_block:
                pot_lines.append('msgstr ""\n')
                in_msgid_block = False
        else:
            pot_lines.append(line)
    
        # POT 파일로 저장
        with open(pot_file_path, 'w', encoding='utf-8') as pot_file:
            pot_file.writelines(pot_lines)

def po_to_pot(po_file_path: str, pot_file_path: str):
    """Convert a .po file to a .pot file."""
    
    try:
        import polib
        po = polib.pofile(po_file_path)
        pot = polib.POFile()

        for entry in po:
            entry.msgstr = ""
            pot.append(entry)

        pot.save(pot_file_path)
    except ImportError:
        _po_to_pot(po_file_path, pot_file_path)


def find_all_doc_files(project: str, path: str) -> List[File]:
    """Find all doc files in the given path and return a list of File objects.
    
    If the template file(.pot) does not exist, create it from the doc file.
    """
    
    root_path = Path(path)

    files: List[File] = []
    for file in root_path.rglob('*.po'):
        if file.is_file():
            po_file = File.from_path(project, path)
            files.append(po_file)

        if not Path(files[-1].template_path).is_file():
            po_to_pot(files[-1].path, files[-1].template_path)
    
    return files
    

def find_all_project_name_from_dirs(base_path: str="./") -> List[str]:
    """Find all project names from the given path and return a list of project names."""
    
    directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    return directories
