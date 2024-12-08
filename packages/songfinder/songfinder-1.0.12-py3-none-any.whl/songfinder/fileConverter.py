# -*- coding: utf-8 -*-

import os
import errno
import time
import logging
import codecs
import re

from songfinder import elements
from songfinder.elements import exports
from songfinder import classSet
import songfinder
from songfinder import fonctions as fonc
from songfinder import classSettings as settings


class Converter(object):
    def __init__(self, htmlStylePath=None, exportSettings=None, doDecline=False):
        import markdown  # Consumes lots of memory

        self._markdowner = markdown.Markdown()
        self._songExtentions = settings.GENSETTINGS.get(
            "Extentions", "chordpro"
        ) + settings.GENSETTINGS.get("Extentions", "song")
        self._listeExtentions = settings.GENSETTINGS.get("Extentions", "liste")
        self._set = classSet.Set()

        self._dateList = dict()
        self._doDecline = doDecline
        self._toDecline = set()
        self._decliningPass = False
        self._counter = 0
        self._makeSubDir = False
        self._elementDict = dict()

        if not exportSettings:
            self._exportSettings = settings.LATEXSETTINGS
        else:
            self._exportSettings = exportSettings
        self._exportSettingsOrig = self._exportSettings

        self._declineFunctionsSetter = (
            self._setListOptions,
            self._setBassOptions,
            self._setGuitareOptions,
        )

        if not htmlStylePath:
            htmlStylePath = os.path.join(
                songfinder.__dataPath__, "htmlTemplates", "defaultStyle.html"
            )
        if os.path.isfile(htmlStylePath):
            with codecs.open(htmlStylePath, "r", encoding="utf-8") as styleFile:
                self._htmlStyle = styleFile.read()
        else:
            self._htmlStyle = ""

    def _setDefaultOptions(self):
        self._exportSettings = self._exportSettingsOrig
        self._exportSettings.set("Export_Parameters", "sol_chords", True)
        self._suffix = ""

    def _setListOptions(self):
        self._setDefaultOptions()
        self._exportSettings.set("Export_Parameters", "list", True)
        self._suffix = "_list"

    def _setBassOptions(self):
        self._setDefaultOptions()
        self._exportSettings.set("Export_Parameters", "keep_last", True)
        self._exportSettings.set("Export_Parameters", "simple_chords", True)
        self._suffix = "_bass"

    def _setGuitareOptions(self):
        self._setDefaultOptions()
        self._exportSettings.set("Export_Parameters", "keep_first", True)
        self._exportSettings.set("Export_Parameters", "capo", True)
        self._exportSettings.set("Export_Parameters", "simple_chords", True)
        self._suffix = "_guitar"

    def markdown(self, inputFiles, outputFiles, verbose=True):
        self._exportClass = exports.ExportMarkdown
        self._optionSongs = {"exportSettings": self._exportSettings}
        self._optionSets = {"exportSettings": self._exportSettings, "titleLevel": 2}
        self._ext = ".md"
        self._titleMark = "# @@title@@\n"
        self._bodyMark = ""
        if verbose:
            logging.info(f'Converting files in "{inputFiles}" to markdown.')
        self._convert(inputFiles, outputFiles, verbose)

    def latex(self, inputFiles, outputFiles, verbose=True):
        self._exportClass = exports.ExportLatex
        self._optionSongs = {"exportSettings": self._exportSettings}
        self._optionSets = {"exportSettings": self._exportSettings}
        self._ext = ".tex"
        self._titleMark = "@@title@@\n"
        self._bodyMark = ""
        if verbose:
            logging.info(f'Converting files in "{inputFiles}" to markdown.')
        self._convert(inputFiles, outputFiles, verbose)

    def html(self, inputFiles, outputFiles, verbose=True):
        self._exportClass = exports.ExportHtml
        self._optionSongs = {
            "exportSettings": self._exportSettings,
            "markdowner": self._markdowner,
        }
        self._optionSets = {
            "exportSettings": self._exportSettings,
            "markdowner": self._markdowner,
            "htmlStyle": "@@body@@",
            "titleLevel": 2,
        }
        self._ext = ".html"
        self._titleMark = "<title>@@title@@</title>\n<h1>@@title@@</h1>\n"
        self._bodyMark = self._htmlStyle
        if verbose:
            logging.info(f'Converting files in "{inputFiles}" to html.')
        self._convert(inputFiles, outputFiles, verbose)

    def _force_ccli_ref(self, inputFile, outputFile):
        elem = elements.Chant(inputFile)
        filename = fonc.get_file_name(inputFile)
        if elem.ccli:
            filename = re.sub(r"SUP\d{3,4}", elem.ccli, filename)
        return os.path.join(fonc.get_path(outputFile), filename + self._ext)

    def _convert(self, inputFiles, outputFiles, verbose=True):
        refTime = time.time()
        self._setDefaultOptions()
        if os.path.isfile(inputFiles):
            inputFile = inputFiles
            outputFile = self._force_ccli_ref(inputFile, outputFiles)
            self._convertOneFile(inputFile, outputFile, preferedPath=inputFiles)
        elif os.path.isdir(inputFiles):
            if outputFiles[-1] != os.sep:
                outputFiles = outputFiles + os.sep
            for root, _, files in os.walk(inputFiles):
                for fileName in files:
                    inputFile = os.path.join(root, fileName)
                    outputFile = inputFile.replace(inputFiles, outputFiles)
                    outputFile = self._force_ccli_ref(inputFile, outputFile)
                    self._convertOneFile(inputFile, outputFile, preferedPath=inputFiles)

        if self._doDecline:
            # Declining file to guitar/bass/list version
            self._decliningPass = True
            if self._dateList:
                lastKey = sorted(self._dateList.keys())[-1]
                toAdd = (lastKey, self._dateList[lastKey])
                self._toDecline.add(toAdd)
            if self._toDecline:
                for declineParameterSet in self._declineFunctionsSetter:
                    declineParameterSet()
                    for inputFile, outputFile in self._toDecline:
                        outputFile = inputFile.replace(inputFiles, outputFiles)
                        outputFile = (
                            fonc.get_file_path(outputFile) + self._suffix + self._ext
                        )
                        self._convertOneFile(
                            inputFile, outputFile, preferedPath=inputFiles
                        )
            self._setDefaultOptions()
            self._dateList = dict()
            self._toDecline = set()
            self._decliningPass = False

        if verbose:
            logging.info(
                f"Converted {self._counter} files. Convertion took {time.time() - refTime}s."
            )
        self._counter = 0

    def _convertOneFile(self, inputFile, outputFile, preferedPath=None):
        if fonc.get_ext(inputFile) not in self._songExtentions + self._listeExtentions:
            return None
        outputFile = self._makeDirs(outputFile)
        logging.info(f'Converting "{inputFile}" to "{outputFile}"')
        if fonc.get_ext(inputFile) in self._songExtentions:
            myElem = elements.Chant(inputFile)
            try:
                myElem = self._elementDict[myElem.nom]
                myElem.resetDiapos()
            except KeyError:
                self._elementDict[myElem.nom] = myElem
            myExport = self._exportClass(myElem, **self._optionSongs)
            with codecs.open(outputFile, "w", encoding="utf-8") as out:
                out.write(myExport.exportText)
            self._counter += 1

        elif fonc.get_ext(inputFile) in self._listeExtentions:
            self._set.load(
                inputFile, preferedPath=preferedPath, dataBase=self._elementDict
            )
            text = ""
            for myElem in self._set:
                logging.debug(f'Converting "{myElem.chemin}"')
                myExport = self._exportClass(myElem, **self._optionSets)
                text += f"{myExport.exportText}\n"
            title = self._fillMark("title", self._titleMark, str(self._set))
            text = f"{title}{text}"
            text = self._fillMark("body", self._bodyMark, text)
            with codecs.open(outputFile, "w", encoding="utf-8") as out:
                out.write(text)

            # Filling set to decline in guitar/bass/list versions
            if not self._decliningPass:
                if self._isDate(inputFile):
                    self._dateList[inputFile] = outputFile
                else:
                    self._toDecline.add((inputFile, outputFile))
            self._counter += 1

    def _fillMark(self, mark, styledText, content):
        if styledText:
            output = styledText.replace(f"@@{mark}@@", content)
        else:
            output = content
        return output

    def _makeDirs(self, outputFile):
        if self._makeSubDir:
            outputFile = self._makeSubDirectory(outputFile)
        try:
            os.makedirs(fonc.get_path(outputFile))
        except (OSError, IOError) as error:
            if error.errno == errno.EEXIST:
                pass
            else:
                raise
        return outputFile

    def _makeSubDirectory(self, fullPath):
        filePath = fonc.get_path(fullPath)
        fileName = fonc.get_file_name_ext(fullPath)
        subDirectory = ""
        # Match songs
        match = re.match(r"([A-Z]{3})(\d{3,4})", fileName)
        # Match sets
        if not match:
            match = re.match(r"(\d{4})-\d{2}-\d{2}", fileName)
        # Match special sets
        if not match:
            match = re.match(r"(\d{2})", fileName)
        if match:
            collection = match.group(1)
            # To avoid S3-Directory-Listing limitation by putting JEM songs in several subdirs
            # https://github.com/flightlesstux/S3-Directory-Listing/issues/13
            if collection == "JEM":
                num = int(match.group(2))
                if num < 373:
                    collection = f"{collection}1"
                elif num < 722:
                    collection = f"{collection}2"
                elif num < 1000:
                    collection = f"{collection}3"
                else:
                    collection = f"{collection}4"
            subDirectory = collection

        filePath = os.path.join(filePath, subDirectory)
        try:
            os.makedirs(filePath)
        except (OSError, IOError) as error:
            if error.errno == errno.EEXIST:
                pass
            else:
                raise
        return os.path.join(filePath, fileName)

    def _isDate(self, path):
        fileName = fonc.get_file_name(path)
        listElem = [
            subsubsubElem
            for elem in fileName.split("-")
            for subElem in elem.split("_")
            for subsubElem in subElem.split(".")
            for subsubsubElem in subsubElem.split(" ")
        ]
        if all([elem.isdigit() for elem in listElem]):
            return True
        return False

    def makeSubDirOn(self):
        self._makeSubDir = True

    def makeSubDirOff(self):
        self._makeSubDir = False
