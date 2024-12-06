from abc import abstractmethod, ABC
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Optional, Union, Any
from typing_extensions import TypeAlias, Annotated
from .base import BlockbaxModel
from pydantic import PlainSerializer, field_validator, TypeAdapter, model_validator


def normalize_and_remove_exponent(decimal_value: Decimal) -> Decimal:
    return (
        decimal_value.quantize(Decimal(1))
        if decimal_value == decimal_value.to_integral()
        else decimal_value.normalize()
    )


BlockbaxNumber = Annotated[
    Union[int, float, Decimal],
    "blockbax_number",
    PlainSerializer(
        lambda x: str(normalize_and_remove_exponent(x)),
        return_type=str,
        when_used="unless-none",
    ),
]


def convert_number_to_decimal(
    value: Optional[Union[int, float, Decimal, str]]
) -> Optional[Decimal]:
    try:
        # decimal says you can pass an int but mypy disagrees, thats why we ignore the type here
        # https://docs.python.org/3/library/decimal.html#:~:text=Q.%20Some%20decimal,3%27))%0ADecimal(%275000%27)
        return normalize_and_remove_exponent(Decimal(value).quantize(Decimal("1E-8")))  # type: ignore
    except InvalidOperation as exc:
        error_msg = (
            f"Could not convert: {value}, ensure numbers have max 20 digits before "
            "and 8 digits after the decimal point"
        )
        raise ValueError(error_msg) from exc


class Location(BlockbaxModel):
    lat: BlockbaxNumber
    lon: BlockbaxNumber
    alt: Optional[BlockbaxNumber] = None

    @field_validator("lat", "lon", "alt", mode="before")
    def convert_to_decimal(cls, value):  # pylint: disable=C0116.E0213
        return convert_number_to_decimal(value) if value is not None else None


class MapLayer(BlockbaxModel):
    image_path: Optional[str] = None
    image_data: Optional[str] = None
    left_bottom: Location
    left_top: Location
    right_bottom: Location
    right_top: Location

    @model_validator(mode="after")
    def only_path_or_data_exists(self):  # pylint: disable=C0116.E0213
        if self.image_path is None and self.image_data is None:
            raise ValueError(
                "Exactly one fields of image_data or image_path should be set. None were passed."
            )
        if self.image_path is not None and self.image_data is not None:
            raise ValueError(
                "Exactly one fields of image_data or image_path should be set. Both were passed."
            )


class Polygon(BlockbaxModel):
    outer_ring: List[Location]


class Area(BlockbaxModel):
    polygon: Polygon


class Image(BlockbaxModel):
    image_path: Optional[str] = None
    image_data: Optional[str] = None

    @model_validator(mode="after")
    def only_path_or_data_exists(self):  # pylint: disable=C0116.E0213
        if self.image_path is None and self.image_data is None:
            raise ValueError(
                "Exactly one fields of image_data or image_path should be set. None were passed."
            )
        if self.image_path is not None and self.image_data is not None:
            raise ValueError(
                "Exactly one fields of image_data or image_path should be set. Both were passed."
            )


BlockbaxValue: TypeAlias = Union[
    BlockbaxNumber,
    str,
    Location,
    Image,
    MapLayer,
    Area,
]

# Data adapters

location_adapter: TypeAdapter[Location] = TypeAdapter(Location)
map_layer_adapter: TypeAdapter[MapLayer] = TypeAdapter(MapLayer)
area_adapter: TypeAdapter[Area] = TypeAdapter(Area)
image_adapter: TypeAdapter[Image] = TypeAdapter(Image)
blockbax_value_adapter: TypeAdapter[BlockbaxValue] = TypeAdapter(BlockbaxValue)


# Data types


class DataTypeMixinABC(BlockbaxModel, ABC):
    @staticmethod
    def get_data_type() -> str:
        pass

    @abstractmethod
    def get_value(self) -> Optional[BlockbaxValue]:
        pass

    @abstractmethod
    def _set_value(self, new_value: Any):
        pass


class LocationTypeMixin(DataTypeMixinABC):
    location: Location

    @staticmethod
    def get_data_type() -> str:
        return "location"

    def get_value(self) -> Optional[Location]:
        return self.location

    def _set_value(self, new_value: Any):
        if isinstance(new_value, Location):
            self.location = new_value
        elif isinstance(new_value, dict):
            self.location = location_adapter.validate_python(new_value)


class MapLayerTypeMixin(DataTypeMixinABC):
    map_layer: MapLayer

    @staticmethod
    def get_data_type() -> str:
        return "map_layer"

    def get_value(self) -> Optional[MapLayer]:
        return self.map_layer

    def _set_value(self, new_value: Union[Dict[Any, Any], MapLayer]):
        if isinstance(new_value, MapLayer):
            self.map_layer = new_value
        elif isinstance(new_value, dict):
            self.map_layer = map_layer_adapter.validate_python(new_value)


class ImageTypeMixin(DataTypeMixinABC):
    image: Image

    @staticmethod
    def get_data_type() -> str:
        return "image"

    def get_value(self) -> Optional[BlockbaxValue]:
        return self.image

    def _set_value(self, new_value: Any):
        if isinstance(new_value, Image):
            self.image = new_value
        elif isinstance(new_value, dict):
            self.image = image_adapter.validate_python(new_value)


class NumberTypeMixin(DataTypeMixinABC):
    number: BlockbaxNumber

    @field_validator("number", mode="before")
    def convert_to_decimal(cls, value):  # pylint: disable=C0116.E0213
        return convert_number_to_decimal(value)

    @staticmethod
    def get_data_type() -> str:
        return "number"

    def get_value(self) -> Optional[BlockbaxValue]:
        return self.number

    def _set_value(self, new_value: Any):
        if isinstance(new_value, (int, float, Decimal)):
            self.number = Decimal(new_value)


class TextTypeMixin(DataTypeMixinABC):
    text: str

    @staticmethod
    def get_data_type() -> str:
        return "text"

    def get_value(self) -> Optional[BlockbaxValue]:
        return self.text

    def _set_value(self, new_value: Any):
        if isinstance(new_value, str):
            self.text = new_value


class AreaTypeMixin(DataTypeMixinABC):
    area: Area

    @staticmethod
    def get_data_type() -> str:
        return "area"

    def get_value(self) -> Optional[BlockbaxValue]:
        return self.area

    def _set_value(self, new_value: Any):
        if isinstance(new_value, Area):
            self.area = new_value
        elif isinstance(new_value, dict):
            self.area = area_adapter.validate_python(new_value)


class UnknownTypeMixin(DataTypeMixinABC):
    @staticmethod
    def get_data_type() -> str:
        return "unknown"

    def get_value(self) -> Optional[dict]:
        """
        Get extra fields new to the Python SDK set during validation.
        """
        return self.model_extra

    def _set_value(self, new_value: Any):
        pass
