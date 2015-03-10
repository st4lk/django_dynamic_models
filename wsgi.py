#!/usr/bin/python
import os
import sys

sys.path.append(os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'dynamic_project'))
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
from config.wsgi import *
