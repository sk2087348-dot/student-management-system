# Student Management System

A full-stack Student Management System built with **Python, Flask, MySQL, HTML, CSS, and JavaScript**.

This project allows users to manage student records through a simple and professional web interface connected to a MySQL database.

## 🚀 Features

* Add new students
* View all students
* Search students by ID
* Search students by name
* Update student information
* Delete student records
* Dashboard with student statistics
* Input validation
* Error handling
* MySQL database integration
* Responsive frontend design
* REST API using Flask

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **MySQL**
* **MySQL Connector**
* **HTML5**
* **CSS3**
* **JavaScript**

## 🗄️ Database

The project uses **MySQL** to store and manage student records.

### Students Table

The `students` table contains:

* `student_id`
* `name`
* `age`
* `gender`
* `city`
* `department`

## 📂 Project Structure

```text
STUDENT MANAGEMENT DATABASE
│
├── app.py
├── student_management.py
├── student management system.sql
├── README.md
├── .gitignore
│
└── frontend
    ├── index.html
    ├── style.css
    └── script.js
```

## ⚙️ Installation

### 1. Install Python

Make sure Python is installed on your computer.

### 2. Install MySQL

Install MySQL and create the database:

```sql
CREATE DATABASE management_system;
```

### 3. Install Required Python Packages

Open the terminal in the project folder and run:

```bash
pip install flask mysql-connector-python
```

### 4. Configure MySQL Connection

Open `app.py` and update the MySQL password according to your local MySQL setup.

```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD",
    database="management_system"
)
```

**Do not upload your real database password to GitHub.**

### 5. Run the Application

Open the terminal in the project folder and run:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## 🔄 Main Functionality

The application provides complete CRUD operations:

**Create** → Add Student

**Read** → View and Search Students

**Update** → Update Student Information

**Delete** → Delete Student Records

## 📊 Dashboard

The dashboard displays:

* Total Students
* Male Students
* Female Students

## 🎯 Project Purpose

This project was created as a practical learning project to improve my skills in:

* Python programming
* MySQL database management
* Flask web development
* REST APIs
* HTML, CSS, and JavaScript
* CRUD operations
* Full-stack application development

## 🔮 Future Improvements

Possible future improvements include:

* Student login/authentication
* Admin panel
* Pagination
* Advanced search and filtering
* Export student records
* Deployment to a live server

## 👨‍💻 Author

**Muhammad Saqib**

Computer Science / AI Student

---

⭐ If you find this project useful, feel free to explore the repository.

