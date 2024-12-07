import typing
from types import UnionType, GenericAlias
from pydantic import BaseModel
from collections.abc import Iterable
from loguru import logger


class TypeInfo:
    def __init__(self, annotation: typing.Any, is_optional: bool):
        # logger.debug(annotation)
        self.type = annotation
        self.is_optional = is_optional
        self.is_pydantic_model = False
        if isinstance(self.type, type) and issubclass(self.type, BaseModel):
            self.is_pydantic_model = True
        self.is_iterable = hasattr(self.type, "__iter__")
        self.db_type = None
        if hasattr(self.type, "__clickhouse_type__"):
            self.db_type = getattr(self.type, "__clickhouse_type__")
            self.is_pydantic_model = False

        if self.is_iterable:
            _args = typing.get_args(self.type)
            if len(_args) > 0:
                self.item_type = annotation_extract_primary_type(_args[0])

            # self.item_type = self.type.__args__[0]

    type: typing.Type
    item_type: typing.Self | None = None
    is_optional: bool
    is_pydantic_model: bool = False
    is_iterable: bool = False


def annotation_extract_primary_type(annotation: typing.Any) -> TypeInfo:
    if typing.get_origin(annotation) is UnionType:
        args = typing.get_args(annotation)
        if len(args) == 2 and args[1] is type(None):
            return TypeInfo(args[0], is_optional=True)
        else:
            return TypeInfo(annotation, is_optional=False)
    else:
        return TypeInfo(annotation, is_optional=False)
