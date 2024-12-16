# Learning Path Generator API

A FastAPI backend service that generates structured learning paths for different tech careers using AI. The service uses LangChain and OpenAI to create detailed, hierarchical learning paths with resources. It includes user authentication with both email/password and Google OAuth support.

## Project Structure 

```
project_root/
├── app/
│ ├── api/
│ │ └── routes/
│ │ ├── authentication.py
│ │ └── chat.py
│ │
│ ├── ai_integration/
│ │ ├── providers/
│ │ │ ├── langchain_llm.py
│ │ │ └── your_custom_llm.py
│ │ ├── base.py
│ │ └── factory.py
│ │
│ ├── core/
│ │ └── settings.py
│ │
│ ├── models/
│ │ └── chat.py
│ │
│ ├── services/
│ │ ├── ai_service.py
│ │ └── database_connection_service.py
│ │
│ ├── schemas/
│ │ ├── chat.py
│ │ ├── token_schema.py
│ │ └── user.py
│ │
│ └── main.py
│
├── .env
├── requirements.txt
├── runtime.txt
├── Procfile
├── gunicorn_config.py
└── README.md
```

## Features

- Generate structured learning paths for tech careers using AI
- User authentication with email/password
- Google OAuth integration
- Chat history management
- Factory pattern for AI provider integration
- PostgreSQL database integration
- CORS support for frontend integration
- Comprehensive error handling
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
```
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
AI_PROVIDER=langchain

# Database Configuration
DATABASE_USER=your_db_user
DATABASE_USER_PASSWORD=your_db_password
DATABASE_HOST=your_db_host
DATABASE_PORT=your_db_port
DATABASE_NAME=your_db_name

# Authentication
SECRET_KEY=your_secret_key_here
GOOGLE_CLIENT_ID=your_google_client_id

# CORS (optional)
ALLOWED_ORIGINS=http://localhost:5173
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

