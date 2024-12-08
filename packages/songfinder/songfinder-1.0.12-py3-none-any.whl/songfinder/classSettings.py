# -*- coding: utf-8 -*-
# cython: language_level=3

import os
import errno
import logging
import traceback
import xml.etree.cElementTree as ET
import functools

try:  # Windows only imports
    import win32con
    import win32api
except ImportError:
    pass

import songfinder


# This fonction has a duplicate in src.fonctions
def indent(elem, level=0):
    i = f"\n{level * '  '}"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = f"{i}  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subElem in elem:
            indent(subElem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class Settings(object):
    def __init__(self, settingsPath, cheminRoot, portable):
        self._settings = None
        self._settingsPath = settingsPath
        self._dataPath = cheminRoot
        self._portable = portable
        self._name = None
        self._unit_testing = False

        try:
            os.makedirs(self._settingsPath)
            try:
                win32api.SetFileAttributes(
                    self._settingsPath, win32con.FILE_ATTRIBUTE_HIDDEN
                )
            except NameError:  # For Ubuntu
                pass
        except (OSError, IOError) as error:
            if error.errno == errno.EEXIST:
                pass
            else:
                raise
        self._changeCount = 0
        self._maxChange = 10

    @property
    def unit_testing(self):
        return self._unit_testing

    @unit_testing.setter
    def unit_testing(self, value):
        assert isinstance(value, bool)
        self._unit_testing = value

    def create(self):
        raise NotImplementedError

    def write(self):
        fileName = os.path.join(self._settingsPath, self._name)
        indent(self._settings)
        tree = ET.ElementTree(self._settings)
        tree.write(fileName, encoding="UTF-8", xml_declaration=True)

    def read(self):
        # pylint: disable=no-member
        self.get.cache_clear()
        fileName = os.path.join(self._settingsPath, self._name)
        try:
            tree = ET.parse(fileName)
            old_settings_file = tree.getroot()
        except (OSError, IOError, ET.ParseError):
            logging.debug(traceback.format_exc())
            old_settings_file = None
        # Copy old file settings in new file
        if old_settings_file is not None:
            for param in old_settings_file:
                for key, value in param.attrib.items():
                    try:
                        newSetting = self._settings.find(param.tag).attrib[key]
                        if len(newSetting.split(", ")) == len(value.split(", ")):
                            self._settings.find(param.tag).set(key, value)
                    except (AttributeError, KeyError):
                        pass

    @functools.lru_cache(maxsize=20)
    def get(self, setting, parameter):
        try:
            value = self._settings.find(setting).attrib[parameter]
        except (AttributeError, KeyError):
            logging.warning(f'Value for parameter "{setting}/{parameter}" not found')
            self.create()
            if not self.unit_testing:
                self.read()
                self.write()
            value = self._settings.find(setting).attrib[parameter]
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        try:
            newvalue = value.split(", ")
            # This line is actualy usefull to test if newvalue if big enough
            # pylint: disable=pointless-statement
            newvalue[1]
            try:
                newvalue.remove("")
            except ValueError:
                pass
            value = newvalue
        except (AttributeError, IndexError):
            pass

        try:
            lowerValue = value.lower()
        except AttributeError:
            pass
        else:
            if lowerValue in ["true", "oui"]:
                value = True
            elif lowerValue in ["false", "non"]:
                value = False

        if (
            (
                setting.lower() in ["paths", "path"]
                or parameter.lower() in ["background", "backgrounds"]
            )
            and value != ""
            and value.find("http") == -1
        ):
            value = os.path.join(os.path.abspath(value))
            value = value.replace("/", os.sep).replace("\\", os.sep)
        return value

    def set(self, setting, parameter, value):
        # pylint: disable=no-member
        self.get.cache_clear()
        if (
            (
                setting.lower() in ["paths", "path"]
                or parameter.lower() in ["background", "backgrounds"]
            )
            and self._portable
            and value != ""
        ):
            value = os.path.relpath(value)
        try:
            self._settings.find(setting).set(parameter, str(value))
        except AttributeError:
            logging.warning(
                'Not able to set "%s" as value for parameter '
                '"%s/%s" not found' % (str(value), setting, parameter)
            )
            self.create()
            if not self.unit_testing:
                self.read()
                self.write()
            self._settings.find(setting).set(parameter, str(value))
        self._changeCount += 1

        if self._changeCount > self._maxChange:
            self.write()

    def __iter__(self):
        for param in self._settings:
            for key, value in param.attrib.items():
                yield (param.tag, key, value)

    def __str__(self):
        tree = ET.ElementTree(self._settings)
        out_str = f"{self._name}:\n"
        for tag, key, value in self:
            out_str += f'\t"{tag}.{key}" = "{value}"\n'
        return out_str


class GenSettings(Settings):
    def __init__(self, settingsPath, cheminRoot, portable):
        Settings.__init__(self, settingsPath, cheminRoot, portable)
        self._name = "SettingsGen"
        fileName = os.path.join(self._settingsPath, self._name)
        logging.info(f"Using parameter file {fileName}")

    def create(self):
        self._settings = ET.Element(self._name)
        chemins = ET.SubElement(self._settings, "Paths")
        if not self._portable:
            chemins.set("data", "")
        else:
            chemins.set("data", os.path.join(self._dataPath, "songFinderData"))
        chemins.set("jemaf", "")
        chemins.set("shir", "")
        chemins.set("topchretiens", "")
        chemins.set("remote", "")
        chemins.set(
            "conducteurdelouange",
            "https://www.conducteurdelouange.com/chants/consulter",
        )

        extentions = ET.SubElement(self._settings, "Extentions")
        extentions.set(
            "video",
            ".avi, .mp4, .mov, .mkv, .vob, .mpg, .mpa, "
            ".mpg, .webm, .flv, .ogg, .wmv, .amv, .asf, .m4v, "
            ".3gp, .nsv, .mka, .mks, .rmvb, .mxf, .mpeg",
        )
        extentions.set(
            "audio",
            ".mp3, .ogg, .oga, .flac, .wav, .wma, .aif, "
            ".alac, .aa, .aax, .aax+, .aac, .m4a, .m4p, .m4b, "
            ".mp4, .3gp, .aa3, .oma, .at3, .ape, .vqf, .vql, "
            ".vqe, .au, ac3, .amr, .3gpp, .smf",
        )
        extentions.set("image", ".jpg, .png, .gif, .bmp, .tiff, .jpeg")
        extentions.set("presentation", ".ppt, .pptx, .odf, .pdf")
        extentions.set("song", ".sfs, ")
        extentions.set("latex", ".tex, ")
        extentions.set("beamer", ".tex, ")
        extentions.set("media", ".tex, ")
        extentions.set("empty", ",")
        extentions.set("liste", ".sfl, ")
        extentions.set("bible", ".sfb, ")
        extentions.set("chordpro", ".crd, .chopro, .pro, .chordpro, .cho")

        parametres = ET.SubElement(self._settings, "Parameters")
        parametres.set("size_of_previews", "2")
        parametres.set("ratio", "auto")
        parametres.set("ratio_avail", "auto, 5/4, 4/3, 3/2, 16/10, 16/9, 21/9, 32/9")
        parametres.set("autoload", "false")
        parametres.set("sync", "true")
        parametres.set("scm", "git")
        parametres.set("autoreceive", "false")
        parametres.set("highmemusage", "false")
        parametres.set("autoexpand", "false")

        syntax = ET.SubElement(self._settings, "Syntax")
        syntax.set("newslide", "\\ss, \\sc, , \\spc, \\sb")
        syntax.set("newline", "\\l")
        syntax.set(
            "element_type", "song, media, image, verse, empty, preach, latex, beamer"
        )


class LatexSettings(Settings):
    def __init__(self, settingsPath, cheminRoot, portable):
        Settings.__init__(self, settingsPath, cheminRoot, portable)
        self._name = "SettingsLatex"
        fileName = os.path.join(self._settingsPath, self._name)
        logging.info(f"Using parameter file {fileName}")

    def create(self):
        self._settings = ET.Element(self._name)
        latex_parametres = ET.SubElement(self._settings, "Export_Parameters")
        latex_parametres.set("reorder", "true")
        latex_parametres.set("one_song_per_page", "false")
        latex_parametres.set("alphabetic_list", "true")
        latex_parametres.set("transpose", "true")
        latex_parametres.set("chords", "true")
        latex_parametres.set("printkey", "false")
        latex_parametres.set("printtempo", "false")
        latex_parametres.set("list", "false")
        latex_parametres.set("sol_chords", "false")
        latex_parametres.set("num_chords", "false")
        latex_parametres.set("booklet", "false")
        latex_parametres.set("saut_lignes", "true")
        latex_parametres.set("ignore", "true")
        latex_parametres.set("affiche_liste", "true")
        latex_parametres.set("two_columns", "true")
        latex_parametres.set("capo", "false")
        latex_parametres.set("simple_chords", "false")
        latex_parametres.set("keep_first", "false")
        latex_parametres.set("keep_last", "false")
        latex_parametres.set("auto_capo", "false")
        latex_parametres.set("diapo", "false")
        latex_parametres.set("printref", "false")


class PresSettings(Settings):
    def __init__(self, settingsPath, cheminRoot, portable):
        Settings.__init__(self, settingsPath, cheminRoot, portable)
        self._name = "SettingsPres"
        fileName = os.path.join(self._settingsPath, self._name)
        logging.info(f"Using parameter file {fileName}")

    def create(self):
        self._settings = ET.Element(self._name)
        present_parametres = ET.SubElement(self._settings, "Presentation_Parameters")
        present_parametres.set("font", "Arial")
        present_parametres.set("size", "75")
        present_parametres.set("size_line", "27")
        present_parametres.set("line_per_diapo", "6")
        present_parametres.set("FontColor", "white")

        song = ET.SubElement(self._settings, "song")
        song.set("Numerote_diapo", "true")
        song.set("Print_title", "true")
        song.set("Check_bis", "true")
        song.set("Clean_majuscule", "true")
        song.set("Majuscule", "true")
        song.set("Saut_ligne", "true")
        song.set("Saut_ligne_force", "false")
        song.set("oneslide", "false")
        song.set("Ponctuation", "true")
        song.set("Justification", "center")
        song.set(
            "Background", os.path.join(self._dataPath, "backgrounds", "fond_bleu.jpg")
        )

        media = ET.SubElement(self._settings, "media")
        media.set("Numerote_diapo", "false")
        media.set("Print_title", "false")
        media.set("Check_bis", "false")
        media.set("Clean_majuscule", "true")
        media.set("Majuscule", "false")
        media.set("Saut_ligne", "false")
        media.set("Saut_ligne_force", "false")
        media.set("oneslide", "false")
        media.set("Ponctuation", "true")
        media.set("Justification", "center")
        media.set(
            "Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg")
        )

        image = ET.SubElement(self._settings, "image")
        image.set("Numerote_diapo", "false")
        image.set("Print_title", "false")
        image.set("Check_bis", "false")
        image.set("Clean_majuscule", "true")
        image.set("Majuscule", "false")
        image.set("Saut_ligne", "false")
        image.set("Saut_ligne_force", "false")
        image.set("oneslide", "false")
        image.set("Ponctuation", "true")
        image.set("Justification", "center")
        image.set(
            "Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg")
        )

        verse = ET.SubElement(self._settings, "verse")
        verse.set("Numerote_diapo", "true")
        verse.set("Print_title", "true")
        verse.set("Check_bis", "false")
        verse.set("Clean_majuscule", "false")
        verse.set("Majuscule", "false")
        verse.set("Saut_ligne", "true")
        verse.set("Saut_ligne_force", "true")
        verse.set("oneslide", "false")
        verse.set("Ponctuation", "true")
        verse.set("Justification", "left")
        verse.set(
            "Background", os.path.join(self._dataPath, "backgrounds", "fond_bleu.jpg")
        )

        empty = ET.SubElement(self._settings, "empty")
        empty.set("Numerote_diapo", "false")
        empty.set("Print_title", "false")
        empty.set("Check_bis", "false")
        empty.set("Clean_majuscule", "false")
        empty.set("Majuscule", "false")
        empty.set("Saut_ligne", "false")
        empty.set("Saut_ligne_force", "false")
        empty.set("oneslide", "false")
        empty.set("Ponctuation", "false")
        empty.set("Justification", "center")
        empty.set(
            "Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg")
        )

        latex = ET.SubElement(self._settings, "latex")
        latex.set("Numerote_diapo", "false")
        latex.set("Print_title", "false")
        latex.set("Check_bis", "false")
        latex.set("Clean_majuscule", "true")
        latex.set("Majuscule", "true")
        latex.set("Saut_ligne", "true")
        latex.set("Saut_ligne_force", "false")
        latex.set("oneslide", "false")
        latex.set("Ponctuation", "true")
        latex.set("Justification", "left")
        latex.set(
            "Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg")
        )

        latex = ET.SubElement(self._settings, "markdown")
        latex.set("Numerote_diapo", "false")
        latex.set("Print_title", "false")
        latex.set("Check_bis", "false")
        latex.set("Clean_majuscule", "true")
        latex.set("Majuscule", "true")
        latex.set("Saut_ligne", "true")
        latex.set("Saut_ligne_force", "false")
        latex.set("oneslide", "false")
        latex.set("Ponctuation", "true")
        latex.set("Justification", "left")
        latex.set(
            "Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg")
        )

        latex = ET.SubElement(self._settings, "beamer")
        latex.set("Numerote_diapo", "true")
        latex.set("Print_title", "true")
        latex.set("Check_bis", "true")
        latex.set("Clean_majuscule", "true")
        latex.set("Majuscule", "true")
        latex.set("Saut_ligne", "true")
        latex.set("Saut_ligne_force", "false")
        latex.set("oneslide", "false")
        latex.set("Ponctuation", "true")
        latex.set("Justification", "center")
        latex.set(
            "Background", os.path.join(self._dataPath, "backgrounds", "fond_bleu.jpg")
        )

        latex = ET.SubElement(self._settings, "preach")
        latex.set("Numerote_diapo", "false")
        latex.set("Print_title", "true")
        latex.set("Check_bis", "false")
        latex.set("Clean_majuscule", "false")
        latex.set("Majuscule", "false")
        latex.set("Saut_ligne", "true")
        latex.set("Saut_ligne_force", "true")
        latex.set("oneslide", "false")
        latex.set("Ponctuation", "true")
        latex.set("Justification", "left")
        latex.set(
            "Background", os.path.join(self._dataPath, "backgrounds", "fond_noir.jpg")
        )


GENSETTINGS = GenSettings(
    songfinder.__settingsPath__, songfinder.__dataPath__, songfinder.__portable__
)
PRESSETTINGS = PresSettings(
    songfinder.__settingsPath__, songfinder.__dataPath__, songfinder.__portable__
)
LATEXSETTINGS = LatexSettings(
    songfinder.__settingsPath__, songfinder.__dataPath__, songfinder.__portable__
)
GENSETTINGS.create()
GENSETTINGS.read()
logging.debug(GENSETTINGS)
PRESSETTINGS.create()
PRESSETTINGS.read()
LATEXSETTINGS.create()
LATEXSETTINGS.read()
