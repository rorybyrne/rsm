"""Log class

@author Rory Byrne <rory@rory.bio>
"""
import logging
import logging.config


logging.config.fileConfig(fname='log.conf')


class Logger:

    def __init__(self):
        self.log = logging.getLogger(f'msr.{self.__class__.__name__}')
