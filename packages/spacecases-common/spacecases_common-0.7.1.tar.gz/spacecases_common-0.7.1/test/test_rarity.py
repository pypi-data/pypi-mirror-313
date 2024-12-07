import unittest
from spacecases_common import Rarity


class TestRarity(unittest.TestCase):
    def test_get_name_for_regular_item(self):
        for input, expected in [
            (Rarity.Common, "Base Grade"),
            (Rarity.Uncommon, "Industrial Grade"),
            (Rarity.Rare, "High Grade"),
            (Rarity.Mythical, "Remarkable"),
            (Rarity.Legendary, "Exotic"),
            (Rarity.Ancient, "Extraordinary"),
            (Rarity.Contraband, "Contraband"),
        ]:
            self.assertEqual(input.get_name_for_regular_item(), expected)

    def test_get_name_for_skin(self):
        for input, expected in [
            (Rarity.Common, "Consumer Grade"),
            (Rarity.Uncommon, "Industrial Grade"),
            (Rarity.Rare, "Mil-Spec"),
            (Rarity.Mythical, "Restricted"),
            (Rarity.Legendary, "Classified"),
            (Rarity.Ancient, "Covert"),
            (Rarity.Contraband, "Contraband"),
        ]:
            self.assertEqual(input.get_name_for_skin(), expected)


if __name__ == "__main__":
    unittest.main()
