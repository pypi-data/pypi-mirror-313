import unittest
from smcore import TagSet

base = TagSet("hello", "world", "tags")


class TestTagSet(unittest.TestCase):
    def test_match1(self):
        test_case = TagSet("hello", "world", "tags")
        self.assertTrue(base.matches(test_case))

    def test_match2(self):
        test_case = TagSet("hello", "world", "a-different-tag")
        self.assertFalse(base.matches(test_case))

    def test_match3(self):
        test_case = TagSet("hello", "world")
        self.assertFalse(base.matches(test_case))

    def test_match4(self):
        test_case = TagSet("hello", "world", "tags", "test")
        self.assertTrue(base.matches(test_case))

    def test_match5(self):
        test_case = TagSet("hello", "world", "tags", "test", "no-test")
        self.assertTrue(base.matches(test_case))


if __name__ == "__main__":
    unittest.main()
