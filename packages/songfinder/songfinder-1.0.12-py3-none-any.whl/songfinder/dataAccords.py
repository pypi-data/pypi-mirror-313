# -*- coding: utf-8 -*-
from collections import OrderedDict


class AccordsData(object):
    def __init__(self):
        self.accordsTon = ["Do", "Ré", "Mi", "Fa", "Sol", "La", "Si"]
        self.accordsTonang = ["C", "D", "E", "F", "G", "A", "B"]
        self.execpt = {"B#": "C", "E#": "F", "Cb": "B", "Fb": "E"}
        self.ordreDiez = ["F", "C", "G", "D", "A", "E", "B"]
        alterations = ["b", "", "#"]
        parfait = ["", "m"]
        self.modulation = [
            "",
            "2",
            "sus2",
            "4",
            "sus4",
            "5",
            "6",
            "maj6",
            "7M",
            "M7",
            "maj7",
            "MA7",
            "7",
            "9",
            "add9",
            "°7",
            "dim7",
            "°",
            "dim",
        ]
        # Order is important for ex: sus4 must be applied befor sus correction
        self.dicoCompact = OrderedDict(
            [
                ("sus2", "2"),
                ("sus4", "4"),
                ("sus", "4"),
                ("add9", "9"),
                ("maj6", "6"),
                ("maj7", "M7"),
                ("MA7", "M7"),
                ("dim", "°"),
            ]
        )

        self.accordsDie = []
        self.accordsBem = []
        self.accPossible = []
        self.accSimple = []
        for acc in self.accordsTonang:
            for alt in alterations:
                if acc + alt not in self.execpt:
                    if alt in ["", "#"]:
                        self.accordsDie.append(acc + alt)
                    if alt in ["b", ""]:
                        self.accordsBem.append(acc + alt)
                    for par in parfait:
                        self.accSimple.append((acc + alt + par))
                        for mod in self.modulation:
                            self.accPossible.append((acc + alt + par + mod))
