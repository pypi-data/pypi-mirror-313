# -*- coding: utf-8 -*-

import os
import re
import json
import yaml
import fnmatch
from functools import reduce
import argparse
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from checkmate.lib.backend import SQLBackend

def get_project_path(path=None):
    if not path:
        path = os.getcwd()
    while path != "/":
        config_path = os.path.join(path, '.checkmate')
        if os.path.exists(config_path) and os.path.isdir(config_path):
            return path
        path = os.path.dirname(path)
    return None

def get_project_config(path):
    with open(os.path.join(path, ".checkmate/config.json"), "r") as config_file:
        return json.loads(config_file.read())

def save_project_config(path, config):
    with open(os.path.join(path, ".checkmate/config.json"), "w") as config_file:
        config_file.write(json.dumps(config))

def get_files_list(path, with_sha=False):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend([(os.path.join(dirpath, f))[len(path):] for f in filenames])
    return files

def apply_filter(filename, patterns):
    return reduce(lambda x, y: x or y, [bool(re.search(pattern, filename)) for pattern in patterns], False)

def filter_filenames_by_analyzers(filenames, analyzers, language_patterns):
    filtered_filenames = []
    for filename in filenames:
        for analyzer_params in analyzers:
            if analyzer_params['language'] not in language_patterns:
                continue
            language_pattern = language_patterns[analyzer_params['language']]
            if 'patterns' not in language_pattern or not apply_filter(filename, language_pattern['patterns']):
                continue
            filtered_filenames.append(filename)
            break
    return filtered_filenames

def filter_filenames_by_checkignore(file_paths, checkignore_patterns):
    filtered_file_paths = []
    for file_path in file_paths:
        excluded = False
        always_included = False
        for pattern in checkignore_patterns:
            if pattern.startswith("!") and fnmatch.fnmatch(file_path, pattern[1:]):
                always_included = True
                break
            elif fnmatch.fnmatch(file_path, pattern):
                excluded = True
        if not excluded or always_included:
            filtered_file_paths.append(file_path)
    return filtered_file_paths

def parse_checkmate_settings(content):
    """Parse .yml content and return a dictionary."""
    return yaml.safe_load(content)

def parse_checkignore(content):
    lines = [l for l in (s.strip() for s in content.split("\n")) if l and not l.startswith("#")]
    return lines

def get_project_and_backend(path, settings, echo=False, initialize_db=True):
    project_path = get_project_path(path)
    project_config = get_project_config(project_path)
    backend = get_backend(project_path, project_config, settings, echo=echo, initialize_db=initialize_db)
    project = get_project(project_path, project_config, settings, backend)
    return project, backend

def get_backend(project_path, project_config, settings, echo=False, initialize_db=True):
    """Return the appropriate backend instance based on the project configuration and settings."""
    backend_config = project_config.get('backend', {})
    backend_type = backend_config.get('driver')
    connection_string = backend_config.get('connection_string', None)

    if backend_type == "sql":
        if not connection_string:
            raise ValueError("Connection string is required for the 'sql' backend.")
        engine = create_engine(connection_string)
        backend = SQLBackend(engine)
    elif backend_type == "sqlite":
        if not connection_string:
            connection_string = f"sqlite:///{project_path}/database.db"
        engine = create_engine(connection_string, echo=echo)
        backend = SQLBackend(engine)
    else:
        raise ValueError("Unsupported backend type specified.")

    if initialize_db:
        try:
            backend.create_tables()
        except SQLAlchemyError as e:
            print(f"Error initializing database: {e}")

    return backend

def get_project(project_path, project_config, settings, backend):
    project_class = project_config.get('project_class', 'Project')
    ProjectClass = settings.models[project_class]

    # Attempt to find the project by project_id
    project = backend.filter(ProjectClass, {'pk': project_config['project_id']}).first()

    # If the project doesn't exist, create a new one
    if project is None:
        project = ProjectClass(pk=project_config['project_id'])
        backend.add(project)
        # If needed, ensure that the project is persisted
        backend.commit()  # If your backend requires an explicit commit

    return project

def main():
    parser = argparse.ArgumentParser(description="Checkmate backend configuration")
    parser.add_argument('--backend', type=str, help="Specify the backend type (e.g., sqlite, sql)", default="sqlite")
    parser.add_argument('--connection-string', type=str, help="Connection string for the backend", default=None)
    args = parser.parse_args()

    backend_type = args.backend
    connection_string = args.connection_string

    print(f"Using backend: {backend_type}")
    if connection_string:
        print(f"Using connection string: {connection_string}")

if __name__ == "__main__":
    main()

