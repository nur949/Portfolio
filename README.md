# 🎨 Django Portfolio Backend

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Live Demo:** [https://portfolio-yshg.onrender.com/](https://portfolio-yshg.onrender.com/) 🚀

---

## 💡 Project Overview

This project is a **professional portfolio backend** built with Django and Django REST Framework, designed to serve content for:

- Personal projects  
- Skills & expertise  
- Work experience  
- Testimonials  

The backend is **fully API-ready**, admin-managed, and deployable on Render with PostgreSQL.

---

## ⚡ Features

- Fully **RESTful API** for projects, skills, experiences, and testimonials  
- **Django Admin panel** for content management  
- Seed command to populate portfolio with sample content  
- Production-ready **Render deployment** with PostgreSQL  
- Secure authentication for admin users  
- Optimized for **scalability and maintainability**  

---

## 🛠 Tech Stack

| Layer              | Technology                             |
|-------------------|----------------------------------------|
| Backend           | Django, Django REST Framework          |
| Database          | PostgreSQL                             |
| Deployment        | Render (Blueprint)                     |
| Web Server        | Gunicorn                               |
| Environment       | `.env` variables                       |
| Seed Data         | Custom management command (`seed_portfolio`) |

---

## ⚙ Installation (Full Setup)

### 1. Prerequisites

- **Python 3.11+**  
  Download and install: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
  Make sure `python --version` works in terminal.

- **PostgreSQL**  
  Install PostgreSQL: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)  
  Create a database and user for the project.

- **Git**  
  Install Git: [https://git-scm.com/downloads](https://git-scm.com/downloads)

---

### 2. Clone the repository

```bash
git clone https://github.com/nur949/Portfolio.git


```bash
python -m venv venv
# Activate environment:
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

```bash
pip install -r requirements.txt

```bash
python manage.py migrate

```bash
python manage.py seed_portfolio

```bash
python manage.py runserver

### Open http://127.0.0.1:8000
 in your browser.
