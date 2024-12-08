# -*- coding: utf-8 -*-

import os
import errno
import shutil
import codecs
import traceback
import random
import traceback
import logging

import tkinter as tk

try:
    from PyPDF2 import PdfReader

    HAVEPYPDF = True
except ImportError:
    logging.warning(traceback.format_exc())
    HAVEPYPDF = False


import songfinder
from songfinder import messages as tkMessageBox
from songfinder import messages as tkFileDialog  # pylint: disable=reimported
from songfinder import classPaths
from songfinder import fonctions as fonc
from songfinder import commandLine
from songfinder.elements import exports
from songfinder import exception
from songfinder import classSettings as settings
from songfinder.gui import guiHelper


class LatexParam(tk.Frame, object):
    def __init__(
        self,
        fenetre,
        chants_selection,
        papa,
        noCompile,
        screens=None,
        exportSettings=None,
        **kwargs,
    ):
        tk.Frame.__init__(self, fenetre, **kwargs)
        with guiHelper.SmoothWindowCreation(fenetre, screens=screens):
            self.grid()
            self.chants_selection = chants_selection
            self.papa = papa
            self.noCompile = noCompile

            if not exportSettings:
                self._exportSettings = settings.LATEXSETTINGS
            else:
                self._exportSettings = exportSettings

            self.deps = {
                "reorder": [("list", False)],
                "alphabetic_list": [("affiche_liste", True)],
                "one_song_per_page": [("list", False)],
                "transpose": [("chords", True)],
                "capo": [("chords", True)],
                "list": [("affiche_liste", True)],
                "sol_chords": [("chords", True)],
                "num_chords": [("chords", True)],
                "two_columns": [("affiche_liste", True)],
                "simple_chords": [("chords", True)],
                "keep_first": [("chords", True), ("keep_last", False)],
                "keep_last": [("chords", True), ("keep_first", False)],
                "auto_capo": [("chords", True), ("capo", True)],
                "diapo": [
                    ("reorder", False),
                    ("alphabetic_list", False),
                    ("one_song_per_page", False),
                    ("transpose", False),
                    ("list", False),
                    ("booklet", False),
                    ("two_columns", False),
                    ("capo", False),
                    ("simple_chords", False),
                    ("keep_first", False),
                    ("keep_last", False),
                    ("sol_chords", False),
                    ("num_chords", False),
                    ("affiche_liste", False),
                    ("chords", False),
                    ("keep_first", False),
                ],
            }

            self.dictParam = {
                "Reordonner les chants pour remplir les pages.": "reorder",
                "Sommaire alphabetique.": "alphabetic_list",
                "Afficher un chant par page.": "one_song_per_page",
                "Transposer les accords.": "transpose",
                "Afficher les accords.": "chords",
                "Afficher la tonalité.": "printkey",
                "Afficher le tempo.": "printtempo",
                "Liste des chants seule.": "list",
                "Accords en français.": "sol_chords",
                "Accords en degré": "num_chords",
                "Format carnet imprimable.": "booklet",
                "Refaire les sauts de lignes.": "saut_lignes",
                "Afficher le sommaire.": "affiche_liste",
                "Afficher le sommaire sur deux collones.": "two_columns",
                "Appliquer les capo.": "capo",
                "Simplifier les accords (retire sus4, Maj6 etc.).": "simple_chords",
                "Ne garder que le premier accord (Do/Mi -> Do).": "keep_first",
                "Ne garder que le second accord (Do/Mi -> Mi).": "keep_last",
                "Utiliser le capo pour avoir les accords en Do, Mi ou Sol": "auto_capo",
                "Diaporama.": "diapo",
                "Afficher la référence.": "printref",
            }
            self.dictValeurs = dict()
            self.dictButton = dict()
            self.pressed = None
            nb_boutton = len(self.dictParam)
            column_width = 5
            nb_row = (nb_boutton + 1) // 2
            for i, (param, item) in enumerate(self.dictParam.items()):
                var = tk.IntVar()
                button = tk.Checkbutton(
                    self,
                    text=param,
                    variable=var,  # ~ command=self.save)
                    command=lambda identifyer=item: self.save(identifyer),
                )
                self.dictValeurs[param] = var
                self.dictButton[item] = button
                # ~ self.liste_buttons.append(button)
                column_num = i // nb_row * (column_width + 1)
                button.grid(
                    row=i % nb_row,
                    column=column_num,
                    columnspan=column_width,
                    sticky="w",
                )

            self.bouton_ok = tk.Button(self, text="OK", command=self.createFiles)
            self.bouton_ok.grid(
                row=nb_row, column=0, columnspan=column_width // 2, sticky="w"
            )
            self.bouton_ok = tk.Button(self, text="Annuler", command=self.quit)
            self.bouton_ok.grid(
                row=nb_row,
                column=column_width // 2,
                columnspan=column_width // 2,
                sticky="w",
            )

            self.maj()

    def save(self, identifyer, event=0):  # pylint: disable=unused-argument
        self.pressed = identifyer
        for param, valeur in self.dictValeurs.items():
            self._exportSettings.set(
                "Export_Parameters", self.dictParam[param], bool(valeur.get())
            )
        if self._exportSettings.get("Export_Parameters", "booklet") and not HAVEPYPDF:
            self._exportSettings.set("Export_Parameters", "booklet", False)
            tkMessageBox.showinfo(
                "Info",
                "pypdf2 is not installed, this fonctionality is not available. "
                'Run "pip install pypdf2" to install it.',
            )

        self.maj()

    def maj(self):
        for param in self.dictParam.values():
            if self._exportSettings.get("Export_Parameters", param):
                self.dictButton[param].select()
            else:
                self.dictButton[param].deselect()

        if self.pressed:
            pressedValue = self._exportSettings.get("Export_Parameters", self.pressed)
            if pressedValue:
                if self.pressed in self.deps:
                    for condition in self.deps[self.pressed]:
                        self._exportSettings.set(
                            "Export_Parameters", condition[0], condition[1]
                        )
                        if condition[1]:
                            self.dictButton[condition[0]].select()
                        else:
                            self.dictButton[condition[0]].deselect()

            for param, conditions in self.deps.items():
                for condition in conditions:
                    if condition[0] == self.pressed:
                        if condition[1] != pressedValue:
                            self.dictButton[param].deselect()
                            self._exportSettings.set("Export_Parameters", param, False)

    def createFiles(self):
        self._exportSettings.write()
        pdfFile = CreatePDF(self.chants_selection, exportSettings=self._exportSettings)
        pdfFile.writeFiles()
        close = 0
        if self.noCompile == 0:
            try:
                close = pdfFile.compileLatex()
            except exception.CommandLineError:
                tkMessageBox.showerror("Erreur", traceback.format_exc(limit=1))
        if close == 0:
            self.quit()
        else:
            self.papa.liftLatexWindow()

    def quit(self):
        self.papa.closeLatexWindow()


class CreatePDF(object):
    def __init__(self, elements_selection, exportSettings=None):
        if not exportSettings:
            self._exportSettings = settings.LATEXSETTINGS
        else:
            self._exportSettings = exportSettings

        if self._exportSettings.get("Export_Parameters", "diapo"):
            self.__prefix = "genBeamer"
            ClassType = exports.ExportBeamer
            logging.debug("Creating beamer output")
        else:
            self.__prefix = "genCarnet"
            ClassType = exports.ExportLatex
            logging.debug("Creating regular latex output")

        self.__listLatex = []
        for element in elements_selection:
            newlatex = ClassType(element, exportSettings=self._exportSettings)
            if newlatex.exportText:
                self.__listLatex.append(newlatex)

        if self._exportSettings.get("Export_Parameters", "reorder"):
            self.__listLatex = reorderLatex(self.__listLatex)

        self.__pdflatex = commandLine.MyCommand("pdflatex")

        self.__chemin = os.path.join(songfinder.__settingsPath__, "latexTemplates")
        self.__songFolder = os.path.join(self.__chemin, "songs")
        self.__songList = os.path.join(self.__chemin, "listeChants.tex")
        self.__tableOfContent = os.path.join(self.__chemin, "sommaire.tex")
        self.__bookletizer = os.path.join(self.__chemin, "bookletizer.tex")
        self.__tmpName = os.path.join(self.__chemin, f"{self.__prefix}.pdf")
        logging.debug(f"Folder for latex file is '{self.__chemin}'")

        self.__checkFiles()

    def __getTableOfContent(self):
        text = ""
        if self._exportSettings.get("Export_Parameters", "affiche_liste"):
            # Liste sommaire
            dicoTitres = {
                latexElem.title: str(self.__listLatex.index(latexElem) + 1)
                for latexElem in self.__listLatex
            }
            # Alphabetic
            if self._exportSettings.get("Export_Parameters", "alphabetic_list"):
                listTitres = sorted(dicoTitres.keys())
            else:
                listTitres = [latexElem.title for latexElem in self.__listLatex]

            text = "\\section*{Le Turf Auto}\n\\label{sommaire}\n"
            for title in listTitres:
                elem = self.__listLatex[int(dicoTitres[title]) - 1]
                text = "%s\\contentsline{section}{%s \\dotfill}{%s}{section.%s}\n" % (
                    text,
                    elem.escape(title),
                    dicoTitres[title],
                    dicoTitres[title],
                )

            if self._exportSettings.get("Export_Parameters", "two_columns"):
                text = "\\begin{multicols}{2}\n%s\n\\end{multicols}" % text
        return text

    def __getSongList(self):
        text = "\\newcommand{\\songsPath}{%s}\n" % self.__songFolder.replace("\\", "/")
        if not self._exportSettings.get("Export_Parameters", "list"):
            for i, latexElem in enumerate(self.__listLatex):
                text = '%s\\input{\\songsPath/"%s"}\n' % (text, latexElem.nom)
                if (i + 1) % 99 == 0:
                    text = f"{text}\\clearpage\n"
        text = text.replace("#", "\\#")
        return text

    def __getBookletizer(self):
        # Get number of pages of original pdf file
        with open(self.__tmpName, "rb") as fileIn:
            numPage = len(PdfReader(fileIn).pages)
        numPage_rounded = ((numPage + 4 - 1) // 4) * 4
        logging.debug(
            f"Rounding number of PDF pages from {numPage} to {numPage_rounded}"
        )
        # Write bookletizer tex file
        text = """\\documentclass[a4paper]{article}
\\usepackage{pdfpages}
\\begin{document}
\\includepdf[pages=-, nup=1x2, signature*=%s, landscape,
angle=180, delta=0 1cm]{%s}
\\end{document}""" % (
            numPage_rounded,
            self.__tmpName.replace("\\", "/"),
        )
        return text

    def writeFiles(self):
        # List of song to import
        with codecs.open(self.__songList, "w", encoding="utf-8") as out:
            logging.debug(f"Writting latex song list in '{self.__songList}'")
            out.write(self.__getSongList())
        # Songs
        if not self._exportSettings.get("Export_Parameters", "list"):
            for latexElem in self.__listLatex:
                fileName = os.path.join(self.__songFolder, f"{latexElem.nom}.tex")
                with codecs.open(fileName, "w", encoding="utf-8") as out:
                    logging.debug(f"Writting latex song '{fileName}'")
                    out.write(latexElem.exportText)
        # Table of content
        with codecs.open(self.__tableOfContent, "w", encoding="utf-8") as out:
            logging.debug(
                f"Writting latex table of content in '{self.__tableOfContent}'"
            )
            out.write(self.__getTableOfContent())

    def __checkFiles(self):
        try:
            os.makedirs(self.__chemin)
        except (OSError, IOError) as error:
            if error.errno == errno.EEXIST:
                pass
            else:
                raise
        try:
            logging.debug(f"Creating directory '{self.__songFolder}'")
            os.makedirs(self.__songFolder)
        except (OSError, IOError) as error:
            if error.errno == errno.EEXIST:
                logging.log(5, traceback.format_exc())
                pass
            else:
                raise
        source = os.path.join(songfinder.__dataPath__, "latexTemplates")
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                sourceFile = os.path.join(source, item)
                currentFile = os.path.join(self.__chemin, item)
                if (
                    not os.path.isfile(currentFile)
                    or os.stat(sourceFile).st_mtime > os.stat(currentFile).st_mtime
                ):
                    shutil.copy(sourceFile, currentFile)

    def __getOutFile(self):
        defaultName = "turfAuto"
        defaultPath = classPaths.PATHS.pdf
        if not self._exportSettings.get(
            "Export_Parameters", "reorder"
        ) and not self._exportSettings.get("Export_Parameters", "alphabetic_list"):
            defaultName = fonc.cree_nom_sortie()
        self.pdfName = tkFileDialog.asksaveasfilename(
            initialdir=defaultPath,
            initialfile=defaultName,
            defaultextension=".pdf",
            filetypes=(("pdf file", "*.pdf"), ("All Files", "*.*")),
        )

    def compileLatex(self):
        self.__getOutFile()
        if not self.pdfName:
            return 1
        fileToCompile = os.path.join(self.__chemin, f"{self.__prefix}.tex")
        # Compile
        self.__pdflatex.checkCommand()
        os.chdir(self.__chemin)
        code, out, err = self.__pdflatex.run(
            options=["-interaction=nonstopmode", fileToCompile]
        )
        if code == 0:
            code, out, err = self.__pdflatex.run(
                options=["-interaction=nonstopmode", fileToCompile]
            )
        os.chdir(songfinder.__chemin_root__)
        if code != 0:
            tkMessageBox.showerror(
                "Attention",
                f"Error while compiling latex files.\n Error {str(code)}:\n{err}",
            )
            return 1

        if not self.__isOutput():
            return 1

        # Compile booklet
        if self._exportSettings.get("Export_Parameters", "booklet"):
            # Write bookletizer file
            with codecs.open(self.__bookletizer, "w", encoding="utf-8") as out:
                logging.debug(f"Writting bookletizer file in '{self.__bookletizer}'")
                out.write(self.__getBookletizer())
            os.chdir(self.__chemin)
            code, out, err = self.__pdflatex.run(
                options=["-interaction=nonstopmode", self.__bookletizer]
            )
            os.chdir(songfinder.__chemin_root__)
            if code != 0:
                tkMessageBox.showerror(
                    "Attention",
                    f"Error while compiling latex files.\n Error {str(code)}:\n{err}",
                )
            else:
                self.__tmpName = os.path.join(self.__chemin, "bookletizer.pdf")

        if not self.__isOutput():
            return 1

        # Move file to specified directory
        shutil.move(self.__tmpName, self.pdfName)
        logging.info("Succes creating pdf file")
        self.__cleanDir()
        self.__openFile()
        return 0

    def __isOutput(self):
        if not os.path.isfile(self.__tmpName):
            tkMessageBox.showerror(
                "Attention",
                "Error while "
                "generating latex files. Output file %s does not exist"
                % (self.__tmpName),
            )
            return False
        return True

    def __openFile(self):
        if os.path.isfile(self.pdfName):
            if tkMessageBox.askyesno(
                "Confirmation",
                f'Le fichier "{self.pdfName}" à été créé.\nVoulez-vous l\'ouvrire ?',
            ):
                commandLine.run_file(self.pdfName)

    def __cleanDir(self):
        logging.debug(f"Cleaning latex compilation file in '{self.__chemin}'")
        listExt = [
            ".aux",
            ".idx",
            ".ilg",
            ".ind",
            ".log",
            ".out",
            ".toc",
            ".pdf",
            ".synctex.gz",
        ]
        for root, _, files in os.walk(self.__chemin):
            for fichier in files:
                fullName = os.path.join(root, fichier)
                if fonc.get_ext(fullName) in listExt:
                    os.remove(fullName)


def reorderLatex(listLatex):
    # Suprimme les doublons, change le nombre de ligne des chant qui ont le meme
    dictNbLigne = dict()
    for i, elem in enumerate(listLatex):
        nbLigne = elem.nbLine
        if nbLigne in dictNbLigne:
            texte1 = elem.text
            texte2 = listLatex[dictNbLigne[nbLigne]].text
            if texte1 != texte2:
                dictNbLigne[nbLigne - random.randint(1, 10**7) * 10 ** (-7)] = i
        else:
            dictNbLigne[nbLigne] = i
    # change les titles identiques
    titles = []
    for elem in listLatex:
        title = elem.title
        if title in titles:
            logging.warning(f'Two elements have the same title "{title}"')
            title = f"{title}~"
            elem.title = title
        titles.append(title)
    sortedKeys = sorted(dictNbLigne.keys(), reverse=True)
    maxLine = 40
    suptitle = 4
    newKey = []
    nb = len(sortedKeys)
    inList = []
    for i, key in enumerate(sortedKeys):
        if key > maxLine:
            logging.warning(
                'Song "%s" is to big to fit one page, size: %d, max size: %d'
                % (listLatex[dictNbLigne[key]].title, key, maxLine)
            )
        if i not in inList:
            newKey.append(key)
            inList.append(i)
            addSong(inList, newKey, sortedKeys, maxLine, suptitle, nb, key, i)

    newListe = [listLatex[i] for i in [dictNbLigne[key] for key in newKey]]
    return newListe


def addSong(inList, newKey, sortedKeys, maxLine, suptitle, nb, nbLine, i):
    # Add song to list accrding to size of song
    previous = -1
    maxLine = maxLine - suptitle
    for j, key in enumerate(reversed(sortedKeys)):
        if nbLine + key > maxLine or i == nb - j - 1:
            if previous != -1:
                if nb - j not in inList:
                    newKey.append(previous)
                    inList.append(nb - j)
                    newNbLine = nbLine + previous
                else:
                    newNbLine = nbLine
                    maxLine = maxLine + suptitle
                addSong(
                    inList, newKey, sortedKeys, maxLine, suptitle, nb, newNbLine, nb - j
                )
            break
        previous = key
