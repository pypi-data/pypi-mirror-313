import unittest
from spacecases_common import SkinMetadatum, StickerItemMetadatum, Rarity


class TestItemMetadatum(unittest.TestCase):
    def test_sticker_item_metadatum_get_name_string(self):
        item_metadatum = StickerItemMetadatum(
            "Sticker | Crown Foil",
            Rarity.Legendary,
            4636400,
            "https://assets.spacecases.xyz/generated/images/unformatted/stickercrownfoil.png",
        )
        self.assertEqual(item_metadatum.get_rarity_string(), "Exotic")

    def test_skin_metadatum_get_name_string(self):
        item_metadatum = SkinMetadatum(
            "Souvenir AWP | Dragon Lore (Factory New)",
            Rarity.Ancient,
            48091900,
            "https://assets.spacecases.xyz/generated/images/unformatted/souvenirawpdragonlorefactorynew.png",
            "It has been custom painted with a knotwork dragon.",
            0.0,
            0.7,
        )
        self.assertEqual(item_metadatum.get_rarity_string(), "Covert")


if __name__ == "__main__":
    unittest.main()
