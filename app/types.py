"""Custom types"""
import json
from dataclasses import is_dataclass, asdict
from collections.abc import Callable

from PyQt6.QtCore import pyqtSlot, QObject


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

    def __call__(self, *args):
        if self._callback is not None:
            self._callback(*args)

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


class PendingCallback(SimpleCallback):
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
