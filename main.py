import os

from wlc import Weblate
from wlc.config import WeblateConfig


class WeblateMigrator(Weblate):
    """https://docs.weblate.org/en/latest/user/files.html#uploading-translation-files"""
    
    def __init__(self, key: str, url: str):
        super().__init__(key=key, url=url, config=WeblateConfig())
                        
    def _create_project_if_not_exists(self, project_name):
        try:
            self.create_project(project_name)
        except Exception as e:
            print(f"Failed to create project: {project_name}, Error: {str(e)}")
            
    def _create_component_if_not_exists(self, project_name, component_name):
        try:
            self.create_component(project_name, component_name)
        except Exception as e:
            print(f"Failed to create component: {component_name}, Error: {str(e)}")
            
    def _upload_pre_translated_po_files(self, project_name, component_name, directory_path):
        pass
            
    def upload_translation_po_files(self, translation_id, directory_path):
        for filename in os.listdir(directory_path):
            if filename.endswith(".po"):
                file_path = os.path.join(directory_path, filename)

                with open(file_path, "rb") as file_content:
                    try:
                        self.upload_translation_file(translation_id, file_content)
                        print(f"Successfully uploaded: {filename}")
                    except Exception as e:
                        print(f"Failed to upload: {filename}, Error: {str(e)}")


if __name__ == "__main__":
    key = 'sample'
    url = 'https://example.weblate.org'
    
    weblate_migrator = WeblateMigrator(key, url)
    weblate_migrator.upload_translation_po_files("/path/to/your/po/files", "your_translation_id")