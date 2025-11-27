"""
The Student Grade Analyzer.

Program that manage and analyze student grades.
"""


def main():
    """
    Runs the grade analyzer program.
    Shows the menu and processes what the user chooses to do.
    """
    students = []  # List to store all data about student

    while True:
        # Display menu
        print("\n--- Student Grade Analyzer ---")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Show report (all students)")
        print("4. Find top performer")
        print("5. Exit")

        try:
            choice = input("Enter your choice: ").strip()
            # Handle what the user selected from the menu
            if not choice:
                print("Error: Choice cannot be empty. Please enter a number between 1-5.")
                continue
            if choice == "1":
                add_new_student(students)
            elif choice == "2":
                add_grades_for_student(students)
            elif choice == "3":
                show_report(students)
            elif choice == "4":
                find_top_performer(students)
            elif choice == "5":
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please enter a number between 1-5.")

        except Exception as e:
            print(f"An error occurred: {e}")


def add_new_student(students):
    """
    Adds another student to our records.

    Args:
     students (list): Current list of all students we're tracking
    """
    name = input("Enter student name: ").strip()
    if not name:
        print("Error: Student name cannot be empty.")
        return

    # Check if student already exists
    for student in students:
        if student["name"].lower() == name.lower():
            print(f"Student '{name}' already exists.")
            return

    # New student dictionary with empty grades list
    new_student = {
        "name": name,
        "grades": []  # individual grades
    }
    students.append(new_student)
    print(f"Student '{name}' added successfully.")


def add_grades_for_student(students):
    """
    Add grades for an existing student.

    Args:
        students (list): List of student dictionaries
    """
    name = input("Enter student name: ").strip()
    if not name:
        print("Error: Student name cannot be empty.")
        return

    # Find the student
    student_found = None
    for student in students:
        if student["name"].lower() == name.lower():
            student_found = student
            break

    # Message if student not found
    if student_found is None:
        print(f"Student '{name}' not found.")
        return

    print(f"Adding grades for {student_found['name']}. Enter 'done' to finish.")

    while True:
        grade_input = input("Enter a grade (or 'done' to finish): ").strip()
        if not grade_input:
            print("Error: Input cannot be empty. Please enter a grade or 'done'.")
            continue

        # Exit
        if grade_input.lower() == 'done':
            break
        try:
            # Validate and convert grade
            grade = int(grade_input)
            if grade < 0 or grade > 100:
                print("Invalid grade. Please enter a number between 0 and 100.")
            else:
                # Add valid grade to student's record
                student_found["grades"].append(grade)
                print(f"Grade {grade} added successfully.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def show_report(students):
    """
    Generate full student report with statistics.

    Args:
        students (list): Student data to display
    """
    if not students:
        print("No students available.")
        return

    print("\n--- Student Report ---")

    averages = []  # List to store average grades

    for student in students:
        try:
            # Skip students with no grades
            if not student["grades"]:
                print(f"{student['name']}'s average grade is N/A.")
                continue

            # Calculate student average
            average = sum(student["grades"]) / len(student["grades"])
            averages.append(average)
            print(f"{student['name']}'s average grade is {average:.1f}.")

        except ZeroDivisionError:
            print(f"{student['name']}'s average grade is N/A.")

    # Calculate and show statistics
    if averages:
        max_avg = max(averages)
        min_avg = min(averages)
        overall_avg = sum(averages) / len(averages)

        print("---")
        print(f"Max Average: {max_avg:.1f}")
        print(f"Min Average: {min_avg:.1f}")
        print(f"Overall Average: {overall_avg:.1f}")
    else:
        print("No students with grades available for summary statistics.")


def find_top_performer(students):
    """
    Find and display the student with the highest average grade.

    Args:
        students (list): List of student dictionaries
    """
    # Filter out students without grades
    students_with_grades = [s for s in students if s["grades"]]

    if not students_with_grades:
        print("No students with grades available.")
        return

    try:
        # Find student with the highest average
        top_student = max(students_with_grades,
                          key=lambda student: sum(student["grades"]) / len(student["grades"]))

        # Calculate the top average
        top_average = sum(top_student["grades"]) / len(top_student["grades"])

        print(f"The student with the highest average is {top_student['name']} with a grade of {top_average:.1f}.")

    except Exception as e:
        print(f"Error finding top performer: {e}")



if __name__ == "__main__":
    main()