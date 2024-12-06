# -*- coding: utf-8; -*-
"""
Tasks for WuttJamaican
"""

import os
import re
import shutil

from invoke import task


here = os.path.abspath(os.path.dirname(__file__))
__version__ = None
pattern = re.compile(r'^version = "(\d+\.\d+\.\d+)"$')
with open(os.path.join(here, 'pyproject.toml'), 'rt') as f:
    for line in f:
        line = line.rstrip('\n')
        match = pattern.match(line)
        if match:
            __version__ = match.group(1)
            break
if not __version__:
    raise RuntimeError("could not parse version!")


@task
def release(c, skip_tests=False):
    """
    Release a new version of WuttJamaican
    """
    if not skip_tests:
        c.run('pytest')

    # rebuild local tar.gz file for distribution
    if os.path.exists('WuttJamaican.egg-info'):
        shutil.rmtree('WuttJamaican.egg-info')
    c.run('python -m build --sdist')

    # upload to PyPI
    filename = f'wuttjamaican-{__version__}.tar.gz'
    c.run(f'twine upload dist/{filename}')
