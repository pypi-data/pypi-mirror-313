# -*- coding: utf-8 -*-
import logging
import requests
from bs4 import BeautifulSoup


class CDLParser(object):
    def __init__(self, input_url_or_html):
        self._reset()
        try:
            htmlPage = requests.get(input_url_or_html)
        except requests.exceptions.InvalidSchema:
            if bool(BeautifulSoup(input_url_or_html, "html.parser").find()):
                # The input is actualy html content not an URL
                self._url = ""
                logging.debug("parsing html content")
                self._parsedPage = BeautifulSoup(input_url_or_html, "html.parser")
            else:
                raise
        else:
            self._url = input_url_or_html
            logging.debug(f"parsing {self._url}")
            self._parsedPage = BeautifulSoup(htmlPage.content, "html.parser")
            # Make sure link is valid
            self._isValidLink()

    def _reset(self):
        self._tags = []
        self._authors = ""
        self._sources = ""
        self._copyright = ""
        self._key = ""
        self._text = ""
        self._title = ""
        self._song_book = ""
        self._hymnNumber = None
        self._invalidLink = False

    def _getSection(self, sectionName):
        if not self._invalidLink:
            section = self._parsedPage.find_all("section", sectionName)
            if len(section) != 1:
                logging.info(
                    'Parsed section is not of size 1 for "%s": "%s"'
                    % (self.title, str(section))
                )
                return self._parsedPage
        return section[0]

    @property
    def hymnNumber(self):
        if not self._invalidLink and not self._hymnNumber:
            sources = self.sources
            start = sources.find("#")
            if start != -1:
                hymnNumber = sources[start + 1 :]
                self._hymnNumber = int(hymnNumber.strip(" "))
        return self._hymnNumber

    @property
    def song_book(self):
        if not self._invalidLink and not self._song_book:
            repDict = {
                "J'aime l'Éternel": "JEM",
                "EXO": "EXO",
                "ailes de la foi": "AF",
                "Hillsong": "H",
                "Dan Luiten": "DL",
                "Reckless love": "RL",
                "Jesus Culture": "JC",
            }
            sources = self.sources
            for key, value in repDict.items():
                if sources.lower().find(key.lower()) != -1:
                    self._song_book = f"{value}"
                    break
        return self._song_book

    @property
    def tags(self):
        if not self._invalidLink and not self._tags:
            categories = self._getSection("categories")
            labels = categories.find_all("span", "label label-primary")
            for label in labels:
                self._tags.append(label.text.replace("\n", ""))
        return self._tags

    @property
    def authors(self):
        if not self._invalidLink and not self._authors:
            songGredits = self._getSection("credits")
            authors = songGredits.find_all("span", "author")
            authorsList = []
            for author in authors:
                authorsList.append(author.text.replace("\n", ""))
            self._authors = " - ".join(authorsList)
        return self._authors

    @property
    def sources(self):
        if not self._invalidLink and not self._sources:
            songGredits = self._getSection("credits")
            sources = songGredits.find_all("span", "source")
            sourcesList = []
            for source in sources:
                sourcesList.append(source.text.replace("\n", ""))
            if len(sourcesList) > 1:
                logging.debug(
                    'Number of sources is greater than 1 for "%s", taking only the first one: "%s"'
                    % (self.title, ", ".join(sourcesList))
                )
            try:
                self._sources = sourcesList[0]
            except IndexError:
                pass
        return self._sources

    @property
    def copyright(self):
        if not self._invalidLink and not self._copyright:
            songCopyright = self._getSection("copyright")
            self._copyright = songCopyright.text.replace("\n", "")
        return self._copyright

    @property
    def key(self):
        if not self._invalidLink and not self._key:
            body = self._getSection("body")
            keys = body.find_all("div", "chordpro-key")
            # ~ if len(keys) != 1:
            # ~ raise Exception('Parsed keys is not of size 1 %s'%str(keys))
            self._key = keys[0].text.replace("\n", "")
        return self._key

    @property
    def text(self):
        if not self._invalidLink and not self._text:
            body = self._getSection("body")
            text = ""
            for elem in body:
                try:
                    name = elem["class"][0]
                except (TypeError, KeyError):
                    pass
                else:
                    if name == "chordpro-start_of_verse":
                        text = f"{text}\n\\ss"
                    elif name == "chordpro-chorus":
                        text = f"{text}\n\\sc"
                        for subElem in elem:
                            text = f"{text}\n{subElem.text}"
                    elif name == "chordpro-verse":
                        text = f"{text}\n{elem.text}"
            self._text = text.strip("\n")
        return self._text

    @property
    def title(self):
        if not self._invalidLink and not self._title:
            title = self._parsedPage.find_all("h2")
            if len(title) != 1:
                raise Exception(f'Parsed title is not of size 1: "{str(title)}"')
            self._title = title[0].text.strip("\n ")
        return self._title

    def _isValidLink(self):
        if self.title == "Une erreur 404 est survenue":
            logging.error(f'404 ERROR While parsing link "{self._url}"')
            self._invalidLink = True

    def __str__(self):
        name = f"{self.song_book}{self.hymnNumber} {self.title}"
        name = name.strip(" \n")
        return name
