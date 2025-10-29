# Personal Grade Calculator (PGC)

## Disclaimer

The current code for PGC is still under active development.

This version represents approximately 50–60% of the final project completion.

It includes both GET and POST (JSON) APIs, and the system now stores calculation results in the database.

## 1. Prerequisites

- Python 3.10+
- pip (Python package manager)
- pipenv (Python virtualenv management tool)

## 2. Setup Virtual Environment

### 2.1. Install Pipenv

```sh
pip install pipenv
```

### 2.2. Install dependencies

```sh
pipenv sync
```

This will automatically install all dependencies required from the `Pipfile.lock` file.

### 2.3. Activate the virtual environment

```sh
pipenv shell
```

This will activate the virtual environment (venv) in the current shell, to check whether you're running commands from the venv, run `which pip` or `which python` (Linux/macOS).

If the path shown in the output contain `.virtualenvs/` followed by the project name, you're good to go.

## 4. **Apply database migrations**

```bash
python manage.py migrate
```

## 5. **(Optional) Create a superuser for the admin site**

```bash
python manage.py createsuperuser
```

## 6. Run Server

```sh
python manage.py runserver
```

You should see `Starting development server at http://127.0.0.1:8000`

## 5. Test Grade Calculation API (GET Version)

Open your browser or Postman and visit <http://127.0.0.1:8000/api/calculate/?scores=80,90,75&credits=3,3,2>

Note: You can replace the numbers in `scores` and `credits` with any values you want.

Example: `scores=65,72,90&credits=3,2,2`

Expected Response:

```json
{
  "GPA": 82.08,
  "Grade": "A"
}
```

## 6. Test Grade Calculation API (POST JSON Version)

This version uses Django REST Framework and accepts JSON input.

Open Postman and send:

Method: `POST`
URL: `http://127.0.0.1:8000/api/calculate/post/`
Headers: `Content-Type: application/json`

Body (raw JSON):

```json
{
  "subjects": [
    { "name": "Math", "score": 82, "credit": 3 },
    { "name": "ITF", "score": 90, "credit": 2 }
  ]
}
```

Expected Response:

```json
{
  "GPA": 85.2,
  "Grade": "A"
}
```

The result will also be saved automatically into the database (GradeResult table).

## 7. View Stored Results in Admin Panel

After testing, open <http://127.0.0.1:8000/admin/>

Login with your Django superuser account.  
Then click “Grade results” under the GRADECALC section.

You should see a list of previously calculated GPA records,  
including each result’s GPA, grade, and timestamp.

## 8. (Optional) Stop the Server

Press `^c` in your terminal.

You have now successfully tested the 50–60% Django Backend of PGC!
