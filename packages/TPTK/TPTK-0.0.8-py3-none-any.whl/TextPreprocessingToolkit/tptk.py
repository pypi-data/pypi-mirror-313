import string
import re
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from spellchecker import SpellChecker
from typing import List, Optional, Union
from IPython.display import display
import logging

# Download required NLTK resources
import nltk
nltk.download("averaged_perceptron_tagger", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TextPreprocessor:
    """
    Comprehensive text preprocessing class for NLP tasks.
    """
    __version__ = "1.1.0"  # Updated version with optimized code

    def __init__(self, custom_stopwords: Optional[List[str]] = None) -> None:
        """
        Initialize the text preprocessor.

        Parameters:
        custom_stopwords (list, optional): List of additional stopwords to remove.
        """
        self.stopwords = set(stopwords.words("english"))
        if custom_stopwords:
            self.stopwords.update(custom_stopwords)

        self.lemmatizer = WordNetLemmatizer()
        self.spell_checker = SpellChecker()
        self.wordnet_map = {
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "J": wordnet.ADJ,
            "R": wordnet.ADV,
        }

    def tokenize(self, text: Optional[str]) -> List[str]:
        """Tokenize text into words."""
        return word_tokenize(text) if text else []

    def remove_punctuation(self, text: Optional[str]) -> Optional[str]:
        """Remove punctuation from text."""
        return re.sub(f"[{re.escape(string.punctuation)}]", "", text) if text else text

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stopwords from tokenized text."""
        return [word for word in tokens if word.lower() not in self.stopwords]

    def remove_special_characters(self, text: Optional[str]) -> Optional[str]:
        """Remove special characters from text."""
        return re.sub(r"[^a-zA-Z0-9\s]", "", text).strip() if text else text

    def lemmatize_text(self, text: Optional[str]) -> Optional[str]:
        """Lemmatize text using WordNet."""
        if not text:
            return text
        tokens = self.tokenize(text)
        pos_tags = pos_tag(tokens)
        return " ".join(
            self.lemmatizer.lemmatize(word, self.wordnet_map.get(pos[0].upper(), wordnet.NOUN))
            for word, pos in pos_tags
        )

    def correct_spellings(self, text: Optional[str]) -> Optional[str]:
        """Correct misspelled words in text."""
        if not text:
            return text
        tokens = self.tokenize(text)
        return " ".join(self.spell_checker.correction(word) if word in self.spell_checker else word for word in tokens)

    def lowercase(self, text: Optional[str]) -> Optional[str]:
        """Convert text to lowercase."""
        return text.lower() if text else text

    def remove_url(self, text: Optional[str]) -> Optional[str]:
        """Remove URLs from text."""
        return re.sub(r"https?://\S+|www\.\S+", "", text) if text else text

    def remove_html_tags(self, text: Optional[str]) -> Optional[str]:
        """Remove HTML tags from text."""
        return re.sub(r"<[^>]+>", "", text) if text else text

    def preprocess(
        self, text: str, steps: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Preprocess text with a pipeline of processing steps.

        Parameters:
        text (str): The input text to preprocess.
        steps (list, optional): List of preprocessing steps in desired order.

        Returns:
        str: Preprocessed text.
        """
        if not text:
            return text

        steps = steps or [
            "lowercase",
            "remove_url",
            "remove_html_tags",
            "remove_punctuation",
            "remove_special_characters",
            "correct_spellings",
            "lemmatize_text",
        ]

        for step in steps:
            try:
                func = getattr(self, step)
                text = func(text)
                logging.info(f"Step '{step}' completed.")
            except Exception as e:
                logging.error(f"Error during step '{step}': {e}")
        return text

    def head(self, texts: Union[List[str], pd.Series], n: int = 5) -> None:
        """
        Display a summary of the first few entries of the dataset.

        Parameters:
        texts (list or pd.Series): The dataset or list of text entries.
        n (int): Number of rows to display.
        """
        if isinstance(texts, (list, pd.Series)):
            data = pd.DataFrame({"Original Text": texts[:n]})
            data["Processed Text"] = data["Original Text"].apply(self.preprocess)
            data["Word Count"] = data["Processed Text"].apply(lambda x: len(x.split()) if x else 0)
            data["Character Count"] = data["Processed Text"].apply(len)
            display(data)


if __name__ == "__main__":
    # Example usage
    tpt = TextPreprocessor()
