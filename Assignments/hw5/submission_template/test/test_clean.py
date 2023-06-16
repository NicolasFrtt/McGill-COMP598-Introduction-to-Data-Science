import unittest
from pathlib import Path
import os, sys
from src.clean import title_helper
from src.clean import date_helper
from src.clean import author_helper
from src.clean import total_count_helper
from src.clean import valid_format_helper
from src.clean import tags_helper
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class CleanTest(unittest.TestCase):

    def setUp(self):
        dr = os.path.dirname(__file__)
        p_fixture_1 = os.path.join(dr, "fixtures", "test_1.json")
        p_fixture_2 = os.path.join(dr, "fixtures", "test_2.json")
        p_fixture_3 = os.path.join(dr, "fixtures", "test_3.json")
        p_fixture_4 = os.path.join(dr, "fixtures", "test_4.json")
        p_fixture_5 = os.path.join(dr, "fixtures", "test_5.json")
        p_fixture_6 = os.path.join(dr, "fixtures", "test_6.json")
        with open(p_fixture_1) as f:
            record = f.readline()
            self.fixture1 = json.loads(record)
        with open(p_fixture_2) as f:
            record = f.readline()
            self.fixture2 = json.loads(record)
        with open(p_fixture_3) as f:
            record = f.readline()
            self.fixture3 = record #json.loads(record)
        with open(p_fixture_4) as f:
            record = f.readline()
            self.fixture4 = json.loads(record)
        with open(p_fixture_5) as f:
            record = f.readline()
            self.fixture5 = json.loads(record)
        with open(p_fixture_6) as f:
            record = f.readline()
            self.fixture6 = json.loads(record)


    def test_title(self):
        self.assertEqual(title_helper(self.fixture1), False)

    def test_date(self):
        self.assertEqual(date_helper(self.fixture2), False)

    def test_valid_format(self):
        self.assertEqual(valid_format_helper(self.fixture3), False)

    def test_author(self):
        self.assertEqual(author_helper(self.fixture4), False)

    def test_total_count(self):
        self.assertEqual(total_count_helper(self.fixture5), False)

    def test_tags(self):
        self.assertEqual(tags_helper(self.fixture6), 4)
    
if __name__ == '__main__':
    unittest.main()