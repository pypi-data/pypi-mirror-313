# Blog Application

A simple blog application built with Flask and HTML/JavaScript.

## Features

- View all blog posts
- Add new posts
- Automatic timestamps for each post

## Setup

1. Clone the repository
```bash
git https://gitlab.com/y.karzal/2024_assignment2_blogpss
cd 2024_assignment2_blogpss
```

2. Set up the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the application
```bash
python app.py
```

4. Open the frontend
- Open `frontend/index.html` in your browser
- The API will be available at `http://localhost:5000`

## Project Structure

```
blog-app/
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── requirements.txt
│   └── tests/
└── frontend/
    ├── index.html
    ├── css/
    └── js/
```

## Testing

Run backend tests:
```bash
cd backend
pytest tests/
```