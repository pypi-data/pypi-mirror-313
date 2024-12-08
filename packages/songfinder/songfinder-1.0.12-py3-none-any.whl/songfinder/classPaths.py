# -*- coding: utf-8 -*-
# cython: language_level=3

import os
import codecs
import errno
import traceback
from songfinder import messages as tkMessageBox
from songfinder import messages as tkFileDialog  # pylint: disable=reimported

import songfinder
from songfinder import versionning as version
from songfinder import exception
from songfinder import classSettings as settings


class Paths(object):
    def __init__(self, fenetre=None):
        self.fenetre = fenetre
        self.update(showGui=False)
        self._root = None
        self._listPaths = None

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, path):
        if self._isValidDir(path):
            settings.GENSETTINGS.set("Paths", "data", path)
            self._root = path
            self.update(showGui=False)
        else:
            self._root = None

    def _isValidDir(self, path):
        if not path:
            tkMessageBox.showerror(
                "Erreur",
                'Le chemin "%s" n\'est pas '
                "accesible valide, "
                "choisissez un autre répertoire." % path,
                parent=self.fenetre,
            )
            return False
        try:
            fileName = os.path.join(path, "test.test")
            with codecs.open(fileName, "w", encoding="utf-8"):
                pass
            os.remove(fileName)
        except (OSError, IOError) as error:
            if error.errno == errno.EACCES:
                tkMessageBox.showerror(
                    "Erreur",
                    'Le chemin "%s" n\'est pas '
                    "accesible en écriture, "
                    "choisissez un autre répertoire." % path,
                    parent=self.fenetre,
                )
                return False
        try:
            os.makedirs(path)
        except (OSError, IOError) as error:
            if error.errno == errno.EEXIST:
                pass
            else:
                raise
        return True

    def _askDir(self):
        tkMessageBox.showinfo(
            "Répertoire",
            "Aucun répertoire pour les chants et "
            "les listes n'est configuré.\n"
            "Dans le fenêtre suivante, selectionnez "
            "un répertoire existant ou créez en un nouveau. "
            'Par exemple, vous pouvez créer un répertoire "songfinderdata" '
            "parmis vos documents. "
            "Dans ce répertoire seront stocké : "
            "les chants, les listes, les bibles et les partitions pdf.",
            parent=self.fenetre,
        )
        for _ in range(5):
            if not self._root:
                path = tkFileDialog.askdirectory(
                    initialdir=os.path.expanduser("~"), parent=self.fenetre
                )
                if not path:
                    break
                self.root = path

    def update(self, showGui=True):
        self._root = settings.GENSETTINGS.get("Paths", "data")
        if showGui:
            if not self._root and not songfinder.__unittest__:
                self._askDir()
            if not self._root:
                raise Exception(
                    "No data directory configured, shuting down SongFinder."
                )

        self.songs = os.path.join(self._root, "songs")
        self.sets = os.path.join(self._root, "sets")
        self.bibles = os.path.join(self._root, "bibles")
        self.pdf = os.path.join(self._root, "pdf")
        self.preach = os.path.join(self._root, "preach")
        self._listPaths = [self.songs, self.sets, self.bibles, self.pdf, self.preach]

        self._createSubDirs()

    def _createSubDirs(self):
        if self._root:
            for path in self._listPaths:
                try:
                    os.makedirs(path)
                except (OSError, IOError) as error:
                    if error.errno == errno.EEXIST:
                        pass
                    else:
                        raise

    def sync(self, screens=None, updateData=None):
        scm = settings.GENSETTINGS.get("Parameters", "scm")
        if settings.GENSETTINGS.get("Parameters", "sync") and not os.path.isdir(
            os.path.join(self._root, f".{scm}")
        ):
            if tkMessageBox.askyesno(
                "Dépot",
                "Voulez-vous définir le dépot de chants et listes ?\n"
                'Ceci supprimera tout documents présent dans "%s"' % self._root,
            ):
                try:
                    version.AddRepo(self, scm, screens, updateData)
                except exception.CommandLineError:
                    tkMessageBox.showerror("Erreur", traceback.format_exc(limit=1))
            else:
                settings.GENSETTINGS.set("Parameters", "sync", False)


PATHS = Paths()
