from langcode_turner import langcode_turner
import unittest

class Test(unittest.TestCase):

    def test_iso639_turner(self):
        turn = langcode_turner("fr")
        assert turn.iso_639_3 == "fra"

    def test_iso639_turn_to_ids_code(self):
        turn = langcode_turner("est")
        assert turn.ids_code == 127
if __name__ == '__main__':
    unittest.main()