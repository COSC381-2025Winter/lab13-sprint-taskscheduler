# 🗓️ Task Scheduler App

This is a Python-based task scheduler that integrates with the Google Calendar API. It allows users to add, fetch, edit, and delete calendar events using a simple interface.

This project was developed as part of the **COSC381 Final Lab** at Eastern Michigan University, using Agile and GitHub Flow practices.

---

## 🚀 Features

- 🗂️ Add, view, edit, and delete Google Calendar events
- 🔒 OAuth2 authentication using Google API
- ✅ 100% test coverage using `pytest` and `pytest-cov`
- 🧪 Continuous integration using GitHub Actions
- 📐 Low-level design documented with UML
- 📦 Clean modular structure with `scheduler/` and `tests/` directories

---

## 🧰 Tech Stack

- Python 3.10+
- Google Calendar API
- `google-api-python-client`, `google-auth`, `google-auth-oauthlib`
- `pytest`, `pytest-cov` for testing
- GitHub Actions for CI/CD

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/COSC381-2025Winter/lab13-sprint-taskscheduler.git
cd lab13-sprint-taskscheduler
```
### 2. Set Up Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Set Up Google Calendar API (if applicable)
- If you're using the Google Calendar API, make sure you have the `credentials.json` file from
the Google Developer Console.
- Place it in the root directory of the project.
### 5. Environment Variables
- Add any environment variables needed, such as your API keys, to a `.env` file. For example:
```bash
GOOGLE_API_KEY= - your_google_api_key - 
CALENDAR_ID= - your_calendar_id -
```
### 6. Run Tests (Optional but Recommended)
```bash
pytest # Run all tests to verify your setup
```
### 7. Run the Program
```bash
python src/taskscheduler_mhussei9/main.py
