
from dataclasses import dataclass


@dataclass
class File:
    name: str
    project: str
    component: str
    locale: str
    path: str
    
    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        if isinstance(other, File):
            return self.path == other.path
        return False

    def __repr__(self):
        return f"File(name={self.name}, project={self.project}, component={self.component}, locale={self.locale}, path={self.path})"
    
    @staticmethod
    def from_path(project:str, path: str):
        if not path.endswith(".po"):
            return None
        
        parts = path.split('/')
        name = parts[-1]
        locale = parts[1]
        component = name.split('.')[0]

        return File(
            name = name,
            project = project,
            locale = locale,
            component = component,
            path = path,
        )