import re
import string
from dataclasses import dataclass
from typing import Optional
from enum import IntEnum
from abc import ABC, abstractmethod

__all__ = [
    "Rarity",
    "ItemMetadatum",
    "SkinMetadatum",
    "RegularItemMetadatum",
    "Container",
    "remove_skin_name_formatting",
]


class Rarity(IntEnum):
    Common = 0
    Uncommon = 1
    Rare = 2
    Mythical = 3
    Legendary = 4
    Ancient = 5
    Contraband = 6

    def get_name_for_skin(self) -> str:
        """
        Get the rarity string if the item is a skin
        """
        return [
            "Consumer Grade",
            "Industrial Grade",
            "Mil-Spec",
            "Restricted",
            "Classified",
            "Covert",
            "Contraband",
        ][self.value]

    def get_name_for_regular_item(self) -> str:
        """
        Get the rarity string if the item is a regular item
        """
        return [
            "Base Grade",
            "Industrial Grade",
            "High Grade",
            "Remarkable",
            "Exotic",
            "Extraordinary",
            "Contraband",
        ][self.value]


@dataclass
class ItemMetadatum(ABC):
    """
    Base class for different types of ItemMetadatum. Every single item contains atleast these fields and implements these methods.
    """

    formatted_name: str
    rarity: Rarity
    price: int
    image_url: str

    @abstractmethod
    def get_rarity_string(self) -> str:
        """
        Obtain the corresponding rarity string on the type of the item
        """


@dataclass
class SkinMetadatum(ItemMetadatum):
    """
    An ItemMetadatum that also includes an optional description and a float range.
    """

    description: Optional[str]
    min_float: float
    max_float: float

    def get_rarity_string(self) -> str:
        return self.rarity.get_name_for_skin()


@dataclass
class RegularItemMetadatum(ItemMetadatum):
    """A RegularItemMetadatum is just an item metadatum for all items apart from skins. Regular items don't have descriptions or floats."""

    def get_rarity_string(self) -> str:
        return self.rarity.get_name_for_regular_item()


@dataclass
class Container:
    formatted_name: str
    image_url: str
    price: int
    contains: dict[Rarity, list[str]]


_SPECIAL_CHARS_REGEX = re.compile(r"[™★♥\s]")


def remove_skin_name_formatting(skin_name: str) -> str:
    """
    Removes formatting from skin names:
    - Converts to lowercase
    - Removes punctuation, whitespace and special characters
    """
    skin_name = _SPECIAL_CHARS_REGEX.sub("", skin_name.lower())
    return skin_name.translate(str.maketrans("", "", string.punctuation))
