# -*- coding: utf-8 -*-

import os
import codecs
import errno
import sys
import platform
import logging
import datetime
from songfinder import logger_formatter

__version__ = "1.0.12"
__author__ = "danbei"
__appName__ = "songfinder"

# Define root diretcory
__chemin_root__ = os.getcwd()

# Define data directory
__dataPath__ = os.path.join(os.path.split(__file__)[0], "data")


def _isPortable():
    # Check if installation is portable
    isPortable = os.path.isfile(os.path.join(__chemin_root__, "PORTABLE"))
    try:
        with codecs.open(
            os.path.join(__chemin_root__, "test.test"), "w", encoding="utf-8"
        ):
            pass
        os.remove(os.path.join(__chemin_root__, "test.test"))
    except (OSError, IOError) as error:
        if error.errno == errno.EACCES:
            isPortable = False
        else:
            raise
    return isPortable


__portable__ = _isPortable()

# Define Settings directory
if __portable__:
    __settingsPath__ = os.path.join(__chemin_root__, f".{__appName__}", "")
else:
    __settingsPath__ = os.path.join(os.path.expanduser("~"), f".{__appName__}", "")


def _loggerConfiguration():
    # Set logger configuration
    logFormatter = logger_formatter.MyFormatter()
    consoleHandler = logging.StreamHandler(sys.stdout)
    logDirectory = os.path.join(__settingsPath__, "logs")
    logFile = os.path.join(
        logDirectory, f"{datetime.datetime.now().strftime('%Y-%m-%d-%Hh%Mm%Ss')}.log"
    )
    try:
        os.makedirs(logDirectory)
    except (OSError, IOError) as error:
        if error.errno == errno.EEXIST:
            pass
        else:
            raise
    fileHandler = logging.FileHandler(logFile)
    consoleHandler.setFormatter(logFormatter)
    fileHandler.setFormatter(logFormatter)
    logging.root.addHandler(consoleHandler)
    logging.root.addHandler(fileHandler)

    logging.root.setLevel(logging.DEBUG)
    fileHandler.setLevel(logging.DEBUG)
    return consoleHandler


__consoleHandler__ = _loggerConfiguration()


def _getOs():
    system = platform.system()
    if system == "Linux":
        platformInfo = platform.platform().split("-")
        if platformInfo[0] == "Ubuntu":
            outOs = "ubuntu"
        else:
            outOs = "linux"
    elif system == "Windows":
        outOs = "windows"
    elif system == "Darwin":
        outOs = "darwin"
    else:
        outOs = "notSupported"
        logging.info(f"Your `{system}` isn't a supported operatin system`.")
    return outOs


__myOs__ = _getOs()

if sys.maxsize == 9223372036854775807:
    __arch__ = "x64"
else:
    __arch__ = "x86"
__dependances__ = f"deps-{__arch__}"
__unittest__ = False


def _gui(fenetre, fileIn=None):
    # Creat main window and splash icon
    import traceback
    from songfinder.gui import guiHelper
    from songfinder.gui import screen
    from songfinder.gui import splash

    screens = screen.Screens()
    with guiHelper.SmoothWindowCreation(fenetre, screens):
        screens.update(referenceWidget=fenetre)

        with splash.Splash(fenetre, os.path.join(__dataPath__, "icon.png"), screens):
            # Compile cython file and cmodules
            if not __portable__:
                try:
                    import subprocess

                    python = sys.executable
                    if python:
                        command = [
                            python,
                            os.path.join(os.path.split(__file__)[0], "setup_cython.py"),
                            "build_ext",
                            "--inplace",
                        ]
                        proc = subprocess.Popen(
                            command,
                            shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        )
                        out, err = proc.communicate()
                        try:
                            logging.debug(out.decode())
                            logging.debug(err.decode())
                        except UnicodeDecodeError:
                            logging.debug(out)
                            logging.debug(err)
                except Exception:  # pylint: disable=broad-except
                    logging.warning(traceback.format_exc())

            from songfinder.gui import interface

            # Set bar icon
            try:
                from PIL import ImageTk

                if os.name == "posix":
                    img = ImageTk.PhotoImage(
                        file=os.path.join(__dataPath__, "icon.png")
                    )
                    fenetre.tk.call(
                        "wm", "iconphoto", fenetre._w, img
                    )  # pylint: disable=protected-access
                else:
                    fenetre.iconbitmap(os.path.join(__dataPath__, "icon.ico"))
            except Exception:  # pylint: disable=broad-except
                logging.warning(traceback.format_exc())
            if fileIn:
                fileIn = fileIn[0]
            songFinder = interface.Interface(fenetre, screens=screens, fileIn=fileIn)
            fenetre.title("SongFinder")
            fenetre.protocol("WM_DELETE_WINDOW", songFinder.quit)

    songFinder.__syncPath__()  # TODO This is a hack
    fenetre.mainloop()


def _song2markdown(fileIn, fileOut):
    from songfinder import fileConverter

    converter = fileConverter.Converter()
    converter.makeSubDirOn()
    converter.markdown(fileIn, fileOut)


def _song2latex(fileIn, fileOut):
    from songfinder import fileConverter

    converter = fileConverter.Converter()
    converter.makeSubDirOn()
    converter.latex(fileIn, fileOut)


def _song2html(fileIn, fileOut):
    from songfinder import fileConverter

    converter = fileConverter.Converter()
    converter.makeSubDirOn()
    converter.html(fileIn, fileOut)


def _add_info_from(database_names):
    from songfinder import dataBase

    localData = dataBase.DataBase()
    localData.add_info_from(database_names)


def _parseArgs():
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser = argparse.ArgumentParser(
        description=f"{__appName__} v{__version__}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument(
        "-f",
        "--file",
        nargs=1,
        metavar=("inputFile",),
        help="Song file or set file to open",
    )

    arg_parser.add_argument(
        "-m",
        "--songtomarkdown",
        nargs=2,
        metavar=("song[File/Dir]", "markdown[File/Dir]"),
        help="Convert song file (xml or chordpro) files to markdown file",
    )

    arg_parser.add_argument(
        "-L",
        "--songtolatex",
        nargs=2,
        metavar=("song[File/Dir]", "latex[File/Dir]"),
        help="Convert song file (xml or chordpro) files to latex file",
    )

    arg_parser.add_argument(
        "-t",
        "--songtohtml",
        nargs=2,
        metavar=("song[File/Dir]", "html[File/Dir]"),
        help="Convert song file (xml or chordpro) files to html file",
    )

    arg_parser.add_argument(
        "-a",
        "--addinfo",
        nargs=1,
        metavar=("database_names"),
        help="Scan database for songs additional songs infos",
    )

    arg_parser.add_argument(
        "--version", action="store_true", default=False, help="Print songfinder version"
    )

    levelChoices = [
        logging.getLevelName(x)
        for x in range(1, 101)
        if not logging.getLevelName(x).startswith("Level")
    ]

    arg_parser.add_argument(
        "-l",
        "--loglevel",
        choices=levelChoices,
        default="INFO",
        help="Increase output verbosity",
    )

    return arg_parser.parse_args()


def songFinderMain():
    args = _parseArgs()
    numeric_level = logging.getLevelName(args.loglevel)
    __consoleHandler__.setLevel(numeric_level)

    logging.info(f"{__appName__} v{__version__}")
    platformInfos = [
        platform.node(),
        platform.python_implementation(),
        platform.python_version(),
        platform.python_compiler(),
        platform.platform(),
        platform.processor(),
    ]
    logging.info(", ".join(platformInfos))

    logging.info(f'Settings are in "{__settingsPath__}"')
    logging.info(f'Datas are in "{__dataPath__}"')
    logging.info(f'Root dir is "{__chemin_root__}"')

    if __portable__:
        logging.info("Portable version")
    else:
        logging.info("Installed version")
    if args.songtomarkdown:
        _song2markdown(*args.songtomarkdown)
    elif args.songtolatex:
        _song2latex(*args.songtolatex)
    elif args.songtohtml:
        _song2html(*args.songtohtml)
    elif args.addinfo:
        _add_info_from(args.addinfo)
    elif args.version:
        print(f"{__appName__} v.{__version__} by {__author__}")
    else:
        import tkinter as tk
        import traceback
        from songfinder import messages as tkMessageBox

        fenetre = tk.Tk()
        dpi_value = fenetre.winfo_fpixels("1i")
        logging.info(f"Screen DPI: {dpi_value}")
        fenetre.tk.call("tk", "scaling", "-displayof", ".", dpi_value / 72.0)

        # Override tkinter methode to raise exception occuring in tkinter callbacks
        def report_callback_exception(self, exc, val, tb):
            tkMessageBox.showerror("Erreur", traceback.format_exc(limit=1))

        tk.Tk.report_callback_exception = report_callback_exception

        try:
            _gui(fenetre, fileIn=args.file)
        except SystemExit:
            raise
        except:
            if not getattr(sys, "frozen", False):
                tkMessageBox.showerror("Erreur", traceback.format_exc(limit=1))
            logging.critical(traceback.format_exc())
            raise


if __name__ == "__main__":
    songFinderMain()
