import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(os.path.join(parentdir, 'src'))
from compile_word_counts import compute_word_counts
from compute_pony_lang import compute_lang


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')

    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion,
        # i.e. self.assertEquals(...)
        print("\n\nRUNNING TEST FOR TASK 3")
        print("Ensure compile_word_counts.py works on the fixture")
        stopwords_path = os.path.join(os.getcwd(), "data", "stopwords.txt")
        with open(self.true_word_counts, 'r') as f:
            word_counts = json.load(f)
        self.assertEqual(compute_word_counts(self.mock_dialog, stopwords_path) == word_counts, True)
        print("OK")

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion,
        # i.e. self.assertEquals(...)
        print("\nRUNNING TEST FOR TASK 3")
        print("Ensure compute_pony_lang.py works on the fixture")
        with open(self.true_tf_idfs, 'r') as fh:
            scores = json.load(fh)
        self.assertEqual(compute_lang(self.true_word_counts, 5) == scores, True)
        print("OK")
        
    
if __name__ == '__main__':
    unittest.main()