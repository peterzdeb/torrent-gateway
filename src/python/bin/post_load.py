
__author__ = 'pzdeb'

import logging
import os
import sys

PROD_ROOT = os.environ.get('PROD_ROOT', os.getcwd())
sys.path.append(os.path.join(PROD_ROOT, 'src', 'python'))

from core.utils import remove_xdc
from processors.file_analyzer import FileAnalyzer

# 'TR_TORRENT_NAME': '1996 - \udcd0\udca4\udcd0\udcb0\udcd0\udcbd\udcd1\udc82\udcd0\udcbe\udcd0\udcbc-2 - \udcd0\udc97\udcd0\udcbe\udcd1\udc80\udcd1\udc8f\udcd0\udcbd\udcd1\udc96 \udcd0\udcb2\udcd1\udc96\udcd0\udcb9\udcd0\udcbd\udcd0\udcb8',
# 'TR_TORRENT_HASH': '21b63e3641ea2045ae2257dcca0ab469c4a4d09a',
# 'TR_TORRENT_DIR': '/media/Disk-D/Torrents',
# 'UPSTART_JOB': 'transmission-daemon',
# 'TR_TIME_LOCALTIME': 'Sat Oct 25 09:19:08 2014',
# 'TR_APP_VERSION': '2.82',
# 'TR_TORRENT_ID': '5'


if __name__ == '__main__':
    logging.basicConfig(filename='/var/log/torrent_gw.log',
                        format='%(asctime)-15s %(name)s %(levelname)s %(message)s')
    logger = logging.getLogger('gateway')
    logger.setLevel(logging.DEBUG)

    env = os.environ
    torrent_file = ''
    try:
        if 'TR_TORRENT_NAME' in env:
            torrent_file = env.get('TR_TORRENT_NAME', torrent_file)
            torrent_file = remove_xdc(torrent_file)
        if len(sys.argv) >= 4:
            logger.debug('parsing args: %s', str(sys.argv))
            torrent_id = sys.argv[1]
            torrent_name = ' '.join(sys.argv[2:-1])
            torrent_dir = sys.argv[-1]
            torrent_file = os.path.join(torrent_dir, torrent_name)
        else:
            #torrent_file = '1996 - \udcd0\udca4\udcd0\udcb0\udcd0\udcbd\udcd1\udc82\udcd0\udcbe\udcd0\udcbc-2 - \udcd0\udc97\udcd0\udcbe\udcd1\udc80\udcd1\udc8f\udcd0\udcbd\udcd1\udc96 \udcd0\udcb2\udcd1\udc96\udcd0\udcb9\udcd0\udcbd\udcd0\udcb8'
            #torrent_file = 'Aut\xf3mata (2014) BDRip 1080p [UKR_ENG] [Hurtom].mkv'
            torrent_file = remove_xdc(torrent_file)

        if not torrent_file:
            logger.error('Torrent error - empty torrent file received')
            sys.exit(1)

        logger.info('Start processing file: %s' % torrent_file)
        analyzer = FileAnalyzer(env.get('TR_TORRENT_DIR', '/media/Disk-D/Torrents'))
        analyzer.process_file(torrent_file)
    except Exception as err:
        try:
            logger.exception('Error occurred when downloading file "%s": %s' % (torrent_file, err))
        except Exception as err:
            logger.exception('Critical internal server error: %s' % err)
