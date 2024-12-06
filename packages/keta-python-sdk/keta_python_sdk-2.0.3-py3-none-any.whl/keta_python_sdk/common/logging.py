"""
Copyright 2024 KetaOps (xishuhq.com)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import sys
import logging
from os.path import dirname, basename
from logging.handlers import RotatingFileHandler


def config_logging(level=None, filename=None, max_bytes=1024 * 1024 * 20, backup_count=5):
    app_name = basename(dirname(dirname(sys.argv[0])))

    if filename is None:
        log_dir = os.environ.get('KETA_PATH_LOGS')

        if log_dir is None or len(log_dir) == 0:
            log_dir = dirname(dirname(sys.argv[0])) + '/logs'

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        filename = log_dir + '/app-' + app_name.replace(' ', '_') + '.log'

        if not os.path.exists(filename):
            open(filename, 'w').close()

    if level is None:
        level = 'INFO'

    handler = RotatingFileHandler(filename, maxBytes=max_bytes, backupCount=backup_count)

    logging.basicConfig(level=level,
                        handlers=[handler],
                        format="[%(asctime)s,%(msecs)03d][%(levelname)-5s][%(filename)-25s] [" + app_name + "] %(message)s",
                        datefmt='%Y-%m-%dT%H:%M:%S')
