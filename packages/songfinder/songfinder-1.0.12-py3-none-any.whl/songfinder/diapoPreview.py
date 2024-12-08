# -*- coding: utf-8 -*-

import tkinter as tk


import time

from songfinder.gui import screen
from songfinder.gui import themes
from songfinder import classSettings as settings


class Preview(object):
    def __init__(self, frame, diapoList, screens=None):
        self._frame = frame
        self._diapoList = diapoList

        self._previewSize = int(pow(screens[0].width, 1.0 / 3) * 32)

        self._previews = []

        self._frame.bind("<Button-1>", self._nextSlide)
        self._frame.bind("<Button-3>", self._previousSlide)
        self._frame.bind("<Configure>", self.updatePreviews)
        self._delayId = None
        self._passed = 0
        self._delayAmount = 0
        self._callbackDelay = 0
        self._lastCallback = 0

        self.printer()

    def _previousSlide(self, event):  # pylint: disable=unused-argument
        self._diapoList.decremente()

    def _nextSlide(self, event):  # pylint: disable=unused-argument
        self._diapoList.incremente()

    def updatePreviews(self, event=None, delay=True):  # pylint: disable=unused-argument
        ratio = screen.getRatio(settings.GENSETTINGS.get("Parameters", "ratio"))
        previewCount = max(
            int(self._frame.winfo_height() // (self._previewSize / ratio)), 1
        )
        if len(self._previews) > previewCount:
            for theme in self._previews[previewCount:]:
                theme.pack_forget()
            del self._previews[previewCount:]
        elif len(self._previews) < previewCount:
            for _ in range(previewCount - len(self._previews)):
                theme = themes.Theme(
                    self._frame,
                    width=self._previewSize,
                    height=self._previewSize / ratio,
                )
                self._previews.append(theme)
                theme.pack(side=tk.TOP)
        self.printer(delay)

    def printer(self, delay=True):
        if delay:
            self._callbackDelay = int(round((time.time() - self._lastCallback) * 1000))
            self._lastCallback = time.time()
            if self._delayId:
                self._frame.after_cancel(self._delayId)
            self._delayId = self._frame.after(self._delayAmount, self._printer)
        else:
            self._printer()

    def _printer(self):
        startTime = time.time()
        self._passed += 1
        ratio = screen.getRatio(settings.GENSETTINGS.get("Parameters", "ratio"))
        for i, theme in enumerate(self._previews):
            diapo = self._diapoList[i]
            if theme.name != diapo.themeName:
                theme.destroy()
                theme = themes.Theme(
                    self._frame,
                    width=self._previewSize,
                    height=self._previewSize / ratio,
                )
                self._previews[i] = theme
                theme.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            diapo.printDiapo(theme)
        self._prefetcher()

        # Compute printer delay to lower pression on slow computers
        printerTime = int(round((time.time() - startTime) * 1000))
        if printerTime > self._callbackDelay:
            self._delayAmount = printerTime
        else:
            self._delayAmount = 0

    def _prefetcher(self):
        self._diapoList[-1].prefetch(self._previews)
        self._diapoList[1].prefetch(self._previews)
