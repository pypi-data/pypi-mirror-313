from os.path import abspath, exists, join
import sys
INSTALL_PREFIX = abspath(sys.prefix)
if not exists(join(INSTALL_PREFIX, 'lib/pkgcore')):
    INSTALL_PREFIX = abspath(sys.base_prefix)
DATA_PATH = join(INSTALL_PREFIX, 'share/pkgcheck')
