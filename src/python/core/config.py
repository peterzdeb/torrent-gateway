__author__ = 'pzdeb'

from configparser import ConfigParser
import os

CONF_PATH = os.path.join(os.environ.get('PROD_ROOT', os.getcwd()),
                         'etc',
                         'gateway.conf')


__conf = None

def lazy_config():
    global __conf
    if not __conf:
        __conf = ConfigParser()
        __conf.read([CONF_PATH])
    return __conf

