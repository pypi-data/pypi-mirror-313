from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import platform

if platform.system() != 'Windows':
    from .MqProducer import MqProducer

from .Logger import Logger