# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk


import os
import sys
import traceback
import logging

import songfinder
from songfinder import messages as tkMessageBox
from songfinder import versionning as version
from songfinder import latex
from songfinder import elements
from songfinder import fonctions as fonc
from songfinder import commandLine
from songfinder import classPaths
from songfinder import exception
from songfinder import dataBase
from songfinder import background
from songfinder.gui import preferences as pref
from songfinder.gui import simpleProgress
from songfinder.gui import searchGui
from songfinder.gui import editGui
from songfinder.gui import selectionListGui
from songfinder.gui import presentGui
from songfinder.gui import diapoListGui
from songfinder import diapoList
from songfinder import classSettings as settings
from songfinder.gui import guiHelper
from songfinder import diapoPreview
from songfinder import __version__


class Interface(tk.Frame, object):
    def __init__(self, fenetre, screens=None, fileIn=None, **kwargs):
        tk.Frame.__init__(self, fenetre, **kwargs)

        self._screens = screens
        self._fenetre = fenetre

        if screens[0].width < 1000:
            fontSize = 8
        elif screens[0].width < 2000:
            fontSize = 9
        else:
            fontSize = 10

        logging.debug(f"FontSize {fontSize}")

        for font in ["TkDefaultFont", "TkTextFont", "TkFixedFont", "TkMenuFont"]:
            tkFont.nametofont(font).configure(size=fontSize)

        mainmenu = tk.Menu(fenetre)  ## Barre de menu
        menuFichier = tk.Menu(mainmenu)  ## tk.Menu fils menuExample
        menuFichier.add_command(
            label="Mettre à jour la base de données", command=self.updateData
        )
        menuFichier.add_command(
            label="Utiliser les bases de données additionelles",
            command=self._addRemoveDataBases,
        )
        menuFichier.add_command(
            label="Mettre à jour SongFinder", command=self._updateSongFinder
        )
        menuFichier.add_command(label="Quitter", command=self.quit)
        mainmenu.add_cascade(label="Fichier", menu=menuFichier)

        menuEditer = tk.Menu(mainmenu)
        menuEditer.add_command(label="Paramètres généraux", command=self._paramGen)
        menuEditer.add_command(
            label="Paramètres de présentation", command=self._paramPres
        )
        mainmenu.add_cascade(label="Paramètres", menu=menuEditer)

        menuSync = tk.Menu(mainmenu)
        menuSync.add_command(label="Envoyer les chants", command=self._sendSongs)
        menuSync.add_command(label="Recevoir les chants", command=self._receiveSongs)
        mainmenu.add_cascade(label="Réception/Envoi", menu=menuSync)

        menuLatex = tk.Menu(mainmenu)
        menuLatex.add_command(label="Générer un fichier PDF", command=self._quickPDF)
        menuLatex.add_command(
            label="Générer les fichiers Latex",
            command=lambda noCompile=1: self._writeLatex(noCompile),
        )
        menuLatex.add_command(
            label="Compiler les fichiers Latex", command=self._compileLatex
        )
        mainmenu.add_cascade(label="PDF", menu=menuLatex)

        menuHelp = tk.Menu(mainmenu)
        menuHelp.add_command(label="Version", command=self._showVersion)
        menuHelp.add_command(label="README", command=self._showREADME)
        menuHelp.add_command(label="Documentation", command=self._showDoc)
        mainmenu.add_cascade(label="Aide", menu=menuHelp)

        fenetre.config(menu=mainmenu)

        self._generalParamWindow = None
        self._presentationParamWindow = None
        self._latexWindow = None
        self._scrollWidget = None

        self._dataBaseAreMerged = False

        leftPanel = ttk.Frame(fenetre)
        searchPanel = ttk.Frame(leftPanel)
        listPanel = ttk.Frame(leftPanel)
        editPanel = ttk.Frame(fenetre)
        rightPanel = ttk.Frame(fenetre)
        expandPanel = ttk.Frame(fenetre)
        presentPanel = ttk.Frame(leftPanel)
        presentedListPanel = ttk.Frame(fenetre)
        previewPanel = ttk.Frame(presentedListPanel)
        listGuiPanel = ttk.Frame(presentedListPanel)

        searchPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        listPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        leftPanel.pack(side=tk.LEFT, fill=tk.BOTH)
        editPanel.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        rightPanel.pack(side=tk.LEFT, fill=tk.X)
        expandPanel.pack(side=tk.LEFT, fill=tk.X)
        presentPanel.pack(side=tk.TOP, fill=tk.X)
        previewPanel.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        listGuiPanel.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        #######

        ####### Path definition
        classPaths.PATHS.update()
        try:
            scm = settings.GENSETTINGS.get("Parameters", "scm")
            self._repo = version.Repo(classPaths.PATHS.root, scm, self, screens=screens)
        except exception.CommandLineError:
            logging.error(traceback.format_exc())
            tkMessageBox.showerror("Erreur", traceback.format_exc(limit=1))
        self._dataBase = dataBase.DataBase()

        self._diapoList = diapoList.DiapoList()

        # Modular panels
        self._editGui = editGui.EditGui(
            editPanel,
            dataBase=self._dataBase,
            screens=screens,
            diapoList=self._diapoList,
        )
        self._selectionListGui = selectionListGui.SelectionListGui(
            listPanel, diapoList=self._diapoList
        )
        self._searchGui = searchGui.SearchGui(
            searchPanel, self._dataBase, screens=screens, diapoList=self._diapoList
        )
        self._presentGui = presentGui.PresentGui(
            presentPanel, self._diapoList, screens=screens
        )
        self._diapoListGui = diapoListGui.DiapoListGui(listGuiPanel, self._diapoList)
        self._previews = diapoPreview.Preview(
            previewPanel, self._diapoList, screens=screens
        )
        #######

        # Modular panels bindings
        self._editGui.bindSaveCallback(self._resetTextAndCache)
        self._editGui.bindSetSong(self._searchGui.setSong)
        self._selectionListGui.bindPrinter(self._editGui.printer)
        self._selectionListGui.bindSearcher(self._searchGui.searcher.search)
        self._searchGui.bindPrinter(self._editGui.printer)
        self._searchGui.bindAddElementToSelection(
            self._selectionListGui.addElementToSelection
        )
        self._presentGui.bindElementToPresent(self._editGui.printedElement)
        self._presentGui.bindListToPresent(self._selectionListGui.list)
        self._presentGui.bindRatioCallback(self._previews.updatePreviews)

        self._diapoListGui.bindCallback(self._previews.printer, "self._previews")
        self._diapoList.bindloadCallback(self._diapoListGui.write)
        self._diapoList.bindloadCallback(self._previews.printer)
        self._diapoList.bindIsLoadAlowed(self._presentGui.presentIsOff)
        self._diapoList.bindFrameEvent(fenetre)
        self._diapoList.bindGuiUpdate(self._previews.printer)
        self._diapoList.bindGuiUpdate(self._diapoListGui.updateSelected)
        #######

        # List present panel
        #######
        self._expandInLook = "<\n" * 15
        self._expandOutLook = ">\n" * 15
        previewExpanded = False
        editExpanded = False
        expandGuiButton = tk.Button(
            expandPanel,
            text=self._expandOutLook,
            command=lambda name="preview": self._expandGui(name),
        )
        expandEditButton = tk.Button(
            expandPanel,
            text=self._expandOutLook,
            command=lambda name="edit": self._expandGui(name),
        )

        expandGuiButton.pack(side=tk.TOP, fill=tk.X)
        # expandEditButton.pack(side=tk.TOP, fill=tk.X)

        self._expandables = {
            "preview": {
                "isExpanded": previewExpanded,
                "panel": presentedListPanel,
                "button": expandGuiButton,
            },
            "edit": {
                "isExpanded": editExpanded,
                "panel": editPanel,
                "button": expandEditButton,
            },
        }

        self.bind_all("<Enter>", self._bound_to_mousewheel)
        self.bind_all("<Leave>", self._unbound_to_mousewheel)

        # ~ backColor = '#F0F0F0'
        # ~ self.configure(background=backColor)
        # ~ for item in fonc.all_children(self):
        # ~ if item.winfo_class() == 'Label' or item.winfo_class() == 'Radiobutton':
        # ~ item['bg'] = backColor
        # ~ elif item.winfo_class() == 'Text' or item.winfo_class() == 'Entry':
        # ~ item['bg'] = 'white'
        # ~ elif item.winfo_class() == 'tk.Button' or item.winfo_class() == 'tk.Menu':
        # ~ item['bg'] = '#FFFBF5'

        # Open file in argument
        if fileIn:
            fileIn = os.path.abspath(fileIn)
            ext = fonc.get_ext(fileIn)
            if ext in settings.GENSETTINGS.get("Extentions", "song"):
                element = elements.Chant(fileIn)
                if element.exist():
                    self._searchGui.setSong(element)
                    self._editGui.printer(toPrintDict={element: 100})
            elif ext in settings.GENSETTINGS.get("Extentions", "liste"):
                self._selectionListGui.setList(fileIn)

        if settings.GENSETTINGS.get("Parameters", "autoexpand"):
            self._expandGui("preview", resize=False)
            self._diapoListGui.write()

        if settings.GENSETTINGS.get("Parameters", "autoreceive"):
            self._receiveSongs(showGui=False)

    def _addRemoveDataBases(self):
        if self._dataBaseAreMerged:
            self._dataBase.removeExtraDatabases()
            self._dataBaseAreMerged = False
            self.updateData()
        else:
            jemafPath = settings.GENSETTINGS.get("Paths", "jemaf")
            shirPath = settings.GENSETTINGS.get("Paths", "shir")
            topChretiensPath = settings.GENSETTINGS.get("Paths", "topchretiens")
            logging.info(f'Adding "{jemafPath}" to database.')
            logging.info(f'Adding "{shirPath}" to database.')
            logging.info(f'Adding "{topChretiensPath}" to database.')
            jemafDataBase = dataBase.DataBase(jemafPath)
            shirDataBase = dataBase.DataBase(shirPath)
            topChretiensDataBase = dataBase.DataBase(topChretiensPath)
            self._dataBase.merge([jemafDataBase, shirDataBase, topChretiensDataBase])
            self._dataBaseAreMerged = True

    def __syncPath__(self):
        # Workaround should reorganize path class
        classPaths.PATHS.sync(self._screens, self.updateData)

    def _expandGui(self, name, resize=True):
        if self._expandables[name]["isExpanded"]:
            self._expandables[name]["panel"].pack_forget()
            self._expandables[name]["button"]["text"] = self._expandOutLook
            self._expandables[name]["isExpanded"] = False
        else:
            self._expandables[name]["panel"].pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
            self._expandables[name]["button"]["text"] = self._expandInLook
            self._expandables[name]["isExpanded"] = True
            self._previews.updatePreviews(delay=False)
        if resize:
            self._resizeMainWindow()

    def _resizeMainWindow(self):
        self._fenetre.update()
        width = max(self._fenetre.winfo_width(), self._fenetre.winfo_reqwidth())
        height = max(self._fenetre.winfo_height(), self._fenetre.winfo_reqheight())
        self._screens.resizeFrame(self._fenetre, width, height)

    def closeLatexWindow(self):
        if self._latexWindow:
            self._latexWindow.destroy()
            self._latexWindow = None

    def liftLatexWindow(self):
        guiHelper.upFront(self._latexWindow)

    def _resetTextAndCache(self):
        if self._searchGui:
            self._searchGui.resetCache()
            self._searchGui.resetText()
        if self._selectionListGui:
            self._selectionListGui.resetText()
        if self._diapoList is not None:
            self._diapoList.resetText()
        self._diapoListGui.write()
        self._previews.printer()

    def _bound_to_mousewheel(self, event):
        self._scrollWidget = event.widget
        self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):  # pylint: disable=unused-argument
        self._scrollWidget = None
        self.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        try:
            self._scrollWidget.focus_set()
            self._scrollWidget.yview_scroll(-1 * (event.delta // 8), "units")
        except AttributeError:
            pass

    def updateData(self, showGui=True):
        if showGui:
            progressBar = simpleProgress.SimpleProgress(
                "Mise à jour de la base de données", screens=self._screens
            )
            total = len(self._dataBase) if self._dataBase else 1000
            progressBar.start(total=total)
            self._dataBase.update(callback=progressBar.update)
        else:
            self._dataBase.update()
        self._selectionListGui.getSetList()
        self._searchGui.resetText()
        self._selectionListGui.resetText()
        self._searchGui.resetCache()
        self._editGui.resetText()
        self._editGui.printer()
        if showGui:
            progressBar.stop()
            tkMessageBox.showinfo(
                "Confirmation",
                f"La base de donnée a été mise à jour: {len(self._dataBase)} chants.",
            )

    def quit(self):
        try:
            settings.GENSETTINGS.write()
            settings.PRESSETTINGS.write()
            settings.LATEXSETTINGS.write()
        except Exception:  # pylint: disable=broad-except
            logging.error(traceback.format_exc())
            tkMessageBox.showerror(
                "Attention",
                f"Error while writting settings:\n{traceback.format_exc(limit=1)}",
            )
        try:
            background.cleanDiskCacheImage()
        except Exception:  # pylint: disable=broad-except
            logging.error(traceback.format_exc())
            tkMessageBox.showerror(
                "Attention", f"Error in clean cache:\n{traceback.format_exc(limit=1)}"
            )
        self.destroy()
        sys.exit()

    def _paramGen(self):
        if self._generalParamWindow:
            self._generalParamWindow.close()
            self._generalParamWindow = None
        self._generalParamWindow = pref.ParamGen(self, screens=self._screens)

    def _paramPres(self):
        if self._presentationParamWindow:
            self._presentationParamWindow.close()
            self._presentationParamWindow = None
        self._presentationParamWindow = pref.ParamPres(self, screens=self._screens)
        self._searchGui.resetDiapos()
        self._selectionListGui.resetDiapos()

    def _writeLatex(self, noCompile=0):
        chants_selection = self._selectionListGui.list()
        if chants_selection == []:
            tkMessageBox.showerror("Erreur", "Il n'y a aucun chants dans la liste.")
        elif len(set(chants_selection)) != len(chants_selection):
            tkMessageBox.showerror(
                "Erreur",
                "Certains chants apparaissent plusieurs fois dans la liste. Ceci est proscrit",
            )
        else:
            if self._latexWindow:
                self._latexWindow.destroy()
                self._latexWindow = None
            self._latexWindow = tk.Toplevel()
            self._latexWindow.title("Paramètres Export PDF")
            self.LatexParam = latex.LatexParam(
                self._latexWindow,
                chants_selection,
                self,
                noCompile,
                screens=self._screens,
            )

    def _compileLatex(self):
        latexCompiler = latex.CreatePDF([])
        latexCompiler.compileLatex()

    def _quickPDF(self):
        self._writeLatex()

    def _showDoc(self):
        docPath = os.path.join(songfinder.__dataPath__, "documentation")
        docFile = os.path.join(docPath, f"{songfinder.__appName__}.pdf")
        if not os.path.isfile(docFile):
            fileToCompile = os.path.join(docPath, f"{songfinder.__appName__}.tex")
            if os.path.isfile(fileToCompile):
                os.chdir(docPath)
                pdflatex = commandLine.MyCommand("pdflatex")
                pdflatex.checkCommand()
                code, _, err = pdflatex.run(
                    options=[fonc.get_file_name_ext(fileToCompile)], timeOut=10
                )
                if code == 0:
                    code, _, err = pdflatex.run(
                        options=[fonc.get_file_name_ext(fileToCompile)], timeOut=10
                    )
                os.chdir(songfinder.__chemin_root__)
                if code != 0:
                    tkMessageBox.showerror(
                        "Attention",
                        f"Error while compiling latex files. Error {str(code)}:\n{err}",
                    )
        if os.path.isfile(docFile):
            commandLine.run_file(docFile)
        else:
            tkMessageBox.showerror(
                "Attention",
                "Impossible d'ouvrire "
                'la documentation, le fichier "%s" n\'existe pas.' % docFile,
            )

    def _showREADME(self):
        fileName = "README.md"
        pathsReadme = [
            os.path.join(songfinder.__dataPath__, "documentation", fileName),
            os.path.join(fileName),
        ]
        found = False
        for readmeFile in pathsReadme:
            if os.path.isfile(readmeFile):
                commandLine.run_file(readmeFile)
                found = True
                break
        if not found:
            tkMessageBox.showerror(
                "Attention",
                "Impossible d'ouvrire "
                'le fichier README, le fichier "%s" n\'existe pas.'
                % ", ".join(pathsReadme),
            )

    def _showVersion(self):
        tkMessageBox.showinfo(
            f"Songfinder Version {__version__}",
            f"Songfinder Version {__version__}.",
        )

    def _sendSongs(self, showGui=True):
        if self._repo.send(showGui=showGui) == 0:
            self.updateData(showGui=showGui)

    def _receiveSongs(self, showGui=True):
        if self._repo.receive(showGui=showGui) == 0:
            self.updateData(showGui=showGui)

    def _updateSongFinder(self):
        pip = commandLine.MyCommand(sys.executable)
        try:
            pip.checkCommand()
        except exception.CommandLineError:
            logging.error(traceback.format_exc())
            tkMessageBox.showerror("Erreur", traceback.format_exc(limit=1))
        else:
            job = simpleProgress.UpdateJob(
                function=pip.run,
                options=[
                    "-m",
                    "pip",
                    "install",
                    f"{songfinder.__appName__}[gui]",
                    "--upgrade",
                ],
                timeOut=120,
            )
            progressBar = simpleProgress.Progress(
                "Mise à jour de SongFinder", job, screens=self._screens
            )
            progressBar.start()
