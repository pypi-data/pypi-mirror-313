# -*- coding: utf-8 -*-
# cython: language_level=3

import os

try:
    from songfinder import libLoader

    module = libLoader.load(__file__)
    globals().update(
        {n: getattr(module, n) for n in module.__all__}
        if hasattr(module, "__all__")
        else {k: v for (k, v) in module.__dict__.items() if not k.startswith("_")}
    )
except (ImportError, NameError):
    # logging.info(traceback.format_exc())

    import sys

    from songfinder import fonctions as fonc
    from songfinder import classPaths
    from songfinder import pyreplace
    from songfinder import classSettings as settings

    def clean_line(text):
        for _ in range(5):
            text = text.replace("\n\n", "\n")
            text = text.replace("\n \n", "\n")
        newline = settings.GENSETTINGS.get("Syntax", "newline")
        text = text.replace(newline, "")
        return text

    def numerote(text, numero, nombre, etype="song"):
        if nombre > 1 or settings.PRESSETTINGS.get(etype, "oneslide"):
            if settings.PRESSETTINGS.get(etype, "Numerote_diapo"):
                if numero:
                    text = "(%s/%s)%s" % (str(numero), str(nombre), text)
        return text

    def print_title(text, title, numero, etype):
        if settings.PRESSETTINGS.get(etype, "Print_title"):
            if numero == 1:
                text = "%s\n%s" % (title.upper(), text)
        return text

    def check_bis(text, etype="song"):
        if settings.PRESSETTINGS.get(etype, "Check_bis"):
            numDict = {"2": "bis", "3": "ter", "4": "quarter"}
            for num, litteral in numDict.items():
                text = (
                    text.replace("(x%s)" % num, "(%s)" % litteral)
                    .replace("(X%s)" % num, "(%s)" % litteral)
                    .replace("(%sx)" % num, "(%s)" % litteral)
                    .replace("(%sX)" % num, "(%s)" % litteral)
                    .replace("(× %s)" % num, "(%s)" % litteral)
                    .replace("(* %s)" % num, "(%s)" % litteral)
                    .replace("X%s" % num, "(%s)" % litteral)
                    .replace("x%s" % num, "(%s)" % litteral)
                    .replace("%sx" % num, "(%s)" % litteral)
                    .replace("%sX" % num, "(%s)" % litteral)
                )
                text = text.replace(
                    "\n (%s)" % litteral, "\n(%s)" % fonc.upper_first(litteral)
                )
                text = text.replace(
                    "\n(%s)" % litteral, "\n(%s)" % fonc.upper_first(litteral)
                )
        return text

    def clean_maj(text, etype="song"):
        # Must be before maj at starting lines
        # Must be after check of ponctuation but maybe not
        if settings.PRESSETTINGS.get(etype, "Clean_majuscule"):
            text = text + " "
            postPonct = [",", ".", " ", "\n"]
            list_pronoms = [
                "Oint",
                "Sa",
                "Ta",
                "Il",
                "Tu",
                "Te",
                "Toi",
                "Son",
                "Ses",
                "Tes",
                "Ton",
                "Nom",
                "Lui",
                "Roi",
                "Celui",
                "Agneau",
                "Fils",
            ]
            for pronom in list_pronoms:
                for ponct in postPonct:
                    text = text.replace(pronom + ponct, pronom.lower() + ponct)
            text = text.strip(" ")
        return text

    def majuscule(text, etype="song"):
        if settings.PRESSETTINGS.get(etype, "Majuscule"):
            lignes = text.splitlines()
            lignes = [ligne.strip(" ") for ligne in lignes if ligne.strip(" ") != ""]
            new_lignes = []
            for ligne in lignes:
                ligne = fonc.upper_first(ligne)
                if ligne[0] == '"' or ligne[0] == "'" or ligne[0] == "(":
                    ligne = ligne[0] + fonc.upper_first(ligne[1:])
                new_lignes.append(ligne)

            text = "\n".join(new_lignes)
        return text

    def enleve_ponctuation(text):
        return (
            text.replace(".", " ")
            .replace(",", " ")
            .replace(";", " ")
            .replace(":", " ")
            .replace("!", " ")
            .replace("'", " ")
            .replace("?", " ")
            .replace("  ", " ")
            .replace("_", " ")
            .replace("-", " ")
        )

    def verifie_ponctuation(text, etype="song"):
        # verification ponctuation
        if settings.PRESSETTINGS.get(etype, "Ponctuation"):
            ponctuations0 = [":"]
            for car in ponctuations0:
                text = text.replace(car, " %s " % car).replace("  ", " ")
            ponctuations1 = [";", "!", "?"]
            for car in ponctuations1:
                text = (
                    text.replace(car, " %s " % car)
                    .replace("  ", " ")
                    .replace('%s "' % car, '%s"' % car)
                )
            ponctuations2 = [".", ","]
            for car in ponctuations2:
                text = (
                    text.replace(car, "%s " % car)
                    .replace("  ", " ")
                    .replace('%s "' % car, '%s"' % car)
                )
            text = text.replace(" \n", "\n")
            for _ in range(5):
                text = text.replace(". .", "..")
            for ponct in ponctuations0 + ponctuations1 + ponctuations2:
                text = text.replace("%s )" % ponct, "%s)" % ponct)
        return text

    def verifie_ponctuation_maj(text, etype="song"):
        # Majuscule après les points ? et !
        if settings.PRESSETTINGS.get(etype, "Ponctuation"):
            ponctuations_maj = ["!", "?", "."]
            for ponct in ponctuations_maj:
                deb = 0
                while text.find(ponct, deb) != -1:
                    index = text.find(ponct, deb)
                    if len(text) > index + 3:
                        text = (
                            text[: index + 2]
                            + text[index + 2].upper()
                            + text[index + 3 :]
                        )
                    deb = index + 1
        return text

    def newSongTitle(title, max_sup):
        if not ((title[:3] == "JEM" or title[:3] == "SUP") and title[3:6].isdigit()):
            title = "SUP" + str(max_sup + 1) + " " + title

        chemin_chants = classPaths.PATHS.songs
        chemin = os.path.join(
            chemin_chants,
            fonc.enleve_accents(title)
            + settings.GENSETTINGS.get("Extentions", "song")[0],
        )
        return chemin, title

    def saut_ligne(text, max_car, etype="song", force=None):
        newLineSuggest = r"\newline"
        liste_sep = [newLineSuggest, ".", "!", "?", " et ", " Et ", ";", ","]
        liste_sep_after = [" et ", " Et ", ":"]
        do_not = ["(bis)", "(Bis)"]
        new_text = text
        if settings.PRESSETTINGS.get(etype, "Saut_ligne") or force == "force":
            for i in range(5):
                lignes = new_text.splitlines()
                new_text = ""
                for ligne in lignes:
                    trouve = -1

                    if len(ligne) > max_car and ligne.find("\\ac") == -1:
                        ind = len(ligne) * 2 // 5
                        for sep in liste_sep:
                            trouve = ligne.find(sep, ind, -1)
                            if trouve > -1:
                                if sep in liste_sep_after:
                                    plus = 0
                                else:
                                    plus = len(sep)
                                if (
                                    ligne[trouve + len(sep) + 1 : trouve + len(sep) + 6]
                                    not in do_not
                                ):
                                    new_text = new_text + ligne[: trouve + plus] + "\n"
                                    new_text = new_text + ligne[trouve + plus :] + "\n"
                                    break
                    if trouve == -1:
                        new_text = new_text + ligne + "\n"
            if settings.PRESSETTINGS.get(etype, "Saut_ligne_force") or force == "force":
                lignes = new_text.splitlines()
                new_text = ""
                for ligne in lignes:
                    trouve = -1
                    longueur = len(ligne)
                    if longueur > max_car:
                        div = (longueur + max_car - 1) // max_car
                        new_longueur = longueur // div
                        trouve = ligne.find(" ", new_longueur, -1)
                        new_text = new_text + " " + ligne[: trouve + 1] + "\n"
                        if div > 2:
                            for i in range(div - 2):
                                trouve1 = ligne.find(" ", (i + 1) * new_longueur, -1)
                                trouve = ligne.find(" ", (i + 2) * new_longueur, -1)
                                new_text = (
                                    new_text
                                    + " "
                                    + ligne[trouve1 + 1 : trouve + 1]
                                    + "\n"
                                )
                        new_text = new_text + " " + ligne[trouve + 1 :] + "\n"

                    if trouve == -1:
                        new_text = new_text + ligne + "\n"

        new_text = new_text.replace(newLineSuggest, "")

        for sep in set(liste_sep) - set(liste_sep_after):
            new_text = (
                new_text.replace("\n%s" % sep, "%s\n" % sep)
                .replace("\n %s" % sep, "%s\n " % sep)
                .replace("%s\n)" % sep, "%s)\n" % sep)
                .replace('%s\n"' % sep, '%s"\n' % sep)
                .replace("%s\n" "" % sep, "%s" "\n" % sep)
            )
        for sep in [":", ": "]:
            new_text = new_text.replace('%s"\n' % sep, '%s\n"' % sep).replace(
                "%s" "\n" % sep, "%s\n" "" % sep
            )
        return new_text

    def nettoyage(text):
        newslide = settings.GENSETTINGS.get("Syntax", "newslide")
        newline = settings.GENSETTINGS.get("Syntax", "newline")

        text = (
            text.replace(". .", "..")
            .replace(". .", "..")
            .replace("\u2018", "'")
            .replace("\u2019", "'")
            .replace("\u0020", " ")
            .replace("\u00A0", " ")
        )

        text = pyreplace.cleanupChar(text.encode("utf-8"))
        text = pyreplace.cleanupSpace(text).decode("utf-8")

        for _ in range(2):
            text = text.strip(" _\n")
            text = fonc.strip_perso(text, newline)
        for newslideSyntax in newslide:
            text = text.replace("\n" + newslideSyntax, "\n\n" + newslideSyntax)

        return text

    def getListStypePlus(listStype):
        # Trouve les suite de type de diapo
        i = 0
        previous = ""
        listStypePlus = []  # (type, list des numero)
        tmp = []
        for k, stype in enumerate(listStype):
            tmp.append(k - 1)
            if stype == previous:
                i = i + 1
            else:
                listStypePlus.append((previous, tmp))
                i = 0
                tmp = []
            previous = stype

        tmp.append(len(listStype) - 1)
        listStypePlus.append((previous, tmp))
        del listStypePlus[0]
        return listStypePlus

    # ~ def getPlusIndex(listStypePlus, index):
    # ~ for plusIndex, (Stype, numList) in enumerate(listStypePlus):
    # ~ if index in numList:
    # ~ return plusIndex

    def getPlusNum(listStypePlus, index):
        for _, numList in listStypePlus:
            if index in numList:
                return len(numList)
        return 0

    def getIndexes(liste, elem):
        return [i for i, j in enumerate(liste) if j == elem]

    def applyMaxNumberLinePerDiapo(listText, listStype, nbMaxLine):
        if nbMaxLine > 0:
            index = 0
            counter = 0
            listTextOutput = []
            listStypeOutput = []

            newline = settings.GENSETTINGS.get("Syntax", "newline")

            for numDiapo, text in enumerate(listText):
                lines = text.split("\n")
                # Remove line breacks if needed
                if len(lines) > nbMaxLine:
                    text = text.replace("%s\n" % newline, "")
                    lines = text.split("\n")

                # Copie severals times a diapo if it is bis or ter
                numIter = 1
                repetLines = []
                if len(lines) > nbMaxLine:
                    # Get all the repet syntax present in a diapo
                    for numLine, line in enumerate(lines):
                        if line.lower() == "(bis)":
                            numIter = 2
                            repetLines.append(numLine)
                        elif line.lower() == "(x2)":
                            numIter = 2
                            repetLines.append(numLine)
                        elif line.lower() == "(ter)":
                            numIter = 3
                            repetLines.append(numLine)
                        elif line.lower() == "(x3)":
                            numIter = 3
                            repetLines.append(numLine)

                # only take into account last repet syntax for now
                try:
                    repetLines = [repetLines[-1]]
                except IndexError:
                    pass
                else:
                    # Delete Lines containing bis ter etc.
                    for offset, numLine in enumerate(repetLines):
                        del lines[numLine - offset]
                        # Update repetLine array to contains new diapo numbers correponding to repetition
                        repetLines[offset] = numLine - offset

                nbDiapo = (len(lines) + nbMaxLine - 1) // nbMaxLine
                linePerDiapo = (len(lines) + nbDiapo - 1) // nbDiapo

                for iteration in range(numIter):
                    # Stop at the repet syntax except for the last repetition
                    try:
                        if iteration == numIter - 1:
                            raise IndexError
                        # only take into account last repet syntax for now
                        stopLine = repetLines[-1]
                    except IndexError:
                        stopLine = sys.maxsize

                    for lineNumber, line in enumerate(lines):
                        # Stop at the repet syntax except for the last repetition
                        if lineNumber == stopLine:
                            counter = 0
                            index += 1
                        else:
                            try:
                                # Append to current diapo
                                listTextOutput[index] += "\n" + line
                            except IndexError:
                                # Create new diapo
                                listTextOutput.append(line)
                                listStypeOutput.append(listStype[numDiapo])
                            # New diapo if max number of line or and of diapo reached
                            if (
                                counter < linePerDiapo - 1
                                and lineNumber < len(lines) - 1
                            ):
                                counter += 1
                            else:
                                counter = 0
                                index += 1
        else:
            listStypeOutput = listStype
            listTextOutput = listText

        return listTextOutput, listStypeOutput

    def netoyage_paroles(paroles):
        newline = settings.GENSETTINGS.get("Syntax", "newline")
        newslide = settings.GENSETTINGS.get("Syntax", "newslide")

        paroles = fonc.enleve_accents_unicode(paroles)
        paroles = "%s\n" % paroles
        paroles = fonc.supressB(paroles, "\\ac", "\n")
        paroles = paroles.strip("\n")
        for newslideSyntax in newslide:
            paroles = paroles.replace(newslideSyntax, "")

        paroles = (
            paroles.replace(newline, "")
            .replace("\u2019", " ")
            .replace("\u2018", " ")
            .replace("\u0020", " ")
            .replace("\u00A0", " ")
        )

        paroles = paroles.replace(newline, "")
        paroles = paroles.lower()

        paroles = pyreplace.simplifyChar(paroles.encode("utf-8"))
        paroles = pyreplace.cleanupSpace(paroles).decode("utf-8")

        paroles = paroles.strip(" ")
        return paroles
