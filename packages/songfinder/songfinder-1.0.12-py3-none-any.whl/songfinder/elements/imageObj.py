# -*- coding: utf-8 -*-

import os

from songfinder import fonctions as fonc
from songfinder import classSettings as settings
from songfinder.elements import Element


class ImageObj(Element):
    def __init__(self, chemin):
        self.etype = "image"
        self._extention = fonc.get_ext(chemin)
        if self._extention == "":
            for ext in settings.GENSETTINGS.get("Extentions", "image"):
                if os.path.isfile(chemin + ext):
                    self._extention = ext
                    chemin = chemin + ext
                    break
        Element.__init__(
            self, nom=fonc.get_file_name(chemin), etype=self.etype, chemin=chemin
        )

    @property
    def extention(self):
        return self._extention

    @property
    def text(self):
        return settings.GENSETTINGS.get("Syntax", "newslide")[0]

    def exist(self):
        return os.path.isfile(self.chemin)
