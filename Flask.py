from flask import Flask, request, jsonify, render_template_string
import spacy
from textblob import TextBlob
from collections import Counter

# Initialize Flask app
app = Flask(__name__)

# Load spaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    # If model isn't found, provide a helpful error message
    import sys
    print("Error: en_core_web_sm model not found. Please install it with:")
    print("python -m spacy download en_core_web_sm")
    sys.exit(1)

def get_entities(text):
    """Extract named entities using spaCy"""
    doc = nlp(text)
    entities = []
    
    for ent in doc.ents:
        entities.append({
            'text': ent.text,
            'label': ent.label_,
            'start': ent.start_char,
            'end': ent.end_char
        })
    
    # Count entity types
    entity_counts = dict(Counter(ent['label'] for ent in entities))
    
    return {
        'entities': entities,
        'entity_counts': entity_counts
    }

def get_sentiment(text):
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Categorize sentiment based on polarity
    if polarity > 0.1:
        category = "positive"
    elif polarity < -0.1:
        category = "negative"
    else:
        category = "neutral"
    
    return {
        'polarity': round(polarity, 2),
        'subjectivity': round(subjectivity, 2),
        'category': category
    }

# Add a root route to provide API documentation and test interface
@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>NLP API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            pre { background: #f5f5f5; padding: 10px; border-radius: 5px; }
            .form { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            textarea { width: 100%; height: 100px; }
            button { margin-top: 10px; padding: 8px 15px; }
            #result { white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>Text Analysis API</h1>
        <h2>API Endpoints</h2>
        <h3>POST /analyze</h3>
        <p>Analyzes text for named entities and sentiment</p>
        <pre>
Request body:
{
    "text": "Your text to analyze"
}

Response:
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
        </pre>
        
        <div class="form">
            <h3>Test the API</h3>
            <textarea id="text" placeholder="Enter text to analyze..."></textarea>
            <br>
            <button onclick="analyzeText()">Analyze</button>
            <div id="result"></div>
        </div>
        
        <script>
        function analyzeText() {
            const text = document.getElementById('text').value;
            if (!text) {
                alert('Please enter some text to analyze');
                return;
            }
            
            fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({text})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                document.getElementById('result').textContent = 'Error: ' + error;
            });
        }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/analyze', methods=['POST'])
def analyze_text():
    # Check if request contains JSON data
    if not request.is_json:
        return jsonify({
            'error': 'Request must be JSON with a text field'
        }), 400
    
    # Get text from request
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({
            'error': 'Text field cannot be empty'
        }), 400
    
    try:
        # Perform NER and sentiment analysis
        ner_results = get_entities(text)
        sentiment_results = get_sentiment(text)
        
        # Combine results
        response = {
            'text': text,
            'ner': ner_results,
            'sentiment': sentiment_results
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': f'Analysis failed: {str(e)}'
        }), 500

# Add a health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    print(f"NLP API running at http://localhost:5000/")
    app.run(debug=True, port=5000, host='0.0.0.0')