import os

import logging
import re
from typing import List

from requests import Response

from http_client import HttpClient


OPENDEV_OPENSTACK_WEB = "https://opendev.org/openstack/"
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
    
    def parse_language(self, language: str) -> str:
        """parse language from locale

        e.g. ko_KR -> ko
        """
        match = re.match(r'^([a-z]+)_', language)
        if match:
            return match.group(1)
        else:
            return language
        
    def get_or_create_project(self, project_name: str):
        try:
            res = self._get_project(project_name)
            if res.status_code == 404:
                res = self._create_project(project_name)

            return res.json()
        except Exception as e:
            logger.error(f"Failed to get project: {project_name}, Error: {e}")
            
    def get_or_create_component(self, project_name: str, component_name: str):
        try:
            res = self._get_component(project_name, component_name)
            if res.status_code == 404:
                res = self._create_component(project_name, component_name)

            return res.json()
        except Exception as e:
            logger.error(f"Failed to get component: {project_name}/{component_name}, Error: {e}")
         
    def _upload_file(self, url: str, file_path: str):
        try:
            return self.post(url, file_path = file_path)
        except Exception as e:
            logger.error(f"Failed to upload file: {file_path}, {e}")

    def upload_translation_po_files(self, project_name: str, component_name: str, language: str, dir_path: str):
        upload_response = {
            "project": project_name,
            "component": component_name,
            "language": language,
        }
        
        files: List = []
        
        for filename in os.listdir(dir_path):
            if filename.endswith(".po"):
                file_path = os.path.join(dir_path, filename)
                res = self._upload_file(f'api/translations/{project_name}/{component_name}/{language}/file/', file_path)
                
                if res.status_code > 400:
                    logger.error(f"Failed to upload translation file: {file_path}, {res.text}")
                    
                files.append(res.json())
        
        upload_response["files"] = files
        
        return upload_response


if __name__ == "__main__":
    migrator = WeblateMigrator()
    
    # example path is /example/<project_name>/<component_name>/locale/<language>/LC_MESSAGES/<component_name>.po
    # e.g. /example/glance_store/glance_store/locale/ko_KR/LC_MESSAGES/glance_store.po
    # we need to get "openstack"/project_name, "openstack"/component_name, language, and dir_path
    
    base_path = "/example"

    for project_name in os.listdir(base_path):
        project = migrator.get_or_create_project(project_name)
        
        for component_name in os.listdir(f"{base_path}/{project_name}"):
            component = migrator.get_or_create_component(project_name, component_name)
            
            for locale in os.listdir(f"{base_path}/{project_name}/{component_name}/locale"):
                language = migrator.parse_language(locale)
                dir_path = f"{base_path}/{project_name}/{component_name}/locale/{language}/LC_MESSAGES"
                migrator.upload_translation_po_files(project_name, component_name, language, dir_path)