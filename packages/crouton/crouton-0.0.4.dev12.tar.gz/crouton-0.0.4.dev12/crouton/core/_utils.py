from typing import Optional, Type, Any
from fastapi import Depends, HTTPException
from pydantic import create_model

from ._types import T, PAGINATION, PYDANTIC_SCHEMA


class AttrDict(dict):  # type: ignore
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def get_pk_type(schema: Type[PYDANTIC_SCHEMA], pk_field: str) -> Any:
    """
    Patched method to get primary key type.
    This patch replaces the original get_pk_type method.
    """
    try:
        return schema.__fields__[pk_field].annotation  
    except KeyError:
        return int


def schema_factory(
    schema_cls: Type[T], pk_field_name: str = "id", name: str = "Create"
) -> Type[T]:
    """
    Patched method to create a schema without the primary key field.
    This patch replaces the original schema_factory method.
    """
    fields = {
        name: (f.annotation, ...)  
        for name, f in schema_cls.__fields__.items()
        if name != pk_field_name
    }

    name = schema_cls.__name__ + name
    schema: Type[T] = create_model(__model_name=name, **fields)  # type: ignore
    return schema


def create_query_validation_exception(field: str, msg: str) -> HTTPException:
    return HTTPException(
        422,
        detail={
            "detail": [
                {"loc": ["query", field], "msg": msg, "type": "type_error.integer"}
            ]
        },
    )


def pagination_factory(max_limit: Optional[int] = None) -> Any:
    """
    Creates the pagination dependency to be used in the router.
    """
    def pagination(skip: int = 0, limit: Optional[int] = max_limit) -> PAGINATION:
        if skip < 0:
            raise create_query_validation_exception(
                field="skip",
                msg="skip query parameter must be greater or equal to zero",
            )

        if limit is not None:
            if limit <= 0:
                raise create_query_validation_exception(
                    field="limit", msg="limit query parameter must be greater than zero"
                )

            elif max_limit and max_limit < limit:
                raise create_query_validation_exception(
                    field="limit",
                    msg=f"limit query parameter must be less than {max_limit}",
                )

        return {"skip": skip, "limit": limit}

    return Depends(pagination)
