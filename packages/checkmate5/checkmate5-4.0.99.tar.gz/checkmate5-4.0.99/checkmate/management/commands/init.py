# -*- coding: utf-8 -*-

from .base import BaseCommand
from checkmate.management.helpers import save_project_config

import sys
import os
import os.path
import json
import uuid
import logging

logger = logging.getLogger(__name__)

"""
Creates a new project. The command proceeds as follows:

-We create a .checkmate directory in the current directory.
-If a project already exists in the same directory, we do nothing.
"""

class Command(BaseCommand):

    requires_valid_project = False

    options = BaseCommand.options + [
        {
            'name': '--backend',
            'action': 'store',
            'dest': 'backend',
            'type': str,
            'default': 'sql',
            'help': 'The backend to use. Choices are "sql" (default) or "sqlite".'
        },
        {
            'name': '--backend-opts',
            'action': 'store',
            'dest': 'backend_opts',
            'type': str,
            'default': '',
            'help': 'Backend options (e.g. connection string for SQL databases or file path for SQLite).'
        },
        {
            'name': '--path',
            'action': 'store',
            'dest': 'path',
            'default': None,
            'type': str,
            'help': 'The path where to create a new project (default: current working directory)'
        },
        {
            'name': '--pk',
            'action': 'store',
            'dest': 'pk',
            'type': str,
            'default': None,
            'help': 'The primary key to use for the project',
        }
    ]

    description = """
    Initializes a new checkmate project.
    """

    def run(self):
        logger.info("Initializing new project in the current directory.")

        project_path = self.opts['path'] or os.getcwd()
        config_path = os.path.join(project_path, ".checkmate")

        if os.path.exists(config_path):
            logger.error("Found another project with the same path, aborting.")
            return -1

        # Validate backend option
        if self.opts['backend'] not in ('sql', 'sqlite'):
            logger.error("Unsupported backend: %s. Supported options are 'sql' and 'sqlite'." % self.opts['backend'])
            return -1

        # Backend configuration
        if self.opts['backend'] == 'sql':
            backend_opts = self.opts['backend_opts'] or 'postgresql://user:password@localhost/mydatabase'
        elif self.opts['backend'] == 'sqlite':
            # Default to an in-memory SQLite database if no path is provided
            backend_opts = self.opts['backend_opts'] or 'sqlite:///:memory:'

        # Configuration dictionary for the project
        config = {
            'project_id': uuid.uuid4().hex if not self.opts['pk'] else self.opts['pk'],
            'project_class': 'Project',
            'backend': {
                'driver': self.opts['backend'],
                'connection_string': backend_opts
            }
        }

        # Create the project directory and save the configuration
        os.makedirs(config_path)
        save_project_config(project_path, config)

        logger.info(f"Project initialized with {self.opts['backend']} backend at {project_path}")
        return 0

