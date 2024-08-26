import os

import logging

from requests import Response

from http_client import HttpClient
from . import OPENDEV_OPENSTACK_WEB


logger = logging.getLogger(__name__)

class WeblateMigrator(HttpClient):
    """https://docs.weblate.org/en/latest/user/files.html#uploading-translation-files"""
    
    def __init__(self, url: str, key: str):
        super().__init__(base_url=url, key=key)
        
    def _get_project(self, project_name: str) -> Response:
        return self.get(f"api/projects/{project_name}/")
    
    def _create_project(self, project_name: str) -> Response:
        data = {
            "name": f"openstack/{project_name}",
            "slug": f"openstack_{project_name}",
            "web": f"{OPENDEV_OPENSTACK_WEB}{project_name}",
        }
        return self.post("api/projects/", data)
    
    def _get_component(self, project_name: str, component_name: str) -> Response:
        return self.get(f"api/projects/{project_name}/components/{component_name}/")
    
    def _create_component(self, project_name: str, component_name: str) -> Response:
        data = {
            "name": component_name,
            "slug": component_name,
        }
        return self.post(f"api/projects/{project_name}/components/", data)
        
    def get_or_create_project(self, project_name: str):
        try:
            res = self._get_project(project_name)
            if res.status_code == 404:
                res = self.create_project(project_name)

            return res.json()
        except Exception as e:
            logger.error(f"Failed to get project: {project_name}, Error: {str(e)}")
            
    def get_or_create_component(self, project_name: str, component_name: str):
        try:
            res = self._get_component(project_name, component_name)
            if res.status_code == 404:
                res = self.create_component(project_name, component_name)

            return res.json()
        except Exception as e:
            logger.error(f"Failed to get component: {project_name}/{component_name}, Error: {str(e)}")
 
            
    def _upload_pre_translated_po_files(self, project_name: str, component_name: str, directory_path: str):
        pass
            
    def upload_translation_po_files(self, translation_id: str, directory_path: str):
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
    migrator = WeblateMigrator()
