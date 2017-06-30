
"""
    Globally accessible config object. All variables that are specific
    to a project should be in here.

    Config is a singleton class. To access its variables, for example
    to access p0, do::
        import swap.config as config
        config.p0
"""

import os
import sys
import importlib.util


class Object:
    """
    Accepts a dict as an argument. Sets an instance variable
    for each key value mapping in the dict
    """

    def __init__(self, obj):
        if type(obj) is dict:
            for key, value in obj.items():
                if type(value) is dict:
                    value = Object(value)
                setattr(self, key, value)


# Prior probabilities
p0 = 0.12
epsilon = 0.5

# Retirement Thresholds
mdr = 0.1
fpr = 0.01

# Methodology
# Set this flag to true to use the back-updating transactional methodology
# Setting this flag to false uses the traditional SWAP methodology
back_update = False

# Operator used in controversial and consensus score calculation
controversial_version = 'pow'


# Database config options
class database:
    name = 'swapDB'
    host = 'localhost'
    port = 27017
    max_batch_size = 1e5

    class builder:
        _core_types = {
            'classification_id': int,
            'user_id': int,
            'annotation': int,
            'gold_label': int,
            'subject_id': int,
            'seen_before': bool,
            'time_stamp': 'timestamp',
        }

        types = {
            'object_id': int,
            'machine_score': float,
            'mag': float,
            'mag_err': float
        }

        metadata = ['mag', 'mag_err', 'machine_score', 'diff', 'object_id'] + \
            ['random%d' % (i + 1) for i in range(15)]

        core = [
            'classification_id', 'user_id', 'annotation', 'gold_label',
            'subject_id', 'seen_before', 'time_stamp', 'session_id']


class online_swap:
    # Flask app config
    port = '5000'
    bind = '0.0.0.0'
    debug = False

    class caesar:
        # Address configuration for accessing caesar
        host = 'localhost'
        port = '3000'
        # Authorization token for panoptes
        OAUTH = None
        # Response data for reductions
        workflow = '1737'
        reducer = 'swap'
        field = 'swap_score'

    # Caesar URL format
    _addr_format = 'http://%(host)s:%(port)s/workflows/%(workflow)s' + \
                   '/reducers/%(reducer)s/reductions'


class logging:
    file_format = '%(asctime)s:%(levelname)s::%(name)s:%(funcName)s ' + \
                  '%(message)s'
    console_format = '%(asctime)s %(levelname)s %(message)s'
    date_format = '%Y%m%d_%H:%M:%S'
    level = 'DEBUG'
    console_level = 'INFO'
    keep_logs = 5
    filename = 'swap-%d.log'


def local_config():
    # Import local_config.py to seamlessly override
    # config defaults without having to check in to git repo
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'config.py')
    if os.path.isfile(path):
        # pylint: disable=E0401,W0401
        import_config(path)


def module():
    return sys.modules[__name__]


def import_config(path):
    """
    Import a custom fon
    """
    spec = importlib.util.spec_from_file_location('module', path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    foo.override(module())


local_config()
