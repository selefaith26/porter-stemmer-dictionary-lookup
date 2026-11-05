import unittest

from dictionary_checker import BUNDLED_DICTIONARY, build_stem_index, load_dictionary, look_up
from porter_stemmer import measure, stem

# 1. Examples taken from the rules in Porter (1980)
PAPER_EXAMPLES = {
    "step 1a": {"caresses": "caress", "ponies": "poni", "ties": "ti", "caress": "caress", "cats": "cat"},
    "step 1b": {"feed": "feed", "agreed": "agre", "plastered": "plaster", "bled": "bled",
                "motoring": "motor", "sing": "sing", "conflated": "conflat", "troubled": "troubl",
                "sized": "size", "hopping": "hop", "tanned": "tan", "falling": "fall",
                "hissing": "hiss", "fizzed": "fizz", "failing": "fail", "filing": "file"},
    "step 1c": {"happy": "happi", "sky": "sky"},
    "step 2": {"relational": "relat", "conditional": "condit", "rational": "ration",
               "digitizer": "digit", "conformabli": "conform", "radicalli": "radic",
               "differentli": "differ", "vileli": "vile", "analogousli": "analog"},
    "step 3": {"triplicate": "triplic", "formative": "form", "formalize": "formal",
               "electriciti": "electr", "electrical": "electr", "hopeful": "hope", "goodness": "good"},
    "step 4": {"revival": "reviv", "allowance": "allow", "inference": "infer", "airliner": "airlin",
               "gyroscopic": "gyroscop", "adjustable": "adjust", "defensible": "defens",
               "irritant": "irrit", "replacement": "replac", "adjustment": "adjust",
               "dependent": "depend", "adoption": "adopt", "communism": "commun",
               "activate": "activ", "effective": "effect", "bowdlerize": "bowdler"},
    "step 5": {"probate": "probat", "rate": "rate", "cease": "ceas", "controll": "control", "roll": "roll"},
}


class TestPorterRules(unittest.TestCase):
    def test_measure_examples_from_paper(self):
        for word, m in {"tr": 0, "ee": 0, "tree": 0, "y": 0, "by": 0, "trouble": 1, "oats": 1,
                        "trees": 1, "ivy": 1, "troubles": 2, "private": 2, "oaten": 2, "orrery": 2}.items():
            self.assertEqual(measure(word), m, word)

    def test_examples_from_paper(self):
        for step, cases in PAPER_EXAMPLES.items():
            for word, expected in cases.items():
                self.assertEqual(stem(word), expected, f"{step}: {word}")

    def test_short_words_are_left_alone(self):
        for word in ["a", "is", "us", "be"]:
            self.assertEqual(stem(word), word)

    def test_uppercase_is_lowered(self):
        self.assertEqual(stem("RUNNING"), "run")


class TestAssignmentExample(unittest.TestCase):
    def setUp(self):
        self.index = build_stem_index({"swim", "fish", "cheese"})

    def test_yes_cases(self):
        for word in ["swimming", "fishing", "cheeses", "swim", "fish", "cheese"]:
            self.assertEqual(look_up(word, self.index)[0], "yes", word)

    def test_no_cases(self):
        for word in ["chocolate", "swam"]:
            self.assertEqual(look_up(word, self.index)[0], "no", word)


class TestInputHandling(unittest.TestCase):
    def setUp(self):
        self.index = build_stem_index({"swim", "fish", "cheese"})

    def test_case_spaces_and_punctuation(self):
        for text in ["SWIMMING", "  swimming  ", "Swimming!", "(swimming)", "swimming."]:
            self.assertEqual(look_up(text, self.index)[0], "yes", text)

    def test_invalid_input_is_rejected(self):
        for text in ["", "   ", "42", "swim-ming", "two words", "café", "don't", "a1"]:
            self.assertIsNone(look_up(text, self.index)[0], text)

    def test_unknown_word(self):
        self.assertEqual(look_up("xyzzy", self.index)[0], "no")


class TestFullDictionary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.words = load_dictionary(BUNDLED_DICTIONARY)
        cls.index = build_stem_index(cls.words)

    def test_dictionary_size(self):
        self.assertGreater(len(self.words), 200000)

    def test_every_dictionary_word_is_found(self):
        missing = [w for w in self.words if look_up(w, self.index)[0] != "yes"]
        self.assertEqual(missing, [])

    def test_regular_inflections_of_missing_forms(self):
        forms = ["walked", "jumping", "computers", "pencils", "swims", "houses"]
        for word in forms:
            self.assertNotIn(word, self.words)
            self.assertEqual(look_up(word, self.index)[0], "yes", word)

    def test_words_newer_than_the_dictionary_are_rejected(self):
        self.assertNotIn("laptop", self.words)
        self.assertEqual(look_up("laptops", self.index)[0], "no")

    def test_nonsense_words_are_rejected(self):
        for word in ["qzxv", "blorptastic", "xxyyzz"]:
            self.assertEqual(look_up(word, self.index)[0], "no", word)


class TestAgainstReference(unittest.TestCase):
    def test_matches_nltk_original_algorithm(self):
        try:
            from nltk.stem.porter import PorterStemmer
        except ImportError:
            self.skipTest("nltk is not installed")
        reference = PorterStemmer(mode="ORIGINAL_ALGORITHM")
        words = load_dictionary(BUNDLED_DICTIONARY)
        differences = [w for w in words if len(w) > 2 and stem(w) != reference.stem(w)]
        print(f"\nCompared {len(words):,} words with NLTK: {len(differences)} differences")
        self.assertEqual(differences, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
