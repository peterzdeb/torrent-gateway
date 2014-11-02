__author__ = 'pzdeb'

import os
from processors.__init__ import BaseProcessor


class FilmsProcessor(BaseProcessor):
    def process(self, path, filename):
        src_path = os.path.join(path, filename)
        dest_path = os.path.join(self.conf.get('targets', 'films'), filename)
        self.link_files(src_path, dest_path)