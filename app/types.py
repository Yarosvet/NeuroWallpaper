"""Custom types"""
import json
from dataclasses import is_dataclass, asdict
from collections.abc import Callable

from PyQt6.QtCore import pyqtSlot, QObject, pyqtSignal


class DataDictMixin:
    """Mixin for dataclasses (and others) to convert to and from dict"""

    def to_dict(self) -> dict:
        """Convert to dict"""
        return asdict(self)  # noqa

    @classmethod
    def from_dict(cls, data: dict):
        """Create from dict"""
        args = data.copy()
        for name, annotation in cls.__annotations__.items():
            if is_dataclass(annotation):
                if args[name] is None:
                    continue
                if hasattr(annotation, "from_dict") and callable(annotation.from_dict):
                    args[name] = annotation.from_dict(args[name])
                else:
                    args[name] = annotation(**args[name])
        return cls(**args)  # noqa

    @classmethod
    def from_json(cls, data: str):
        """Create from JSON"""
        return cls.from_dict(json.loads(data))

    def to_json(self) -> str:
        """Convert to JSON"""
        return json.dumps(self.to_dict())


class SimpleCallback:
    """Provides a simple callback mechanism"""

    def __init__(self):
        self._callback = None

    def __call__(self, *args, **kwargs):
        if self._callback is not None:
            self._callback(*args, **kwargs)

    def set_callable(self, func: Callable):
        """Set the callback function"""
        self._callback = func


class QtCallback(SimpleCallback, QObject):
    """Provides a callback for Qt signals"""

    @property
    def void_slot(self):
        """Acts like a slot for Qt signals without arguments"""

        @pyqtSlot()
        def _slot():
            self()

        return _slot

    def slot(self, *types):
        """Return a slot for Qt signals with the specified types"""

        @pyqtSlot(*types)
        def _slot(*args):
            self(*args)

        return _slot


class PendingCallback(SimpleCallback):  # Now it's not used, but let it be here
    """Provides a callback that can be called before setting the function"""

    def __init__(self):
        super().__init__()
        self._pending = False
        self._args = None

    def __call__(self, *args):
        if self._callback is not None:
            self._callback(*args)
        else:
            self._pending = True
            self._args = args

    def set_callable(self, func: Callable):
        """Set the callback function and call it if there are pending arguments"""
        self._callback = func
        if self._pending:
            self._pending = False
            self._callback(*self._args)


class QtEventBridge(QObject):  # pylint: disable=too-few-public-methods
    """
    Bridge between a callback (which may be from another thread) to qt signal and slot
    Warning! All arguments must be JSON-serializable
    """

    _signal = pyqtSignal(str, str)

    def __init__(self, safe_callable: Callable, parent: QObject | None = None) -> None:
        super().__init__(parent=parent)
        self._safe_callable = safe_callable

        @pyqtSlot(str, str)
        def _slot(json_args: str, json_kwargs: str):
            self._safe_callable(*json.loads(json_args), **json.loads(json_kwargs))

        self._slot = _slot
        self._signal.connect(self._slot)  # noqa  # Why IDE doesn't see connect() method again?

    def __call__(self, *args, **kwargs):
        """Emit the signal"""
        self._signal.emit(json.dumps(args), json.dumps(kwargs))  # noqa  # Why IDE doesn't see emit() method?
