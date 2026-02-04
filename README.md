# Indian Language Text Normalization + SSML Rule Generator for TTS

A production-ready framework for automatically normalizing raw user text into speech-friendly expanded form with SSML rules for multiple Indian languages. Designed for Speech Synthesis platforms like Samsung Bixby TTS.

## Features

✅ **Full Support for Hindi (hi-IN) and Tamil (ta-IN)**
- Cardinal numbers: "123" → "एक सौ तेईस" (Hindi) / "நூற்று இருபத்து மூன்று" (Tamil)
- Ordinal numbers: "1st" → "पहला" / Tamil equivalent
- Currency: "₹250" → "दो सौ पचास रुपये" / "இருநூறு ஐம்பது ரூபாய்"
- Dates: "12/03/2024" → Spoken date form
- Units: "5kg" → "पाँच किलोग्राम" / Tamil equivalent
- Time: "10:30AM" → "सुबह दस बजकर तीस मिनट" / Tamil equivalent
- Abbreviations: "Dr." → "डॉक्टर" / Tamil equivalent

✅ **Scalable Architecture**
- Easy to add new Indian languages (te-IN, kn-IN, ml-IN, bn-IN, mr-IN, gu-IN, pa-IN, etc.)
- Rule-based system with YAML configuration files
- DFA-based pattern matching for fast runtime normalization

✅ **Production Ready**
- FastAPI backend with comprehensive API endpoints
- React frontend with Tailwind CSS dashboard
- Docker containerization
- Unit tests included
- Well-documented codebase

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── normalization/
│   │   ├── pipeline.py         # Main normalization pipeline
│   │   ├── rule_engine.py      # Rule loading and management
│   │   ├── dfa_engine.py       # DFA pattern matching
│   │   ├── ssml_generator.py   # SSML output generation
│   │   ├── number_normalizer.py
│   │   ├── date_normalizer.py
│   │   ├── time_normalizer.py
│   │   ├── currency_normalizer.py
│   │   ├── unit_normalizer.py
│   │   └── abbreviation_normalizer.py
│   ├── locales/
│   │   ├── hi-IN.yml           # Hindi rules
│   │   └── ta-IN.yml           # Tamil rules
│   ├── tests/                  # Unit tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── index.js
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- (Optional) Python 3.11+ and Node.js 18+ for local development

### Running with Docker

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Start the services:**
   ```bash
   docker-compose up
   ```

3. **Access the application:**
   - Frontend Dashboard: http://localhost:3000
   - Backend API Docs: http://localhost:8000/docs
   - Backend Health Check: http://localhost:8000/health

### Local Development

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

## API Endpoints

### POST /normalize
Normalize text for a given locale.

**Request:**
```json
{
  "locale": "hi-IN",
  "text": "₹250 on 12/03/2024"
}
```

**Response:**
```json
{
  "original_text": "₹250 on 12/03/2024",
  "normalized_text": "दो सौ पचास रुपये on बारह मार्च दो हजार चौबीस",
  "locale": "hi-IN",
  "tokens": [
    {
      "original": "₹250",
      "normalized": "दो सौ पचास रुपये",
      "category": "currency",
      "start": 0,
      "end": 4
    }
  ]
}
```

### POST /generate_ssml
Generate SSML output for normalized text.

**Request:**
```json
{
  "locale": "hi-IN",
  "text": "₹250",
  "use_ssml": true
}
```

**Response:**
```json
{
  "original_text": "₹250",
  "normalized_text": "दो सौ पचास रुपये",
  "ssml": "<speak xml:lang=\"hi-IN\"><say-as interpret-as=\"currency\">दो सौ पचास रुपये</say-as></speak>",
  "locale": "hi-IN"
}
```

### GET /locales
Get all supported locales.

**Response:**
```json
{
  "locales": ["hi-IN", "ta-IN"],
  "count": 2
}
```

### GET /export_rules/{locale}
Export normalization rules for a locale.

**Response:**
```json
{
  "locale": "hi-IN",
  "rules": { ... }
}
```

## Adding a New Language

To add support for a new Indian language (e.g., Telugu `te-IN`):

1. **Create a new locale file:**
   ```bash
   cp backend/locales/hi-IN.yml backend/locales/te-IN.yml
   ```

2. **Edit the locale file** with Telugu-specific rules:
   - Update `locale`, `language`, and `name` fields
   - Translate all number words, month names, etc.
   - Update patterns and mappings

3. **Test the new locale:**
   ```bash
   cd backend
   python -m pytest tests/
   ```

4. **Restart the service:**
   ```bash
   docker-compose restart backend
   ```

The new locale will automatically be available in the API and frontend!

## Testing

Run the test suite:

```bash
cd backend
python -m pytest tests/
```

Or run specific tests:

```bash
python -m pytest tests/test_number_normalizer.py
python -m pytest tests/test_pipeline.py
python -m pytest tests/test_samples.py
```

## Architecture Details

### Normalization Pipeline

The pipeline processes text in the following order:

1. **Tokenization**: Identifies potential normalization targets
2. **Category Detection**: Determines the type (number, currency, date, etc.)
3. **Pattern Matching**: Uses DFA-based matching for fast recognition
4. **Expansion**: Converts to speech-friendly form using locale rules
5. **SSML Generation**: Wraps normalized text in SSML tags for TTS

### Rule Engine

- Rules are stored as YAML files in `backend/locales/`
- Each locale file contains:
  - Number words (ones, tens, hundreds, thousands, lakhs, crores)
  - Currency names and symbols
  - Month and day names
  - Time expressions
  - Unit mappings
  - Abbreviation mappings
  - Regex patterns for detection

### DFA Engine

The DFA engine provides fast pattern matching by:
- Converting regex patterns to deterministic finite automata
- Enabling O(n) text scanning complexity
- Supporting overlapping pattern resolution

## Sample Test Sentences

### Hindi (hi-IN)
- `₹250 on 12/03/2024` → Currency and date normalization
- `10:30AM पर मिलते हैं` → Time normalization
- `5kg चावल` → Unit normalization
- `Dr. शर्मा आए` → Abbreviation normalization
- `123 लोग` → Number normalization

### Tamil (ta-IN)
- `₹250 on 12/03/2024` → Currency and date normalization
- `10:30AM க்கு வருகிறேன்` → Time normalization
- `5kg அரிசி` → Unit normalization
- `Dr. குமார் வந்தார்` → Abbreviation normalization
- `123 பேர்` → Number normalization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is open source and available for use in production TTS systems.

## Support

For issues, questions, or contributions, please open an issue on the repository.

---

**Built with ❤️ for Indian Language TTS Systems**
