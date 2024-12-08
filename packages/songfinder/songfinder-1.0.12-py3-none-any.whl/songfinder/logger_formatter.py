# -*- coding: utf-8 -*-

import logging


class MyFormatter(logging.Formatter):
    default_fmt = "[SongFinder] %(levelname)s:%(asctime)s: `%(module)s` In `%(funcName)s` l.%(lineno)s: %(message)s"
    debug_fmt = "[SongFinder] %(levelname)s:%(asctime)s: `%(module)s` In `%(funcName)s` l.%(lineno)s: %(message)s"
    warn_fmt = "[SongFinder] %(levelname)s: `%(module)s` In `%(funcName)s` l.%(lineno)s: %(message)s"
    info_fmt = "[SongFinder] %(levelname)s: %(message)s"

    def __init__(self):
        super(MyFormatter, self).__init__(
            fmt="%(levelno)d: %(msg)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

    def format(self, record):
        # Replace the original format with one customized by logging level
        try:
            if record.levelno == logging.DEBUG:
                # pylint: disable=protected-access
                self._style._fmt = MyFormatter.debug_fmt
                self.datefmt = "%Y-%m-%d"
            elif record.levelno == logging.INFO:
                # pylint: disable=protected-access
                self._style._fmt = MyFormatter.info_fmt
            elif record.levelno == logging.WARNING:
                # pylint: disable=protected-access
                self._style._fmt = MyFormatter.warn_fmt
            else:
                # pylint: disable=protected-access
                self._style._fmt = MyFormatter.default_fmt
        except AttributeError:
            pass
        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)
        return result
