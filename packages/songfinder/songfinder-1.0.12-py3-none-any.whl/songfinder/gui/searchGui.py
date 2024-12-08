# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk

import os
import time
import logging

import songfinder
from songfinder import messages as tkMessageBox
from songfinder import fonctions as fonc
from songfinder.gui import inputFrame
from songfinder import search


class SearchGui(object):
    def __init__(
        self,
        frame,
        dataBase=None,
        screens=None,
        addElementToSelection=None,
        printer=None,
        diapoList=None,
    ):
        # TODO remove _database reference if possible

        self._frame = frame
        self._printer = printer
        self._songFound = []

        self.useDataBase(dataBase)

        self._diapoList = diapoList

        self._addElementToSelection = addElementToSelection

        self._priorityMultiplicator = 1

        if screens and screens[0].width > 2000:
            width = 65
        else:
            width = 55

        self._inputSearch = inputFrame.entryField(
            frame, width=width, text="Recherche: "
        )

        typeSearchSubPanel = ttk.Frame(frame)
        searchResultPanel = ttk.Frame(frame)

        self._varSearcher = tk.IntVar()
        lyricsSearcherButton = tk.Radiobutton(
            typeSearchSubPanel,
            text="Paroles",
            variable=self._varSearcher,
            value=0,
            command=lambda str_id="lyrics": self._changeSearcher(str_id),
        )
        titleSearcherButton = tk.Radiobutton(
            typeSearchSubPanel,
            text="Titres",
            variable=self._varSearcher,
            value=1,
            command=lambda str_id="titles": self._changeSearcher(str_id),
        )
        tagsSearcherButton = tk.Radiobutton(
            typeSearchSubPanel,
            text="Tags",
            variable=self._varSearcher,
            value=2,
            command=lambda str_id="tags": self._changeSearcher(str_id),
        )

        self._allSearcher_buttons = [
            lyricsSearcherButton,
            titleSearcherButton,
            tagsSearcherButton,
        ]

        tagLabel = tk.Label(typeSearchSubPanel, text="Tags :")
        tagSelectionVar = tk.StringVar()
        # TODO update tag list when database is updated
        self._tagSelection = ttk.Combobox(
            typeSearchSubPanel,
            textvariable=tagSelectionVar,
            values=self._dataBase.tags,
            state="readonly",
            width=30,
        )

        explainLabel = tk.Label(
            frame,
            text="Chants trouvés: \n"
            "Utilisez leur numéro dans la liste pour les selectionner",
        )
        self._searchResults = tk.Listbox(searchResultPanel, width=width, height=9)
        searchResultsScroll = tk.Scrollbar(
            searchResultPanel, command=self._searchResults.yview
        )
        self._searchResults["yscrollcommand"] = searchResultsScroll.set

        self._upButton = tk.Button(
            frame,
            text="Ajouter chant",
            command=lambda event=None, mouseClic=1: self._select(event, mouseClic),
        )

        self._inputSearch.pack(side=tk.TOP, fill=tk.X)
        typeSearchSubPanel.pack(side=tk.TOP, fill=tk.X)
        for searcher_buttons in self._allSearcher_buttons:
            searcher_buttons.pack(side=tk.LEFT, fill=tk.X)
        self._tagSelection.pack(side=tk.RIGHT, fill=tk.X)
        tagLabel.pack(side=tk.RIGHT, fill=tk.X)

        explainLabel.pack(side=tk.TOP, fill=tk.X)

        searchResultPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self._searchResults.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        searchResultsScroll.pack(side=tk.LEFT, fill=tk.Y)

        self._upButton.pack(side=tk.TOP, fill=tk.X)
        self._searchResults.bind("<ButtonRelease-1>", self._printerWrapper)
        self._searchResults.bind(
            "<Double-Button-1>",
            lambda event, mouseClic=1: self._select(event, mouseClic),
        )

        self._searchResults.bind("<KeyRelease-Up>", self._printerWrapper)
        self._searchResults.bind("<KeyRelease-Down>", self._printerWrapper)
        self._searchResults.bind("<Delete>", self._deleteSong)

        self._inputSearch.bind("<Key>", self._search)
        self._inputSearch.bind("<KeyRelease-BackSpace>", self._nothing)
        self._inputSearch.bind("<KeyRelease-Left>", self._nothing)
        self._inputSearch.bind("<KeyRelease-Right>", self._nothing)
        self._inputSearch.bind("<KeyRelease-Up>", self._nothing)
        self._inputSearch.bind("<KeyRelease-Down>", self._nothing)

        self._tagSelection.bind("<<ComboboxSelected>>", self._selectTag)
        self._tagSelection.bind("<FocusIn>", self._update_tags)

        self._inputSearch.focus_set()

        self._delayId = None
        self._passed = 0
        self._total = 0
        self._delayAmount = 0
        self._callbackDelay = 0
        self._lastCallback = 0

        self._search()

        self._printMod = 10
        self._printCounter = 0

    def _selectTag(self, event):
        self._changeSearcher("tags")
        self._varSearcher.set(2)
        tag = self._tagSelection.get()
        self._inputSearch.delete(0, tk.END)  # pylint: disable=no-member
        self._inputSearch.insert(0, tag)  # pylint: disable=no-member
        self._search()

    def _update_tags(self, event=None):
        self._tagSelection["values"] = self._dataBase.tags

    @property
    def searcher(self):
        return self._searcher

    def _changeSearcher(self, new_mode):
        if new_mode != self._searcher.mode:
            logging.info(
                f'Changing searcher from "{self._searcher.mode}" to "{new_mode}"'
            )
            self._searcher.mode = new_mode
            self._search()

    def _printerWrapper(self, event=None):
        outDictElements = {}
        if self._searchResults.curselection() and self._songFound:
            select = self._searchResults.curselection()[0]
            toAdd = self._songFound[select]
            outDictElements[toAdd] = 18 * self._priorityMultiplicator
        if self._searchResults.size() > 0 and self._songFound:  # ValueError None
            toAdd = self._songFound[0]
            outDictElements[toAdd] = 6 * self._priorityMultiplicator

        if self._printer:
            time.sleep(
                0.1
            )  # TTODO, this is a hack for linux/mac, it enable double clic binding
            self._printer(event=event, toPrintDict=outDictElements, loadDiapo=True)
        elif self._diapoList is not None and hasattr(self._diapoList, "load"):
            self._diapoList.load([toAdd], wantedDiapoNumber=1)

    def _search(self, event=None):
        currentTime = time.time()
        self._callbackDelay = int(round((currentTime - self._lastCallback) * 1000))
        self._lastCallback = currentTime
        self._priorityMultiplicator = 10
        self._total += 1
        if self._delayId:
            self._frame.after_cancel(self._delayId)
        self._delayId = self._frame.after(self._delayAmount, self._searchCore, event)
        self._priorityMultiplicator = 1

    def _searchCore(self, event):
        startTime = time.time()
        self._passed += 1
        if self._searcher:
            if self._inputSearch.get():  # pylint: disable=no-member
                searchInput = fonc.safeUnicode(
                    self._inputSearch.get()  # pylint: disable=no-member
                )
                self._songFound = self._searcher.search(searchInput)
            else:
                self._songFound = list(self._dataBase.keys())
            self._showResults()
            self._select(event)
            self._printerWrapper(event)
        else:
            logging.warning("No searcher have been defined for searchGui")

        # Compute printer delay to lower pression on slow computers
        printerTime = int(round((time.time() - startTime) * 1000))
        if printerTime > self._callbackDelay:
            self._delayAmount = min(printerTime, 2)
        else:
            self._delayAmount = 0

    def _showResults(self):
        self._searchResults.delete(0, "end")
        for i, song in enumerate(self._songFound):
            self._searchResults.insert(i, (f"{i + 1} -- {song}"))
        if self._printCounter % self._printMod == 0:
            logging.debug(f"Printing {len(self._songFound)} search results")
        self._printCounter += 1

    def _select(self, event, mouseClic=0):
        if self._addElementToSelection:
            keyboardInput = ""
            if event:
                # For ubuntu num lock wierd behaviour
                toucheNumPad = event.keycode
                if songfinder.__myOs__ in ["ubuntu", "darwin"]:
                    listNumPad = [87, 88, 89, 83, 84, 85, 79, 80, 81]
                else:
                    listNumPad = []
                if not self._inputSearch.get().isdigit():  # pylint: disable=no-member
                    if toucheNumPad in listNumPad:
                        keyboardInput = str(listNumPad.index(toucheNumPad) + 1)
                    else:
                        keyboardInput = event.keysym
            if mouseClic == 1:
                if self._searchResults.curselection():
                    keyboardInput = str(int(self._searchResults.curselection()[0]) + 1)
                    if int(keyboardInput) >= self._searchResults.size() + 1:
                        logging.warning(
                            'The input element number "%s" is invalid, '
                            "can not figure out what element to add."
                            'Maximum entry is "%s"'
                            % (keyboardInput, self._searchResults.size() + 1)
                        )
                else:
                    logging.warning(
                        "The result list was not selected, "
                        "can not figure out what element to add."
                    )

            if keyboardInput.isdigit():
                if int(keyboardInput) < self._searchResults.size() + 1:
                    element = self._songFound[int(keyboardInput) - 1]
                    self._addElementToSelection(element)
                    self._inputSearch.delete(0, tk.END)  # pylint: disable=no-member
                    self._inputSearch.focus_set()
                else:
                    logging.warning(
                        'Got an invalid number from event "%s", '
                        "can not figure out what element to add." % keyboardInput
                    )

    def _deleteSong(self, event):  # pylint: disable=unused-argument
        if self._dataBase and self._searchResults.curselection():
            select = self._searchResults.curselection()[0]
            toDelete = self._songFound[select]
            if tkMessageBox.askyesno(
                "Confirmation",
                f'Etes-vous sur de supprimer le chant:\n"{toDelete.nom}" ?',
            ):
                path = toDelete.chemin
                if os.path.isfile(path):
                    os.remove(path)
                self._dataBase.remove(toDelete)
                self.resetCache()
                if toDelete in self._songFound:
                    self._songFound.remove(toDelete)
                try:
                    logging.info(f'Deleted "{toDelete.chemin}"')
                except UnicodeEncodeError:
                    logging.info(f'Deleted "{repr(toDelete.chemin)}"')
                self._showResults()
                self._printerWrapper()

    def _nothing(self, event=0):
        pass

    def setSong(self, song):
        self._songFound = [song]
        self._showResults()

    def resetCache(self):
        self._searcher.resetCache()

    def resetText(self):
        for song in self._songFound:
            song.reset()

    def resetDiapos(self):
        for element in self._songFound:
            element.resetDiapos()

    def bindAddElementToSelection(self, function):
        self._addElementToSelection = function

    def bindPrinter(self, function):
        self._printer = function

    def useDataBase(self, dataBase):
        self._dataBase = dataBase
        self._searcher = search.SearcherWrapper(self._dataBase)
