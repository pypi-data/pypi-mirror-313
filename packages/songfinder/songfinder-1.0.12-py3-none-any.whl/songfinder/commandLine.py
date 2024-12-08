# -*- coding: utf-8 -*-

import os
import sys
import logging
import traceback
import shutil
import threading
import subprocess

import songfinder
from songfinder import exception

try:
    __MAX_TIMEOUT__ = threading.TIMEOUT_MAX
except AttributeError:
    __MAX_TIMEOUT__ = float("inf")


class MyCommand(object):
    def __init__(self, command):
        self._command = command
        self._locaPaths = os.path.join(
            songfinder.__chemin_root__, songfinder.__dependances__, ""
        )
        self._myOs = songfinder.__myOs__

    def checkCommand(self):
        if (
            self._command != ""
            and self._checkInPath()
            and self._checkAuto()
            and self._checkLocal()
        ):
            logging.error(f'Command "{self._command}" not found')
            raise exception.CommandLineError(self._command)
        logging.debug(f'Command "{self._command}" found')
        return 0

    def _checkInPath(self):
        # try to find command in path
        if self._myOs in ["ubuntu", "linux", "darwin"]:
            code, _, _ = self.run(before=["bash", "type", "-a"])
        elif self._myOs == "windows":
            code, _, _ = self.run(before=["where"])
        else:
            code = 1
        return code

    def _checkAuto(self):
        command = shutil.which(self._command)
        if not command:
            return 1
        self._command = command
        return 0

    def _checkLocal(self):
        # Look for portable instalaltion packaged with the software
        for root, _, files in os.walk(self._locaPaths):
            for fichier in files:
                if fichier in [self._command, f"{self._command}.exe"]:
                    self._command = os.path.join(root, fichier)
                    return 0
        return 1

    def run(self, options=(), timeOut=__MAX_TIMEOUT__, **kwargs):
        before = kwargs.get("before", None)
        winOptions = kwargs.get("winOptions", None)
        linuxOptions = kwargs.get("linuxOptions", None)
        darwinOptions = kwargs.get("darwinOptions", None)

        commandList = []
        if before:
            commandList = before
        commandList.append(self._command)

        if self._myOs in ["ubuntu", "linux"] and linuxOptions:
            commandList += linuxOptions
        elif self._myOs == "windows" and winOptions:
            commandList += winOptions
        elif self._myOs == "darwin" and darwinOptions:
            commandList += darwinOptions

        commandList += list(options)
        if "|" in commandList:
            # do import latter to enable deletion of fonction compiled librarie when needed
            from songfinder import fonctions as fonc

            commandLists = fonc.splitList(commandList, "|")
            proc = subprocess.Popen(
                commandLists[0],
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for commandList in commandLists[1:]:
                proc = subprocess.Popen(
                    commandList,
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=proc.stdout,
                )
        else:
            proc = subprocess.Popen(
                commandList, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        timer = threading.Timer(timeOut, proc.kill)
        try:
            timer.start()
            stdout, stderr = proc.communicate()
            try:
                stdout = stdout.decode(sys.getfilesystemencoding())
                stderr = stderr.decode(sys.getfilesystemencoding())
            except UnicodeDecodeError:
                logging.debug(traceback.format_exc())
                try:
                    stdout = stdout.decode("latin-1")
                    stderr = stderr.decode("latin-1")
                except (UnicodeDecodeError, AttributeError):
                    logging.debug(traceback.format_exc())
                pass
        finally:
            timer.cancel()
            returncode = proc.returncode
        if not stdout:
            stdout = ""
        if not stderr:
            stderr = ""
        stderr = f"{' '.join(commandList)}\n{str(stderr)}"
        if returncode:
            logging.error(f"FAILED run \"{' '.join(commandList)}\"")
        else:
            logging.debug(f"Succesfully run \"{' '.join(commandList)}\"")
        return returncode, stdout, stderr


class Ping(MyCommand):
    def __init__(self, host):
        self._host = host
        MyCommand.__init__(self, "ping")
        self._timeout = 10  # in seconds
        self._retry = 2

    def run(self):
        code, _, _ = super(Ping, self).run(
            linuxOptions=["-c", f"{self._retry}", "-w", f"{self._timeout}"],
            darwinOptions=["-c", f"{self._retry}", "-t", f"{self._timeout}"],
            winOptions=["-n", f"{self._retry}", "-w", f"{self._timeout * 1000}"],
            options=[self._host],
            timeout=self._timeout,
        )
        return code


def run_file(path):
    # Pas de EAFP cette fois puisqu'on est dans un process externe,
    # on ne peut pas gérer l'exception aussi facilement, donc on fait
    # des checks essentiels avant.

    # Vérifier que le fichier existe
    if not os.path.exists(path):
        raise IOError(f"No such file: {path}")

    # On a accès en lecture ?
    if hasattr(os, "access") and not os.access(path, os.R_OK):
        raise IOError(f"Cannot access file: {path}")

    # Lancer le bon programme pour le bon OS:

    if hasattr(os, "startfile"):  # Windows
        # Startfile est très limité sous Windows, on ne pourra pas savoir
        # si il y a eu une erreu
        proc = os.startfile(path)  # pylint: disable=no-member

    elif sys.platform.startswith("linux"):  # Linux:
        proc = subprocess.Popen(
            ["xdg-open", path],
            # on capture stdin et out pour rendre le
            # tout non bloquant
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    elif sys.platform == "darwin":  # Mac:
        proc = subprocess.Popen(
            ["open", "--", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    else:
        raise NotImplementedError(
            f"Your `{sys.platform}` isn't a supported operatin system`."
        )

    # Proc sera toujours None sous Windows. Sous les autres OS, il permet de
    # récupérer le status code du programme, and lire / ecrire sur stdin et out
    return proc
