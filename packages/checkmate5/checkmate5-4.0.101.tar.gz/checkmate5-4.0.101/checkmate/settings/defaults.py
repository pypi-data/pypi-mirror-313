from checkmate.lib.stats.helpers import directory_splitter
from checkmate.lib.models import (Project,
                                  Snapshot,
                                  FileRevision,
                                  Issue)
from checkmate.contrib.plugins.git.models import GitSnapshot
from collections import defaultdict


"""
Default settings values
"""

hooks = defaultdict(list)

plugins = {
    'git': 'checkmate.contrib.plugins.git',
    #'trufflehog3':  'checkmate.contrib.plugins.all.trufflehog3',
    #'trojansource': 'checkmate.contrib.plugins.all.trojansource',
    #'yara': 'checkmate.contrib.plugins.all.yara',
    #'metrics': 'checkmate.contrib.plugins.all.metrics',
    'bandit': 'checkmate.contrib.plugins.python.bandit',
    'brakeman': 'checkmate.contrib.plugins.ruby.brakeman',
    #'phpanalyzer':  'checkmate.contrib.plugins.php.progpilot',
    #'pmd': 'checkmate.contrib.plugins.java.pmd',
    #'apex': 'checkmate.contrib.plugins.apex.pmdapex',
    #'semgrep': 'checkmate.contrib.plugins.java.semgrep',
    #'checkov': 'checkmate.contrib.plugins.iac.checkov',
    'tfsec': 'checkmate.contrib.plugins.iac.tfsec',
    'kubescape': 'checkmate.contrib.plugins.iac.kubescape',
    #'insidersecswift': 'checkmate.contrib.plugins.swift.insidersecswift',
    #'insiderseckotlin': 'checkmate.contrib.plugins.kotlin.insiderseckotlin',
    #'insiderseccsharp': 'checkmate.contrib.plugins.csharp.insiderseccsharp',
    #'pmdapex': 'checkmate.contrib.plugins.apex.pmdapex',
    'semgrepjava': 'checkmate.contrib.plugins.java.semgrepjava',
    'semgrepeslint': 'checkmate.contrib.plugins.javascript.semgrepeslint',
    'graudit': 'checkmate.contrib.plugins.perl.graudit',
    'text4shell': 'checkmate.contrib.plugins.cve.text4shell',
    #'fluidattackscsharp': 'checkmate.contrib.plugins.csharp.fluidattacksscanner',
    #'fluidattacksgolang': 'checkmate.contrib.plugins.golang.fluidattacksscanner',
    #'fluidattacksjava': 'checkmate.contrib.plugins.java.fluidattacksscanner',
    #'fluidattacksjavascript': 'checkmate.contrib.plugins.javascript.fluidattacksscanner',
    #'fluidattacksswift': 'checkmate.contrib.plugins.swift.fluidattacksscanner',
    #'fluidattackskotlin': 'checkmate.contrib.plugins.kotlin.fluidattacksscanner',
    #'fluidattackspython': 'checkmate.contrib.plugins.python.fluidattacksscanner',
    #'fluidattacksscannercsharp': 'checkmate.contrib.plugins.csharp.fluidattacksscanner',
    #'fluidattacksscannergolang': 'checkmate.contrib.plugins.golang.fluidattacksscanner',
    #'fluidattacksscannerjava': 'checkmate.contrib.plugins.java.fluidattacksscanner',
    #'fluidattacksscannerjavascript': 'checkmate.contrib.plugins.javascript.fluidattacksscanner',
    #'fluidattacksscannerswift': 'checkmate.contrib.plugins.swift.fluidattacksscanner',
    #'fluidattacksscannerkotlin': 'checkmate.contrib.plugins.kotlin.fluidattacksscanner',
    #'fluidattacksscannerpython': 'checkmate.contrib.plugins.python.fluidattacksscanner',
    'gostaticcheck': 'checkmate.contrib.plugins.golang.gostaticcheck',
    'gptanalyzer': 'checkmate.contrib.plugins.all.gptanalyzer',
    #'privategptanalyzer': 'checkmate.contrib.plugins.all.privategpt',
}

language_patterns = {
    'perl': {
        'name': 'Perl',
        'patterns': [u'\.pl$'],
    },
    'python': {
        'name': 'Python',
        'patterns': [u'\.py$'],
    },
    'javascript': {
        'name': 'Javascript',
        'patterns': [u'\.js$', u'\.ts$'],
    },
    'java': {
        'name': 'Java',
        'patterns': [u'\.java$'],
    },
    'ruby': {
        'name': 'Ruby',
        'patterns': [u'\.rb$'],
    },
    'golang': {
        'name': 'Golang',
        'patterns': [u'\.go$'],
    },
    'iac': {
        'name': 'IaC',
        'patterns': [u'\.yml$', u'\.yaml$', u'Dockerfile$', u'\.tf$'],
    },
    'all': {
        'name': 'All',
        'patterns': [u'.*\.*$'],
    },
}

analyzers = {}

commands = {
    'alembic': 'checkmate.management.commands.alembic.Command',
    'init': 'checkmate.management.commands.init.Command',
    'analyze': 'checkmate.management.commands.analyze.Command',
    'reset': 'checkmate.management.commands.reset.Command',
    'shell': 'checkmate.management.commands.shell.Command',
    'summary': 'checkmate.management.commands.summary.Command',
    'snapshots': 'checkmate.management.commands.snapshots.Command',
    'issues': 'checkmate.management.commands.issues.Command',
    'props': {
        'get': 'checkmate.management.commands.props.get.Command',
        'set': 'checkmate.management.commands.props.set.Command',
        'delete': 'checkmate.management.commands.props.delete.Command',
    }
}

models = {
    'Project': Project,
    'Snapshot': Snapshot,
    'GitSnapshot': GitSnapshot,
    'FileRevision': FileRevision,
    'Issue': Issue,
}

aggregators = {
    'directory': {
        'mapper': lambda file_revision: directory_splitter(file_revision['path'], include_filename=True)
    }
}

checkignore = """*/site-packages/*
*/dist-packages/*
*/build/*
*/eggs/*
*/migrations/*
*/alembic/versions/*
*/node_modules/*
*/.checkmate/*
"""
