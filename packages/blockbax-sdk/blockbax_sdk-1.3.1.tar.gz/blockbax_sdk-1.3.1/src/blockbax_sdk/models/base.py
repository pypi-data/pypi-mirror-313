from __future__ import annotations
from decimal import Decimal
from typing import Any, Dict, Optional, Type, TypeVar, Union, cast
import enum
import abc
import json
import httpx
from pydantic import BaseModel, ConfigDict

TBlockbaxModel = TypeVar("TBlockbaxModel", bound="BlockbaxModel")


def alias_generator(string: str) -> str:
    # Convert field to camel case
    pascal_case = "".join(word.capitalize() for word in string.split("_"))
    camel_case = pascal_case[0].lower() + pascal_case[1:]
    return camel_case


class JSONEncoderWithDecimal(json.JSONEncoder):
    def default(self, o: object):
        if isinstance(o, Decimal):
            return "{:f}".format(o)
        return super().default(o)


class BlockbaxModel(BaseModel, abc.ABC):
    model_config = ConfigDict(
        validate_assignment=True,
        revalidate_instances="subclass-instances",
        populate_by_name=True,
        use_enum_values=True,
        extra="allow",
        arbitrary_types_allowed=True,
        alias_generator=alias_generator,
    )

    @classmethod
    def from_response(
        cls: Type[TBlockbaxModel],
        response: Optional[Union[httpx.Response, Dict[Any, Any], str]],
    ) -> Optional[TBlockbaxModel]:
        if response is None:
            return None
        if isinstance(response, httpx.Response):
            response_json: Dict[Any, Any] = response.json()

        elif isinstance(response, str):
            response_json = json.loads(response)

        else:
            response_json = response
        return cast(Optional[TBlockbaxModel], cls.model_validate(response_json))

    def to_request(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True, mode="json")


class BlockbaxEnum(str, enum.Enum):
    pass
