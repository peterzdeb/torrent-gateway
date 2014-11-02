__author__ = 'pzdeb'

MEDIA_TYPES = {
    'music': ['mp3'],
    'films': ['avi', 'ac3', 'mpg', 'divx', 'mkv', 'mp2', 'mp4'],
    'photos': [],
}

ALL_MEDIA_TYPES = []
for exts in MEDIA_TYPES.values():
    ALL_MEDIA_TYPES.extend(exts)

