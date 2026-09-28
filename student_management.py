import mysql.connector


# ================= DATABASE CONNECTION =================

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="526304",
        database="management_system"
    )

    print("Database connected successfully!")

    cursor = connection.cursor()

except mysql.connector.Error as e:
    print("Database connection failed:", e)
    exit()


# ================= ADD STUDENT =================

def add_student():

    # Name validation
    while True:
        name = input("Enter the name: ").strip()

        if name and name.replace(" ", "").isalpha():
            name = name.title()
            break

        print("Please enter a valid name!")

    # Age validation
    while True:
        try:
            age = int(input("Enter the age: "))

            if 5 <= age <= 100:
                break

            print("Age must be between 5 and 100!")

        except ValueError:
            print("Please enter a valid number!")

    # Gender validation
    while True:
        gender = input("Enter the gender (Male/Female): ").strip()

        if gender.lower() in ["male", "female"]:
            gender = gender.capitalize()
            break

        print("Please enter Male or Female!")

    # City validation
    while True:
        city = input("Enter the city: ").strip()

        if city and city.replace(" ", "").isalpha():
            city = city.title()
            break

        print("Please enter a valid city name!")

    # Department validation
    while True:
        department = input("Enter the department: ").strip()

        if department and department.replace(" ", "").isalpha():
            department = department.title()
            break

        print("Please enter a valid department!")

    query = """
    INSERT INTO students(name, age, gender, city, department)
    VALUES(%s, %s, %s, %s, %s)
    """

    values = (name, age, gender, city, department)

    try:
        cursor.execute(query, values)
        connection.commit()

    except mysql.connector.Error as e:
        connection.rollback()
        print("Database error:", e)

    else:
        print("Student added successfully!")


# ================= VIEW STUDENTS =================

def view_students():

    query = "SELECT * FROM students ORDER BY student_id ASC"

    try:
        cursor.execute(query)
        students = cursor.fetchall()

    except mysql.connector.Error as e:
        print("Database error:", e)
        return

    if students:

        print(
            "\nID   Name                 Age   Gender   "
            "City                 Department"
        )
        print("-" * 75)

        for student in students:
            print(
                f"{student[0]:<4} "
                f"{student[1]:<20} "
                f"{student[2]:<5} "
                f"{student[3]:<8} "
                f"{student[4]:<20} "
                f"{student[5]}"
            )

    else:
        print("No students found!")


# ================= SEARCH BY NAME =================

def search_student(name):

    query = """
    SELECT * FROM students
    WHERE name LIKE %s
    ORDER BY student_id ASC
    """

    try:
        cursor.execute(query, (f"%{name}%",))
        students = cursor.fetchall()

    except mysql.connector.Error as e:
        print("Database error:", e)
        return

    if students:

        print(
            "\nID   Name                 Age   Gender   "
            "City                 Department"
        )
        print("-" * 75)

        for student in students:
            print(
                f"{student[0]:<4} "
                f"{student[1]:<20} "
                f"{student[2]:<5} "
                f"{student[3]:<8} "
                f"{student[4]:<20} "
                f"{student[5]}"
            )

    else:
        print("No student found with this name!")


# ================= SEARCH BY ID =================

def search_student_by_id(student_id):

    query = "SELECT * FROM students WHERE student_id = %s"

    try:
        cursor.execute(query, (student_id,))
        student = cursor.fetchone()

    except mysql.connector.Error as e:
        print("Database error:", e)
        return

    if student:

        print(
            "\nID   Name                 Age   Gender   "
            "City                 Department"
        )
        print("-" * 75)

        print(
            f"{student[0]:<4} "
            f"{student[1]:<20} "
            f"{student[2]:<5} "
            f"{student[3]:<8} "
            f"{student[4]:<20} "
            f"{student[5]}"
        )

    else:
        print("Student ID not found!")


# ================= DELETE STUDENT =================

def delete_student(student_id):

    if not student_exists(student_id):
        print("Student ID not found!")
        return

    while True:

        confirm = input(
            "Are you sure you want to delete this student? (y/n): "
        ).strip().lower()

        if confirm == "y":
            break

        elif confirm == "n":
            print("Delete cancelled!")
            return

        else:
            print("Please enter y or n!")

    query = "DELETE FROM students WHERE student_id = %s"

    try:
        cursor.execute(query, (student_id,))
        connection.commit()

    except mysql.connector.Error as e:
        connection.rollback()
        print("Database error:", e)
        return

    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("Student was not deleted!")


# ================= UPDATE NAME =================

def update_student(student_id, new_name):

    if not student_exists(student_id):
        print("Student ID not found!")
        return

    query = "UPDATE students SET name = %s WHERE student_id = %s"

    try:
        cursor.execute(query, (new_name, student_id))
        connection.commit()

    except mysql.connector.Error as e:
        connection.rollback()
        print("Database error:", e)
        return

    if cursor.rowcount > 0:
        print("Student name updated successfully!")
    else:
        print("Student name was not changed!")


# ================= UPDATE AGE =================

def update_age(student_id):

    check_query = "SELECT age FROM students WHERE student_id = %s"

    try:
        cursor.execute(check_query, (student_id,))
        student = cursor.fetchone()

    except mysql.connector.Error as e:
        print("Database error:", e)
        return

    if student is None:
        print("Student ID not found!")
        return

    while True:

        try:
            new_age = int(input("Enter new age: "))

            if 5 <= new_age <= 100:
                break

            print("Age must be between 5 and 100!")

        except ValueError:
            print("Please enter a valid age!")

    if new_age == student[0]:
        print("New age is same as current age!")
        return

    query = "UPDATE students SET age = %s WHERE student_id = %s"

    try:
        cursor.execute(query, (new_age, student_id))
        connection.commit()

    except mysql.connector.Error as e:
        connection.rollback()
        print("Database error:", e)
        return

    if cursor.rowcount > 0:
        print("Student age updated successfully!")
    else:
        print("Student age was not changed!")


# ================= UPDATE GENDER =================

def update_gender(student_id):

    if not student_exists(student_id):
        print("Student ID not found!")
        return

    while True:

        gender = input(
            "Enter new gender (Male/Female): "
        ).strip()

        if gender.lower() in ["male", "female"]:
            gender = gender.capitalize()
            break

        print("Please enter Male or Female!")

    query = "UPDATE students SET gender = %s WHERE student_id = %s"

    values = (gender, student_id)

    try:
        cursor.execute(query, values)
        connection.commit()

    except mysql.connector.Error as e:
        connection.rollback()
        print("Database error:", e)
        return

    if cursor.rowcount > 0:
        print("Student gender updated successfully!")
    else:
        print("Student gender was not changed!")


# ================= UPDATE CITY =================

def update_city(student_id):

    if not student_exists(student_id):
        print("Student ID not found!")
        return

    while True:

        city = input("Enter new city: ").strip()

        if city and city.replace(" ", "").isalpha():
            city = city.title()
            break

        print("Please enter a valid city name!")

    query = "UPDATE students SET city = %s WHERE student_id = %s"

    values = (city, student_id)

    try:
        cursor.execute(query, values)
        connection.commit()

    except mysql.connector.Error as e:
        connection.rollback()
        print("Database error:", e)
        return

    if cursor.rowcount > 0:
        print("Student city updated successfully!")
    else:
        print("Student city was not changed!")


# ================= UPDATE DEPARTMENT =================

def update_department(student_id):

    if not student_exists(student_id):
        print("Student ID not found!")
        return

    while True:

        department = input("Enter new department: ").strip()

        if department and department.replace(" ", "").isalpha():
            department = department.title()
            break

        print("Please enter a valid department!")

    query = """
    UPDATE students
    SET department = %s
    WHERE student_id = %s
    """

    values = (department, student_id)

    try:
        cursor.execute(query, values)
        connection.commit()

    except mysql.connector.Error as e:
        connection.rollback()
        print("Database error:", e)
        return

    if cursor.rowcount > 0:
        print("Student department updated successfully!")
    else:
        print("Student department was not changed!")


# ================= GET STUDENT ID =================

def get_student_id():

    while True:

        try:
            student_id = int(input("Enter student ID: "))

            if student_id > 0:
                return student_id

            print("Student ID must be greater than 0!")

        except ValueError:
            print("Please enter a valid student ID!")


# ================= GET VALID NAME =================

def get_valid_name():

    while True:

        name = input("Enter name: ").strip()

        if name and name.replace(" ", "").isalpha():
            return name.title()

        print("Please enter a valid name!")


# ================= CHECK STUDENT EXISTS =================

def student_exists(student_id):

    query = "SELECT student_id FROM students WHERE student_id = %s"

    try:
        cursor.execute(query, (student_id,))
        return cursor.fetchone() is not None

    except mysql.connector.Error as e:
        print("Database error:", e)
        return False


# ================= SEARCH MENU =================

def search_menu():

    while True:

        print("\n1. Search by Name")
        print("2. Search by ID")
        print("3. Back to Main Menu")

        search_choice = input("Enter your choice: ")

        if search_choice == "1":

            name = get_valid_name()
            search_student(name)

        elif search_choice == "2":

            student_id = get_student_id()
            search_student_by_id(student_id)

        elif search_choice == "3":

            break

        else:

            print("Invalid choice!")


# ================= UPDATE MENU =================

def update_menu():

    student_id = get_student_id()

    if not student_exists(student_id):
        print("Student ID not found!")
        return

    while True:

        print("\n1. Update Name")
        print("2. Update Age")
        print("3. Update Gender")
        print("4. Update City")
        print("5. Update Department")
        print("6. Back to Main Menu")

        update_choice = input("Enter your choice: ")

        if update_choice == "1":

            new_name = get_valid_name()
            update_student(student_id, new_name)

        elif update_choice == "2":

            update_age(student_id)

        elif update_choice == "3":

            update_gender(student_id)

        elif update_choice == "4":

            update_city(student_id)

        elif update_choice == "5":

            update_department(student_id)

        elif update_choice == "6":

            break

        else:

            print("Invalid choice!")


# ================= DELETE MENU =================

def delete_menu():

    student_id = get_student_id()
    delete_student(student_id)


# ================= MAIN MENU =================

def main_menu():

    while True:

        print("\n" + "=" * 45)
        print("       STUDENT MANAGEMENT SYSTEM")
        print("=" * 45)

        print("\n1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            add_student()

        elif choice == "2":

            view_students()

        elif choice == "3":

            search_menu()

        elif choice == "4":

            update_menu()

        elif choice == "5":

            delete_menu()

        elif choice == "6":

            print("THANK YOU! Program exited.")
            break

        else:

            print("Invalid choice! Please enter 1 to 6.")


# ================= PROGRAM START =================

try:

    main_menu()

finally:

    if connection.is_connected():
        cursor.close()
        connection.close()

    print("Database connection closed.")