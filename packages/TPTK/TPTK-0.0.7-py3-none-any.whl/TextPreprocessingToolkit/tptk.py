import string
import re
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from spellchecker import SpellChecker
from typing import List, Optional, Union
from IPython.display import display
import logging

# Download required NLTK resources if not already downloaded
import nltk

nltk.download("averaged_perceptron_tagger", quiet=True)  # Fixed resource name
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)  # Tokenizer required for word_tokenize

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TextPreprocessor:
    """
    A comprehensive text preprocessing class supporting common NLP tasks, 
    such as tokenization, removing stopwords, lemmatization, stemming, and more.
    """
    __version__ = "0.0.7"  # Updated version with tokenization and bug fixes

    def __init__(self, custom_stopwords: Optional[List[str]] = None) -> None:
        """
        Initialize the text preprocessor.

        Parameters:
        custom_stopwords (list, optional): List of additional stopwords to remove.
        """
        self.stopwords: set[str] = set(stopwords.words("english"))
        if custom_stopwords:
            self.stopwords.update(custom_stopwords)

        self.lemmatizer: WordNetLemmatizer = WordNetLemmatizer()
        self.spell_checker: SpellChecker = SpellChecker()
        self.stemmer: PorterStemmer = PorterStemmer()
        self.wordnet_map: dict[str, wordnet] = {
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "J": wordnet.ADJ,
            "R": wordnet.ADV,
        }

    def _safe_call(self, func, text: Optional[str]) -> Optional[str]:
        """
        Helper function to safely call processing methods and log errors.
        """
        try:
            return func(text)
        except Exception as e:
            logging.error(f"Error in '{func.__name__}': {e}")
            return text

    def tokenize(self, text: Optional[str]) -> Optional[List[str]]:
        """Tokenize text into words."""
        return word_tokenize(text) if text else []

    def remove_punctuation(self, text: Optional[str]) -> Optional[str]:
        """Remove punctuation from text."""
        return text.translate(str.maketrans("", "", string.punctuation)) if text else text

    def remove_stopwords(self, text: Optional[str]) -> Optional[str]:
        """Remove stopwords from text."""
        tokens = self.tokenize(text)
        return " ".join([word for word in tokens if word.lower() not in self.stopwords]) if text else text

    def remove_special_characters(self, text: Optional[str]) -> Optional[str]:
        """Remove special characters from text."""
        return re.sub(r"\s+", " ", re.sub(r"[^a-zA-Z0-9\s]", " ", text)).strip() if text else text

    def stem_text(self, text: Optional[str]) -> Optional[str]:
        """Apply stemming to text."""
        tokens = self.tokenize(text)
        return " ".join([self.stemmer.stem(word) for word in tokens]) if text else text

    def lemmatize_text(self, text: Optional[str]) -> Optional[str]:
        """Lemmatize text using WordNet."""
        if text:
            tokens = self.tokenize(text)
            pos_text = pos_tag(tokens)
            return " ".join(
                [
                    self.lemmatizer.lemmatize(
                        word, self.wordnet_map.get(pos[0].upper(), wordnet.NOUN)
                    )
                    for word, pos in pos_text
                ]
            )
        return text

    def remove_url(self, text: Optional[str]) -> Optional[str]:
        """Remove URLs from text."""
        return re.sub(r"https?://\S+|www\.\S+", "", text) if text else text

    def remove_html_tags(self, text: Optional[str]) -> Optional[str]:
        """Remove HTML tags from text."""
        return re.sub(r"<[^>]+>", "", text) if text else text

    def correct_spellings(self, text: Optional[str]) -> Optional[str]:
        """Correct misspelled words in text."""
        tokens = self.tokenize(text)
        if tokens:
            misspelled_words = self.spell_checker.unknown(tokens)
            return " ".join(
                [self.spell_checker.correction(word) if word in misspelled_words else word for word in tokens]
            )
        return text

    def lowercase(self, text: Optional[str]) -> Optional[str]:
        """Convert text to lowercase."""
        return text.lower() if text else text

    def preprocess(
        self, text: str, steps: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Preprocess text with a pipeline of processing steps.

        Parameters:
        text (str): The input text to preprocess.
        steps (list, optional): List of preprocessing steps in desired order. If None, the default pipeline is applied.

        Returns:
        str: Preprocessed text.
        """
        if not text:
            return text

        default_pipeline = [
            "lowercase",
            "remove_punctuation",
            "remove_stopwords",
            "remove_special_characters",
            "remove_url",
            "remove_html_tags",
            "correct_spellings",
            "lemmatize_text",
        ]
        steps = steps or default_pipeline

        for step in steps:
            text = self._safe_call(getattr(self, step), text)
            logging.info(f"Step '{step}' completed.")
        return text

    def head(self, texts: Union[List[str], pd.Series], n: int = 5) -> None:
        """
        Display a summary of the first few entries of the dataset for quick visualization.

        Parameters:
        texts (list or pd.Series): The dataset or list of text entries to display.
        n (int): The number of rows to display. Default is 5.

        Returns:
        None
        """
        if isinstance(texts, (list, pd.Series)):
            data = pd.DataFrame({"Original Text": texts[:n]})
            data["Processed Text"] = data["Original Text"].apply(self.preprocess)
            data["Word Count"] = data["Processed Text"].apply(lambda x: len(x.split()))
            data["Character Count"] = data["Processed Text"].apply(len)
            display(data)


if __name__ == "__main__":
    # Correct class usage
    tpt = TextPreprocessor()

