from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(
    __name__,
    template_folder="frontend",
    static_folder="frontend"
)


# ===============================
# DATABASE CONNECTION
# ===============================

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="526304",
        database="management_system"
    )


# ===============================
# HOME
# ===============================

@app.route("/")
def home():

    return render_template("index.html")


# ===============================
# VIEW ALL STUDENTS
# ===============================

@app.route("/api/students", methods=["GET"])
def get_students():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                student_id,
                name,
                age,
                gender,
                city,
                department
            FROM students
            ORDER BY student_id
        """)

        students = cursor.fetchall()

        return jsonify(students)

    except mysql.connector.Error as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ===============================
# ADD STUDENT
# ===============================

@app.route("/api/students", methods=["POST"])
def add_student():

    data = request.get_json()

    name = data.get("name", "").strip()
    age = data.get("age")
    gender = data.get("gender", "").strip()
    city = data.get("city", "").strip()
    department = data.get("department", "").strip()


    if not name or not age or not gender or not city or not department:

        return jsonify({
            "success": False,
            "message": "Please fill all fields."
        }), 400


    try:

        age = int(age)

    except ValueError:

        return jsonify({
            "success": False,
            "message": "Age must be a number."
        }), 400


    if age < 5 or age > 100:

        return jsonify({
            "success": False,
            "message": "Age must be between 5 and 100."
        }), 400


    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO students
            (name, age, gender, city, department)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            name,
            age,
            gender,
            city,
            department
        )

        cursor.execute(query, values)

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Student added successfully!",
            "student_id": cursor.lastrowid
        })

    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ===============================
# SEARCH BY NAME
# ===============================

@app.route("/api/students/search", methods=["GET"])
def search_by_name():

    name = request.args.get("name", "").strip()

    if not name:

        return jsonify({
            "success": False,
            "message": "Please enter a student name."
        }), 400


    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                student_id,
                name,
                age,
                gender,
                city,
                department
            FROM students
            WHERE name LIKE %s
            ORDER BY student_id
        """

        cursor.execute(query, (f"%{name}%",))

        students = cursor.fetchall()

        return jsonify(students)

    except mysql.connector.Error as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ===============================
# SEARCH BY ID
# ===============================

@app.route("/api/students/<int:student_id>", methods=["GET"])
def search_by_id(student_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                student_id,
                name,
                age,
                gender,
                city,
                department
            FROM students
            WHERE student_id = %s
        """

        cursor.execute(query, (student_id,))

        student = cursor.fetchone()

        if not student:

            return jsonify({
                "success": False,
                "message": "Student ID not found."
            }), 404

        return jsonify(student)

    except mysql.connector.Error as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ===============================
# UPDATE STUDENT
# ===============================

@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):

    data = request.get_json()

    name = data.get("name", "").strip()
    age = data.get("age")
    gender = data.get("gender", "").strip()
    city = data.get("city", "").strip()
    department = data.get("department", "").strip()


    if not name or not age or not gender or not city or not department:

        return jsonify({
            "success": False,
            "message": "Please fill all fields."
        }), 400


    try:

        age = int(age)

    except ValueError:

        return jsonify({
            "success": False,
            "message": "Age must be a number."
        }), 400


    if age < 5 or age > 100:

        return jsonify({
            "success": False,
            "message": "Age must be between 5 and 100."
        }), 400


    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE students
            SET
                name = %s,
                age = %s,
                gender = %s,
                city = %s,
                department = %s
            WHERE student_id = %s
        """

        values = (
            name,
            age,
            gender,
            city,
            department,
            student_id
        )

        cursor.execute(query, values)

        if cursor.rowcount == 0:

            return jsonify({
                "success": False,
                "message": "Student ID not found."
            }), 404

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Student updated successfully!"
        })

    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ===============================
# DELETE STUDENT
# ===============================

@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM students
            WHERE student_id = %s
        """

        cursor.execute(query, (student_id,))

        if cursor.rowcount == 0:

            return jsonify({
                "success": False,
                "message": "Student ID not found."
            }), 404

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Student deleted successfully!"
        })

    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ===============================
# RUN APPLICATION
# ===============================

if __name__ == "__main__":

    app.run(debug=True)