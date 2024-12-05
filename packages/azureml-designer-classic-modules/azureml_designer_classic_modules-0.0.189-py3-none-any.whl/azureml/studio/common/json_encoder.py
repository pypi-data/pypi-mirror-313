from enum import Enum
from json import JSONEncoder
from uuid import UUID

from azureml.studio.common.mixins import MetaExtractMixin
from azureml.studio.internal.utils.dependencies import Dependencies


class EnhancedJsonEncoder(JSONEncoder):
    """
    Enhanced JSONEncoder to support AutoEnum.
    """
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, Enum):
            return obj.name
        elif isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, MetaExtractMixin):
            return obj.to_dict()
        elif isinstance(obj, Dependencies):
            return obj.to_dict()
        return super().default(obj)
