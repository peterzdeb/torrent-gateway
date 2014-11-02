__author__ = 'pzdeb'

from core.consts import *
import logging
import os
from processors.music import MP3Processor
from processors.films import FilmsProcessor

class FileAnalyzer():
    def __init__(self, dir=None):
        self.log = logging.getLogger('analyzer')
        self.dir = dir
        self.processors = {}

    def detect_pathtype(self, path):
        medias = {}
        for curr_dir, dirs, names,  in os.walk(path):
            for name in names:
                file_parts = name.rsplit('.', 2)
                if len(file_parts) > 1:
                    medias.setdefault(file_parts[-1], []).append(name)
        media_rate = sorted([(len(names), ext) for ext, names in medias.items() if ext in ALL_MEDIA_TYPES])
        if not media_rate:
            return ''
        else:
            return media_rate[-1][1]

    def parse_attributes(self, filename):
        file_path = os.path.join(self.dir, filename)
        media_type = ''
        if os.path.isdir(file_path):
            media_type = self.detect_pathtype(file_path)
        else:
            parts = filename.rsplit('.', 2)
            if len(parts) > 1:
                media_type = parts[-1]
        return media_type


    def process_file(self, filename):

        media_type = self.parse_attributes(filename)
        if media_type in MEDIA_TYPES['music']:
            self.processors.setdefault('mp3',
                                       MP3Processor(self.dir)).process(self.dir, filename)
        elif media_type in MEDIA_TYPES['films']:
            self.processors.setdefault('avi',
                                       FilmsProcessor(self.dir)).process(self.dir, filename)
        else:
            self.log.error('Unknown media type for torrent "%s"' % filename)
