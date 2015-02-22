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
        base_src = os.path.split(src)[0]
        base_dst = os.path.split(dst)[0]
        def __process_subdir(sub_path):
            for cdir, dirs, names, in os.walk(os.path.join(src, sub_path)):
                curr_dir = cdir.replace(base_src, '').replace('/', '')
                for subdir in dirs:
                    dest_subdir = os.path.join(dst, sub_path, subdir)
                    if not os.path.exists(dest_subdir):
                        self.log.debug('Creating subdir for linking files: %s', dest_subdir)
                        os.mkdir(dest_subdir)

                    __process_subdir(os.path.join(sub_path, subdir))

                for name in names:
                    os.link(os.path.join(base_src, curr_dir, name),
                            os.path.join(base_dst, curr_dir, name))


        try:
            self.log.info('Trying to link path %s -> %s' % (src, dst))
            if os.path.isdir(src):
                if not os.path.exists(dst):
                    self.log.debug('Creating directory for linking files: %s', dst)
                    os.mkdir(dst)
                self.log.debug('Walking through files to link from dir: %s', src)
                __process_subdir('')
            else:
                self.log.info('Linking file %s -> %s' % (src, dst))
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
