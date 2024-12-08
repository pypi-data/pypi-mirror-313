# -*- coding: utf-8 -*-

import logging
import time
import functools

from songfinder import corrector
from songfinder import gestchant


class SearcherBase(object):
    def search(self, to_search):
        raise NotImplementedError


class SearcherNum(SearcherBase):
    def __init__(self, num_dict):
        self._num_dict = num_dict

    def search(self, num_to_search):
        if not isinstance(num_to_search, int):
            raise TypeError("Search input should be integer type")

        try:
            return list(self._num_dict[num_to_search])
        except KeyError:
            logging.warning(
                f"{num_to_search} does not correspond to any number song number"
            )
            return []


class SearcherString(SearcherBase):
    def __init__(self, song_dict):
        self._song_dict = song_dict

    def search(self, toSearch):
        if not isinstance(toSearch, str):
            raise TypeError("Search input should be string type")

        self._found = list(self._song_dict.keys())
        self._retry_threshold = min(len(self._found), 10)
        self._searchCore(toSearch)
        return self._found

    def _searchCore(self, toSearch):
        toSearchList = toSearch.split(" ")

        for _ in range(2):
            nb_found = len(self._found)
            if nb_found != 1 and nb_found >= self._retry_threshold:
                self._keyWordSearch(1, toSearchList)
                if len(toSearchList) > 1 and len(self._found) > 5:
                    self._keyWordSearch(2, toSearchList)
                if len(toSearchList) > 2 and len(self._found) > 5:
                    self._keyWordSearch(3, toSearchList)
                if len(toSearchList) > 1 and len(self._found) > 5:
                    self._keyWordSearch(2, toSearchList, tolerance=0.2)
                if len(toSearchList) > 1 and len(self._found) > 5:
                    self._keyWordSearch(2, toSearchList, tolerance=0.1)
                if len(toSearchList) > 2 and len(self._found) > 5:
                    self._keyWordSearch(3, toSearchList)

    def _keyWordSearch(self, nbWords, toSearchList, tolerance=0.3):
        dico_taux = dict()
        toSearchSet = set()
        plusieurs_mots = []
        for i, mot in enumerate(toSearchList):
            plusieurs_mots.append(mot)
            if i > nbWords - 2:
                toSearchSet.add(" ".join(plusieurs_mots))
                plusieurs_mots = plusieurs_mots[1:]
        taux_max = 0
        for song in self._found:
            refWords = self._song_dict[song][nbWords - 1]
            refSet = set(refWords.split(";"))
            taux = len(toSearchSet & refSet) / len(toSearchSet)

            try:
                dico_taux[taux].append(song)
            except KeyError:
                dico_taux[taux] = [song]

            if taux > taux_max:
                taux_max = taux

        self._found = []
        taux_ordered = sorted(dico_taux.keys(), reverse=True)
        for taux in taux_ordered:
            if taux > taux_max - tolerance - nbWords / 10:
                self._found += sorted(dico_taux[taux])


class SearcherWrapper(SearcherBase):
    def __init__(self, dataBase):
        self._dataBase = dataBase
        self._searchers = dict()
        for mode in self._dataBase.available_modes:
            # TODO Accessing private member here
            # Remove this when refactoring if finished
            self._searchers[mode] = SearcherString(self._dataBase._dicts[mode])
        self._searchers["num"] = SearcherNum(self._dataBase.dict_nums)

        self._debugPrintMod = 10
        self._searchCounter = 0
        self._searchTimeCumul = 0
        self._correctTimeCumul = 0

        self._getCorrector()

    def _getCorrector(self):
        singles = ";".join((sets[0] for sets in self._dataBase.values()))
        couples = ""
        if self._dataBase.mode != "tags":
            couples = ";".join((sets[1] for sets in self._dataBase.values()))
        self._corrector = corrector.Corrector(singles, couples)

    @property
    def mode(self):
        return self._dataBase.mode

    @mode.setter
    def mode(self, in_mode):
        self._dataBase.mode = in_mode
        self._getCorrector()
        self._cached_search.cache_clear()

    def search(self, string_to_search):
        if not string_to_search.isdigit():
            string_to_search = gestchant.netoyage_paroles(string_to_search)
            start = time.time()
            string_to_search = self._corrector.check(string_to_search)
            self._correctTimeCumul += time.time() - start
        if self._searchCounter % self._debugPrintMod == 0:
            try:
                correctTimeMean = self._correctTimeCumul / self._searchCounter
                searchTimeMean = self._searchTimeCumul / self._searchCounter
            except ZeroDivisionError:
                correctTimeMean = 0
                searchTimeMean = 0

            # pylint: disable=no-value-for-parameter,no-member
            hits = self._cached_search.cache_info().hits
            misses = self._cached_search.cache_info().misses
            try:
                ratio = hits / (hits + misses)
            except ZeroDivisionError:
                ratio = float("inf")
            logging.debug(
                'Searcher "%s": %d searches,\n'
                "\tCorrect time (mean): %.3fs, "
                "Search time (mean): %.3fs,\n"
                "\tCache hit/miss ratio: %.2f, "
                'Searching "%s"'
                % (
                    type(self).__name__,
                    self._searchCounter,
                    correctTimeMean,
                    searchTimeMean,
                    ratio,
                    string_to_search,
                )
            )
        self._searchCounter += 1
        return self._cached_search(string_to_search)

    @functools.lru_cache(maxsize=100)
    def _cached_search(self, string_to_search):  # Use of caching
        start = time.time()
        try:
            num_to_search = int(string_to_search)
        except ValueError:
            found = self._searchers[self._dataBase.mode].search(string_to_search)
        else:
            found = self._searchers["num"].search(num_to_search)
        self._searchTimeCumul += time.time() - start
        return found

    def resetCache(self):
        # pylint: disable=no-member
        self._cached_search.cache_clear()
        self._corrector.resetCache()
