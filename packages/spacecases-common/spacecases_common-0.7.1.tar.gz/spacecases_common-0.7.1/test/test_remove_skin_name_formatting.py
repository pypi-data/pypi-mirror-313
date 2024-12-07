import unittest
import string
from spacecases_common import remove_skin_name_formatting


class TestRemoveSkinNameFormatting(unittest.TestCase):
    def test_basic_skin_name(self):
        self.assertEqual(
            remove_skin_name_formatting("AK-47 | Redline (Factory New)"),
            "ak47redlinefactorynew",
        )

    def test_name_with_characters_to_be_removed(self):
        self.assertEqual(
            remove_skin_name_formatting("★ Bayonet | Doppler - Phase 1 (Field-Tested)"),
            "bayonetdopplerphase1fieldtested",
        )
        self.assertEqual(
            remove_skin_name_formatting("StatTrak™ M4A4 | Asiimov"),
            "stattrakm4a4asiimov",
        )
        self.assertEqual(
            remove_skin_name_formatting("Negev | dev_texture (Field-Tested)"),
            "negevdevtexturefieldtested",
        )
        self.assertEqual(
            remove_skin_name_formatting("SG 553 | Ol' Rusty (Battle-Scarred)"),
            "sg553olrustybattlescarred",
        )
        self.assertEqual(
            remove_skin_name_formatting("Souvenir Negev | Mjölnir (Well-Worn)"),
            "souvenirnegevmjölnirwellworn",
        )

    def test_name_with_spaces(self):
        self.assertEqual(
            remove_skin_name_formatting(
                "          ★ Bayonet        | Doppler - Phase 1 (Field-Tested)         "
            ),
            "bayonetdopplerphase1fieldtested",
        )
        self.assertEqual(
            remove_skin_name_formatting("  S    tatTrak™ M4A4 | Asi     imov"),
            "stattrakm4a4asiimov",
        )

    def test_name_with_special_characeters(self):
        self.assertEqual(
            remove_skin_name_formatting("Desert Eagle | Sunset Storm 弐"),
            "deserteaglesunsetstorm弐",
        )
        self.assertEqual(
            remove_skin_name_formatting("Desert Eagle | Sunset Storm 壱"),
            "deserteaglesunsetstorm壱",
        )

    def test_punctuation_string(self):
        self.assertEqual(remove_skin_name_formatting(string.punctuation), "")


if __name__ == "__main__":
    unittest.main()
