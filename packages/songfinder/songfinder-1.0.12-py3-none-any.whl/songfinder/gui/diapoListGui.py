# -*- coding: utf-8 -*-

import tkinter as tk


class DiapoListGui(object):
    def __init__(self, frame, diapoList, callbacks=None):
        self._diapoList = diapoList
        if not callbacks:
            self._callbacks = dict()
        self._listBox = tk.Listbox(frame, selectmode=tk.BROWSE, width=40)
        self._scrollBar = tk.Scrollbar(frame, command=self._listBox.yview)
        self._listBox["yscrollcommand"] = self._scrollBar.set

        self._listBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self._scrollBar.pack(side=tk.LEFT, fill=tk.Y)

        self._listBox.bind("<KeyRelease-Up>", self._getSelect)
        self._listBox.bind("<KeyRelease-Down>", self._getSelect)
        self._listBox.bind("<ButtonRelease-1>", self._getSelect)

    def _getSelect(self, event=None):  # pylint: disable=unused-argument
        if self._listBox.curselection():
            self._diapoList.diapoNumber = int(self._listBox.curselection()[0])
        for callback in self._callbacks.values():
            callback()

    def updateSelected(self, focus=False):
        if focus:
            self._listBox.select_clear(0, tk.END)
            self._listBox.select_set(self._diapoList.diapoNumber)
        else:
            self._listBox.activate(self._diapoList.diapoNumber)
            self._listBox.see(self._diapoList.diapoNumber)

    def write(self):
        self._listBox.delete(0, "end")
        for i, diapo in enumerate(self._diapoList.list):
            self._listBox.insert(i, diapo.title)
            if diapo.etype == "empty":
                self._listBox.itemconfig(i, bg="green")
            elif diapo.etype == "image":
                self._listBox.itemconfig(i, bg="blue")

    def width(self):
        return self._listBox.winfo_reqwidth() + self._scrollBar.winfo_reqwidth()

    def bindDiapoList(self, diapoList):
        self._diapoList = diapoList
        self.write()

    def bindCallback(self, callback, classId):
        self._callbacks[classId] = callback
