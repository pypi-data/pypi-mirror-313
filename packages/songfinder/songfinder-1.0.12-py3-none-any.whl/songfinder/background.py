# -*- coding: utf-8 -*-
import os
import errno
import shutil
import logging
import traceback

try:
    import psutil
except ImportError:
    logging.warning("psutil is not available.")
from PIL import Image, ImageTk

import songfinder
from songfinder import cache
from songfinder.gui import screen
from songfinder import fonctions as fonc
from songfinder import classSettings as settings


class Background(object):
    def __init__(self, path, width, height, keepRatio):
        self.width = width
        self.height = height
        self._path = path
        self._keepRatio = keepRatio

    @property
    def keepRatio(self):
        return self._keepRatio

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = int(value)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = int(value)

    @property
    def path(self):
        return self._path

    def __str__(self):
        fileName = fonc.get_file_name(self._path)
        return f"{fileName}_{self.width}_{self.height}"

    def __repr__(self):
        return repr(str(self))


class Backgrounds(object):
    def __init__(self):
        self._imageFile = None
        self._cachePath = os.path.join(songfinder.__settingsPath__, "cache")
        try:
            os.makedirs(self._cachePath)
        except (OSError, IOError) as error:
            if error.errno == errno.EEXIST:
                pass
            else:
                raise
        self._cache = cache.Cache(0, self._getImageFile)
        self._screens = screen.Screens()
        if settings.GENSETTINGS.get("Parameters", "highmemusage"):
            self.resizeCache("high")
        else:
            self.resizeCache("low")

    def _getImageFile(self, back):
        try:
            path = os.path.join(self._cachePath, f"{str(back)}.png")
            self._imageFile = Image.open(path)
        except (OSError, IOError):
            try:
                self._imageFile = Image.open(back.path)
            except (OSError, IOError):
                logging.debug(traceback.format_exc())
                return None
            self._resize(back)
            self._imageFile.save(path)
        return ImageTk.PhotoImage(self._imageFile)

    def _resize(self, back):
        if back.keepRatio == "keep":
            im_w, im_h = self._imageFile.size
            aspect_ratio = im_w / im_h
            back.width = min(back.width, int(back.height * aspect_ratio))
            back.height = int(back.width / aspect_ratio)
        self._imageFile = self._imageFile.resize(
            (back.width, back.height), Image.Resampling.LANCZOS
        )

    def get(self, back):
        return self._cache.get(str(back), [back])

    def resizeCache(self, mode="low"):
        self._screens.update(verbose=False)
        maxWidths = max([_screen.width for _screen in self._screens])
        maxHeight = max([_screen.height for _screen in self._screens])
        sizeRatio = maxWidths * maxHeight / (1920 * 1080)
        try:
            if mode == "high":
                cacheSlots = 20 + int(psutil.virtual_memory()[1] * 6e-8 / sizeRatio)
            elif mode == "low":
                cacheSlots = 10 + int(psutil.virtual_memory()[1] * 2e-8 / sizeRatio)
            else:
                cacheSlots = self._cache.maxSize
                logging.warning(
                    f'Cache size mode "{mode}" for backgrounds not recognize'
                )
        except NameError:
            logging.debug(traceback.format_exc())
            cacheSlots = 40
        logging.info(f"Using {cacheSlots} cache slots for backgrounds")
        self._cache.maxSize = cacheSlots


def cleanDiskCacheImage():
    path = os.path.join(songfinder.__settingsPath__, "cache")
    if os.path.isdir(path):
        size = directorySize(path)
        if size > 10**8:
            logging.info(f"Cleaning image cache: {prettySize(size)}")
            shutil.rmtree(path, ignore_errors=True, onerror=None)


def directorySize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += directorySize(itempath)
    return total_size


def prettySize(size):
    base = 1024
    echelles = [" o", " Ko", " Mo", " Go", " To", "Po"]
    str_size = str(0)
    for i, echelle in enumerate(echelles):
        if size >= base ** (i):
            str_size = str(round(size / base ** (i), 2)) + echelle
    return str_size


def checkBackgrounds():
    etypes = settings.GENSETTINGS.get("Syntax", "element_type")
    notOk = []
    for etype in etypes:
        fileToCheck = settings.PRESSETTINGS.get(etype, "Background")
        if not os.path.isfile(fileToCheck):
            notOk.append(etype)
    return notOk


BACKGROUNDS = Backgrounds()
