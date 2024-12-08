# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
import queue

import traceback
import threading
import sys
import logging

from songfinder.gui import guiHelper
from songfinder import messages as tkMessageBox
import songfinder

MULTIPROCESSING = 0
THREADS = 1


class SimpleProgress(object):
    def __init__(self, title, mode="determinate", screens=None):
        self._fen = tk.Toplevel()
        self._fen.withdraw()
        self._fen.title("Progression")
        self._fen.resizable(False, False)
        self._mode = mode
        if screens:
            screens[0].centerFrame(self._fen)

        prog = tk.Label(self._fen, text=title, justify="left")
        self._progresseBar = ttk.Progressbar(
            self._fen, orient="horizontal", length=200, mode=self._mode, value=0.0
        )
        cancelButton = tk.Button(self._fen, text="Annuler", command=self._cancel)
        prog.pack(side=tk.TOP)
        self._progresseBar.pack(side=tk.TOP)
        cancelButton.pack(side=tk.TOP)
        self._counter = 0

    def start(self, total=100, steps=100):
        self._fen.deiconify()
        guiHelper.upFront(self._fen)
        self._total = total
        self._ratio = (total + steps - 1) // steps
        self._progresseBar["value"] = 0.0
        self._progresseBar["maximum"] = self._total
        self._progresseBar.start()

    def update(self):
        if self._mode == "determinate":
            self._counter += 1
            self._progresseBar["value"] = self._counter
        if self._counter % self._ratio == 0:  # Lowers the graphical overhead
            self._fen.update()
            guiHelper.upFront(self._fen)

    def stop(self):
        self._progresseBar.stop()
        self._fen.destroy()

    def _cancel(self):
        self.stop()


def tk_call_async(
    window,
    computation,
    args=(),
    kwargs=None,
    callback=None,
    errback=None,
    polling=500,
    method=MULTIPROCESSING,
):
    if kwargs is None:
        kwargs = {}
    if method == MULTIPROCESSING:
        # I use threads because on windows creating a new python process
        # freezes a little the event loop.
        future_result = queue.Queue()

        worker = threading.Thread(
            target=_request_result_using_multiprocessing,
            args=(computation, args, kwargs, future_result),
        )
        worker.daemon = True
        worker.start()
    elif method == THREADS:
        future_result = _request_result_using_threads(
            computation, args=args, kwargs=kwargs
        )
    else:
        raise ValueError("Not valid method")

    if callback is not None or errback is not None:
        _after_completion(window, future_result, callback, errback, polling)

    return future_result


def _request_result_using_multiprocessing(func, args, kwargs, future_result):
    import multiprocessing

    queue = multiprocessing.Queue()

    worker = multiprocessing.Process(
        target=_compute_result, args=(func, args, kwargs, queue)
    )
    worker.daemon = True
    worker.start()

    return future_result.put(queue.get())


def _request_result_using_threads(func, args, kwargs):
    future_result = queue.Queue()

    worker = threading.Thread(
        target=_compute_result, args=(func, args, kwargs, future_result)
    )
    worker.daemon = True
    worker.start()

    return future_result


def _after_completion(window, future_result, callback, errback, polling):
    def check():
        try:
            result = future_result.get(block=False)
        except Exception:  # pylint: disable=broad-except
            window.after(polling, check)
        else:
            if isinstance(result, Exception):
                if errback is not None:
                    errback(result)
            else:
                if callback is not None:
                    callback(result)

    window.after(0, check)


def _compute_result(func, func_args, func_kwargs, future_result):
    try:
        _result = func(*func_args, **func_kwargs)
    except Exception:  # pylint: disable=broad-except
        _result = Exception(traceback.format_exc())

    future_result.put(_result)


class Progress(object):
    def __init__(self, title, job, screens=None):
        self._fen = tk.Toplevel()
        self._fen.withdraw()
        self._fen.title("Progression")
        self._fen.resizable(False, False)

        if screens:
            screens[0].centerFrame(self._fen)

        prog = tk.Label(self._fen, text=title, justify="left")
        self._progresseBar = ttk.Progressbar(
            self._fen, orient="horizontal", length=200, mode="indeterminate"
        )
        cancelButton = tk.Button(self._fen, text="Annuler", command=self._cancel)
        prog.pack(side=tk.TOP)
        self._progresseBar.pack(side=tk.TOP)
        cancelButton.pack(side=tk.TOP)

        self._cancelMessage = False
        self._quitMessage = False
        self._errorMessage = False
        self._interrupt = False
        self._job = job

    def start(self):
        self._fen.deiconify()
        guiHelper.upFront(self._fen)
        self._progresseBar["maximum"] = 100
        self._progresseBar["value"] = 0.0
        self._progresseBar["mode"] = "indeterminate"
        self._progresseBar.start()
        tk_call_async(
            self._fen,
            self._job.function,
            args=self._job.args,
            callback=self._callback,
            method=THREADS,
        )

    def _callback(self, result):
        self._progresseBar.stop()
        self._job.postProcess(result)
        self._properClose()
        return 0

    def _cancel(self):
        if not self._cancelMessage:
            self._cancelMessage = True
            if tkMessageBox.askyesno(
                "Confirmation", "Etes-vous sur de vouloir annuler ?"
            ):
                logging.warning("Interupting")
                self._properClose()
            self._cancelMessage = False

    def _properClose(self):
        self._interrupt = True
        if self._fen:
            self._fen.destroy()
            self._fen = None


class Job(object):
    def __init__(self, function, args=(), **kwargs):
        self.function = getExceptionWrapper
        self.args = (function, args, kwargs)

    def postProcess(self, result):
        if result != 0:
            raise Exception(f"Job returned {str(result)}")


class UpdateJob(Job):
    def postProcess(self, result):
        code, out, err = result
        if code != 0:
            tkMessageBox.showerror(
                "Attention",
                f"Error while updating SongFinder. Error {str(code)}:\n{err}",
            )
        else:
            if out.find(f"Successfully installed {songfinder.__appName__}") != -1:
                tkMessageBox.showinfo(
                    "Confirmation",
                    "SongFinder a "
                    "été mis à jour et va être fermé. "
                    "Veuillez le démarrer à nouveau pour "
                    "que les changements prennent effet.",
                )
                sys.exit()
            else:
                tkMessageBox.showinfo("Confirmation", "SongFinder est déjà à jour.")


def getExceptionWrapper(function, args, kwargs):
    try:
        return function(*args, **kwargs)
    except Exception:  # pylint: disable=broad-except
        return traceback.format_exc()
