# Architecture Documentation

## System Overview

The Indian Language Text Normalization system is built with a microservices architecture:

- **Backend**: FastAPI-based REST API
- **Frontend**: React SPA with Tailwind CSS
- **Containerization**: Docker and Docker Compose

## Backend Architecture

### Core Components

#### 1. Normalization Pipeline (`normalization/pipeline.py`)
The main orchestrator that:
- Coordinates all normalization steps
- Manages token detection and replacement
- Handles overlapping matches
- Returns normalized text with token metadata

#### 2. Rule Engine (`normalization/rule_engine.py`)
- Loads locale-specific rules from YAML files
- Caches rules for performance
- Provides rule access API

#### 3. DFA Engine (`normalization/dfa_engine.py`)
- Pattern matching using regex (DFA-ready architecture)
- Handles overlapping pattern resolution
- Fast O(n) text scanning

#### 4. Specialized Normalizers
- **NumberNormalizer**: Handles cardinal and ordinal numbers
- **CurrencyNormalizer**: Normalizes currency expressions
- **DateNormalizer**: Converts dates to spoken form
- **TimeNormalizer**: Converts time to spoken form
- **UnitNormalizer**: Expands unit abbreviations
- **AbbreviationNormalizer**: Expands common abbreviations

#### 5. SSML Generator (`normalization/ssml_generator.py`)
- Wraps normalized text in SSML tags
- Maps categories to SSML `interpret-as` attributes
- Generates TTS-ready output

### Data Flow

```
User Input Text
    ↓
Pipeline.normalize()
    ↓
[For each category]
    ├─→ Find matches (regex patterns)
    ├─→ Normalize matches (specialized normalizers)
    └─→ Collect segments
    ↓
Remove overlapping matches
    ↓
Build normalized text
    ↓
Generate tokens metadata
    ↓
Return result
```

### Rule File Structure

Each locale file (`locales/{locale}.yml`) contains:

```yaml
locale: hi-IN
language: Hindi

numbers:
  cardinal:
    patterns: [...]
    words:
      ones: [...]
      tens: [...]
      hundreds: [...]
      # etc.

currency:
  symbol: "₹"
  name:
    singular: "..."
    plural: "..."
  patterns: [...]
  number_words: {...}

# Similar structure for dates, time, units, abbreviations
```

## Frontend Architecture

### Components

- **App.js**: Main component with state management
- **API Integration**: Axios-based HTTP client
- **UI Components**: 
  - Input textarea
  - Locale selector
  - Output displays (normalized text, SSML)
  - Token table
  - Rules viewer

### State Management

React hooks for:
- Input text
- Selected locale
- Normalized output
- SSML output
- Tokens
- Loading states
- Error handling

## API Design

### RESTful Endpoints

- `GET /`: API information
- `GET /locales`: List supported locales
- `POST /normalize`: Normalize text
- `POST /generate_ssml`: Generate SSML
- `GET /export_rules/{locale}`: Export rules
- `GET /health`: Health check

### Request/Response Format

All requests use JSON. Responses follow consistent structure:

```json
{
  "original_text": "...",
  "normalized_text": "...",
  "locale": "hi-IN",
  "tokens": [...]
}
```

## Deployment

### Docker Architecture

- **Backend Container**: Python 3.11, FastAPI, Uvicorn
- **Frontend Container**: Node.js build → Nginx serving static files
- **Docker Compose**: Orchestrates both services

### Networking

- Backend: Port 8000
- Frontend: Port 3000 (mapped to Nginx port 80)
- Services communicate via Docker network

## Extensibility

### Adding a New Language

1. Create `locales/{locale}.yml`
2. Translate all rule mappings
3. Test with sample sentences
4. Restart service

The system automatically detects new locale files.

### Adding a New Normalization Category

1. Create new normalizer class
2. Add to pipeline
3. Update locale files with new rules
4. Add tests

## Performance Considerations

- Rule caching in memory
- Regex compilation optimization
- Efficient pattern matching
- Token-based processing (only processes matches)

## Security

- CORS configuration for frontend
- Input validation via Pydantic
- Error handling without exposing internals
- Docker network isolation

## Testing Strategy

- Unit tests for each normalizer
- Integration tests for pipeline
- Sample sentence tests
- API endpoint tests (via FastAPI test client)

## Future Enhancements

- [ ] Add more Indian languages
- [ ] Machine learning-based normalization
- [ ] Custom rule editor UI
- [ ] Batch processing API
- [ ] WebSocket for real-time normalization
- [ ] Rule versioning
- [ ] Analytics and logging
