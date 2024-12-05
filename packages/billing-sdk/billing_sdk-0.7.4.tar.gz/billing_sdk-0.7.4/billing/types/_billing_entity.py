from datetime import datetime
from typing import Any, ClassVar, Dict, Literal

from pydantic import VERSION as PYDANTIC_VERSION
from pydantic import BaseModel
from typing_extensions import Self

from billing._utils import json_loads

IS_PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

if IS_PYDANTIC_V2:
    from pydantic import ConfigDict


class BillingObject(BaseModel):
    """
    Data Transfer Object for a billing API object.
    """

    if IS_PYDANTIC_V2:
        model_config: ClassVar[ConfigDict] = ConfigDict(
            frozen=True,
        )
    else:

        class Config:
            frozen = True

    @classmethod
    def parse(cls, obj: Any) -> Self:
        if IS_PYDANTIC_V2:
            return cls.model_validate(obj)
        else:
            return cls.parse_obj(obj)

    def dump(self, mode: Literal["python", "json"] = "python") -> Dict[str, Any]:
        if IS_PYDANTIC_V2:
            return self.model_dump(mode=mode)
        elif mode == "python":
            return self.dict()
        else:
            return json_loads(self.json())  # type: ignore[no-any-return]


if IS_PYDANTIC_V2:
    from pydantic import RootModel

    class DynamicDictModel(BillingObject, RootModel[Dict[str, Any]]):

        @classmethod
        def init(cls, dict_: Dict[str, Any]) -> Self:
            return cls(dict_)

else:

    class DynamicDictModel(BillingObject):  # type: ignore[no-redef]
        __root__: Dict[str, Any]

        @classmethod
        def init(cls, dict_: Dict[str, Any]) -> Self:
            return cls(__root__=dict_)


class BillingEntity(BillingObject):
    id: str
    created_at: datetime


class BillingEntityWithTimestamps(BillingEntity):
    updated_at: datetime
