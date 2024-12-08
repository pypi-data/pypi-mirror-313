# -*- coding: utf-8 -*-

import os

import tkinter as tk
import tkinter.ttk as ttk

import shutil
import filecmp
from songfinder import messages as tkMessageBox
from songfinder import messages as tkFileDialog  # pylint: disable=reimported

import songfinder
from songfinder import classPaths
from songfinder import classSettings as settings
from songfinder.gui import guiHelper
from songfinder import background
from songfinder import fonctions as fonc


class ParamGen(object):
    def __init__(self, papa, screens=None):
        fenetre = tk.Toplevel()
        with guiHelper.SmoothWindowCreation(fenetre, screens=screens):
            fenetre.title("Paramètres généraux")

            fenetre.grid()
            self.fenetre = fenetre
            self.papa = papa
            self.paths = classPaths.PATHS
            self.settingName = "SettingsGen"

            self.reset_button = tk.Button(fenetre, text="Reset", command=self.reset)
            self.ext_image = settings.GENSETTINGS.get("Extentions", "image")
            self.FILETYPES_image = [
                (ext[1:].upper(), ext) for ext in self.ext_image
            ] + [("All files", "*.*")]

            self.mot_data = tk.Label(fenetre, text="Base de données local: ")
            self.data_button = tk.Button(
                fenetre, text="Sauver/parcourir", command=self.change_rep
            )
            self.data_str = tk.Entry(fenetre, width=50)

            self._paramDict = {
                "autoload": {
                    "text": "Charger la dernière liste au démarrage de SongFinder."
                },
                "sync": {
                    "text": "Synchroniser la base de données avec un dépôt en ligne."
                },
                "autoreceive": {
                    "text": "Recevoir automatiquement les changements au démarrage de SongFinder."
                },
                "highmemusage": {
                    "text": (
                        "Autoriser SongFinder à utiliser beaucoup de mémoire.\n"
                        "Cette option peut résoudre certains problèmes de performances."
                    )
                },
                "autoexpand": {
                    "text": "Etendre la fenêtre principal au démarrage de SongFinder."
                },
            }

            for i, (dictParameter, config) in enumerate(self._paramDict.items()):
                tkintVar = tk.IntVar()
                button = tk.Checkbutton(
                    fenetre,
                    text=config["text"],
                    variable=tkintVar,
                    command=lambda intVar=tkintVar, parameter=dictParameter: self.save_setting(
                        intVar, parameter
                    ),
                )
                config["button"] = button
                button.grid(row=i, column=0, columnspan=5, sticky="w")

            self.var_scm = tk.IntVar()
            self.scm_hg = tk.Radiobutton(
                fenetre,
                text="Mercurial (hg)",
                variable=self.var_scm,
                value=1,
                command=lambda intVar=self.var_scm, parameter="scm": self.save_setting(
                    intVar, parameter
                ),
            )
            self.scm_git = tk.Radiobutton(
                fenetre,
                text="Git",
                variable=self.var_scm,
                value=0,
                command=lambda intVar=self.var_scm, parameter="scm": self.save_setting(
                    intVar, parameter
                ),
            )

            self.scm_hg.grid(
                row=len(self._paramDict), column=0, columnspan=2, sticky="w"
            )
            self.scm_git.grid(
                row=len(self._paramDict) + 1, column=0, columnspan=2, sticky="w"
            )

            self.mot_data.grid(
                row=len(self._paramDict) + 2, column=0, columnspan=2, sticky="w"
            )
            self.data_str.grid(
                row=len(self._paramDict) + 2, column=2, columnspan=7, sticky="w"
            )
            self.data_button.grid(
                row=len(self._paramDict) + 2, column=9, columnspan=1, sticky="w"
            )
            self.reset_button.grid(row=len(self._paramDict) + 3, column=0, columnspan=2)

            self.maj()

    def maj(self):
        for parameter, config in self._paramDict.items():
            if settings.GENSETTINGS.get("Parameters", parameter):
                config["button"].select()
        self.data_str.delete(0, tk.END)
        self.data_str.insert(0, self.paths.root)
        if settings.GENSETTINGS.get("Parameters", "scm") == "hg":
            self.var_scm.set(1)
        elif settings.GENSETTINGS.get("Parameters", "scm") == "git":
            self.var_scm.set(0)

    def change_rep(self):
        chemin = self.data_str.get()
        if chemin == self.paths.root:
            self.paths.root = tkFileDialog.askdirectory(parent=self.fenetre)
        else:
            self.paths.root = chemin
        self.maj()
        self.papa.updateData()

    def save_setting(self, settingIntVar, parameter):
        value = bool(settingIntVar.get())
        settings.GENSETTINGS.set("Parameters", parameter, value)
        if parameter == "highmemusage":
            if value:
                background.BACKGROUNDS.resizeCache("high")
            elif value:
                background.BACKGROUNDS.resizeCache("low")
        if parameter == "sync" and value:
            classPaths.PATHS.sync()
        if parameter == "scm":
            if settingIntVar.get():
                value = "hg"
            else:
                value = "git"
            settings.GENSETTINGS.set("Parameters", parameter, value)
        self.maj()

    def reset(self):
        if tkMessageBox.askyesno(
            "Defaut", "Etes vous sur de remettre " "les paramètres par defaut ?"
        ):
            settings.GENSETTINGS.create()
            self.maj()

    def close(self):
        self.fenetre.destroy()


class ParamPres(object):
    def __init__(self, papa, screens=None):
        fenetre = tk.Toplevel()
        with guiHelper.SmoothWindowCreation(fenetre, screens=screens):
            fenetre.title("Paramètres de présentation")
            fenetre.grid()
            self.fenetre = fenetre
            self.papa = papa
            self.paths = classPaths.PATHS
            self.petit_mot_profil = tk.Label(fenetre, text="Profil: ")
            self.petit_mot_profil.grid(row=0, column=0, columnspan=3, sticky="w")

            self.settingName = "SettingsPres"

            self.fenetre_profil = None
            self.profil = ""
            self.liste_profil = []

            self.profil_selection = tk.StringVar()
            self.combobox_profil = ttk.Combobox(
                fenetre,
                textvariable=self.profil_selection,
                values=self.liste_profil,
                state="readonly",
            )
            self.combobox_profil.grid(row=0, column=3, columnspan=5)
            self.get_profil_liste()
            self.start_profil()

            self.etype = "song"

            self.petit_mot_type = tk.Label(fenetre, text="Paramètres pour le type: ")
            self.petit_mot_type.grid(row=1, column=0, columnspan=3, sticky="w")

            self.liste_etype = settings.GENSETTINGS.get("Syntax", "element_type")

            self.etype_selection = tk.StringVar()
            self.combobox_etype = ttk.Combobox(
                fenetre,
                textvariable=self.etype_selection,
                values=self.liste_etype,
                state="readonly",
            )
            self.combobox_etype.grid(row=1, column=3, columnspan=5)
            self.combobox_etype.set("song")

            self.ext_image = settings.GENSETTINGS.get("Extentions", "image")
            self.FILETYPES_image = [
                (ext[1:].upper(), ext) for ext in self.ext_image
            ] + [("All files", "*.*")]

            self.mot_background = tk.Label(fenetre, text="Arrière plan: ")
            self.background_button = tk.Button(
                fenetre, text="Sauver/parcourir", command=self.change_background
            )
            self.background_str = tk.Entry(fenetre, width=60)

            self.add_profil_button = tk.Button(
                fenetre,
                text="Sauvegarder le profil",
                command=self.fenetre_creation_profil,
            )

            self.dictParam = {
                "Numéroter les diapositives.": "Numerote_diapo",
                "Afficher le titre/commentaire.": "Print_title",
                "Enlever les majuscules aux pronoms.": "Clean_majuscule",
                "Mettre des majuscules en début de lignes.": "Majuscule",
                'Verifier les "bis".': "Check_bis",
                "Passer à la ligne en fonction de la ponctuation.": "Saut_ligne",
                "Passer à la lignes même sans ponctuation.": "Saut_ligne_force",
                "Vérifier les espaces autour des ponctuations.": "Ponctuation",
                "Numeroter les éléments ne contenant qu'une seul diapo.": "oneslide",
            }

            self.var_justification = tk.IntVar()
            self.justification_gauche = tk.Radiobutton(
                fenetre,
                text="Justifier à gauche.",
                variable=self.var_justification,
                value=0,
                command=self.save,
            )
            self.justification_centre = tk.Radiobutton(
                fenetre,
                text="Justifier au centre.",
                variable=self.var_justification,
                value=1,
                command=self.save,
            )
            self.justification_droite = tk.Radiobutton(
                fenetre,
                text="Justifier à droite.",
                variable=self.var_justification,
                value=2,
                command=self.save,
            )

            self.liste_mep_justification = [
                "left",
                "center",
                "right",
            ]

            self.var_fontColor = tk.IntVar()
            self.fontColor_white = tk.Radiobutton(
                fenetre,
                text="Police blanche",
                variable=self.var_fontColor,
                value=0,
                command=self.save,
            )
            self.fontColor_black = tk.Radiobutton(
                fenetre,
                text="Police noir",
                variable=self.var_fontColor,
                value=1,
                command=self.save,
            )
            self.liste_mep_fontColor = [
                "white",
                "black",
            ]

            self.liste_radioButton = [
                self.justification_gauche,
                self.justification_centre,
                self.justification_droite,
                self.fontColor_white,
                self.fontColor_black,
            ]

            self.var_size = tk.StringVar()
            self.mot_size = tk.Label(fenetre, text="Taille police: ")
            self.size_entry = tk.Entry(fenetre, textvariable=self.var_size, width=5)
            self.var_max_car = tk.StringVar()
            self.mot_max_car = tk.Label(fenetre, text="Taille des lignes: ")
            self.max_car_entry = tk.Entry(
                fenetre, textvariable=self.var_max_car, width=5
            )
            self.var_max_line = tk.StringVar()
            self.mot_max_line = tk.Label(fenetre, text="Lignes par diapo: ")
            self.max_line_entry = tk.Entry(
                fenetre, textvariable=self.var_max_line, width=5
            )
            self.save_sizes_button = tk.Button(
                fenetre, text="Sauver", command=self.save_sizes
            )

            self.combobox_etype.bind("<<ComboboxSelected>>", self.select_etype)
            self.combobox_profil.bind("<<ComboboxSelected>>", self.select_profil)

            for i, just in enumerate(self.liste_radioButton):
                just.bind("<ButtonRelease-1>", self.save)

            nb_boutton = len(self.dictParam)
            nb_justification = len(self.liste_radioButton)

            self.mot_background.grid(
                row=nb_boutton + 5 + nb_justification,
                column=0,
                columnspan=2,
                sticky="w",
            )
            self.background_str.grid(
                row=nb_boutton + 5 + nb_justification,
                column=2,
                columnspan=7,
                sticky="w",
            )
            self.background_button.grid(
                row=nb_boutton + 5 + nb_justification,
                column=9,
                columnspan=1,
                sticky="w",
            )
            self.add_profil_button.grid(
                row=nb_boutton + 12 + nb_justification,
                column=0,
                columnspan=10,
                sticky="ew",
            )

            column_width = 5
            nb_row = (nb_boutton + 1) // 2
            self.dictValeurs = dict()
            self.dictButton = dict()
            for i, (param, item) in enumerate(self.dictParam.items()):
                var = tk.IntVar()
                button = tk.Checkbutton(
                    fenetre, text=param, variable=var, command=self.save
                )
                self.dictValeurs[param] = var
                self.dictButton[item] = button
                column_num = i // nb_row * (column_width + 1)
                button.grid(
                    row=i % nb_row + 3,
                    column=column_num,
                    columnspan=column_width,
                    sticky="w",
                )

            for i, just in enumerate(self.liste_radioButton):
                just.grid(row=nb_row + 3 + i, column=0, columnspan=5, sticky="w")

            self.mot_size.grid(
                row=nb_boutton + 8 + nb_justification,
                column=0,
                columnspan=2,
                sticky="w",
            )
            self.size_entry.grid(
                row=nb_boutton + 8 + nb_justification,
                column=2,
                columnspan=1,
                sticky="w",
            )
            self.mot_max_car.grid(
                row=nb_boutton + 8 + nb_justification + 1,
                column=0,
                columnspan=2,
                sticky="w",
            )
            self.max_car_entry.grid(
                row=nb_boutton + 8 + nb_justification + 1,
                column=2,
                columnspan=1,
                sticky="w",
            )
            self.mot_max_line.grid(
                row=nb_boutton + 8 + nb_justification + 2,
                column=0,
                columnspan=2,
                sticky="w",
            )
            self.max_line_entry.grid(
                row=nb_boutton + 8 + nb_justification + 2,
                column=2,
                columnspan=1,
                sticky="w",
            )
            self.save_sizes_button.grid(
                row=nb_boutton + 8 + nb_justification,
                column=3,
                columnspan=1,
                rowspan=2,
                sticky="w",
            )

            self.separator0 = ttk.Separator(fenetre, orient="horizontal")
            self.separator1 = ttk.Separator(fenetre, orient="horizontal")
            self.separator2 = ttk.Separator(fenetre, orient="horizontal")
            self.separator3 = ttk.Separator(fenetre, orient="vertical")
            self.separator5 = ttk.Separator(fenetre, orient="horizontal")

            self.separator0.grid(row=2, column=0, columnspan=10, sticky="ew")
            self.separator1.grid(
                row=nb_boutton + 4 + nb_justification,
                column=0,
                columnspan=10,
                sticky="ew",
            )
            self.separator2.grid(
                row=nb_boutton + 7 + nb_justification,
                column=0,
                columnspan=10,
                sticky="ew",
            )
            self.separator3.grid(
                row=2,
                column=5,
                rowspan=nb_boutton + 4 + nb_justification - 2,
                sticky="ns",
            )
            self.separator5.grid(
                row=nb_boutton + 11 + nb_justification,
                column=0,
                columnspan=10,
                sticky="ew",
            )

            self.maj()

    def maj(self):
        for param in self.dictParam.values():
            if settings.PRESSETTINGS.get(self.etype, param):
                self.dictButton[param].select()
            else:
                self.dictButton[param].deselect()
        if self.etype == "song":
            for button in self.dictButton.values():
                button.config(state=tk.NORMAL)
            for just in self.liste_radioButton:
                just.config(state=tk.NORMAL)

        elif self.etype == "verse":
            for button in self.dictButton.values():
                button.config(state=tk.NORMAL)
            for just in self.liste_radioButton:
                just.config(state=tk.NORMAL)
            for param in ["Check_bis", "Clean_majuscule"]:
                self.dictButton[param].deselect()
                self.dictButton[param].config(state=tk.DISABLED)

        elif self.etype == "media":
            for button in self.dictButton.values():
                button.deselect()
                button.config(state=tk.DISABLED)
            for param in ["Print_title", "Ponctuation"]:
                self.dictButton[param].config(state=tk.NORMAL)
            for just in self.liste_radioButton:
                just.config(state=tk.NORMAL)

        elif self.etype == "image":
            for button in self.dictButton.values():
                button.deselect()
                button.config(state=tk.DISABLED)
            for param in ["Print_title", "Ponctuation"]:
                self.dictButton[param].config(state=tk.NORMAL)
            for just in self.liste_radioButton:
                just.config(state=tk.NORMAL)

        elif self.etype == "empty":
            for button in self.dictButton.values():
                button.deselect()
                button.config(state=tk.DISABLED)
            for just in self.liste_radioButton:
                just.config(state=tk.DISABLED)

        elif self.etype == "preach":
            for button in self.dictButton.values():
                button.config(state=tk.NORMAL)
            for param in ["Check_bis", "Clean_majuscule", "oneslide"]:
                self.dictButton[param].deselect()
                self.dictButton[param].config(state=tk.DISABLED)

        param = settings.PRESSETTINGS.get(self.etype, "Justification")
        self.var_justification.set(self.liste_mep_justification.index(param))

        param = settings.PRESSETTINGS.get("Presentation_Parameters", "FontColor")
        self.var_fontColor.set(self.liste_mep_fontColor.index(param))

        self.background = settings.PRESSETTINGS.get(self.etype, "Background")
        self.background_str.delete(0, tk.END)
        self.background_str.insert(0, self.background)

        self.var_size.set(settings.PRESSETTINGS.get("Presentation_Parameters", "size"))
        self.var_max_car.set(
            settings.PRESSETTINGS.get("Presentation_Parameters", "size_line")
        )
        self.var_max_line.set(
            settings.PRESSETTINGS.get("Presentation_Parameters", "line_per_diapo")
        )

    def save(self, event=0):  # pylint: disable=unused-argument
        for param, valeur in self.dictValeurs.items():
            settings.PRESSETTINGS.set(
                self.etype, self.dictParam[param], bool(valeur.get())
            )

        num = self.liste_mep_justification[self.var_justification.get()]
        settings.PRESSETTINGS.set(self.etype, "Justification", str(num))

        num = self.liste_mep_fontColor[self.var_fontColor.get()]
        settings.PRESSETTINGS.set("Presentation_Parameters", "FontColor", str(num))

    def save_sizes(self):
        size = str(int(round(float(self.var_size.get()))))
        max_car = str(int(round(float(self.var_max_car.get()))))
        max_line = str(int(round(float(self.var_max_line.get()))))
        if fonc.isNumber(size):
            settings.PRESSETTINGS.set("Presentation_Parameters", "size", size)
        if fonc.isNumber(max_car):
            settings.PRESSETTINGS.set("Presentation_Parameters", "size_line", max_car)
        if fonc.isNumber(max_line):
            settings.PRESSETTINGS.set(
                "Presentation_Parameters", "line_per_diapo", max_line
            )

        self.var_size.set(settings.PRESSETTINGS.get("Presentation_Parameters", "size"))
        self.var_max_car.set(
            settings.PRESSETTINGS.get("Presentation_Parameters", "size_line")
        )
        self.var_max_line.set(
            settings.PRESSETTINGS.get("Presentation_Parameters", "line_per_diapo")
        )

    def change_background(self):
        chemin = self.background_str.get()
        if chemin == self.background:
            chemin = tkFileDialog.askopenfilename(
                filetypes=self.FILETYPES_image, parent=self.fenetre
            )
            if chemin and os.path.isfile(chemin):
                self.background = chemin
            elif chemin:
                tkMessageBox.showerror(
                    "Erreur", "Le fichier est introuvable", parent=self.fenetre
                )
        else:
            if chemin and os.path.isfile(chemin):
                self.background = chemin
            elif chemin:
                tkMessageBox.showerror(
                    "Erreur", "Le fichier est introuvable", parent=self.fenetre
                )
        settings.PRESSETTINGS.set(self.etype, "Background", self.background)
        self.maj()

    def select_etype(self, event):  # pylint: disable=unused-argument
        if self.combobox_etype.get():
            self.etype = self.combobox_etype.get()
            self.maj()

    def select_profil(self, event):  # pylint: disable=unused-argument
        if self.combobox_profil.get():
            self.profil = self.combobox_profil.get()
            shutil.copy(
                os.path.join(
                    songfinder.__settingsPath__, self.settingName + "_" + self.profil
                ),
                os.path.join(songfinder.__settingsPath__, self.settingName),
            )
            settings.PRESSETTINGS.read()
            self.maj()

    def start_profil(self):
        for filename in os.listdir(songfinder.__settingsPath__):
            if filename.find(self.settingName + "_") != -1 and filecmp.cmp(
                os.path.join(songfinder.__settingsPath__, filename),
                os.path.join(songfinder.__settingsPath__, self.settingName),
            ):
                self.profil = filename[filename.find("_") + 1 :]
                self.combobox_profil.set(self.profil)

    def fenetre_creation_profil(self):
        if not self.fenetre_profil:
            self.fenetre_profil = tk.Toplevel()
            with guiHelper.SmoothWindowCreation(self.fenetre_profil):
                self.fenetre_profil.title("Nouveau profil")

                self.text_set = tk.Label(
                    self.fenetre_profil, text="Nom du nouveau profil"
                )
                self.nom_profil = tk.Entry(self.fenetre_profil, width=20)
                self.bouton_set = tk.Button(
                    self.fenetre_profil, text="Créer", command=self.cree_profil
                )

                self.text_set.grid(row=0, column=0)
                self.nom_profil.grid(row=1, column=0)
                self.bouton_set.grid(row=2, column=0)

                self.nom_profil.focus_set()

    def cree_profil(self):
        if self.nom_profil.get():
            self.profil = self.nom_profil.get()
            profil = os.path.join(
                songfinder.__settingsPath__, self.settingName + "_" + self.profil
            )
            if not os.path.isfile(profil) or tkMessageBox.askyesno(
                "Conflit",
                "Le fichier %s existe déjà, " "voulez-vous le remplacer ?" % profil,
                parent=self.fenetre_profil,
            ):
                settings.PRESSETTINGS.write()
                shutil.copy(
                    os.path.join(songfinder.__settingsPath__, self.settingName), profil
                )
                self.fenetre_profil.destroy()
                self.fenetre_profil = None
                if os.path.isfile(profil):
                    tkMessageBox.showinfo(
                        "Confirmation",
                        "Le fichier %s a été écrit" % profil,
                        parent=self.fenetre,
                    )
                    self.combobox_profil.set(self.profil)
            else:
                tkMessageBox.showerror(
                    "Erreur",
                    "Le fichier %s n'a pas été crée" % profil,
                    parent=self.fenetre,
                )
        self.get_profil_liste()

    def get_profil_liste(self):
        # Creation de la liste de profil
        self.liste_profil = []
        for _, _, files in os.walk(songfinder.__settingsPath__):
            for fichier in files:
                if fichier.find("Settings_") != -1:
                    self.liste_profil.append(fichier[9:])
            break
        self.combobox_profil["values"] = self.liste_profil

    def close(self):
        self.fenetre.destroy()
