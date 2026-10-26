# 📚 Library Management System

An end-to-end, full-stack web application designed to streamline library cataloging, user registration, and book borrowing operations. Built using **Python (Flask)** for backend business logic and routing, **MySQL** for relational data persistence, and **HTML5/CSS3** for a clean, responsive user interface.

---

## 👥 Team & Project Information

* **Group Number:** Group 2
* **Course:** Computer & Communications Engineering — Senior Year

### 🆔 Team Members

| Name | Student ID | Role |
| :--- | :--- | :--- |
| **Jana Alaa** | `2304024` | Full-Stack Developer |
| **Salma** | `2304018` | Full-Stack Developer |

---

## Division of Responsibilities & Tasks

Tasks were equally distributed to ensure a balanced development workflow across backend engineering, database administration, and frontend design:

### Jana Alaa
* **Authentication & User Management:** Developed user registration (`/register`) and login (`/login`) routes with Flask session control.
* **Frontend UI/UX:** Designed and styled intuitive, user-friendly HTML forms and web templates (`register.html`, `login.html`).
* **Session Handling:** Implemented secure session handling and error notifications for unauthorized access.
* **System Testing:** Conducted end-to-end authentication testing and debugged backend route exceptions.

### Salma Walid
* **Database Architecture:** Designed relational MySQL tables (`users`, `books`, `author`) and established foreign key relationships.
* **Catalog Management:** Implemented logic and database queries for adding, viewing, and managing library books and authors.
* **Borrowing Logic:** Programmed transactional database operations for issuing and returning books.
* **Data Validation:** Configured frontend and backend validation rules to prevent invalid form submissions and duplicate entries.

---

## Key Features

- **User Authentication:** Secure user registration, unique credential verification, and login management.
- **Relational Data Storage:** Structured MySQL tables with primary keys, unique constraints, and automatic timestamps.
- **Book Catalog:** Ability to browse available books, search catalog entries, and track inventory.
- **Borrowing & Returns:** Transactional management of library books issued to registered accounts.
- **Responsive Web Interface:** Modern, accessible layout styled for ease of navigation.

---

## ⚙️ How the Code Works

1. **Database Layer (`MySQL`):** Stores persistent records inside `library_db`, enforcing unique constraints on usernames and email addresses.
2. **Backend Controller (`app.py`):** Establishes connections to MySQL via `pymysql`, processes HTTP requests, executes SQL queries, and manages login sessions.
3. **Frontend View Layer (`templates/`):** Jinja2 templates render dynamic HTML forms and UI views for user registration and authentication.

---

## Database Schema & Architecture

```sql
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    username          VARCHAR(50) NOT NULL UNIQUE,
    email             VARCHAR(255) NOT NULL UNIQUE,
    password          VARCHAR(255) NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Tech Stack
Language: Python 3.x

Framework: Flask

Database: MySQL Server 8.0 / MySQL Workbench

Database Driver: PyMySQL

Frontend: HTML5, CSS3, Jinja2

