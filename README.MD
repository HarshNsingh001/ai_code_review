AI Code Review Assistant
A Django REST API that analyzes source code for complexity, best practices, and common bugs using static analysis and OpenAI's GPT models.

Features
Cyclomatic Complexity Analysis - Identifies complex functions that need refactoring
Static Code Analysis - Detects common issues like long lines, print statements, bare except clauses
AI-Powered Reviews - Uses OpenAI GPT to provide intelligent feedback
Maintainability Index - Calculates code maintainability score
REST API - Easy integration with any frontend or tool
Prerequisites
Python 3.10 or higher
OpenAI API Key (get from https://platform.openai.com/)
Git (for version control)
Installation
1. Clone the repository
bash
git clone https://github.com/YOUR_USERNAME/code-review-assistant.git
cd code-review-assistant
2. Create virtual environment
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Set up environment variables
Create a .env file in the project root:

env
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your-django-secret-key
DEBUG=True
5. Run migrations
bash
python manage.py makemigrations
python manage.py migrate
6. Start the server
bash
python manage.py runserver
The API will be available at http://127.0.0.1:8000/

API Endpoints
1. Review Code
POST /api/review/

Submit code for review.

Request Body:

json
{
  "code": "def example():\n    print('Hello')",
  "language": "python",
  "use_ai": true
}
Response:

json
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
2. Get Review History
GET /api/reviews/

Get list of previous reviews.

3. Get Review Details
GET /api/review/<id>/

Get details of a specific review.

4. Health Check
GET /api/health/

Check if the API is running.

Testing the API
Using cURL
bash
curl -X POST http://127.0.0.1:8000/api/review/ \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def add(a, b):\n    return a + b",
    "language": "python",
    "use_ai": true
  }'
Using Python requests
python
import requests

response = requests.post('http://127.0.0.1:8000/api/review/', json={
    'code': 'def add(a, b):\n    return a + b',
    'language': 'python',
    'use_ai': True
})

print(response.json())
Using the Browser
Navigate to http://127.0.0.1:8000/api/review/ in your browser to use Django REST Framework's browsable API.

Project Structure
code-review-assistant/
├── config/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── reviewer/            # Main application
│   ├── models.py        # Database models
│   ├── views.py         # API endpoints
│   ├── serializers.py   # Data serialization
│   ├── analyzers.py     # Static code analysis
│   ├── ai_checker.py    # OpenAI integration
│   └── urls.py          # URL routing
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
Technologies Used
Django - Web framework
Django REST Framework - API development
Radon - Code complexity analysis
OpenAI API - AI-powered code review
SQLite - Database (can be changed to PostgreSQL/MySQL)
Contributing
Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
License
This project is open source and available under the MIT License.

Support
For issues and questions, please create an issue on GitHub.

Author
Your Name - [Your GitHub Profile]

Acknowledgments
OpenAI for providing the GPT API
Django and DRF communities
Radon for code metrics
