# -*- coding: utf-8 -*-
import os
import re

from songfinder import gestchant
from songfinder import fonctions as fonc
from songfinder import classDiapo
from songfinder.gui import screen
from songfinder import classSettings as settings


class Element(object):
    def __init__(self, nom="", etype="empty", chemin=""):
        self.newline = settings.GENSETTINGS.get("Syntax", "newline")
        self.nom = fonc.enleve_accents(nom)
        self._title = self.nom
        self._supInfo = ""
        if nom:
            self.nom = fonc.upper_first(self.nom)

        self._diapos = []
        self._chemin = None
        self._text = None
        self._author = None
        self._copyright = None
        self._customNumber = None
        self._turfNumber = None
        self._hymnNumber = None
        self._tags = []
        self.etype = etype
        self.chemin = chemin

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.chemin}')"

    def __str__(self):
        out = f"{self.etype} -- "
        out = f"{out}{self.title}"
        return out

    @property
    def text(self):
        return self._text

    @property
    def title(self):
        if self._title == "":
            self.text  # pylint: disable=pointless-statement
        return self._title

    @property
    def supInfo(self):
        return self._supInfo

    @supInfo.setter
    def supInfo(self, info_in):
        if info_in is not None:
            self._supInfo = info_in

    @property
    def transpose(self):
        return None

    @property
    def capo(self):
        return None

    @property
    def key(self):
        return ""

    @property
    def nums(self):
        return dict()

    @property
    def turfNumber(self):
        return None

    @property
    def hymnNumber(self):
        return None

    @property
    def customNumber(self):
        return None

    @property
    def author(self):
        return ""

    @property
    def copyright(self):
        return ""

    @property
    def ccli(self):
        return ""

    @property
    def tags(self):
        return ",".join(self._tags)

    @tags.setter
    def tags(self, tags):
        if isinstance(tags, list):
            self._tags = [gestchant.nettoyage(tag) for tag in tags]
        else:
            tags = (
                tags.replace(" et ", ",")
                .replace(" / ", ",")
                .replace(" - ", ",")
                .replace(";", ",")
            )

            def cleaupTag(tag):
                tag = fonc.upper_first(gestchant.nettoyage(tag))
                tag = tag.replace("st-", "saint").replace("St-", "Saint")
                return tag

            self._tags = [cleaupTag(tag) for tag in tags.split(",")]
            self._tags.sort()

    @property
    def diapos(self):
        if self._diapos != []:
            return self._diapos
        # ~ self._diapos = []

        text = f"{self.text}\n"
        text = fonc.supressB(text, "\\ac", "\n")
        text = text.strip("\n")
        ratio = screen.getRatio(settings.GENSETTINGS.get("Parameters", "ratio"))
        max_car = int(
            settings.PRESSETTINGS.get("Presentation_Parameters", "size_line") * ratio
        )

        listStype = []
        # La première est vide ie au dessus du premier \s
        linePerSlide = settings.PRESSETTINGS.get(
            "Presentation_Parameters", "line_per_diapo"
        )
        listText, listStype = fonc.splitPerso(
            [text], settings.GENSETTINGS.get("Syntax", "newslide"), listStype, 0
        )
        del listText[0]
        listStypePlus = gestchant.getListStypePlus(listStype)
        # Completion des diapo vide
        diapoVide = [
            i
            for i, text in enumerate(listText)
            if text.find("\\...") != -1 or gestchant.nettoyage(text) == ""
        ]

        plus = 0
        for index in diapoVide:
            listCandidat = gestchant.getIndexes(listStype[:index], listStype[index])
            if listCandidat != []:
                # Si plus de diapos que disponibles sont demande,
                # cela veut dire qu'il faut dupliquer plusieurs fois les diapos
                if not gestchant.getPlusNum(listStypePlus, index) > len(listCandidat):
                    plus = 0
                elif plus == 0:
                    plus = gestchant.getPlusNum(listStypePlus, index) - len(
                        listCandidat
                    )
                toTake = -gestchant.getPlusNum(listStypePlus, index) + plus
                indexCopie = listCandidat[toTake]
                if listText[index].find("\\...") != -1:
                    listText[index] = listText[index].replace(
                        "\\...", listText[indexCopie]
                    )
                else:
                    listText[index] = listText[indexCopie]

        linePerSlide = settings.PRESSETTINGS.get(
            "Presentation_Parameters", "line_per_diapo"
        )
        listText, listStype = gestchant.applyMaxNumberLinePerDiapo(
            listText, listStype, linePerSlide
        )

        nombre = len(listText)
        for i, text in enumerate(listText):
            diapo = classDiapo.Diapo(self, i + 1, listStype[i], max_car, nombre, text)
            self._diapos.append(diapo)
        return self._diapos

    @property
    def chemin(self):
        return self._chemin

    @chemin.setter
    def chemin(self, value):
        cdlPath = settings.GENSETTINGS.get("Paths", "conducteurdelouange")
        if not os.path.isfile(value) and value.find(cdlPath) == -1:
            ext = settings.GENSETTINGS.get("Extentions", self.etype)[0]
            path = fonc.get_path(value)
            name = fonc.get_file_name(value)
            name = fonc.enleve_accents(name)
            name = re.sub(r'[\/?!,;:*<>"|^\n]+', "", name)
            name = re.sub(r"[\'() ]+", "_", name)
            name = re.sub(r"_+", "_", name)
            name = name.strip("_")
            self._chemin = os.path.join(path, name) + ext
        else:
            self._chemin = value

    def resetDiapos(self):
        del self._diapos[:]

    @title.setter
    def title(self, newTitle):
        if newTitle:
            if newTitle[:3] in ["JEM", "SUP"] and newTitle[3:6].isdigit():
                newTitle = newTitle[7:]
            newTitle = newTitle.replace("\n", "")
            newTitle = newTitle.strip(" ")

            deb = self.nom.find("(")
            fin = self.nom.find(")")
            if deb != -1 and fin != -1:
                self._supInfo = self.nom[deb + 1 : fin]

            deb = newTitle.find("(")
            fin = newTitle.find(")")
            if deb != -1 and fin != -1:
                newTitle = newTitle[:deb] + newTitle[fin + 1 :]

        else:
            newTitle = ""
        self._title = fonc.safeUnicode(newTitle)
        self._latexText = ""
        self._beamerText = ""
        self._markdownText = ""

    def exist(self):
        return os.path.isfile(self.chemin) and self.text

    def save(self):
        pass

    def safeUpdateXML(self, xmlRoot, field, value):
        if isinstance(value, (int, float)):
            value = str(value).encode("utf-8").decode("utf-8")
        if value is not None:
            try:
                xmlRoot.find(field).text = fonc.safeUnicode(value)
            except AttributeError:
                import lxml.etree as ET_write

                ET_write.SubElement(xmlRoot, field)
                xmlRoot.find(field).text = fonc.safeUnicode(value)
