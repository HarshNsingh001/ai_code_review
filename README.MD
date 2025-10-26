# AI Code Review Assistant

A Django REST API that analyzes source code for complexity, best practices, and common bugs using static analysis and OpenAI's GPT models.

## Features
- Cyclomatic Complexity Analysis - Identifies complex functions that need refactoring
- Static Code Analysis - Detects common issues like long lines, print statements, bare except clauses
- AI-Powered Reviews - Uses OpenAI GPT to provide intelligent feedback
- Maintainability Index - Calculates code maintainability score
- REST API - Easy integration with any frontend or tool

## Prerequisites
- Python 3.10 or higher
- OpenAI API Key ([Get it here](https://platform.openai.com/))
- Git (for version control)

## Installation

### Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/code-review-assistant.git
cd code-review-assistant

Create virtual environment

Windows

python -m venv venv
venv\Scripts\activate


Mac/Linux

python3 -m venv venv
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Set up environment variables

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your-django-secret-key
DEBUG=True

Run migrations
python manage.py makemigrations
python manage.py migrate

Start the server
python manage.py runserver


The API will be available at http://127.0.0.1:8000/

API Endpoints
Review Code

POST /api/review/

Request Body

{
  "code": "def example():\n print('Hello')",
  "language": "python",
  "use_ai": true
}


Response

{
  "id": 1,
  "language": "python",
  "analysis": {
    "complexity": {
      "average_complexity": 1.0,
      "max_complexity": 1
    },
    "maintainability_index": 100.0,
    "lines_of_code": 2,
    "total_issues": 1
  },
  "issues": [
    {
      "type": "debug",
      "line": 1,
      "message": "Line 1 contains print statement - consider using logging"
    }
  ],
  "ai_feedback": "...",
  "created_at": "2025-10-26T10:30:00Z"
}

Get Review History

GET /api/reviews/
Get a list of previous reviews.

Get Review Details

GET /api/review/<id>/
Get details of a specific review.

Health Check

GET /api/health/
Check if the API is running.

Testing the API
Using cURL
curl -X POST http://127.0.0.1:8000/api/review/ \
-H "Content-Type: application/json" \
-d '{ "code": "def add(a, b):\n return a + b", "language": "python", "use_ai": true }'

Using Python requests
import requests

response = requests.post(
    'http://127.0.0.1:8000/api/review/',
    json={
        'code': 'def add(a, b):\n return a + b',
        'language': 'python',
        'use_ai': True
    }
)
print(response.json())

Using Browser

Navigate to http://127.0.0.1:8000/api/review/
 to use Django REST Framework's browsable API.

Project Structure
code-review-assistant/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── reviewer/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── analyzers.py
│   ├── ai_checker.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

Technologies Used

--Django - Web framework
--Django REST Framework - API development
--Radon - Code complexity analysis
--OpenAI API - AI-powered code review
--SQLite - Database (can be changed to PostgreSQL/MySQL)

Contributing

--Fork the repository
--Create your feature branch: git checkout -b feature/AmazingFeature
--Commit your changes: git commit -m 'Add some AmazingFeature'
--Push to the branch: git push origin feature/AmazingFeature
--Open a Pull Request

License
--MIT License
Support
--For issues and questions, please create an issue on GitHub.

Author
Your Name - HARSH  NARAYAN SINGH

Acknowledgments
--OpenAI for providing the GPT API
--Django and DRF communities
--Radon for code metrics