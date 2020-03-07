# README.md

1. Setup environment

   - Install virtualenv
     python3 -m venv {env}
     source {env}/bin/activate
   - Install packages
     pip install -r requirements.txt
   - Start server
     python manage.py runserver

2. API Routes

   - Questions
     /api/questions/
   - Answers
     /api/questions/{questionId}/answers/
   - Bookmarks
     /api/bookmarks/

3. Tests
   - Running tests
     python manage.py test
   - To see coverage
     coverage run --source='.' manage.py test
     coverage report -m
