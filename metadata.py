
from dataclasses import dataclass


@dataclass
class File:
    name: str
    project: str
    component: str
    locale: str
    path: str
    template_path: str
    
    @staticmethod
    def from_path(project:str, path: str):
        if not path.endswith(".po"):
            return None
        
        parts = path.split('/')
        name = parts[-1]
        locale = parts[0]
        component = name.split('.')[0]
        template_path = f"{project}/{component}.pot"

        return File(
            name = name,
            project = project,
            locale = locale,
            component = component,
            path = path,
            template = template_path
        )