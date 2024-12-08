

# TextPreprocessor

`TextPreprocessor` is a comprehensive Python library for text preprocessing in NLP tasks. It includes a suite of features such as tokenization, punctuation removal, stopword removal, lemmatization, spell correction, and more. This package is designed to streamline and simplify text preprocessing for data analysis, machine learning, and natural language processing projects.

---

## Features

- Tokenization
- Stopword removal (with customizable stopwords)
- Punctuation removal
- Special character removal
- URL and HTML tag removal
- Lowercasing
- Lemmatization (WordNet-based)
- Spell correction
- Modular preprocessing pipeline

---

## Installation

Ensure the following dependencies are installed:
- Python 3.7 or higher
- Required Python packages:
  ```bash
  pip install nltk pyspellchecker pandas
  ```

Additionally, download required NLTK resources:
```python
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
```

---

## Usage

### Initialization

Import the `TextPreprocessing` class and initialize it. Optionally, pass a list of custom stopwords:

```python
from textPreprocessingToolkit import TextPreprocessor

# Initialize with optional custom stopwords
tpt = TextPreprocessor(custom_stopwords=["example", "test"])
```

---

### Preprocessing Text

Preprocess a single piece of text by specifying a sequence of preprocessing steps:

```python
text = "Hello! This is an <b>example</b> sentence. Visit https://example.com for more info!"
processed_text = tpt.preprocess(
    text, 
    steps=[
        "lowercase",
        "remove_punctuation",
        "remove_special_characters",
        "remove_url",
        "remove_html_tags",
        "correct_spellings",
        "lemmatize_text"
    ]
)
print("Processed Text:", processed_text)
```

**Output:**
```
Processed Text: hello this is an example sentence visit for more info
```

---

### Batch Processing

You can preprocess a batch of texts and view a summary:

```python
texts = [
    "NLP preprocessing includes tokenization, lemmatization, and stemming.",
    "Special characters like @, $, %, &, should be removed!",
    "Spelling erorrs in this sentense should be fixed.",
]
tpt.head(texts, n=3)
```

This will display a table (in Jupyter or IPython environments) with the following columns:
- **Original Text**
- **Processed Text**
- **Word Count**
- **Character Count**

---

### Modular Methods

You can also use individual methods for specific preprocessing tasks:

```python
text = "Check for spelling erorrs in this sentense."
print("Tokenized:", tpt.tokenize(text))
print("Spell-corrected:", tpt.correct_spellings(text))
print("Lemmatized:", tpt.lemmatize_text(text))
```

---

## Class Documentation

### `TextPreprocessor`

#### Initialization:
```python
TextPreprocessor(custom_stopwords: Optional[List[str]] = None)
```
- `custom_stopwords`: (Optional) A list of additional stopwords to remove.

#### Methods:
- **`preprocess(text: str, steps: Optional[List[str]] = None) -> str`**
  - Preprocesses the input text according to the specified pipeline steps.
- **`tokenize(text: str) -> List[str]`**
  - Tokenizes text into words.
- **`remove_punctuation(text: str) -> str`**
  - Removes punctuation from the text.
- **`remove_stopwords(tokens: List[str]) -> List[str]`**
  - Removes stopwords from a tokenized list.
- **`remove_special_characters(text: str) -> str`**
  - Removes non-alphanumeric characters from the text.
- **`correct_spellings(text: str) -> str`**
  - Corrects misspellings in the text.
- **`lemmatize_text(text: str) -> str`**
  - Lemmatizes text using WordNet.

---

## Logging

The package includes built-in logging for debugging and tracking progress. Logs are displayed for each preprocessing step completed.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author

Developed by **[Your Name]**. Feel free to reach out for suggestions or collaboration!

---

## Feedback

If you encounter any issues or have suggestions for improvement, please open an issue on GitHub or contact jaiswalgaurav863@gmail.com.

