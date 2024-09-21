import os
import logging
import re
import time

from wlc import Weblate, Project, Component, WeblateException

from typing import List
from requests import Response
from pathlib import Path

from http_client import HttpClient
from metadata import File
from docs_explorer import find_all_project_name_from_dirs, find_all_doc_files, po_to_pot

OPENDEV_OPENSTACK_WEB = "https://opendev.org/openstack/"
logger = logging.getLogger(__name__)


class WeblateMigrator(HttpClient):
    """https://docs.weblate.org/en/latest/user/files.html#uploading-translation-files"""
    
    def __init__(self, url: str, key: str):
        super().__init__(base_url=url, key=key)
        self.weblate = Weblate(key=key, url=url)
        
    def make_slug(self, name: str) -> str:
        return name.lower().replace("/", "_")
    
    def parse_language(self, language: str) -> str:
        """parse language from locale

        e.g. ko_KR -> ko
        """
        match = re.match(r'^([a-z]+)_', language)
        if match:
            return match.group(1)
        else:
            return language
    
    def validate_project(self, project_name: str) -> bool:
        pattern = r'^[^a-zA-Z]|(__|\.)'
        
        return re.search(pattern, project_name)
        
    def get_or_create_project(self, project_name: str):
        try:            
            slug = self.make_slug(project_name)
            self.weblate.create_project(project_name, slug, OPENDEV_OPENSTACK_WEB + project_name)
        except WeblateException as wlce:
            logger.error(f"WeblateException: {project_name}, Error: {wlce}")
        except Exception as e:
            logger.error(f"Failed to get or create project: {project_name}, Error: {e}")
        finally:
            time.sleep(1)
            return self.weblate.get_project(slug)


    def get_or_create_component(self, project_slug: str, component_name: str, component_slug: str,  docfile_path: str):
        try:
            with open(docfile_path, 'rb') as docfile:
                self.weblate.create_component(
                    project_slug, docfile=docfile, name=component_name, slug=component_slug, file_format="po", filemask="*.po", repo="local:")
        except WeblateException as wlce:
            logger.error(f"WeblateException: {project_slug}/{component_name}, Error: {wlce}")
        except Exception as e:
            logger.error(f"Failed to get or create component: {project_slug}/{component_name}, Error: {e}")
        finally:
            return self.weblate.get_component(f"{project_slug}/{component_slug}")
         
    def _upload_file(self, url: str, file_path: str):
        try:
            return self.post(url, file_path = file_path)
        except Exception as e:
            logger.error(f"Failed to upload file: {file_path}, {e}")

    def upload_translation_po_files(self, project_slug: str, component_slug: str, language: str, dir_path: str):
        files: List = []

        candidate_count = 0        
        for filename in os.listdir(dir_path):
            if filename.endswith(".po"):
                candidate_count += 1
                file_path = os.path.join(dir_path, filename)
                res = self._upload_file(f'api/translations/{project_slug}/{component_slug}/{language}/file/', file_path)
                
                if res.status_code >= 400:
                    logger.error(f"Failed to upload translation file: {file_path}, {res.text}")
                    continue
                    
                files.append(res)
                logger.info(f"Uploaded: {project_slug}/{component_slug}/{language}")     
        
        logger.info(f"Total Uploaded: {len(files)/candidate_count}")

    
    def upload_all_translation_po_files(self, projects: List[str], project_path: str="./"):
        for project in projects:
            docs = find_all_doc_files(project, project_path)
            
            if len(docs) == 0:
                continue
            
            if self.validate_project(project):
                continue
            
            project_name = f"openstack/{project}"
            project_slug = self.make_slug(project_name)
            _project = migrator.get_or_create_project(project_name)
            logger.debug(f"Project Response: {_project}")

            for document in docs:  
                if document is None:
                    continue

                language = migrator.parse_language(document.locale)
                component_slug = self.make_slug(document.component)
                try:  
                    _component = migrator.get_or_create_component(project_slug, document.component, component_slug, document.template_path)
                    logger.debug(f"Component Response: {_component}")
                    migrator.upload_translation_po_files(project_slug, component_slug, language, document.path)
                except Exception as e:
                    logger.error(f"Failed to upload translation file: {document.path}, {e}")
                

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('pairs', nargs='*')
    args = parser.parse_args()
    arg_dict = {}
    for pair in args.pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            arg_dict[key] = value

    if 'debug' in arg_dict and arg_dict['debug'] == 'true':
        logger.level = logging.DEBUG

    migrator = WeblateMigrator(
        url=f"WEBLATE_OPENSTACK_API_URL",
        key="your_weblate_api_key"
    )

    projects = find_all_project_name_from_dirs()
    migrator.upload_all_translation_po_files(projects)