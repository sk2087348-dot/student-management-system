import mysql.connector
connection = mysql.connector.connect(host="localhost",user="root",password="526304",database="management_system")
print("database connected succcessfully!")
print(connection.is_connected())
cursor = connection.cursor()
def add_student():

    # Name validation
    while True:
        name = input("Enter the name: ").strip()

        if name and name.replace(" ", "").isalpha():
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
        gender = input("Enter the gender (Male/Female): ")

        if gender.lower() in ["male", "female"]:
            break

        print("Please enter Male or Female!")

    # City validation
    while True:
        city = input("Enter the city: ").strip()

        if city and city.replace(" ", "").isalpha():
         break

        print("Please enter a valid city name!")

    # Department validation
   
    while True:
        department = input("Enter the department: ").strip()

        if department and department.replace(" ", "").isalpha():
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
        print("Database error:", e)

    else:
        print("Student added successfully!")
def view_students():
    query = "SELECT * FROM students"

    try:
        cursor.execute(query)
        students = cursor.fetchall()

    except mysql.connector.Error as e:
        print("Database error:", e)
        return

    if students:
        print("\nID   Name                 Age   Gender   City                 Department")
        print("-" * 75)

        for student in students:
            print(f"{student[0]:<4} {student[1]:<20} {student[2]:<5} {student[3]:<8} {student[4]:<20} {student[5]}")

    else:
        print("No students found!")
def search_student(name):

    query = "SELECT * FROM students WHERE name LIKE %s"

    try:
        cursor.execute(query, (f"%{name}%",))
        students = cursor.fetchall()

    except mysql.connector.Error as e:
        print("Database error:", e)
        return

    if students:
        print("\nID   Name                 Age   Gender   City                 Department")
        print("-" * 75)

        for student in students:
            print(f"{student[0]:<4} {student[1]:<20} {student[2]:<5} {student[3]:<8} {student[4]:<20} {student[5]}")

    else:
        print("Student not found!")

      

def delete_student(student_id):
    query = "DELETE FROM students WHERE student_id = %s"

    try:
        cursor.execute(query, (student_id,))
        connection.commit()

    except mysql.connector.Error as e:
        print("Database error:", e)
        return

    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("Student not found!")


def get_student_id():

    while True:
        try:
            student_id = int(input("Enter student ID: "))
            return student_id

        except ValueError:
            print("Please enter a valid student ID!")        
def get_valid_name():

    while True:
        name = input("Enter name: ").strip()

        if name and name.replace(" ", "").isalpha():
            return name
        print("Please enter a valid name!")


def update_student(student_id, new_name):
    print("ID received:", student_id)

    check_query = "SELECT student_id FROM students WHERE student_id = %s"

    cursor.execute(check_query, (student_id,))

    if cursor.fetchone() is None:
        print("Student ID not found!")
        return

    query = "UPDATE students SET name = %s WHERE student_id = %s"

    try:
        cursor.execute(query, (new_name, student_id))
        connection.commit()

    except mysql.connector.Error as e:
        print("Database error:", e)
        return

    print("Student name updated successfully!")

def update_age(student_id):

    while True:
        try:
            new_age = int(input("Enter new age: "))

            if 5 <= new_age <= 100:
                break

            print("Age must be between 5 and 100!")
        except ValueError:
            print("Please enter a valid age!")

    query = "UPDATE students SET age = %s WHERE student_id = %s"

    try:
        cursor.execute(query, (new_age, student_id))
        connection.commit()

    except mysql.connector.Error as e:
        print("Database error:", e)
        return

    if cursor.rowcount > 0:
        print("Student age updated successfully!")
    else:
        print("Student not found!")    
# Main Menu
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
            name = get_valid_name()
            search_student(name)

        elif choice == "4":
            student_id = get_student_id()

            check_query = "SELECT student_id FROM students WHERE student_id = %s"
            cursor.execute(check_query, (student_id,))

            if cursor.fetchone() is None:
                print("Student ID not found!")
                continue

            print("\n1. Update Name")
            print("2. Update Age")

            update_choice = input("Enter your choice: ")

            if update_choice == "1":
                new_name = get_valid_name()
                update_student(student_id, new_name)

            elif update_choice == "2":
                update_age(student_id)

            else:
                print("Invalid choice!")

        elif choice == "5":
            student_id = get_student_id()

            confirm = input(
                "Are you sure you want to delete this student? (y/n): "
            )

            if confirm.lower() == "y":
                delete_student(student_id)
            else:
                print("Delete cancelled!")

        elif choice == "6":
            print("THANK YOU! Program exited.")
            break

        else:
            print("Invalid choice! Please enter 1 to 6.")
main_menu()

cursor.close()
connection.close()

print("Database connection closed.")            