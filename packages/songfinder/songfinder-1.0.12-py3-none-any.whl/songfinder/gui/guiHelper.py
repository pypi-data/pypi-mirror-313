# -*- coding: utf-8 -*-

import tkinter as tk

import os

import songfinder


class SmoothWindowCreation(object):
    def __init__(self, window, screens=None):
        self._window = window
        self._screens = screens

    def __enter__(self):
        self._window.withdraw()
        self._window.resizable(width=True, height=True)

    def __exit__(self, exception_type, exception_value, traceback):
        self._window.update_idletasks()
        width = self._window.winfo_reqwidth()
        height = self._window.winfo_reqheight()
        self._window.minsize(width, height)
        self._window.geometry(f"{width}x{height}")
        if self._screens:
            self._screens.centerFrame(self._window)
        self._window.deiconify()
        upFront(self._window)
        self._window.focus_set()


def upFront(window):
    if songfinder.__myOs__ != "darwin":
        window.lift()
        window.wm_attributes("-topmost", 1)
        window.after_idle(window.wm_attributes, "-topmost", 0)
    else:
        from Cocoa import (  # pylint: disable=import-error
            NSRunningApplication,
            NSApplicationActivateIgnoringOtherApps,
        )

        app = NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
        app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)


def change_text(widget, text):
    widget.delete(1.0, tk.END)
    widget.insert(1.0, text)  # TclError if text is None


def get_max_width(text, police):
    lignes = text.splitlines()
    lenghs = [police.measure(ligne) for ligne in lignes]
    return max(lenghs + [0])


def get_height(text, police):
    h_line = police.metrics("linespace")
    lignes = text.splitlines()
    return len(lignes) * h_line


def index_plus(index, plus):
    unpack = index.split(".")
    if len(unpack) == 2:
        [a, b] = unpack
        a, b = int(a), int(b)
        b = b + plus
        a, b = str(a), str(b)
        return f"{a}.{b}"
    else:
        return index


def coloration(widget, couleur, chaine="", fin=""):
    # Bold make the tag_config method very slow
    # ~ relou = tkFont.nametofont("TkDefaultFont")
    # ~ police = tkFont.Font(family=relou["family"],size=relou["size"],weight="bold")
    # ~ police["weight"] = "bold"
    # coloration

    if not chaine:
        for tag in widget.tag_names():
            widget.tag_delete(tag)
        return 0

    pos = "1.0"
    pos = widget.search(chaine, pos, stopindex=tk.END, nocase=1)
    while pos:  # Lets Some None pass
        if fin:
            pos_sui = index_plus(widget.search(fin, pos, stopindex=tk.END, nocase=1), 1)
        else:
            pos_sui = index_plus(pos, len(chaine))
        widget.tag_add(chaine, pos, pos_sui)  # TclError None
        pos = widget.search(chaine, pos_sui, stopindex=tk.END, nocase=1)  # TclError ??
    # ~ widget.tag_config(chaine, foreground=couleur, font=police)
    widget.tag_config(chaine, foreground=couleur)


def allChildren(window):
    _list = window.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    return _list
