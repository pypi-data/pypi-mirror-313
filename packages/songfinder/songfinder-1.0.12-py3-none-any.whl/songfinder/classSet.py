# -*- coding: utf-8 -*-
# cython: language_level=3

import xml.etree.cElementTree as ET
import datetime
import os
import errno
import traceback
import logging
import re

from songfinder import elements
from songfinder import fonctions as fonc
from songfinder import classPaths
from songfinder import classSettings as settings


class Set(object):
    def __init__(self):
        self._paths = classPaths.PATHS
        self._listElem = []
        self._generateName()
        self._changed = False

    def __eq__(self, other):
        for i, item in enumerate(self._listElem):
            if item != other[i]:
                return False
        return True

    def __len__(self):
        return len(self._listElem)

    def __setitem__(self, key, value):
        self._listElem[key] = value
        self._changed = True

    def __getitem__(self, index):
        return self._listElem[index]

    def __delitem__(self, index):
        del self._listElem[index]
        self._changed = True

    def __contains__(self, element):
        return element in self._listElem

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._listElem}')"

    def __str__(self):
        return self._name

    def _generateName(self):
        nextSunday = datetime.timedelta(days=6 - datetime.datetime.today().weekday())
        self._name = str(datetime.date.today() + nextSunday)
        while os.path.isfile(self._paths.sets + self._name):
            if len(self._name) == 10:
                self._name = f"{self._name}_1"
            else:
                self._name = self._name[:11] + str(int(self._name[11:]) + 1)
        self.path = (
            os.path.join(self._paths.sets, self._name)
            + settings.GENSETTINGS.get("Extentions", "liste")[0]
        )

    def _read(self, preferedPath, dataBase):
        tmp = None
        self._listElem = []
        try:
            tree = ET.parse(self.path)
            tree.getroot().find("slide_groups")[
                :
            ]  # pylint: disable=expression-not-assigned
        except (OSError, IOError, AttributeError):
            logging.warning(f'Not able to read "{self.path}"\n{traceback.format_exc()}')
            return 1, traceback.format_exc()
        xmlList = tree.getroot()

        pathToSearch = [""]
        if preferedPath:
            pathToSearch.append(preferedPath)
        pathToSearch.append(self._paths.songs)
        self._name = xmlList.attrib["name"]

        for title in xmlList.find("slide_groups"):
            if title.attrib["type"] == "song":
                elem_path = title.attrib["path"]
                elem_name = title.attrib["name"]
                try:
                    song_ext = title.attrib["ext"]
                    elem_name = elem_name + song_ext
                except KeyError:
                    pass
                # Different ways of writting the path, test all

                for path in pathToSearch:
                    tmp = elements.Chant(os.path.join(path, elem_path, elem_name))
                    if not tmp.exist():
                        tmp = elements.Chant(os.path.join(path, elem_name))
                        if not tmp.exist():
                            tmp = elements.Chant(os.path.join(path, "songs", elem_name))
                    if tmp.exist():
                        break

            elif title.attrib["type"] == "media":
                tmp = elements.Element(elem_name, title.attrib["type"], elem_path)
            elif title.attrib["type"] == "image":
                tmp = elements.ImageObj(os.path.join(elem_path, elem_name))
            elif title.attrib["type"] == "verse":
                tmp = elements.Passage(
                    title.attrib["version"],
                    int(title.attrib["livre"]),
                    int(title.attrib["chap1"]),
                    int(title.attrib["chap2"]),
                    int(title.attrib["vers1"]),
                    int(title.attrib["vers2"]),
                )
            if dataBase:
                try:
                    tmp = dataBase[tmp.nom]
                    tmp.resetDiapos()
                except KeyError:
                    pass
            self._listElem.append(tmp)
        self._changed = False
        # TODO Cmon remove this !
        return 0, ""

    def append(self, element):
        self._listElem.append(element)
        self._changed = True

    def insert(self, index, element):
        self._listElem.insert(index, element)
        self._changed = True

    def clear(self):
        del self._listElem[:]
        self._changed = True

    def save(self):
        new_set = ET.Element("set")
        new_set.set("name", self._name)
        slide_groups = ET.SubElement(new_set, "slide_groups")
        slide_group = []
        for i, element in enumerate(self._listElem):
            chemin = fonc.get_path(element.chemin)
            # For compatibility between linux an windows, all path are writtent with slash
            chemin = chemin.replace(os.sep, "/")
            # Write path relative to songs directory
            chemin = chemin.replace(f"{self._paths.songs.replace(os.sep, '/')}", "")

            slide_group.append(ET.SubElement(slide_groups, "slide_group"))
            slide_group[i].set("type", element.etype)
            if element.etype == "song":
                slide_group[i].set("path", chemin)
                slide_group[i].set("name", element.nom)
                slide_group[i].set("ext", element.extention)
            elif element.etype == "verse":
                slide_group[i].set("name", element.nom)
                slide_group[i].set("path", chemin)
                slide_group[i].set("version", element.version)
                slide_group[i].set("livre", str(element.livre))
                slide_group[i].set("chap1", str(element.chap1))
                slide_group[i].set("chap2", str(element.chap2))
                slide_group[i].set("vers1", str(element.vers1))
                slide_group[i].set("vers2", str(element.vers2))
            elif element.etype == "image":
                slide_group[i].set("name", element.nom)
                slide_group[i].set("path", chemin)
                slide_group[i].set("ext", element.extention)

        tree = ET.ElementTree(new_set)
        fonc.indent(new_set)
        tree.write(self.path, encoding="UTF-8", xml_declaration=True)
        self._changed = False

    def delete(self):
        try:
            os.remove(self.path)
        except (OSError, IOError) as error:
            if error.errno == errno.ENOENT:
                logging.warning(f'File "{self.path}" does not exist.')
            elif error.errno == errno.EACCES:
                logging.warning(f'Acces to "{self.path}" is not permited.')
            else:
                logging.error(traceback.format_exc())
                raise
        self._changed = True

    def load(self, fileName, preferedPath=None, dataBase=None):
        setExtention = settings.GENSETTINGS.get("Extentions", "liste")[0]
        if fileName.find("/") != -1:
            candidat = fileName
        else:
            candidat = os.path.join(self._paths.sets, fileName)
        candidat = candidat + setExtention
        candidat = candidat.replace(setExtention * 2, setExtention)
        self.path = candidat
        # For backward compatibility with old file names
        # TODO remove this
        if not os.path.isfile(self.path):
            self._fileName = candidat
        return self._read(preferedPath, dataBase)

    @property
    def path(self):
        return self._fileName

    @path.setter
    def path(self, input_path):
        self._name = fonc.get_file_name(input_path)
        path = fonc.get_path(input_path)
        ext = fonc.get_ext(input_path)
        fileName = fonc.get_file_name(input_path)
        fileName = fonc.enleve_accents(fileName).strip(" ")
        fileName = re.sub(r'[\/?!,;:*<>"|^]+', "", fileName)
        fileName = re.sub(r"[\'() ]+", "_", fileName)
        self._fileName = os.path.join(path, fileName) + ext

    @property
    def changed(self):
        return self._changed
