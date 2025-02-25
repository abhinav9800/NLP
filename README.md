# Text Analysis Script

This script performs text analysis on a `.docx` file, including Named Entity Recognition (NER), Sentiment Analysis, and Word Cloud generation. It uses `spaCy`, `TextBlob`, `NLTK`, and `matplotlib` for various NLP and visualization tasks.

## Features
- **Named Entity Recognition (NER):** Extracts named entities using `spaCy`.
- **Sentiment Analysis:** Determines polarity (positive, neutral, or negative) and subjectivity using `TextBlob`.
- **Word Cloud Generation:** Creates a visualization of the most common words, excluding stopwords.
- **Entity Frequency Distribution:** Displays the frequency of extracted named entities.

## Installation
Make sure you have Python installed. Then, install the required dependencies:

```sh
pip install spacy textblob matplotlib wordcloud pandas python-docx nltk flask
python -m spacy download en_core_web_sm
```

## Usage
Run the script using the following command:

```sh
python script.py /path/to/your/document.docx
```

Replace `/path/to/your/document.docx` with the actual path to your `.docx` file.

## Functions
- `load_text(file_path)`: Loads text from a `.docx` file.
- `perform_ner(text)`: Performs Named Entity Recognition.
- `analyze_sentiment(text)`: Analyzes sentiment polarity and subjectivity.
- `visualize_entities(entity_counts)`: Creates a bar chart for entity frequencies.
- `create_wordcloud(text)`: Generates a word cloud of frequent words.
- `analyze_text(file_path)`: Main function to run the complete analysis.

## Flask API
This project includes a Flask API for text analysis. The API provides endpoints to analyze text for Named Entity Recognition (NER) and sentiment analysis.

### API Endpoints
#### `POST /analyze`
Analyzes the provided text for named entities and sentiment.

**Request Body:**
```json
{
    "text": "Your text to analyze"
}
```

**Response:**
```json
{
    "text": "Your text to analyze",
    "ner": {
        "entities": [...],
        "entity_counts": {...}
    },
    "sentiment": {
        "polarity": 0.0,
        "subjectivity": 0.0,
        "category": "neutral"
    }
}
```

#### `GET /health`
Returns the API health status.

**Response:**
```json
{
    "status": "ok"
}
```

### Running the Flask API
To start the Flask server, run:

```sh
python flask_app.py
```

The API will be accessible at `http://localhost:5000/`.

## Notes
- Ensure that `nltk` resources are downloaded before running the script:
  ```python
  import nltk
  nltk.download('stopwords')
  nltk.download('punkt_tab')
  ```
- The script is designed to run in a Jupyter Notebook or Python script.

## Example Output
After running the script, you will see:
- A printed table of named entities and their categories.
- Sentiment analysis results.
- A bar chart of entity frequencies (if entities are found).
- A word cloud visualization of the most frequent words.


