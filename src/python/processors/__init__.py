__author__ = 'pzdeb'

from core.config import lazy_config
import logging
import os
import shutil


class BaseProcessor(object):

    def __init__(self, dir):
        self.log = logging.getLogger(self.__class__.__name__)
        self.conf = lazy_config()

    def process(self, path):
        raise NotImplementedError

    def link_files(self, src, dst):
        try:
            self.log.debug('Linking file %s -> %s' % (src, dst))
            os.link(src, dst)
        except Exception as err:
            self.log.error('Cannot transfer torrent files: %s' % err)

    def copy_files(self, src, dst):
        try:
            self.log.debug('Copying file %s -> %s' % (src, dst))
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copyfile(src, dst)
            self.log.info('Torrent "%s" transferred successfully' % dst)
        except AttributeError as err:
            self.log.error('Torrent files ("%s) transferred with errors: %s' % (dst, err))
        except Exception as err:
            self.log.error('Cannot transfer torrent files: %s' % err)
