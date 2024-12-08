# -*- coding: utf-8 -*-

import os
import codecs
import re

from songfinder import gestchant
from songfinder import fonctions as fonc
from songfinder import accords
from songfinder import classDiapo
import songfinder
from songfinder import classSettings as settings


class ExportBase(object):
    def __init__(self, element, titleLevel, exportSettings=None):
        self.element = element
        self._nbLignes = -1
        self._forcedNewLine = r"\newac"
        self._newLineSuggest = r"\newline"
        self._chordsMarker = "\t\\hspace*{\\fill}"
        self._diapos = []
        self._exportedText = ""
        self._titleLevel = titleLevel

        self._newlineMarker = "\n"
        self._supportedTypes = []
        self._specialChar = []

        if not exportSettings:
            self._exportSettings = settings.LATEXSETTINGS
        else:
            self._exportSettings = exportSettings

    @property
    def text(self):
        return self.element.text

    @property
    def transpose(self):
        return self.element.transpose

    @property
    def capo(self):
        if self._exportSettings.get("Export_Parameters", "auto_capo") and self.key:
            ref_keys = set(("C", "G"))
            capo = 12
            song_key_num = accords.Chord(self.key).num + self.transpose

            for key in ref_keys:
                ref_key_num = accords.Chord(key).num
                new_capo = (song_key_num - ref_key_num) % 12
                if new_capo < capo:
                    capo = new_capo
        else:
            capo = self.element.capo if self.element.capo else 0
        return capo % 12

    @property
    def diapos(self):
        return self.element.diapos

    @property
    def title(self):
        return self.element.title

    @property
    def etype(self):
        return self.element.etype

    @property
    def nom(self):
        return self.element.nom

    @property
    def key(self):
        return self.element.key

    @property
    def tempo(self):
        return self.element.tempo

    @property
    def printref(self):
        return self.element.printref

    @property
    def ccli(self):
        return self.element.ccli

    @property
    def hymnNumber(self):
        return self.element.hymnNumber

    @property
    def customNumber(self):
        return self.element.customNumber

    @property
    def turfNumber(self):
        return self.element.turfNumber

    @title.setter
    def title(self, value):
        self.element.title = value

    @etype.setter
    def etype(self, value):
        self.element.etype = value

    @property
    def nbLine(self):
        if self._nbLignes == -1:
            self.exportText  # pylint: disable=pointless-statement,no-member
        return self._nbLignes

    def _processChords(self, text):
        deb = 0
        fin = 0
        newtext = ""
        while fin != -1:
            tmp = text.find("\\ac", deb)
            if tmp == -1:
                newtext = newtext + text[deb:]
                fin = -1
            else:
                fin = text.find("\n", tmp)
                if fin != -1:
                    extrait = text[tmp:fin]
                else:
                    extrait = text[tmp:]

                chordsObj = accords.Accords(
                    extrait,
                    transposeNb=self.transpose,
                    capo=self.capo,
                    exportSettings=self._exportSettings,
                )
                chords = chordsObj.getChords(key=self.key)

                if text[deb:tmp] == "":
                    addNewLine = f"{self._forcedNewLine}"
                else:
                    addNewLine = ""
                newtext = "%s%s%s\\ac %s%s" % (
                    newtext,
                    text[deb:tmp],
                    addNewLine,
                    "~~".join(chords),
                    self._forcedNewLine,
                )
                deb = fin + 1
        return newtext

    def _processNewLine(self, text):
        if self._exportSettings.get("Export_Parameters", "saut_lignes"):
            text = text.replace("\n", f" {self._newLineSuggest}")
            # Force newline if one line ends a sentence TODO to keep ?
            for ponct in [".", "!", "?"]:
                text = text.replace(f"{ponct} {self._newLineSuggest}", f"{ponct}\n")

        # Saut de ligne apres et pas avant les chaines suivantes
        for execp in ['"', ' "', " (bis)", " (ter)", " (x4)", ".", "?"]:
            text = text.replace(f"\n{execp}", f"{execp}\n")

        # Proposition de saut de ligne apres et pas avant les chaines suivantes
        for execp in [",", ";", ":"]:
            text = text.replace(f"\n{execp}", execp + self._newLineSuggest)

        # Saut de ligne apres les chaines suivantes
        for execp in ["(bis)", "(ter)", "(x4)", "(bis) ", "(ter) ", "(x4) ", "\\l "]:
            text = text.replace(execp + self._newLineSuggest, f"{execp}\n")

        text = text.replace(".\n.\n.\n", "...\n")
        text = text.replace("Oh !\n", "Oh !")
        text = text.replace("oh !\n", "oh !")
        # Avoid double newline when \l is used after chords
        text = text.replace(f"{self._forcedNewLine}\\l", self._forcedNewLine)
        text = text.replace(self._forcedNewLine, "\n")
        # Force new line after (f) if there are h/f responces)
        text = text.replace(f"(f) {self._newLineSuggest}", "(f) \n")

        supressStarts = [self._newLineSuggest, "\n"]
        supressEnds = ["(bis)", "(Bis)", "(ter)", "(x3)", "(x4)"]
        for start in supressStarts:
            for end in supressEnds:
                text = text.replace(start + end, "")
        # Must be after for the case where (bis) is just befor chords
        acReplace = [self._newLineSuggest, "\n", "\n "]
        for start in acReplace:
            text = text.replace(f"{start}\\ac", "\\ac")

        # Do not take away a new line if there is a bis at the end
        for multiple in ["(bis)", "(ter)", "(x4)"]:
            fin = len(text) - 1
            bis = 0
            while fin != -1 and bis != -1:
                bis = text.rfind(multiple, 0, fin)
                fin = text.rfind(self._newLineSuggest, 0, bis)
                if fin != -1 and bis != -1 and text[fin + 8 : bis].find("\n") == -1:
                    text = f"{text[:fin]}\n{text[fin + 8:]}"
        return text

    def _matchPara(self, text1, text2, ignore=()):
        text1 = f"{text1}\n"
        text2 = f"{text2}\n"
        for toIgnore in ignore:
            text1 = text1.replace(toIgnore, "")
            text2 = text2.replace(toIgnore, "")
        if text1.find("\\ac") == -1 or text2.find("\\ac") == -1:
            text1 = fonc.supressB(text1, "\\ac", "\n")
            text2 = fonc.supressB(text2, "\\ac", "\n")
        text1 = text1.replace("\n", "")
        text2 = text2.replace("\n", "")
        listMot1 = text1.split(" ")
        listMot2 = text2.split(" ")
        matches = len(set(listMot1) & set(listMot2))
        diff = len(set(listMot1) ^ set(listMot2))
        diff = diff * diff / 4
        if diff == 0:
            out = 10000.0
        else:
            out = matches / diff
        return out

    def _getDiapos(self):
        if self._diapos != []:
            return self._diapos

        text = self.text
        if self._exportSettings.get("Export_Parameters", "chords"):
            text = self._processChords(text)
        else:
            text = f"{text}\n"
            text = fonc.supressB(text, "\\ac", "\n")
            text = text.strip("\n")
        text = self._processNewLine(text)
        listStype = []
        # La première est vide ie au dessus du premier \s
        listText, listStype = fonc.splitPerso(
            [text], settings.GENSETTINGS.get("Syntax", "newslide"), listStype, 0
        )
        del listText[0]

        # Suprime les doublons
        newListText = []
        newListStype = []
        must_be_new_diapo = set()
        diapo_count = 0
        toIgnore = [self._newLineSuggest, settings.GENSETTINGS.get("Syntax", "newline")]
        for i, text in enumerate(listText):
            nb_words = len(text.split(" "))
            match = 0.0
            for textRef in newListText:
                match = max(self._matchPara(textRef, text, ignore=toIgnore), match)
            stripedText = text.replace(f" {self._newLineSuggest}", "")
            # This is sketchy: if number of words is small do not consider it
            # as duplicate as it would probably be merged into another diapo
            # This is valable only if the previous diapo was not removed
            if (
                (
                    (nb_words < 15 and diapo_count - 1 not in must_be_new_diapo)
                    or match < 14  # this is very sensible
                )
                and text.find("\\...") == -1
                and stripedText
            ):
                newListText.append(text)
                newListStype.append(listStype[i])
                diapo_count += 1
            else:
                must_be_new_diapo.add(diapo_count - 1)
        listText = newListText
        listStype = newListStype

        listStypePlus = gestchant.getListStypePlus(listStype)

        # Fusion et creation des diapos
        for elem in listStypePlus:
            text = ""
            for i, numDiapo in enumerate(elem[1]):
                text = f"{text}\n{listText[numDiapo]}\n"
                text = self._clean(text)
                nb_lines = text.count("\n")
                try:
                    next_text = listText[numDiapo + 1]
                    self._clean(next_text)
                    next_nb_lines = next_text.count("\n")
                except IndexError:
                    next_nb_lines = 0
                text_no_chords = fonc.supressB(text, "\\ac", "\n")
                if (
                    numDiapo in must_be_new_diapo
                    or numDiapo == elem[1][-1]
                    or (
                        elem[0] == "\\ss"
                        and (
                            len(text_no_chords) > 200
                            or nb_lines + next_nb_lines > 7
                            # If there is allready a new diapo that must be created dont do it with this criteria
                            or (
                                len(elem[1]) % 2 == 1
                                and set(elem[1]).intersection(must_be_new_diapo)
                                == set()
                            )
                            or i % 2 == 1
                        )
                    )
                ):
                    if elem[0] in ["\\sc", "\\spc"]:
                        if text.find("\\ac") != -1:
                            max_car = 85
                        else:
                            max_car = 95
                    else:
                        if text.find("\\ac") != -1:
                            max_car = 90
                        else:
                            max_car = 100
                    diapo = classDiapo.Diapo(
                        self.element,
                        len(self._diapos) + 1,
                        elem[0],
                        max_car,
                        len(listStypePlus),
                        text.strip("\n"),
                    )
                    self._diapos.append(diapo)
                    text = ""
        return self._diapos

    def _clean(self, text):
        for _ in range(5):
            text = text.replace("\n\n\n", "\n\n")
            text = text.replace(
                f"{self._newlineMarker}{self._newlineMarker}", self._newlineMarker
            )
            text = text.replace(f"\n{self._newlineMarker}\n", "\n\n")
        text = text.strip("\n")
        text = fonc.strip_perso(text, self._newlineMarker)
        return text

    def escape(self, inputData):
        """
        Adds a backslash behind latex special characters
        """
        if isinstance(inputData, str):
            output = inputData
            for char in self._specialChar:
                output = output.replace(char, f"\\{char}")
        elif isinstance(inputData, list):
            output = []
            for text in inputData:
                for char in self._specialChar:
                    text = text.replace(char, f"\\{char}")
                output.append(text)
        else:
            raise Exception(
                f'Input "{inputData}"must be str or list, but is {type(inputData)}.'
            )
        return output


class ExportLatex(ExportBase):
    def __init__(self, element, titleLevel=1, exportSettings=None):
        ExportBase.__init__(self, element, titleLevel, exportSettings=exportSettings)
        self._newlineMarker = r"\\"
        self._supportedTypes = ["latex", "verse"]
        self._specialChar = ["#", "_"]

    @property
    def exportText(self):
        if self.etype == "song":
            self.etype = "latex"
        if self.etype not in self._supportedTypes:
            self.etype = "song"
            return ""
        # ~ if self._exportedText != '':
        # ~ self.etype = 'song'
        # ~ return self._exportedText
        self._getDiapos()
        text = "\n\n".join([diapo.latex for diapo in self._diapos])
        text = self.escape(text)
        text = text.replace(r"\ac", self._chordsMarker)
        text = text.replace("\n", f"{self._newlineMarker}\n")
        text = text.replace(f"\n{self._newlineMarker}", "\n")
        text = text.replace(f"\n\\tab {self._newlineMarker}", "\n")

        # Move chords to left side when there is no lyrics
        # Add a new line after each intro chord line
        regex_chord_pattern = r"(\\tab )?\t\\hspace\*\{\\fill\}"
        text = re.sub(
            f"^({regex_chord_pattern} .*$)", r"\1\n", text, flags=re.MULTILINE
        )
        # Remove new line bewteen intro chords
        text = re.sub(
            f"^\n({regex_chord_pattern} .*$)", r"\1", text, flags=re.MULTILINE
        )
        # Remove tabs, spaces and alignment
        text = re.sub(f"^{regex_chord_pattern} ", r"\1", text, flags=re.MULTILINE)

        text = self._clean(text)
        self._nbLignes = len(text.splitlines())

        # Capo
        if self._exportSettings.get("Export_Parameters", "capo") and self.capo:
            text = "\\emph{Capo %s}%s\n%s" % (str(self.capo), self._newlineMarker, text)

        # Title
        text = "\\begin{figure}\n\\section{%s}\n%s\n\\end{figure}\n" % (
            self.escape(self.title),
            text,
        )

        # Song per page
        if self._exportSettings.get("Export_Parameters", "one_song_per_page"):
            text = f"{text}\n\\clearpage"

        self._exportedText = text
        self.etype = "song"
        return text

    @property
    def title(self):
        # Title key
        if self._exportSettings.get("Export_Parameters", "printkey"):
            chord = accords.Accords(
                self.key,
                transposeNb=self.transpose,
                capo=self.capo,
                exportSettings=self._exportSettings,
            )
            key = chord.getChords()[0]
            if key != "":
                key = "~--~\\emph{%s}" % key
        else:
            key = ""
        if self.tempo and self._exportSettings.get("Export_Parameters", "printtempo"):
            tempo = "~--~\\emph{%s}bpm" % self.tempo
        else:
            tempo = ""

        # Reference in title
        if self._exportSettings.get("Export_Parameters", "printref") and self.ccli:
            refID = f" ({self.ccli})"
        else:
            refID = ""

        # Title
        return f"{self.element.title}{refID}{key}{tempo}"


class ExportMarkdown(ExportBase):
    def __init__(self, element, titleLevel=1, exportSettings=None):
        ExportBase.__init__(self, element, titleLevel, exportSettings=exportSettings)
        self._newlineMarker = "  "
        self._supportedTypes = ["markdown"]
        self._specialChar = ["*", "_"]

    @property
    def exportText(self):
        if self.etype == "song":
            self.etype = "markdown"
        if self.etype not in self._supportedTypes:
            self.etype = "song"
            return ""
        # ~ if self._exportedText != '':
        # ~ self.etype = 'song'
        # ~ return self._exportedText
        self._getDiapos()
        text = "\n\n".join([diapo.markdown for diapo in self._diapos])
        text = f"{text}\n"
        deb = 0
        fin = 0
        toFindStart = "\\ac"
        toFindEnd = "\n"
        while deb != -1:
            deb = text.find(toFindStart, fin)
            fin = text.find(toFindEnd, deb)
            if deb == -1 or fin == -1:
                break
            text = "%s`%s`\n%s" % (
                text[:deb],
                text[deb + len(toFindStart) : fin].strip(" "),
                text[fin + len(toFindEnd) :],
            )
            fin -= len(toFindStart) + 2

        text = text.replace("\n", f"{self._newlineMarker}\n")
        text = text.replace("~~", "  ")
        text = self._clean(text)
        text = f"{text}\n"
        self._nbLignes = len(text.splitlines())

        # Capo
        if self._exportSettings.get("Export_Parameters", "capo") and self.capo:
            text = f"*Capo {str(self.capo)}*  \n{text}"

        # Title key
        if self.key and self._exportSettings.get("Export_Parameters", "printkey"):
            chord = accords.Accords(
                self.key,
                transposeNb=self.transpose,
                capo=self.capo,
                exportSettings=self._exportSettings,
            )
            key = chord.getChords()[0]
            if key != "":
                key = f" -- *{key}*"
        else:
            key = ""

        tempo = ""
        if self.tempo and self._exportSettings.get("Export_Parameters", "printtempo"):
            tempo = f" -- *{self.tempo}bpm*"
        else:
            tempo = ""

        # Title
        title = f"{'#' * self._titleLevel} {self.title}{key}{tempo}\n"

        if not self._exportSettings.get("Export_Parameters", "list"):
            text = f"{title}{text}"
        else:
            text = f"{title}"

        self._exportedText = text
        self.etype = "song"
        return text


class ExportBeamer(ExportBase):
    def __init__(self, element, titleLevel=1, exportSettings=None):
        ExportBase.__init__(self, element, titleLevel, exportSettings=exportSettings)
        self._newlineMarker = "\\\\"
        self._supportedTypes = ["beamer", "image", "verse"]
        self._specialChar = ["#", "_"]

    @property
    def exportText(self):
        if self.etype == "song":
            self.etype = "beamer"
        if self.etype not in self._supportedTypes:
            self.etype = "song"
            return ""
        # ~ if self._exportedText != '':
        # ~ self.etype = 'song'
        # ~ return self._exportedText
        self._diapos = []
        text = ""
        for diapo in self.diapos:
            toAdd = self.escape(diapo.beamer)
            toAdd = toAdd.replace("\n", f"{self._newlineMarker}\n")
            toAdd = toAdd.replace(f"\n{self._newlineMarker}", "\n")
            backStr = diapo.backgroundName.replace("\\", "/")
            backStr = '"%s/%s"%s' % (
                fonc.get_path(backStr),
                fonc.get_file_name(backStr),
                fonc.get_ext(backStr),
            )
            text += "\\newframe{%s}\n%s\n\\end{frame}\n\n" % (backStr, toAdd)
        text = self._clean(text)
        self._nbLignes = len(text.splitlines())
        text = fonc.noNewLine(text, "\\newframe", self._newlineMarker)
        text = fonc.noNewLine(text, "\\vspace", self._newlineMarker)
        text = f"{text}\n"
        self._exportedText = text
        self.etype = "song"
        return text


class ExportHtml(ExportBase):
    def __init__(
        self,
        element,
        titleLevel=1,
        markdowner=None,
        htmlStyle=None,
        htmlStylePath=None,
        exportSettings=None,
    ):
        ExportBase.__init__(self, element, titleLevel, exportSettings=exportSettings)
        self._element = element
        self._supportedTypes = ["markdown"]
        if markdowner:
            self._markdowner = markdowner
        else:
            import markdown  # Consumes lots of memory

            self._markdowner = markdown.Markdown()
        self._htmlStyle = htmlStyle

        if not htmlStylePath:
            htmlStylePath = os.path.join(
                songfinder.__dataPath__, "htmlTemplates", "defaultStyle.html"
            )
        if not htmlStyle and os.path.isfile(htmlStylePath):
            with codecs.open(htmlStylePath, "r", encoding="utf-8") as styleFile:
                self._htmlStyle = styleFile.read()

    def _addTitle(self, text):
        if self.title:
            text = f"<title>{self.title}</title>\n{text}"
        return text

    @property
    def exportText(self):
        if self.etype == "song":
            self.etype = "markdown"
        if self.etype not in self._supportedTypes:
            self.etype = "song"
            return ""
        markdownText = ExportMarkdown(
            self._element,
            titleLevel=self._titleLevel,
            exportSettings=self._exportSettings,
        ).exportText

        text = self._markdowner.convert(markdownText)
        if self._titleLevel == 1:
            text = self._addTitle(text)
        if self._htmlStyle:
            text = self._htmlStyle.replace("@@body@@", text)
        self._markdowner.reset()
        self._exportedText = text
        self.etype = "song"
        return text
