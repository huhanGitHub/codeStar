# Importing the required libraries
import re
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import matplotlib.pyplot as plt

# Hard-coded list of common English stopwords for demonstration purposes
STOPWORDS = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", 
                 "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", 
                 "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", 
                 "theirs", "themselves", "what", "which", "who", "whom", "this", "that", 
                 "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", 
                 "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", 
                 "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", 
                 "at", "by", "for", "with", "about", "against", "between", "into", "through", 
                 "during", "before", "after", "above", "below", "to", "from", "up", "down", 
                 "in", "out", "on", "off", "over", "under", "again", "further", "then", "once"])

def f_496(text, n=2):
    """
    This function performs the following tasks:
    1. Removes duplicate consecutive words and stopwords from a string "text."
    2. Generates a square co-occurrence matrix of the words in the text.
    3. Plots the co-occurrence matrix using matplotlib.

    Parameters:
    text (str): The text string to analyze.
    n (int, optional): The size of the n-grams. Defaults to 2.

    Returns:
    tuple: A tuple containing:
        - DataFrame: The square co-occurrence matrix of the words in the text. The DataFrame has both row and column labels as the unique words in the text.
        - AxesSubplot: The matplotlib plot object of the co-occurrence matrix.

    Requirements:
    - re
    - sklearn.feature_extraction.text.CountVectorizer
    - pandas
    - matplotlib.pyplot

    Constants:
    - STOPWORDS: A set of common English stopwords used to filter the words in the text.

    Examples:
    >>> text = "The quick brown fox jumps over the lazy dog and the dog was not that quick to respond."
    >>> matrix, plot = f_496(text, n=2)
    >>> print(matrix)
    >>> print(type(plot))
    """
    # Remove duplicate consecutive words
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text)
    
    # Remove stopwords
    words = [word for word in re.findall(r'\b\w+\b', text.lower()) if word not in STOPWORDS]
    
    # Generate co-occurrence matrix
    vectorizer = CountVectorizer(ngram_range=(n, n))
    X = vectorizer.fit_transform(words)
    matrix = X.T * X
    matrix.setdiag(0)
    matrix_df = pd.DataFrame(matrix.todense(), index=vectorizer.get_feature_names(), columns=vectorizer.get_feature_names())
    
    # Plot co-occurrence matrix
    fig, ax = plt.subplots()
    ax.imshow(matrix_df, cmap='hot', interpolation='nearest')
    ax.set_title("Co-occurrence Matrix")
    ax.set_xlabel("Words")
    ax.set_ylabel("Words")
    
    return matrix_df, ax

# Importing required libraries for testing
import unittest
import pandas as pd
import matplotlib.axes

# Define the run_tests function
def run_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCases))
    runner = unittest.TextTestRunner()
    runner.run(suite)

# Define the TestCases class
class TestCases(unittest.TestCase):

    def test_case_1(self):
        text = "hello world world"
        matrix, plot = f_496(text)
        self.assertIsInstance(matrix, pd.DataFrame)
        self.assertIsInstance(plot, matplotlib.axes.SubplotBase)
        self.assertEqual(matrix.shape, (2, 2))  # 2 unique words: "hello" and "world"

    def test_case_2(self):
        text = "The quick brown fox jumps over the lazy dog."
        matrix, plot = f_496(text)
        self.assertIsInstance(matrix, pd.DataFrame)
        self.assertIsInstance(plot, matplotlib.axes.SubplotBase)
        self.assertEqual(matrix.shape, (8, 8))  # 8 unique words after removing stopwords and duplicates

    def test_case_3(self):
        text = "Python Python is great for data science."
        matrix, plot = f_496(text, n=3)
        self.assertIsInstance(matrix, pd.DataFrame)
        self.assertIsInstance(plot, matplotlib.axes.SubplotBase)
        self.assertEqual(matrix.shape, (4, 4))  # 4 unique words after removing stopwords and duplicates

    def test_case_4(self):
        text = "Simple example with simple words."
        matrix, plot = f_496(text)
        self.assertIsInstance(matrix, pd.DataFrame)
        self.assertIsInstance(plot, matplotlib.axes.SubplotBase)
        self.assertEqual(matrix.shape, (4, 4))  # 4 unique words after removing stopwords and duplicates

    def test_case_5(self):
        text = "Duplicate duplicate words words are are removed."
        matrix, plot = f_496(text)
        self.assertIsInstance(matrix, pd.DataFrame)
        self.assertIsInstance(plot, matplotlib.axes.SubplotBase)
        self.assertEqual(matrix.shape, (3, 3))  # 3 unique words after removing stopwords and duplicates


if __name__ == "__main__":
    run_tests()