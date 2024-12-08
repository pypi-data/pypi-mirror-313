# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk

from songfinder import messages as tkMessageBox

from songfinder.gui import screen
from songfinder import background
from songfinder.gui import fullScreenPresent
from songfinder import classSettings as settings


class PresentGui(object):
    def __init__(
        self,
        frame,
        diapoList,
        screens=None,
        elementToPresent=None,
        listToPresent=None,
        callback=None,
    ):
        self._frame = frame
        self._elementToPresent = elementToPresent
        self._listToPresent = listToPresent
        self._callback = callback
        self._screens = screens
        self._diapoList = diapoList
        self._forceListUpdate = False
        self._activateButton = None
        self._updateListButton = None
        self._ratioLabel = None
        self._ratioSelect = None
        self._presentation = fullScreenPresent.Presentation(
            self._frame, self._diapoList, screens=self._screens
        )
        self._presentation.bindCloseCallback(self._updateButtons)
        self._packWidgets()
        frame.bind_all("<F5>", self._activatePresent)

        self._diapoList.bindGuiUpdate(self._presentation.printer)

    def _packWidgets(self):
        for widget in [
            self._activateButton,
            self._updateListButton,
            self._ratioLabel,
            self._ratioSelect,
        ]:
            try:
                widget.pack_forget()
            except AttributeError:
                pass
        self._activateButton = tk.Button(self._frame, command=self._activatePresent)
        self._updateListButton = tk.Button(
            self._frame, text="Mettre à jour la liste", command=self._updateList
        )
        self._activateButton.pack(side=tk.TOP, fill=tk.X)
        if len(self._screens) > 1:
            self._updateListButton.pack(side=tk.TOP, fill=tk.X)

        self._ratioLabel = tk.Label(self._frame, text="Format de l'écran :")
        ratioList = settings.GENSETTINGS.get("Parameters", "ratio_avail")
        self._ratioSelect = ttk.Combobox(
            self._frame, values=ratioList, state="readonly", width=20
        )
        self._ratioSelect.bind("<<ComboboxSelected>>", self._setRatio)
        self._ratioSelect.set(settings.GENSETTINGS.get("Parameters", "ratio"))
        self._ratioLabel.pack(side=tk.TOP)
        self._ratioSelect.pack(side=tk.TOP)
        self._updateButtons()

    def _setRatio(self, event=0):  # pylint: disable=unused-argument
        ratio = self._ratioSelect.get()
        settings.GENSETTINGS.set("Parameters", "ratio", ratio)
        self._ratio = screen.getRatio(ratio)
        if self._callback:
            self._callback()

    def _updateList(self):
        if self._presentation.isHided():
            self._activatePresent()
        else:
            if self._listToPresent:
                self._forceListUpdate = True
                self._diapoList.load(self._listToPresent())
                self._forceListUpdate = False
                self._presentation.printer()

    def _activatePresent(self, event=0):  # pylint: disable=unused-argument
        if self._presentation.isHided():
            missingBacks = background.checkBackgrounds()
            if missingBacks != []:
                tkMessageBox.showerror(
                    "Attention",
                    "Les fonds d'écran "
                    'pour les types "%s" sont introuvable.' % ", ".join(missingBacks),
                )
            settings.PRESSETTINGS.write()
            self._screens.update(referenceWidget=self._frame)
            self._presentation.show()
            self._packWidgets()
        else:
            self._presentation.hide()

    def _updateButtons(self):
        if self._activateButton:
            if len(self._screens) > 1:
                if self._presentation.isHided():
                    self._activateButton["text"] = "Activer la présentation"
                else:
                    self._activateButton["text"] = "Désactiver la présentation"
            else:
                self._activateButton["text"] = "Présentation de la liste"
        if self._presentation.isHided():
            self._updateListButton.config(state=tk.DISABLED)
        else:
            self._updateListButton.config(state=tk.NORMAL)

    def presentIsOff(self):
        return self._presentation.isHided() or self._forceListUpdate

    def bindListToPresent(self, function):
        self._listToPresent = function

    def bindElementToPresent(self, function):
        self._elementToPresent = function

    def bindRatioCallback(self, function):
        self._callback = function
