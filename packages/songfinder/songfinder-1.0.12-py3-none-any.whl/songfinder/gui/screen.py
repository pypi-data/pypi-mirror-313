# -*- coding: utf-8 -*-

import sys
import logging
import traceback

import tkinter as tk

try:
    import screeninfo
except ImportError:
    pass

from songfinder import commandLine
from songfinder import exception
import songfinder


class Screen(object):
    def __init__(
        self, width=720, height=480, xposition=0, yposition=0, stringScreen=None
    ):
        if not stringScreen:
            try:
                self._width = int(width)
                self._height = int(height)
                self._xposition = int(xposition)
                self._yposition = int(yposition)
                self._isOK = True
            except ValueError:
                logging.warning(
                    "Erreur de lecture des donnees de l'ecran :\n%s"
                    % (
                        "\n".join(
                            [
                                repr(data)
                                for data in [width, height, xposition, yposition]
                            ]
                        )
                    )
                )
                self._isOK = False
        else:
            self._setScreen(stringScreen)
        self._areUsableSet = False

    def _setScreen(self, stringScreen):
        sizeList = stringScreen.split("x")
        if len(sizeList) != 2:
            logging.warning(
                "Erreur de lecture de la resolution de l"
                "ecran, "
                "le format des donnees n"
                'est pas valide : "%s". '
                'Le format valide est : "wxh+pw+ph' % stringScreen
            )
            self._isOK = False
        else:
            positionList = sizeList[1].split("+")
            if len(positionList) != 3:
                logging.warning(
                    "Erreur de lecture de la position de l"
                    "ecran, "
                    "le format des donnees n"
                    'est pas valide : "%s". '
                    'Le format valide est : "wxh+pw+ph' % stringScreen
                )
                self._isOK = False
            else:
                try:
                    self._width = int(float(sizeList[0]))
                    self._height = int(float(positionList[0]))
                    self._xposition = int(float(positionList[1]))
                    self._yposition = int(float(positionList[2]))
                    self._isOK = True
                except ValueError:
                    logging.warning(
                        "Erreur de lecture des donnees de l'ecran :\n%s"
                        % (
                            "\n".join(
                                [
                                    repr(data)
                                    for data in [
                                        sizeList[0],
                                        positionList[0],
                                        positionList[1],
                                        positionList[2],
                                    ]
                                ]
                            )
                        )
                    )
                    self._isOK = False

    def __bool__(self):
        return self._isOK

    def __nonzero__(self):
        return self.__bool__()

    @property
    def xposition(self):
        return self._xposition

    @property
    def yposition(self):
        return self._yposition

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def usableXposition(self):
        self._getUsableScreen()
        return self._usableXposition

    @property
    def usableYposition(self):
        self._getUsableScreen()
        return self._usableYposition

    @property
    def usableWidth(self):
        self._getUsableScreen()
        return self._usableWidth

    @property
    def usableHeight(self):
        self._getUsableScreen()
        return self._usableHeight

    @property
    def ratio(self):
        if self._height != 0:
            ratio = self._width / self._height
        else:
            ratio = 1
        return ratio

    def _getUsableScreen(self):
        if not self._areUsableSet:
            try:
                frame = tk.Toplevel()
                frame.wm_attributes("-alpha", 0)
                frame.withdraw()
                frame.geometry(f"+{self.xposition}+{self.yposition}")
                frame.update()
                frame.state("zoomed")
                frame.withdraw()
            except tk.TclError:
                logging.debug(traceback.format_exc())
                self._usableWidth = int(self.width * 0.9)
                self._usableHeight = int(self.height * 0.9)
                self._usableXposition = int(self.xposition * 0.9)
                self._usableYposition = int(self.yposition * 0.9)
            else:
                frame.update()
                self._usableWidth = frame.winfo_width()
                self._usableHeight = frame.winfo_height()
                self._usableXposition = frame.winfo_rootx()
                self._usableYposition = frame.winfo_rooty()
                frame.destroy()
            self._areUsableSet = True

    def __str__(self):
        out = "".join(
            [
                str(self._width),
                "x",
                str(self._height),
                "+",
                str(self._xposition),
                "+",
                str(self._yposition),
            ]
        )
        return out

    @property
    def usable(self):
        self._getUsableScreen()
        out = "".join(
            [
                str(self._usableWidth),
                "x",
                str(self._usableHeight),
                "+",
                str(self._usableXposition),
                "+",
                str(self._usableYposition),
            ]
        )
        return out

    def isWidgetScreenSizeMine(self, widget):
        widget.update()
        return (
            widget.winfo_screenwidth() == self.width
            and widget.winfo_screenheight() == self.height
        )

    def isWidgetInScreen(self, widget):
        widget.update()
        xposition = widget.winfo_rootx() - self.xposition
        yposition = widget.winfo_rooty() - self.yposition
        logging.debug(
            "Widget position is: %d+%d, Screen is: %s"
            % (widget.winfo_rootx(), widget.winfo_rooty(), str(self))
        )
        return (
            not self.isWidgetScreenSizeMine(widget)
            and xposition >= 0
            and xposition < self.width
            and yposition >= 0
            and yposition < self.height
        )

    def centerFrame(self, frame):
        newx = (self.usableWidth - frame.winfo_reqwidth()) // 2 + self.usableXposition
        newy = (self.usableHeight - frame.winfo_reqheight()) // 2 + self.usableYposition
        frame.geometry(f"+{newx}+{newy}")

    def resizeFrame(self, frame, width, height):
        newWidth = min(self.usableWidth, width)
        newHeight = min(self.usableHeight, height)
        clipx = self.usableWidth - newWidth + self.usableXposition - 1
        clipy = self.usableHeight - newHeight + self.usableYposition - 1
        newx = max(min(frame.winfo_x(), clipx), self.usableXposition)
        newy = max(min(frame.winfo_y(), clipy), self.usableYposition)
        # TODO this is a hack
        # On Ubuntu the frame.winfo_y() is not correct
        if newx == frame.winfo_x() and newy == frame.winfo_y():
            frame.geometry(f"{newWidth}x{newHeight}")
        else:
            frame.geometry(f"{newWidth}x{newHeight}+{newx}+{newy}")

    def chooseOrientation(self, ratio, decal_w, decal_h):
        use_w = self.usableWidth - decal_w
        use_h = self.usableHeight - decal_h
        use_ratio = use_w / use_h
        if use_ratio < ratio:
            return tk.TOP
        else:
            return tk.LEFT

    def fullScreen(self, frame):
        frame.geometry(str(self))
        if songfinder.__myOs__ == "ubuntu":
            frame.attributes("-fullscreen", True)
        if songfinder.__myOs__ == "darwin":
            frame.tk.call(
                "::tk::unsupported::MacWindowStyle", "style", frame._w, "plain", "none"
            )  # pylint: disable=protected-access
            frame.update_idletasks()
            frame.wm_attributes("-fullscreen", True)
        else:
            frame.overrideredirect(1)
        logging.info(f"Fullscreen on: {str(self)}")

    def __repr__(self):
        return repr(str(self))


class Screens(object):
    def __init__(self):
        self._screens = []
        self._maxScreens = sys.maxsize

    def centerFrame(self, frame):
        if hasattr(frame, "master") and frame.master:
            for screen in self._screens:
                if screen.isWidgetInScreen(frame.master):
                    screen.centerFrame(frame)
                    break
        else:
            self._screens[0].centerFrame(frame)

    def resizeFrame(self, frame, width, height):
        for screen in self._screens:
            if screen.isWidgetInScreen(frame):
                screen.resizeFrame(frame, width, height)
                break

    def fullScreen(self, frame):
        self[-1].fullScreen(frame)

    def __getitem__(self, index):
        if index > len(self):
            raise IndexError
        return self._screens[(index % len(self)) % self._maxScreens]

    def __len__(self):
        if not self._screens:
            self.update()
        return len(self._screens)

    @property
    def maxScreens(self):
        return self._maxScreens

    @maxScreens.setter
    def maxScreens(self, value):
        self._maxScreens = int(value)

    def update(self, referenceWidget=None, verbose=True):
        del self._screens[:]
        try:
            monitors = screeninfo.get_monitors()
        except Exception:  # pylint: disable=broad-except
            logging.debug(traceback.format_exc())
            monitors = []
        if monitors:
            for monitor in monitors:
                self._screens.append(
                    Screen(monitor.width, monitor.height, monitor.x, monitor.y)
                )
        else:
            logging.warning("Screeninfo did not output any screen infos")
            if songfinder.__myOs__ == "windows":
                self._getWindowsScreens()
            elif songfinder.__myOs__ == "ubuntu":
                self._getLinuxScreens()
            elif songfinder.__myOs__ == "darwin":
                self._getMacOsScreens()
            else:
                logging.warning("No screen found, OS is not supported.")
                self._getLinuxScreens()

        if referenceWidget:
            self._reorder(referenceWidget)
        if verbose:
            logging.info(f"Using {len(self._screens)} screens: ")
            for screen in self._screens:
                logging.info(f"Fullscreen: {str(screen)}, Usable: {screen.usable}")

    def _reorder(self, referenceWidget):
        for i, screen in enumerate(self._screens):
            if screen.isWidgetInScreen(referenceWidget):
                self._screens[0], self._screens[i] = self._screens[i], self._screens[0]
                logging.debug(
                    "Reordering screens: %s"
                    % (", ".join([str(screen) for screen in self._screens]))
                )
                return None
        logging.warning(
            "Main widget did not appear to be in any screen!\n"
            "\tWidget info:\n"
            "\t\tgeometry: %s\n"
            "\t\trootx: %d\n"
            "\t\trooty: %d\n"
            "\tScreens:\n\t\t%s"
            % (
                referenceWidget.winfo_geometry(),
                referenceWidget.winfo_rootx(),
                referenceWidget.winfo_rooty(),
                "\n\t\t".join([str(screen) for screen in self._screens]),
            )
        )
        # Try again with a less reliable method (comparing only screen size)
        # Will not work if several screen have the same sizes
        for i, screen in enumerate(self._screens):
            if screen.isWidgetScreenSizeMine(referenceWidget):
                self._screens[0], self._screens[i] = self._screens[i], self._screens[0]
                logging.debug(
                    "Reordering screens: %s"
                    % (", ".join([str(screen) for screen in self._screens]))
                )
                return None

    def _getLinuxScreens(self):
        if not self._getXrandrScreen():
            logging.warning("Could not get screen infos with xrand method")
            if not self._getByTopLevelScreens():
                logging.warning("Could not get screen infos with TopLevel method")
                self._getDefaultScreen()

    def _getWindowsScreens(self):
        if not self._getWindowsTopLevelScreens():
            logging.warning("Could not get screen infos with Windows TopLevel method")
            self._getDefaultScreen()

    def _getMacOsScreens(self):
        if not self._getXrandrScreen():
            logging.warning("Could not get screen infos with xrand method")
            if not self._getWindowServerScreens():
                logging.warning("Could not get screen infos with WindowServer method")
                if not self._getSystemProfilerScreens():
                    logging.warning("Could not get screen infos with Profiler method")
                    if not self._getByTopLevelScreens():
                        logging.warning(
                            "Could not get screen infos with TopLevel method"
                        )
                        self._getDefaultScreen()

    def _getDefaultScreen(self):
        self._screens.append(Screen())

    def _getXrandrScreen(self):
        xrandr = commandLine.MyCommand("xrandr")
        try:
            xrandr.checkCommand()
        except exception.CommandLineError:
            return False
        else:
            code, out, err = xrandr.run(["|", "grep", "\\*", "|", "cut", "-d ", "-f4"])
            if code != 0:
                logging.warning(
                    f"Erreur de detection des ecrans\nError {str(code)}\n{err}"
                )
                return False
            liste_res = out.strip("\n").splitlines()
            if "" in liste_res:
                liste_res.remove("")
            if not liste_res:
                liste_res = []
                code, out, err = xrandr.run(["|", "grep", "connected"])
                if code != 0:
                    logging.warning(
                        f"Erreur de detection des ecrans\nError {str(code)}\n{err}"
                    )
                    return False
                line_res = out.replace("\n", "")
                deb = line_res.find("connected")
                fin = line_res.find("+", deb + 1)
                deb = line_res.rfind(" ", 0, fin)
                liste_res.append(line_res[deb + 1 : fin])

            code, out, err = xrandr.run()
            if code != 0:
                logging.warning(
                    f"Erreur de detection des ecrans: Error {str(code)}\n{err}"
                )
                return False
            deb = 0
            for res in liste_res:
                deb = out.find(res + "+", deb)
                fin = out.find(" ", deb)
                addScreen = Screen(stringScreen=out[deb:fin])
                if addScreen:
                    self._screens.append(addScreen)
                else:
                    return False
                deb = fin + 1
        return True

    def _getWindowsTopLevelScreens(self):
        try:
            test = tk.Toplevel()
        except tk.TclError:
            return False
        else:
            test.wm_attributes("-alpha", 0)
            test.withdraw()
            test.update_idletasks()
            test.overrideredirect(1)
            test.state("zoomed")
            test.withdraw()
            w1 = test.winfo_width()
            h1 = test.winfo_height()
            posw1 = test.winfo_x()
            posh1 = test.winfo_y()
            test.state("normal")
            test.withdraw()
            addScreen = Screen(w1, h1, posw1, posh1)
            if addScreen:
                self._screens.append(addScreen)
            else:
                return False
            # Scan for second screen
            test.overrideredirect(1)
            for decal in [
                [w, h] for w in [w1, w1 // 2, -w1 // 8] for h in [h1 // 2, h1, -h1 // 8]
            ]:
                test.geometry(f"{w1 // 8}x{h1 // 8}+{decal[0]}+{decal[1]}")
                test.update_idletasks()
                test.state("zoomed")
                test.withdraw()
                if test.winfo_x() != posw1 or test.winfo_y() != posh1:
                    newW = test.winfo_width()
                    newH = test.winfo_height()
                    newPosW = test.winfo_x()
                    newPosH = test.winfo_y()
                    addScreen = Screen(
                        width=newW, height=newH, xposition=newPosW, yposition=newPosH
                    )
                    if addScreen:
                        self._screens.append(addScreen)
                    else:
                        return False
                test.state("normal")
                test.withdraw()
            test.destroy()
            return True

    def _getWindowServerScreens(self):
        read = commandLine.MyCommand("defaults read")
        try:
            read.checkCommand()
        except exception.CommandLineError:
            return False
        code, _, err = read.run(["/Library/Preferences/com.apple.windowserver.plist"])
        if code != 0:
            logging.warning(f"Erreur de detection des ecrans\nError {str(code)}\n{err}")
            return False
        return False

    def _getSystemProfilerScreens(self):
        systemProfiler = commandLine.MyCommand("system_profiler")
        try:
            systemProfiler.checkCommand()
        except exception.CommandLineError:
            return False
        keyWord = "Resolution:"
        code, out, err = systemProfiler.run(
            ["SPDisplaysDataType", "|", "grep", keyWord]
        )
        if code != 0:
            logging.warning(f"Erreur de detection des ecrans\nError {str(code)}\n{err}")
            return False
        widthOffset = 0
        heightOffset = 0
        for line in [line for line in out.split("\n") if line]:
            deb = line.find(keyWord) + len(keyWord)
            end = line.find("x", deb)
            width = line[deb:end].strip(" ")
            height = line[end + 1 : line.find(" ", end + 2)].strip(" ")
            addScreen = Screen(
                width=width,
                height=height,
                xposition=widthOffset,
                yposition=heightOffset,
            )
            if addScreen:
                self._screens.append(addScreen)
            else:
                return False
            widthOffset = width
        return True

    def _getByTopLevelScreens(self):
        try:
            test = tk.Toplevel()
        except tk.TclError:
            return False
        else:
            test.wm_attributes("-alpha", 0)
            test.withdraw()
            test.update_idletasks()
            scrW = test.winfo_screenwidth()
            scrH = test.winfo_screenheight()
            test.destroy()
            if scrW > 31 * scrH // 9:
                scrW = scrW // 2
            elif scrW < 5 * scrH // 4:
                scrH = scrH // 2
            addScreen = Screen(width=scrW, height=scrH)
            if addScreen:
                self._screens.append(addScreen)
            else:
                return False
            return True


def getRatio(ratio, default=None):
    try:
        a, b = ratio.split("/")
        value = round(int(a) / int(b), 3)
    except (ValueError, AttributeError):
        logging.log(0, traceback.format_exc())
        if default:
            value = default
        else:
            value = 16 / 9
    return value
