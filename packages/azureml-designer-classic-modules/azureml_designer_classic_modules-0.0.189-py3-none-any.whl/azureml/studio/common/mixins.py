from itertools import chain

from azureml.studio.core.utils.strutils import to_camel_case


class MetaExtractMixin:
    """
    A mixin to let other classes be able to export __slots__ to a dict.
    """
    def _slots_to_export(self, exclude):
        slots = chain.from_iterable(getattr(cls, '__slots__', []) for cls in self.__class__.__mro__)
        return [s for s in slots if s not in exclude]

    def to_dict(self, exclude=(), key_converter=to_camel_case):
        return {key_converter(s): getattr(self, s) for s in self._slots_to_export(exclude=exclude)}
