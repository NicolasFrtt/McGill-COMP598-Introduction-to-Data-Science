import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(os.path.join(parentdir, 'src'))
from compile_word_counts import generate_count
from compute_pony_lang import generate_tfidf

class TasksTest(unittest.TestCase):
    
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        
    def test_task1(self):
        stop_words = os.path.join(os.getcwd(), "data", "stopwords.txt")
        json_to_test = generate_count(self.mock_dialog,stop_words)
        with open(self.true_word_counts,"r") as file:
            json_true_values = json.load(file)
        self.assertEqual(json_to_test == json_true_values,True)

    def test_task2(self):
        json_to_test = generate_tfidf(self.true_word_counts,5)
        print(json_to_test)
        with open(self.true_tf_idfs,"r") as file:
            json_true_values = json.load(file)
        self.assertEqual(json_to_test == json_true_values,True)
        
    
if __name__ == '__main__':
    unittest.main()