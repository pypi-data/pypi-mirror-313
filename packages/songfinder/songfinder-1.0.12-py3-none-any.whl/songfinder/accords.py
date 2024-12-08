# -*- coding: utf-8 -*-

import warnings
import re
from enum import Enum

from songfinder import fonctions as fonc
from songfinder import dataAccords
from songfinder import corrector
from songfinder import classSettings as settings

ACCORDSDATA = dataAccords.AccordsData()
CORRALL = corrector.Corrector(";".join(ACCORDSDATA.accPossible))

language = Enum("language", ["FR", "EN", "DEG"])


class Accords(object):
    def __init__(
        self,
        ligneAcc,
        data=None,
        transposeNb=0,
        capo=0,
        corrAll=None,
        exportSettings=None,
    ):
        self.data = data
        self._ligneAcc = ligneAcc
        self._transposeNb = transposeNb
        self._capo = capo
        self._accords = None

        if not corrAll:
            self.corrAll = CORRALL
        if not data:
            self.data = ACCORDSDATA
        if not exportSettings:
            self._exportSettings = settings.LATEXSETTINGS
        else:
            self._exportSettings = exportSettings

        self._haveLeftBracket = set()
        self._haveRightBracket = set()

        self._clean()
        self._getLigne()
        self._compactChord()

    def getChords(self, key=None):
        if self._exportSettings.get("Export_Parameters", "transpose"):
            self._transpose(self._transposeNb)
        if self._exportSettings.get("Export_Parameters", "capo") and self._capo:
            self._transpose(-self._capo)
        if self._exportSettings.get("Export_Parameters", "simple_chords"):
            self._simplifyChord()
        if self._exportSettings.get("Export_Parameters", "keep_first"):
            self._keepFirst()
        if self._exportSettings.get("Export_Parameters", "keep_last"):
            self._keepLast()
        if self._exportSettings.get("Export_Parameters", "sol_chords"):
            self._translate(language.FR)
        if self._exportSettings.get("Export_Parameters", "num_chords"):
            if key is not None:
                self._translate(language.DEG, key=key)
        self._putBrackets()
        self._noDoublon()
        return self._accords

    def _noDoublon(self):
        newChords = []
        previous = None
        for accord in self._accords:
            if not previous or accord.replace(")", "") != previous.replace("(", ""):
                newChords.append(accord)
            elif not accord.find(")") == -1:
                newChords[-1] = f"{newChords[-1]})"
            previous = accord
        self._accords = newChords

    def _clean(self):
        self._ligneAcc = self._ligneAcc
        if not self._ligneAcc:
            warnings.warn("Empty chord")
            self._ligneAcc = ""
            return

        self._ligneAcc = self._ligneAcc.strip(" ")
        self._ligneAcc = fonc.strip_perso(self._ligneAcc, "\n")
        self._ligneAcc = fonc.strip_perso(self._ligneAcc, "\\ac")
        self._ligneAcc = self._ligneAcc.strip(" ")

        for _ in range(5):
            self._ligneAcc = self._ligneAcc.replace("  ", " ")

    def _getLigne(self):
        self._accords = self._ligneAcc.split(" ")
        # Checkif has brackets and removes them
        for i, accord in enumerate(self._accords):
            if accord:
                if accord[0] == "(":
                    self._haveLeftBracket.add(i)
                    accord = accord[1:]
                if accord[-1] == ")":
                    self._haveRightBracket.add(i)
                    accord = accord[:-1]
            self._accords[i] = accord

        self._translate(language.EN)

        for i, accord in enumerate(self._accords):
            if accord[:2] in self.data.execpt:
                accord = self.data.execpt[accord[:2]] + accord[2:]

            if self.corrAll:
                accord = "/".join(
                    [self.corrAll.check(partAcc) for partAcc in accord.split("/")]
                )
            parts = accord.split("/")
            for j, part in enumerate(parts):
                try:
                    parts[j] = self.data.execpt[part]
                except KeyError:
                    pass
            self._accords[i] = "/".join(parts)

    def _putBrackets(self):
        for index in self._haveLeftBracket:
            self._accords[index] = f"({self._accords[index]}"
        for index in self._haveRightBracket:
            self._accords[index] = f"{self._accords[index]})"

    def _translate(self, lang=language.FR, key=None):
        for i, chord in enumerate(self._accords):
            parts = chord.split("/")
            for j, part in enumerate(parts):
                # Ignore multiplication in chords, that is normal
                if re.match(r"x\d{1,2}", part, re.IGNORECASE):
                    break
                part = fonc.upper_first(part)
                Chord(part).translate(lang, key=key)
                parts[j] = str(Chord(part).translate(lang, key=key))
            self._accords[i] = "/".join(parts)

    def _compactChord(self):
        for i, chord in enumerate(self._accords):
            for old, new in self.data.dicoCompact.items():
                chord = chord.replace(old, new)
            self._accords[i] = chord

    def _simplifyChord(self):
        for i, chord in enumerate(self._accords):
            parts = chord.split("/")
            for j, part in enumerate(parts):
                parts[j] = str(Chord(part).simplify)
            self._accords[i] = "/".join(parts)

    def _keepFirst(self):
        for i, chord in enumerate(self._accords):
            self._accords[i] = chord.split("/")[0]

    def _keepLast(self):
        for i, chord in enumerate(self._accords):
            try:
                self._accords[i] = chord.split("/")[1]
            except IndexError:
                self._accords[i] = chord.split("/")[0]

    def _nbAlt(self, accords):
        ind = 0
        for i, diez in enumerate(self.data.ordreDiez):
            if f"{diez}#" in [accord[:2] for accord in accords]:
                ind = i + 1
        for i, bemol in enumerate(reversed(self.data.ordreDiez)):
            if f"{bemol}b" in [accord[:2] for accord in accords]:
                ind = i + 1
        return ind

    def _transposeTest(self, accordsRef, accordsNon, demiTon):
        # Transposition
        newAccords = []
        for chord in accordsRef:
            if len(chord) > 1:
                refAlt = chord[-1]
                break

        for accord in self._accords:
            newPart = []
            for part in accord.split("/"):
                if len(part) > 1 and part[1] in ["#", "b"] and part[1] != refAlt:
                    part = accordsRef[accordsNon.index(part[:2])] + part[2:]
                pre = (
                    f"{part[:1]} {part[1:]}".replace(" #", "#")
                    .replace(" b", "b")[:2]
                    .strip(" ")
                )
                for i, ref in enumerate(accordsRef):
                    if pre == ref:
                        part = part.replace(
                            ref, accordsRef[(i + demiTon) % len(accordsRef)]
                        )
                        break
                newPart.append(part)
            newAccords.append("/".join(newPart))
        return newAccords

    def _transpose(self, demiTon):
        if demiTon:
            accords1 = self._transposeTest(
                self.data.accordsDie, self.data.accordsBem, demiTon
            )
            accords2 = self._transposeTest(
                self.data.accordsBem, self.data.accordsDie, demiTon
            )
            if self._nbAlt(accords2) >= self._nbAlt(accords1):
                self._accords = accords1
            else:
                self._accords = accords2


class Chord:
    def __init__(self, chord_str):
        self._str = chord_str
        self._str = self._str.replace("Re", "Ré")

        self._check()

    def __str__(self):
        return self._str

    def __eq__(self, other):
        return self.translate(language.EN)._str == other.translate(language.EN)._str

    def _check(self):
        work_chord = self.translate(language.EN)
        if not str(work_chord) or str(work_chord)[0] not in ACCORDSDATA.accordsTonang:
            warnings.warn(f"Unknown chord '{work_chord}'")

    @property
    def _is_major(self):
        if re.match(r".+m", self._str):
            return False
        return True

    @property
    def _relative_major(self):
        if self._is_major:
            return self.translate(language.EN)._to_sharp
        else:
            work_chord = self.translate(language.EN)._to_sharp
            stripped_chord = re.sub(r"(.+)m", r"\1", str(work_chord))
            index = ACCORDSDATA.accordsDie.index(stripped_chord)
            relative_str = ACCORDSDATA.accordsDie[(index + 3) % 12]
            return Chord(relative_str)

    @property
    def _relative_minor(self):
        if self._is_major:
            work_chord = self.translate(language.EN)._to_sharp
            index = ACCORDSDATA.accordsDie.index(str(work_chord))
            relative_str = ACCORDSDATA.accordsDie[(index - 3) % 12]
            return Chord(f"{relative_str}m")
        else:
            return self.translate(language.EN)._to_sharp

    @property
    def _to_sharp(self):
        if not re.search(r"b", self._str):
            return self.translate(language.EN)
        else:
            eng_chord = self.translate(language.EN)
            striped_chord = re.sub(r"([A-Z]b).*", r"\1", str(eng_chord))
            index = ACCORDSDATA.accordsBem.index(striped_chord)
            return Chord(ACCORDSDATA.accordsDie[index])

    @property
    def _to_flat(self):
        if not re.search(r"#", self._str):
            return self.translate(language.EN)
        else:
            eng_chord = self.translate(language.EN)
            striped_chord = re.sub(r"([A-Z]#).*", r"\1", str(eng_chord))
            index = ACCORDSDATA.accordsDie.index(striped_chord)
            return Chord(ACCORDSDATA.accordsBem[index])

    @property
    def num(self):
        try:
            return ACCORDSDATA.accordsDie.index(str(self._relative_major))
        except ValueError:
            return ACCORDSDATA.accordsBem.index(str(self._relative_major))

    @property
    def simplify(self):
        simp_chord = str(self)
        for spe in ACCORDSDATA.modulation:
            simp_chord = simp_chord.replace(spe, "")
        return Chord(simp_chord)

    def _get_relative_notation(self, key):
        """Returns the chord numerotation notation relative to the given key.

        Args:
            key (str): The key to get the relative notation from (e.g. 'C', 'Am')

        Returns:
            str: Roman numeral notation of the chord relative to the key
        """
        if key is None:
            raise ValueError("Reference key is None")

        # Convert key to Chord object for easier manipulation
        key_chord = Chord(key)

        # Get the major chord (if chord is minor, get its relative major)
        if key_chord._is_major:
            chord_major = self.simplify
        else:
            chord_major = self._relative_major.simplify

        # Get the major key reference (if key is minor, get its relative major)
        if key_chord._is_major:
            key_chord_major = key_chord
        else:
            key_chord_major = key_chord._relative_major

        # Calculate the interval between the chord and the key
        key_pos = key_chord_major.num
        chord_pos = chord_major.num
        interval = (chord_pos - key_pos) % 12

        # Define the roman numerals for major and minor
        major_numerals = ["I", "II", "III", "IV", "V", "VI", "VII"]
        minor_numerals = ["i", "ii", "iii", "iv", "v", "vi", "vii"]

        # Map intervals to scale degrees (0=I, 2=II, 4=III, 5=IV, 7=V, 9=VI, 11=VII)
        interval_to_degree = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}

        # Get the scale degree
        if interval not in interval_to_degree:
            return "?"  # Return ? for chords not in the diatonic scale

        degree = interval_to_degree[interval]

        # Choose numerals based on chord quality
        numerals = minor_numerals if not self._is_major else major_numerals

        # If chord is minor key, shift the numerals
        if not self._is_major:
            degree = (degree - 2) % 7

        # If key is minor, shift the numerals
        if not key_chord._is_major:
            degree = (degree + 2) % 7

        translation = re.sub(
            r"%s(.*)" % self.simplify,
            r"%s\1" % numerals[degree],
            str(self),
            re.IGNORECASE,
        )
        return translation

    def translate(self, lang, key=None):
        assert lang in language

        if lang == language.DEG:
            return self._get_relative_notation(key)

        from_chords, to_chords = [], []
        from_M7, to_M7 = "", ""
        if lang == language.FR:
            from_chords, to_chords = ACCORDSDATA.accordsTonang, ACCORDSDATA.accordsTon
            from_M7, to_M7 = "M7", "7M"
        elif lang == language.EN:
            from_chords, to_chords = ACCORDSDATA.accordsTon, ACCORDSDATA.accordsTonang
            from_M7, to_M7 = "7M", "M7"

        for i, chord in enumerate(from_chords):
            base_translation = to_chords[i]
            translation = re.sub(
                r"%s(.*)" % chord, r"%s\1" % base_translation, str(self), re.IGNORECASE
            )
            if translation != self._str and translation not in ["Faa", "Réo"]:
                return Chord(translation.replace(from_M7, to_M7))
        return self
