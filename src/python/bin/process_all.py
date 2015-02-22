import logging
import os
import sys

PROD_ROOT = os.environ.get('PROD_ROOT', os.getcwd())
sys.path.append(os.path.join(PROD_ROOT, 'src', 'python'))

from core.utils import remove_xdc
from processors.file_analyzer import FileAnalyzer


if __name__ == '__main__':
    logging.basicConfig(filename='/var/log/torrent_gw.log',
                        format='%(asctime)-15s %(name)s %(levelname)s %(message)s',
                        level=logging.DEBUG)
    logger = logging.getLogger('gateway')
    logger.setLevel(logging.DEBUG)

    env = os.environ
    torrent_file = ''
    try:
        if len(sys.argv) >= 1:
            logger.debug('parsing args: %s', str(sys.argv))
            torrents_dir = sys.argv[1:]
        else:
            torrents_dir = ''

        if not torrent_file:
            logger.error('Torrent error - no torrents dir specified')
            sys.exit(1)

        for torrent_file in os.listdir(torrents_dir)
            logger.info('Start processing file: %s' % torrent_file)
            analyzer = FileAnalyzer(env.get('TR_TORRENT_DIR', '/media/Disk-D/Torrents'))
            analyzer.process_file(torrent_file)
    except Exception as err:
        try:
            logger.exception('Error occurred when downloading file "%s": %s' % (torrent_file, err))
        except Exception as err:
            logger.exception('Critical internal server error: %s' % err)
        sys.exit(1)
    sys.exit(0)
