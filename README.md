# Learning Path Generator API

A FastAPI backend service that generates structured learning paths for different tech careers using AI. The service uses LangChain and OpenAI to create detailed, hierarchical learning paths with resources.

## Project Structure 

```
project_root/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── chat.py
│   │
│   ├── ai_integration/
│   │   ├── providers/
│   │   │   └── langchain_llm.py
│   │   ├── base.py
│   │   └── factory.py
│   │
│   ├── core/
│   │   └── settings.py
│   │
│   ├── services/
│   │   └── ai_service.py
│   │
│   ├── schemas/
│   │   └── chat.py
│   │
│   └── main.py
│
├── .env
├── requirements.txt
└── README.md
```

## Features

- Generate structured learning paths for tech careers
- Factory pattern for AI provider integration
- Clean API response format
- CORS support for frontend integration
- Error handling and validation
- Resource type detection (article, video, course)

## Response Format

The API returns learning paths in the following structure:

```json
{
  "data": {
    "id": "root",
    "title": "Career Title",
    "description": "Learning path description",
    "resources": [
      {
        "title": "Resource Title",
        "url": "https://example.com",
        "type": "article|video|course"
      }
    ],
    "children": [
      {
        "id": "topic-id",
        "title": "Topic Title",
        "description": "Topic description",
        "resources": [],
        "children": []
      }
    ]
  }
}
```
## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd learning-path-generator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
AI_PROVIDER=langchain
```

⚠️ **Security Note**: Never commit your `.env` file or expose your OpenAI API key. The `.env` file is included in `.gitignore` for your security.

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Generate Learning Path

```http
POST /api/chat
```

Request body:
```json
{
    "prompt": "Frontend Developer"
}
```

## Development

- The project uses FastAPI for the web framework
- LangChain for AI integration
- Factory pattern for provider management
- Pydantic for data validation

## Environment Variables

| Variable | Description |
|----------|-------------|
| OPENAI_API_KEY | Your OpenAI API key |
| AI_PROVIDER | AI provider to use (default: langchain) |

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Successful response
- 500: Server error with detail message

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

