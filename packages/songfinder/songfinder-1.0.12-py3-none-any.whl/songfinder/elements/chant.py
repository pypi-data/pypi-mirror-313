# -*- coding: utf-8 -*-

import os
import errno
import xml.etree.cElementTree as ET
import traceback
import string
import codecs
import logging
import re

from songfinder import gestchant
from songfinder import classPaths
from songfinder import fonctions as fonc
from songfinder import messages as tkMessageBox
from songfinder import pyreplace
from songfinder import classSettings as settings
from songfinder.elements import Element
from songfinder.elements import cdlparser

RECEUILS = [
    "JEM",
    "ASA",
    "WOC",
    "HER",
    "HEG",
    "FAP",
    "MAR",
    "CCO",
    "PBL",
    "LDM",
    "JFS",
    "THB",
    "EHO",
    "ALG",
    "BLF",
    "ALR",
    "HLS",
    "IMP",
    "PNK",
    "DNL",
    "ROG",
    "WOC",
    "SOL",
    "FRU",
    "OST",
    "ENC",
    "DIV",
]


class Chant(Element):
    def __init__(self, chant, nom=""):
        self.etype = "song"
        self.extention = fonc.get_ext(chant)
        if self.extention == "" and chant.find("http") == -1:
            self.extention = settings.GENSETTINGS.get("Extentions", "song")[0]
            chant = chant + self.extention
        self.chemin = chant

        Element.__init__(self, chant, self.etype, self.chemin)
        self.nom = fonc.get_file_name(self.chemin)

        self._title = nom
        self._song_book = ""
        self.reset()

    def _getCDL(self):
        parsedSong = cdlparser.CDLParser(self.chemin)
        # Text should be the first to be get because other depends on it
        # Infinite loop is possible if text is not first
        self.text = parsedSong.text
        self.key = parsedSong.key
        self.hymnNumber = parsedSong.hymnNumber
        self.song_book = parsedSong.song_book
        self.title = parsedSong.title
        self.copyright = parsedSong.copyright
        self.tags = parsedSong.tags
        self.author = parsedSong.authors
        fileName = str(parsedSong) + settings.GENSETTINGS.get("Extentions", "song")[0]
        rootPath = classPaths.PATHS.songs
        self.chemin = os.path.join(rootPath, fileName)

    def reset(self):
        self._resetText()
        self._transpose = None
        self._capo = None
        self._key = None
        self._turfNumber = None
        self._hymnNumber = None
        self._tempo = None

    def _resetText(self):
        self._text = None
        self._words = ""
        self._textHash = None
        self.resetDiapos()

    def __save__(self):
        # This function is keept for hidden functionality
        # This is probably not the function you actualy want to edit
        # Look at database save method

        # We use a different xml lib here because it does not add carriage return on Windows for writes
        # There might be a way to use xml.etree.cElementTree that don't but have not figured out
        # xml.etree.cElementTree is faster at parsing so keep it for song parsing
        import lxml.etree as ET_write

        ext = settings.GENSETTINGS.get("Extentions", "song")[0]
        if fonc.get_ext(self.chemin) != ext:
            path = classPaths.PATHS.songs
            self.chemin = "%s%d_%s" % (self.song_book, self.hymnNumber, self.title)
        try:
            tree = ET_write.parse(self.chemin)
            chant_xml = tree.getroot()
        except (OSError, IOError) as error:
            chant_xml = ET_write.Element(self.etype)
        self.safeUpdateXML(chant_xml, "lyrics", self.text)
        self.safeUpdateXML(chant_xml, "title", self.title)
        self.safeUpdateXML(chant_xml, "sup_info", self.supInfo)
        self.safeUpdateXML(chant_xml, "transpose", self.transpose)
        self.safeUpdateXML(chant_xml, "capo", self.capo)
        self.safeUpdateXML(chant_xml, "key", self.key)
        self.safeUpdateXML(chant_xml, "tempo", self.tempo)
        self.safeUpdateXML(chant_xml, "turf_number", self.turfNumber)
        self.safeUpdateXML(chant_xml, "hymn_number", self.hymnNumber)
        self.safeUpdateXML(chant_xml, "author", self.author)
        self.safeUpdateXML(chant_xml, "copyright", self.copyright)
        self.safeUpdateXML(chant_xml, "ccli", self.ccli)
        self.safeUpdateXML(chant_xml, "tags", self.tags)
        fonc.indent(chant_xml)

        tree = ET_write.ElementTree(chant_xml)
        tree.write(self.chemin, encoding="UTF-8", xml_declaration=True)
        self.resetDiapos()

    def _replaceInText(self, toReplace, replaceBy):
        self.text = self.text.replace(toReplace, replaceBy)
        self.__save__()

    @property
    def nums(self):
        return {
            "custom": self.customNumber,
            "turf": self.turfNumber,
            "hymn": self.hymnNumber,
        }

    @property
    def turfNumber(self):
        self.text  # pylint: disable=pointless-statement
        return self._turfNumber

    @property
    def hymnNumber(self):
        self.text  # pylint: disable=pointless-statement
        return self._hymnNumber

    @property
    def customNumber(self):
        match = re.match("([A-Z]{3})(\\d{3,4})", self.nom)
        if match:
            self._customNumber = int(match.group(2))
            return self._customNumber
        return None

    @property
    def transpose(self):
        self.text  # pylint: disable=pointless-statement
        return self._transpose

    @property
    def capo(self):
        self.text  # pylint: disable=pointless-statement
        return self._capo

    @property
    def key(self):
        self.text  # pylint: disable=pointless-statement
        return self._key

    @property
    def tempo(self):
        self.text  # pylint: disable=pointless-statement
        return self._tempo

    @property
    def author(self):
        self.text  # pylint: disable=pointless-statement
        return self._author

    @property
    def copyright(self):
        self.text  # pylint: disable=pointless-statement
        return self._copyright

    @property
    def ccli(self):
        if self.song_book and self.hymnNumber:
            return f"{self.song_book}{self.hymnNumber:>04}"
        else:
            return None

    @property
    def text(self):
        if self._text is None:
            cdlPath = settings.GENSETTINGS.get("Paths", "conducteurdelouange")
            if fonc.get_ext(self.chemin) in settings.GENSETTINGS.get(
                "Extentions", "chordpro"
            ):
                self._getChordPro()
            elif fonc.get_ext(self.chemin) in settings.GENSETTINGS.get(
                "Extentions", "song"
            ):
                self._getXML()
            elif self.chemin.find(cdlPath) != -1:
                self._getCDL()
            else:
                logging.warning(f'Unknown file format for "{self.chemin}".')
        return self._text

    def _getXML(self):
        self.reset()
        try:
            tree = ET.parse(self.chemin)
            chant_xml = tree.getroot()
        except (OSError, IOError):
            logging.warning(
                f'Not able to read "{self.chemin}"\n{traceback.format_exc()}'
            )
            self.title = self.nom
            chant_xml = ET.Element(self.etype)
        except ET.ParseError:
            logging.info(f"Error on {self.chemin}:\n{traceback.format_exc()}")
            tkMessageBox.showerror(
                "Erreur", f'Le fichier "{self.chemin}" est illisible.'
            )
        try:
            tmp = chant_xml.find("lyrics").text
            title = chant_xml.find("title").text
        except (AttributeError, KeyError):
            tmp = ""
            title = ""
        try:
            self.supInfo = chant_xml.find("sup_info").text
        except (AttributeError, KeyError):
            self.supInfo = ""
        if tmp is None:
            tmp = ""
        try:
            self._transpose = int(chant_xml.find("transpose").text)
        except (AttributeError, KeyError, ValueError, TypeError):
            self._transpose = None
        try:
            self._capo = int(chant_xml.find("capo").text)
        except (AttributeError, KeyError, ValueError, TypeError):
            self._capo = None
        try:
            self._tempo = int(chant_xml.find("tempo").text)
        except (AttributeError, KeyError, ValueError, TypeError):
            self._tempo = None
        try:
            self._hymnNumber = int(chant_xml.find("hymn_number").text)
        except (AttributeError, KeyError, ValueError, TypeError):
            self._hymnNumber = None
        try:
            self._turfNumber = int(chant_xml.find("turf_number").text)
        except (AttributeError, KeyError, ValueError, TypeError):
            self._turfNumber = None
        try:
            self._key = chant_xml.find("key").text
        except (AttributeError, KeyError):
            self._key = ""
        try:
            self._key = self._key.replace("\n", "")
        except AttributeError:
            pass
        try:
            self._author = chant_xml.find("author").text
        except (AttributeError, KeyError):
            self._author = None
        try:
            self._copyright = chant_xml.find("copyright").text
        except (AttributeError, KeyError):
            self._copyright = None
        try:
            ccli = chant_xml.find("ccli").text.replace(" ", "")
            match = re.match("([A-Z]{3})\\d{3,4}", ccli)
            if match:
                self._song_book = match.group(1)
        except (AttributeError, KeyError):
            self._song_book = ""
        try:
            tags = chant_xml.find("tags").text
            self.tags = tags
        except (AttributeError, KeyError):
            self._tags = []
        self.title = title
        self.text = tmp

    @transpose.setter
    def transpose(self, value):
        try:
            value = value.strip("\n")
        except AttributeError:
            pass
        try:
            self._transpose = int(value)
        except (ValueError, TypeError):
            if not value:
                self._transpose = 0
            else:
                self._transpose = None

    @capo.setter
    def capo(self, value):
        try:
            value = value.strip("\n")
        except AttributeError:
            pass
        try:
            self._capo = int(value)
        except (ValueError, TypeError):
            if not value:
                self._capo = 0
            else:
                self._capo = None

    @tempo.setter
    def tempo(self, value):
        try:
            value = value.strip("\n")
        except AttributeError:
            pass
        try:
            self._tempo = int(value)
        except (ValueError, TypeError):
            if not value:
                self._tempo = 0
            else:
                self._tempo = None

    @turfNumber.setter
    def turfNumber(self, value):
        try:
            value = value.strip("\n")
        except AttributeError:
            pass
        try:
            self._turfNumber = int(value)
        except (ValueError, TypeError):
            if not value:
                self._turfNumber = 0
            else:
                self._turfNumber = None

    @hymnNumber.setter
    def hymnNumber(self, value):
        try:
            value = value.strip("\n")
        except AttributeError:
            pass
        try:
            self._hymnNumber = int(value)
        except (ValueError, TypeError):
            if not value:
                self._hymnNumber = 0
            else:
                self._hymnNumber = None

    @key.setter
    def key(self, value):
        self._key = value.strip(" \n")

    @text.setter
    def text(self, value):
        self._resetText()
        value = fonc.supressB(value, "[", "]")  ######
        value = gestchant.nettoyage(fonc.safeUnicode(value))
        value = f"{value}\n"
        self._text = value

    @author.setter
    def author(self, value):
        self._author = value.replace("\n", " ").replace("  ", " ").strip(" ")

    @copyright.setter
    def copyright(self, value):
        self._copyright = value.strip(" \n")

    @property
    def words(self):
        if not self._words:
            text = gestchant.netoyage_paroles(self.text)
            self._words = text.split()
            nb_words = 3
            addList = [
                " ".join(self._words[i : i + nb_words])
                for i in range(max(len(self._words) - nb_words + 1, 0))
            ]
            self._words += addList
        return self._words

    @property
    def song_book(self):
        if not self._song_book:
            match = re.match("([A-Z]{3})\\d{3,4}", self.nom)
            if match:
                self._song_book = match.group(1)
        return self._song_book

    @song_book.setter
    def song_book(self, in_song_book):
        in_str = str(in_song_book).strip(" \n")
        if in_str == "":
            in_str = "SUP"
        if not len(in_str) == 3:
            raise ValueError(f"Song book must be 3 charactere long but got: '{in_str}'")
        self._song_book = in_str.upper()

    def _getChordPro(self):
        try:
            with codecs.open(self.chemin, encoding="utf-8") as f:
                brut = f.read()
                if not brut:
                    logging.warning(
                        f'File "{self.chemin}" is empty\n{traceback.format_exc()}'
                    )
                    return ""
        except (OSError, IOError):
            logging.warning(
                f'Not able to read "{self.chemin}"\n{traceback.format_exc()}'
            )
            return ""

        def get_cp(char):
            return re.search("{%s:(.*)}" % char, brut).group(1)

        self.title = get_cp("t")
        self.author = get_cp("st")
        self.copyright = get_cp("c")
        self.key = get_cp("key")
        ccli_brut = re.search("{c: *(jemaf.fr|shir.fr).*([A-Z]{3})(\\d{3,4})}", brut)
        self.song_book = ccli_brut.group(2)
        self.hymnNumber = ccli_brut.group(3)

        brut = pyreplace.cleanupChar(brut.encode("utf-8"))
        brut = pyreplace.cleanupSpace(brut).decode("utf-8")

        # Interprete chorpro syntax
        if re.search("{c: *shir.fr.*}", brut):
            brut = " \\ss\n" + brut
            brut = re.sub("\n\n", "\\n\\n\\\\ss\\n", brut)
            brut = re.sub("{(eoc|start_of_verse|sov)}", "\\n\\n\\\\ss\\n", brut)
            brut = re.sub("{(start_of_chorus|soc)}", "\\n\\n\\\\sc\\n", brut)
        else:
            brut = re.sub("\\W\\d\\.\\W", "", brut)
            brut = re.sub("{c: ?Strophe(.*?)}", "\\n\\n\\\\ss\\n", brut)
            brut = re.sub("{c: ?Refrain(.*?)}", "\\n\\n\\\\sc\\n", brut)
        brut = re.sub("{c: ?Pont(.*?)}", "\\n\\n\\\\sb\\n", brut)

        brut = re.sub("{.*?}", "", brut)

        brut = gestchant.nettoyage(brut)
        brut = gestchant.nettoyage(brut)
        brut = brut.replace("\\ss\n\n\\sc", "\\sc")
        brut = brut.replace("\\ss\n\n\\sb", "\\sb")

        # Put double back slash at the last chord of each line
        brut = brut + "\n"
        fin = len(brut)
        got_to_the_limit = True
        for _ in range(1000):
            if fin == -1:
                got_to_the_limit = False
                break
            line = brut.rfind("\n", 0, fin)
            fin = brut.rfind("]", 0, line)
            if line == fin + 1:
                precedant = fin
                while brut[precedant] == "]":
                    precedant = brut.rfind("[", 0, precedant) - 1
                brut = (
                    brut[: precedant + 2]
                    + ""
                    + brut[precedant + 2 : fin]
                    + "\\"
                    + brut[fin:]
                )
            else:
                brut = brut[:fin] + "\\" + brut[fin:]
        if got_to_the_limit:
            logging.error(
                f"Could not properly handle chords for '{self.chemin}', stoping now"
            )
        brut = fonc.strip_perso(brut, "\\\n")

        # Remove space after chord
        for letter in string.ascii_uppercase[:7]:
            brut = brut.replace(f"\n[{letter}] ", f"\n[{letter}]")
        brut = self._convertChordsFormat(brut)
        self.text = brut

    def _convertChordsFormat(self, text):
        if text != "":
            text = text + "\n"
            listChords = fonc.getB(text, "[", "]")
            where = 0
            last = 0
            for i, chord in enumerate(listChords):
                # Add parenthesis for chord at end of lines
                if chord.find("\\") != -1:
                    toAdd = (
                        "\\ac "
                        + " ".join(listChords[last : i + 1]).replace("\\", "")
                        + "\n"
                    )
                    where = text.find(chord, where)
                    where = text.find("\n", where) + 1
                    text = text[:where] + toAdd + text[where:]
                    last = i + 1
            text = fonc.strip_perso(text, "\n")

            text = fonc.supressB(text, "[", "]")

            for newslide in settings.GENSETTINGS.get("Syntax", "newslide")[0]:
                text = text.replace(f"{newslide}\n\n\\ac", f"{newslide}\n\\ac")
            return text
        return ""

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        if not isinstance(other, Chant):
            raise TypeError(
                f"Expected instance of '{self.__class__.__name__}', but got instance of '{type(other)}'"
            )
        if not self.words and not other.words:
            if self.title == other.title and self.supInfo == other.supInfo:
                return True
            return False
        myWords = set(self.words)
        otherWords = set(other.words)
        commun = len(myWords & otherWords)
        ratio = 2 * commun / (len(myWords) + len(otherWords))
        return ratio > 0.93

    def __hash__(self):
        return hash(repr(self))

    def __gt__(self, other):
        return self.title > other.title

    def __ge__(self, other):
        return self.title >= other.title

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.chemin}')"

    def __str__(self):
        out = f"{self.etype} -- "
        num = self._hymnNumber or self._turfNumber or self._customNumber
        if self.song_book and num:
            out = "%s%s%04d " % (
                out,
                self.song_book,
                num or 0,
            )
        out = f"{out}{self.title}"
        if self.supInfo:
            out = f"{out} ({self.supInfo})"
        return out
