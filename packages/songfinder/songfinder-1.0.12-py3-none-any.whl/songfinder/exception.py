# -*- coding: utf-8 -*-


class CommandLineError(NotImplementedError):
    def __init__(self, command):
        self._command = command
        self._packetDict = {
            "sox": "sox libsox-fmt-mp3",
            "flac": "flac",
            "opusenc": "opus-tools",
            "oggenc": "vorbis-tools",
            "lame": "ubuntu-restricted-extras lame",
            "hg": "mercurial",
        }

    def __str__(self):
        aptCommand = self._packetDict.get(self._command, None)
        if aptCommand:
            ubuntuInfo = f" On Ubuntu try 'sudo apt install {aptCommand}'."
        else:
            ubuntuInfo = ""
        out = "%s is not a valid command. Please install it to use this feature.%s" % (
            self._command,
            ubuntuInfo,
        )
        return repr(out)


class DataReadError(IOError):
    def __init__(self, theFile):
        self._theFile = theFile

    def __str__(self):
        out = f'Impossible de lire le fichier "{self._theFile}"'
        return repr(out)


class DiapoError(Exception):
    def __init__(self, number):
        self._number = number

    def __str__(self):
        out = f'Le numero de diapo "{self._number}" n\'est pas valide'
        return repr(out)


class ConversionError(Exception):
    def __init__(self, theType):
        self._theType = theType
        self._types = ["html", "markdown"]

    def __str__(self):
        out = 'Invalid type conversion "%s". The available types are %s.' % (
            self._theType,
            ", ".join(self._types),
        )
        return repr(out)
