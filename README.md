# Task Manager

A simple full-stack task management web application built with Flask, SQLite, SQLAlchemy, and Bootstrap.

## Features

- User authentication: register, login, logout
- Password hashing with Werkzeug
- Create, read, update, delete tasks
- Mark tasks as completed or pending
- Task properties: title, description, due date, priority, status
- Dashboard with task statistics and filters
- Responsive UI using Bootstrap and custom CSS

## Tech Stack

- Backend: Python, Flask
- Database: SQLite via SQLAlchemy
- Frontend: HTML, CSS, JavaScript
- Templating: Jinja2

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate it:

```bash
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
python app.py
```

5. Open http://127.0.0.1:5000 in your browser.

## Seed Data

To add demo data, run:

```bash
flask --app app seed
```

## Project Structure

```
task-manager/
├── app.py
├── requirements.txt
├── database.db
├── models/
│   ├── __init__.py
│   ├── task.py
│   └── user.py
├── routes/
│   ├── auth.py
│   └── tasks.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   └── task_form.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── README.md
```

## Notes

- Replace `SECRET_KEY` in `app.py` with a secure value before deploying.
- This project is designed for learning and demonstration.
