import json
import datetime
from datetime import date
from rich.console import Console
from rich.table import Table as RichTable
import os
import pandas as pd
import sys, msvcrt
import keyboard
import time
from fuzzywuzzy import process
import plotly.express as px



students = []
marks = []
attendance = []
assignments = []



PASSWORD_FILE = 'passwords.json'
RESTRICTIONS_FILE = 'restrictions.json'


default_passwords = {
    'admin': 'adminpassword',
    'teacher': 'teacherpassword',
    'student': 'studentpassword'
}


default_restrictions = {
    "admin": ["profile", "add data", "edit data", "view data", "calculate class average", "generate report", "clear data", "save data"],
    "teacher": ["add data", "edit data", "view data", "calculate class average", "generate report", "clear data", "save data"],
    "student": ["view data"]
}

def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as f:
            return json.load(f)
    else:
        save_passwords(default_passwords)
        return default_passwords

def save_passwords(passwords):
    with open(PASSWORD_FILE, 'w') as f:
        json.dump(passwords, f)

def load_restrictions():
    if os.path.exists(RESTRICTIONS_FILE):
        with open(RESTRICTIONS_FILE, 'r') as f:
            return json.load(f)
    else:
        save_restrictions(default_restrictions)
        return default_restrictions

def save_restrictions(restrictions):
    with open(RESTRICTIONS_FILE, 'w') as f:
        json.dump(restrictions, f)

def get_password(prompt='Password: '):
    print(prompt, end='', flush=True)
    password = ''
    while True:
        char = msvcrt.getch()
        if char in (b'\r', b'\n'):
            break
        elif char == b'\x08':
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            password += char.decode('utf-8')
            sys.stdout.write('*')
            sys.stdout.flush()
    print()
    return password

def enforce_timeout(attempts_set):
    timeout = 30 * attempts_set
    for i in range(timeout, 0, -1):
        sys.stdout.write(f'\rToo many failed attempts. Try again in {i} seconds.')
        sys.stdout.flush()
        time.sleep(1)
    print()

def login():
    passwords = load_passwords()
    attempts = 0
    attempts_set = 0
    max_attempts = 3

    while True:
        if attempts >= max_attempts:
            attempts_set += 1
            enforce_timeout(attempts_set)
            attempts = 0

        username = input("Enter username: ").lower()
        password = get_password()
        if username in passwords and password == passwords[username]:
            print("Login successful")
            return username
        else:
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts > 0:
                print(f"Incorrect username or password. {remaining_attempts} attempts remaining. Please try again.")
            else:
                print("Maximum login attempts reached.")

def profile():
    passwords = load_passwords()
    restrictions = load_restrictions()

    while True:
        print("\nProfile Menu")
        print("1. Change Admin Password")
        print("2. Change Teacher Password")
        print("3. Change Student Password")
        print("4. Set Teacher Restrictions")
        print("5. Set Student Restrictions")
        print("6. Return to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            new_password = get_password("Enter new admin password: ")
            passwords['admin'] = new_password
            save_passwords(passwords)
            print("Admin password updated successfully.")
        elif choice == '2':
            new_password = get_password("Enter new teacher password: ")
            passwords['teacher'] = new_password
            save_passwords(passwords)
            print("Teacher password updated successfully.")
        elif choice == '3':
            new_password = get_password("Enter new student password: ")
            passwords['student'] = new_password
            save_passwords(passwords)
            print("Student password updated successfully.")
        elif choice == '4':
            set_restrictions('teacher', restrictions)
        elif choice == '5':
            set_restrictions('student', restrictions)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

    save_restrictions(restrictions)

def set_restrictions(role, restrictions):
    print(f"\nSet Restrictions for {role.capitalize()}")


    available_functions = [
        "profile",
        "add data",
        "edit data",
        "view data",
        "calculate class average",
        "generate report",
        "clear data",
        "save data"
    ]

    print("Available functions:")
    for i, func in enumerate(available_functions):
        print(f"{i + 1}. {func}")

    allowed = restrictions.get(role, [])
    print("\nCurrent restrictions:")
    for func in allowed:
        print(f" - {func}")

    choice = input("Enter the numbers (comma-separated) of the functions you want to allow: ").strip()
    allowed_functions = [available_functions[int(x) - 1] for x in choice.split(',') if x.isdigit() and 0 < int(x) <= len(available_functions)]

    restrictions[role] = allowed_functions
    save_restrictions(restrictions)


    print("\nUpdated Restrictions:")
    print(f"\n{role.capitalize()} restrictions:")
    current_restrictions = restrictions.get(role, [])
    for func in current_restrictions:
        print(f" - {func}")


def add_student():
    def get_valid_name():
        while True:
            name = input("Enter student name: ").strip()
            if len(name.split()) >= 2:
                return name.upper()
            else:
                print("Please enter at least two names (first name and surname).")

    def get_valid_age():
        while True:
            age = input("Enter student age: ").strip()
            if age.isdigit() and int(age) >= 0:
                return age
            else:
                print("Please enter a valid non-negative number for age.")

    def get_valid_roll_no():
        while True:
            roll_no = input("Enter student Roll No: ").strip()
            if roll_no.isdigit():
                return roll_no
            else:
                print("Please enter a valid number for Roll No.")

    def get_valid_phone_no():
        while True:
            phone_no = input("Enter student phone number (include country code): ").strip()

            if not phone_no.startswith('+'):
                phone_no = '+' + phone_no
            if phone_no.startswith('+968') and len(phone_no) == 12 and phone_no[4:].isdigit():
                return phone_no
            elif phone_no.startswith('+91') and len(phone_no) == 13 and phone_no[3:].isdigit():
                return phone_no
            else:
                print("Only phone numbers with country codes '+968' (Oman) and '+91' (India) are accepted. "
                  "+968' should be followed by 8 digits and '+91' should be followed by 10 digits.")

    def get_valid_email():
        while True:
            email = input("Enter student email ID: ").strip()
            if email.endswith('@isboman.com'):
                return email
            else:
                print("Only email accounts with the domain 'isboman.com' are accepted.")

    def get_valid_gr_no():
        while True:

            if students:
                max_gr_no = max(int(student['GR No']) for student in students)
                new_gr_no = str(max_gr_no + 1)
            else:
                new_gr_no = '1'

            user_choice = input(f"Do you want to use the generated GR No. {new_gr_no}? (yes/no): ").strip().lower()
            if user_choice == 'yes':
                return new_gr_no
            else:
                gr_no = input("Enter student GR number: ").strip()
                if gr_no.isdigit():
                    if gr_no not in [student['GR No'] for student in students]:
                        return gr_no
                    else:
                        print("This GR number already exists. Please enter a unique GR number.")
                else:
                    print("Please enter a valid number for GR number.")

    def get_valid_grade():
        while True:
            grade = input("Enter student grade: ").strip()
            if grade.isdigit():
                return grade
            else:
                print("Please enter a valid number for grade.")

    def get_valid_section():
        while True:
            section = input("Enter student section: ").strip()
            if section.isalpha() and len(section) == 1:
                return section.upper()
            else:
                print("Please enter a valid single alphabet for section.")

    name = get_valid_name()
    gr_no = get_valid_gr_no()
    phone_no = get_valid_phone_no()
    email = get_valid_email()
    age = get_valid_age()
    grade = get_valid_grade()
    section = get_valid_section()
    roll_no = get_valid_roll_no()

    students.append({
        'Name': name,
        'Age': age,
        'Roll No': roll_no,
        'Phone No': phone_no,
        'Email ID': email,
        'GR No': gr_no,
        'Grade': grade,
        'Section': section
    })

    print("Student added successfully.")


def add_marks():
    def get_valid_term():
        valid_terms = {"PT1", "PT2", "TERM1", "TERM2"}
        while True:
            term = input("Enter Term (PT1, PT2, TERM1, TERM2): ").upper().strip()
            if term in valid_terms:
                return term
            else:
                print("Invalid term. Please enter one of the following: PT1, PT2, TERM1, TERM2.")

    def get_valid_gr_no():
        while True:
            gr_no = input("Enter student GR number: ").strip()
            if gr_no.isdigit():
                if any(student['GR No'] == gr_no for student in students):
                    return gr_no
                else:
                    print("Student with this GR number does not exist.")
            else:
                print("Please enter a valid number for GR number.")


    def get_valid_subject():
        valid_subjects = [
            "MATHS", "ENGLISH", "SCIENCE", "HISTORY", "GEOGRAPHY",
            "PHYSICS", "CHEMISTRY", "BIOLOGY", "COMPUTER SCIENCE", "ART",
            "MUSIC", "PHYSICAL EDUCATION", "ECONOMICS", "SOCIOLOGY",
            "PSYCHOLOGY", "PHILOSOPHY", "LANGUAGE", "LITERATURE", "IT", "AI"
        ]

        while True:
            subject = input("Enter subject: ").upper().strip()

            if subject in valid_subjects:
                return subject

            closest_match, score = process.extractOne(subject, valid_subjects)

            if score >= 60:
                confirmation = input(f"Did you mean {closest_match}? (yes/no): ").strip().lower()
                if confirmation == "yes":
                    return closest_match

            print("Invalid subject. Please enter a valid subject name.")

    def get_valid_marks_obtained():
        while True:
            marks_obtained = input("Enter marks obtained: ").strip()
            if marks_obtained.isdigit() and int(marks_obtained) >= 0:
                return int(marks_obtained)
            else:
                print("Please enter a valid non-negative number for marks obtained.")

    def get_valid_total_marks(marks_obtained):
        while True:
            total_marks = input("Enter total marks: ").strip()
            if total_marks.isdigit() and int(total_marks) >= marks_obtained:
                return int(total_marks)
            else:
                print("Please enter a valid number for total marks that is greater than or equal to marks obtained.")

    gr_no = get_valid_gr_no()
    term = get_valid_term()
    subject = get_valid_subject()
    marks_obtained = get_valid_marks_obtained()
    total_marks = get_valid_total_marks(marks_obtained)
    percentage = str(round((marks_obtained / total_marks) * 100, 2)) + "%"

    marks.append({
        'Term': term,
        'GR No': gr_no,
        'Subject': subject,
        'Marks Obtained': marks_obtained,
        'Total Marks': total_marks,
        'Percentage': percentage
    })

    print("Marks added successfully.")


def record_attendance():
    def get_valid_gr_no():
        while True:
            gr_no = input("Enter student GR number: ").strip()
            if gr_no.isdigit():
                if any(student['GR No'] == gr_no for student in students):
                    return gr_no
                else:
                    print("Student with this GR number does not exist.")
            else:
                print("Please enter a valid number for GR number.")

    gr_no = get_valid_gr_no()

    today_date = datetime.datetime.today().strftime("%d-%m-%Y")
    print("Date to record attendance:", today_date)

    change_date = input("Do you want to change the date? (yes/no): ").lower()
    if change_date == 'yes':
        date = input("Enter date (DD-MM-YYYY): ")
        try:
            parsed_date = datetime.datetime.strptime(date, "%d-%m-%Y")
            today_date = parsed_date.strftime("%d-%m-%Y")
        except ValueError:
            print("Invalid date format. Using today's date.")
    def get_valid_status():
        valid_statuses = ['present', 'absent']
        while True:
            status = input("Enter attendance status (present/absent): ").strip().lower()
            if status in valid_statuses:
                return status
            else:
                print("Invalid status. Please enter 'present' or 'absent'.")

    status = get_valid_status()
    attendance.append({'GR No': gr_no, 'Date': today_date, 'Status': status})
    print("Attendance recorded successfully.")

def add_assignment():
    def get_valid_gr_no():
        while True:
            gr_no = input("Enter student GR number: ").strip()
            if gr_no.isdigit():
                if any(student['GR No'] == gr_no for student in students):
                    return gr_no
                else:
                    print("Student with this GR number does not exist.")
            else:
                print("Please enter a valid number for GR number.")

    def get_valid_subject():
        valid_subjects = [
            "MATHS", "ENGLISH", "SCIENCE", "HISTORY", "GEOGRAPHY",
            "PHYSICS", "CHEMISTRY", "BIOLOGY", "COMPUTER SCIENCE", "ART",
            "MUSIC", "PHYSICAL EDUCATION", "ECONOMICS", "SOCIOLOGY",
            "PSYCHOLOGY", "PHILOSOPHY", "LANGUAGE", "LITERATURE", "IT", "AI"
        ]

        while True:
            subject = input("Enter subject: ").upper().strip()

            if subject in valid_subjects:
                return subject

            closest_match, score = process.extractOne(subject, valid_subjects)

            if score >= 60:
                confirmation = input(f"Did you mean {closest_match}? (yes/no): ").strip().lower()
                if confirmation == "yes":
                    return closest_match

            print("Invalid subject. Please enter a valid subject name.")

    def get_assignment_name():
        while True:
            assignment_name = input("Enter Assignment Name: ").upper().strip()
            if assignment_name:
                return assignment_name
            else:
                print("Assignment name cannot be empty. Please enter a valid name.")

    def get_status():
        valid_status = ['done', 'not done']
        while True:
            status = input("Enter Status (Done/Not Done): ").strip().lower()
            if status in valid_status:
                return status.capitalize()
            else:
                print("Invalid status. Please enter 'Done' or 'Not Done'.")

    def get_submission_date():

        today_date = datetime.datetime.today().strftime("%d-%m-%Y")
        print("Date for submission:", today_date)


        change_date = input("Do you want to change the date? (yes/no): ").lower()
        if change_date == 'yes':

            date = input("Enter date (DD-MM-YYYY): ").strip()
            try:
                parsed_date = datetime.datetime.strptime(date, "%d-%m-%Y")
                return parsed_date.date()
            except ValueError:
                print("Invalid date format. Using today's date.")

        return datetime.datetime.today().date()

    def get_late_submission():
        while True:
            late_submission = input("Late Submission (Yes/No): ").strip().lower()
            if late_submission in ['yes', 'no']:
                return late_submission.capitalize()
            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")

    gr_no = get_valid_gr_no()
    subject = get_valid_subject()
    assignment_name = get_assignment_name()
    status = get_status()
    submission_date = get_submission_date()
    late_submission = get_late_submission()

    assignments.append({
        'GR No': gr_no,
        'Subject': subject,
        'Assignment Name': assignment_name,
        'Status': status,
        'Submission Date': submission_date,
        'Late Submission': late_submission
    })

    print("Assignment added successfully.")

def paginate_data(data, page_size):
    for i in range(0, len(data), page_size):
        yield data[i:i + page_size]

def display_paginated_data(data, display_function, page_size=10):
    def sort_data(data, sort_column, reverse=False):
        return sorted(data, key=lambda x: x.get(sort_column, ''), reverse=reverse)

    def get_sort_column(data_sample):
        columns = list(data_sample[0].keys())
        while True:
            for i, col in enumerate(columns):
                print(f"{i + 1}. {col}")
            try:
                col_choice = input("Select column to sort by (number): ")
                if not col_choice.isdigit() or not (1 <= int(col_choice) <= len(columns)):
                    raise ValueError("Invalid column number.")
                col_choice = int(col_choice) - 1
                order = input("Sort order (asc/desc): ").strip().lower()
                if order not in ['asc', 'desc']:
                    raise ValueError("Invalid sort order.")
                return columns[col_choice], order == 'desc'
            except ValueError as e:
                print(f"Error: {e}. Please try again.")

    pages = list(paginate_data(data, page_size))
    total_pages = len(pages)

    if total_pages == 0:
        print("No data to display.")
        return

    current_page = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        start_sno = current_page * page_size + 1
        display_function(pages[current_page], start_sno=start_sno)
        print(f"\nPage {current_page + 1}/{total_pages}")

        if total_pages == 1:
            break

        print("\nNavigation: [left arrow] Previous, [right arrow] Next, [esc] Exit, [s] Sort")

        key_event = keyboard.read_event(suppress=True)

        if key_event.event_type == keyboard.KEY_DOWN:
            if key_event.name == 'left':
                current_page = (current_page - 1) % total_pages
            elif key_event.name == 'right':
                current_page = (current_page + 1) % total_pages
            elif key_event.name == 'esc':
                break
            elif key_event.name == 's':
                sort_column, reverse = get_sort_column(data)
                data = sort_data(data, sort_column, reverse)
                pages = list(paginate_data(data, page_size))
                total_pages = len(pages)
                current_page = 0

def view_options(student_list, choice):
    if choice == '1':
        display_paginated_data(student_list, display_students)
    elif choice == '2':
        term = input("Enter the Term (leave empty for all): ").upper() or None
        subject = input("Enter the subject (type 'all' for all subjects): ").upper() or 'all'
        marks_data = gather_marks_data(student_list, term, subject)
        display_paginated_data(marks_data, display_marks)
    elif choice == '3':
        date = input("Enter the date (dd-mm-yyyy, leave empty for all): ").strip() or None
        attendance_data = gather_attendance_data(student_list, date)
        display_paginated_data(attendance_data, display_attendance)
    elif choice == '4':
        subject = input("Enter the subject (leave empty for all): ").upper() or 'all'
        assignment_name = input("Enter the assignment name (leave empty for all): ").upper() or 'all'
        assignment_data = gather_assignment_data(student_list, subject, assignment_name)
        display_paginated_data(assignment_data, display_assignments)
    elif choice == '5':
        view_total_attendance(student_list)
    elif choice == '6':
        grade = input("Enter grade: ")
        section = input("Enter section: ").upper()
        term = input("Enter the Term (leave empty for all): ").upper() or None
        subject = input("Enter the subject (type 'all' for all subjects): ").upper() or 'all'
        generate_grade_section_performance_graph(grade, section, term, subject)
    elif choice == '7':
        gr_no = input("Enter student GR number: ")
        term = input("Enter the Term (leave empty for all): ").upper() or None
        subject = input("Enter the subject (type 'all' for all subjects): ").upper() or 'all'
        generate_student_performance_graph(gr_no, term, subject)
    elif choice == '8':
        grade = input("Enter grade: ")
        section = input("Enter section: ").upper()
        generate_class_attendance_graph(grade, section)
    elif choice == '9':
        gr_no = input("Enter student GR number: ")
        generate_student_attendance_graph(gr_no)
    else:
        print("Invalid choice.")

def view_data():
    print("\nWhat would you like to view?")
    print("1. Student Details")
    print("2. Student Marks")
    print("3. Student Attendance")
    print("4. Student Assignments")
    print("5. Student Total Attendance")
    print("6. Class Performance Graph")
    print("7. Student Performance Graph")
    print("8. Class Attendance Graph")
    print("9. Student Attendance Graph")
    choice = input("Enter your choice: ")

    if choice in ['1', '2', '3', '4', '5']:
        grade = input("Enter grade: ")
        section = input("Enter section: ").upper()

        filtered_students = [student for student in students if student['Grade'] == grade and student['Section'] == section]

        if not filtered_students:
            print("No students found for the provided grade and section.")
            return

        if choice != '5':
            print("1. View all students")
            print("2. View a single student")
            option = input("Enter your choice: ")

            if option == '1':
                view_options(filtered_students, choice)
            elif option == '2':
                gr_no = input("Enter student GR number: ")
                found = False
                for student in filtered_students:
                    if student['GR No'] == gr_no:
                        found = True
                        view_options([student], choice)
                        break
                if not found:
                    print("Student not found.")
            else:
                print("Invalid option.")
        else:
            view_total_attendance(filtered_students)
    elif choice in ['6', '7', '8', '9']:
        view_options([], choice)
    else:
        print("Invalid choice.")

def view_total_attendance(student_list):
    print("1. View all students")
    print("2. View a single student")
    option = input("Enter your choice: ")

    if option == '1':
        total_attendance_data = gather_total_attendance_data(student_list)
        display_paginated_data(total_attendance_data, display_total_attendance)
    elif option == '2':
        gr_no = input("Enter student GR number: ")
        found = False
        for student in student_list:
            if student['GR No'] == gr_no:
                found = True
                total_attendance_data = gather_total_attendance_data([student])
                display_paginated_data(total_attendance_data, display_total_attendance)
                break
        if not found:
            print("Student not found.")
    else:
        print("Invalid option.")

def gather_marks_data(student_list, term, subject):
    marks_data = []
    for student in student_list:
        gr_no = student.get('GR No', 'N/A')
        if subject.lower() == 'all':
            filtered_marks = [mark for mark in marks if mark.get('GR No', 'N/A') == gr_no and (term is None or mark.get('Term') == term)]
        else:
            filtered_marks = [mark for mark in marks if mark.get('GR No', 'N/A') == gr_no and (term is None or mark.get('Term') == term) and mark.get('Subject') == subject]
        for mark in filtered_marks:
            marks_data.append({
                'Roll No': student.get('Roll No', 'N/A'),
                'Name': student.get('Name', 'N/A'),
                'GR No': student.get('GR No', 'N/A'),
                'Grade': student.get('Grade', 'N/A'),
                'Section': student.get('Section', 'N/A'),
                'Subject': mark.get('Subject', 'N/A'),
                'Term': mark.get('Term', 'N/A'),
                'Marks Obtained': mark.get('Marks Obtained', 'N/A'),
                'Total Marks': mark.get('Total Marks', 'N/A'),
                'Percentage': mark.get('Percentage', 'N/A')
            })
    return marks_data

def gather_attendance_data(student_list, date):
    attendance_data = []
    for student in student_list:
        gr_no = student.get('GR No', 'N/A')
        if date is None:
            filtered_attendance = [record for record in attendance if record.get('GR No', 'N/A') == gr_no]
        else:
            filtered_attendance = [record for record in attendance if record.get('GR No', 'N/A') == gr_no and record.get('Date') == date]
        for record in filtered_attendance:
            attendance_data.append({
                'Roll No': student.get('Roll No', 'N/A'),
                'Name': student.get('Name', 'N/A'),
                'GR No': student.get('GR No', 'N/A'),
                'Grade': student.get('Grade', 'N/A'),
                'Section': student.get('Section', 'N/A'),
                'Date': record.get('Date', 'N/A'),
                'Status': record.get('Status', 'N/A')
            })
    return attendance_data

def gather_total_attendance_data(student_list):
    total_attendance_data = []
    for student in student_list:
        gr_no = student.get('GR No', 'N/A')
        filtered_attendance = [record for record in attendance if record.get('GR No', 'N/A') == gr_no]
        present_days = sum(1 for record in filtered_attendance if record.get('Status') == 'present')
        absent_days = sum(1 for record in filtered_attendance if record.get('Status') == 'absent')
        holidays = sum(1 for record in filtered_attendance if record.get('Status') == 'holiday')
        total_days = present_days + absent_days
        attendance_percentage = (present_days / total_days) * 100 if total_days > 0 else 0
        total_attendance_data.append({
            'Roll No': student.get('Roll No', 'N/A'),
            'Name': student.get('Name', 'N/A'),
            'GR No': student.get('GR No', 'N/A'),
            'Grade': student.get('Grade', 'N/A'),
            'Section': student.get('Section', 'N/A'),
            'Present Days': present_days,
            'Absent Days': absent_days,
            'Total Days': total_days,
            'Attendance Percentage': round(attendance_percentage, 2),
            'Holidays': holidays
        })
    return total_attendance_data

def gather_assignment_data(student_list, subject='all', assignment_name='all'):
    assignment_data = []

    for student in student_list:
        gr_no = student.get('GR No', 'N/A')
        filtered_assignments = [assignment for assignment in assignments if assignment.get('GR No', 'N/A') == gr_no]

        if subject != 'all':
            filtered_assignments = [assignment for assignment in filtered_assignments if assignment.get('Subject', 'N/A') == subject]
        if assignment_name != 'all':
            filtered_assignments = [assignment for assignment in filtered_assignments if assignment.get('Assignment Name', 'N/A') == assignment_name]

        for assignment in filtered_assignments:
            assignment_data.append({
                'Roll No': student.get('Roll No', 'N/A'),
                'Name': student.get('Name', 'N/A'),
                'GR No': student.get('GR No', 'N/A'),
                'Grade': student.get('Grade', 'N/A'),
                'Section': student.get('Section', 'N/A'),
                'Subject': assignment.get('Subject', 'N/A'),
                'Assignment Name': assignment.get('Assignment Name', 'N/A'),
                'Status': assignment.get('Status', 'N/A'),
                'Submission Date': assignment.get('Submission Date', 'N/A'),
                'Late Submission': assignment.get('Late Submission', 'N/A')
            })

    return assignment_data

def display_students(student_list, start_sno=1):
    console = Console()
    table = RichTable(title="Student Details")
    table.add_column("Sno", style="cyan")
    table.add_column("Roll No", style="cyan")
    table.add_column("Name")
    table.add_column("GR No")
    table.add_column("Grade")
    table.add_column("Section")
    table.add_column("Phone No")
    table.add_column("Email ID")
    table.add_column("Age")

    for idx, student in enumerate(student_list):
        sno = start_sno + idx
        row = [
            str(sno),
            str(student.get('Roll No', 'N/A')),
            str(student.get('Name', 'N/A')),
            str(student.get('GR No', 'N/A')),
            str(student.get('Grade', 'N/A')),
            str(student.get('Section', 'N/A')),
            str(student.get('Phone No', 'N/A')),
            str(student.get('Email ID', 'N/A')),
            str(student.get('Age', 'N/A'))
        ]
        table.add_row(*row)

    console.print(table)



def display_marks(marks_data, start_sno=1):
    console = Console()
    table = RichTable(title="Student Marks")
    table.add_column("S.No", style="cyan")
    table.add_column("Roll No", style="cyan")
    table.add_column("Name")
    table.add_column("GR No")
    table.add_column("Grade")
    table.add_column("Section")
    table.add_column("Subject")
    table.add_column("Term")
    table.add_column("Marks Obtained")
    table.add_column("Total Marks")
    table.add_column("Percentage")

    for idx, mark in enumerate(marks_data):
        sno = start_sno + idx
        row = [
            str(sno),
            str(mark.get('Roll No', 'N/A')),
            str(mark.get('Name', 'N/A')),
            str(mark.get('GR No', 'N/A')),
            str(mark.get('Grade', 'N/A')),
            str(mark.get('Section', 'N/A')),
            str(mark.get('Subject', 'N/A')),
            str(mark.get('Term', 'N/A')),
            str(mark.get('Marks Obtained', 'N/A')),
            str(mark.get('Total Marks', 'N/A')),
            str(mark.get('Percentage', 'N/A'))
        ]
        table.add_row(*row)

    console.print(table)

def display_attendance(attendance_data, start_sno=1):
    console = Console()
    table = RichTable(title="Student Attendance")
    table.add_column("Sno", style="cyan")
    table.add_column("Roll No")
    table.add_column("Name")
    table.add_column("GR No")
    table.add_column("Grade")
    table.add_column("Section")
    table.add_column("Date")
    table.add_column("Status")

    for idx, record in enumerate(attendance_data):
        sno = start_sno + idx
        row = [
            str(sno),
            str(record.get('Roll No', 'N/A')),
            str(record.get('Name', 'N/A')),
            str(record.get('GR No', 'N/A')),
            str(record.get('Grade', 'N/A')),
            str(record.get('Section', 'N/A')),
            str(record.get('Date', 'N/A')),
            str(record.get('Status', 'N/A'))
        ]
        table.add_row(*row)

    console.print(table)

def display_total_attendance(total_attendance_data, start_sno=1):
    console = Console()
    table = RichTable(title="Total Attendance")
    table.add_column("Sno", style="cyan")
    table.add_column("Roll No")
    table.add_column("Name")
    table.add_column("GR No")
    table.add_column("Grade")
    table.add_column("Section")
    table.add_column("Present Days")
    table.add_column("Absent Days")
    table.add_column("Total Days")
    table.add_column("Attendance Percentage")
    table.add_column("Holidays")

    for idx, record in enumerate(total_attendance_data):
        sno = start_sno + idx
        row = [
            str(sno),
            str(record.get('Roll No', 'N/A')),
            str(record.get('Name', 'N/A')),
            str(record.get('GR No', 'N/A')),
            str(record.get('Grade', 'N/A')),
            str(record.get('Section', 'N/A')),
            str(record.get('Present Days', 'N/A')),
            str(record.get('Absent Days', 'N/A')),
            str(record.get('Total Days', 'N/A')),
            str(record.get('Attendance Percentage', 'N/A')),
            str(record.get('Holidays', 'N/A'))
        ]
        table.add_row(*row)

    console.print(table)


def display_assignments(assignment_data, start_sno=1):
    console = Console()
    table = RichTable(title="Student Assignments")
    table.add_column("Sno", style="cyan")
    table.add_column("Roll No")
    table.add_column("Name")
    table.add_column("GR No")
    table.add_column("Grade")
    table.add_column("Section")
    table.add_column("Subject")
    table.add_column("Assignment Name")
    table.add_column("Status")
    table.add_column("Submission Date")
    table.add_column("Late Submission")

    for idx, assignment in enumerate(assignment_data):
        sno = start_sno + idx
        row = [
            str(sno),
            str(assignment.get('Roll No', 'N/A')),
            str(assignment.get('Name', 'N/A')),
            str(assignment.get('GR No', 'N/A')),
            str(assignment.get('Grade', 'N/A')),
            str(assignment.get('Section', 'N/A')),
            str(assignment.get('Subject', 'N/A')),
            str(assignment.get('Assignment Name', 'N/A')),
            str(assignment.get('Status', 'N/A')),
            str(assignment.get('Submission Date', 'N/A')),
            str(assignment.get('Late Submission', 'N/A'))
        ]
        table.add_row(*row)

    console.print(table)


def edit_student():
    gr_no = input("Enter student GR number to edit: ")
    student = next((s for s in students if s['GR No'] == gr_no), None)

    if not student:
        print("Student not found.")
        return

    print("Leave blank to keep the current value.")
    student['Name'] = input(f"Enter new name (current: {student['Name']}): ") or student['Name']
    student['Age'] = input(f"Enter new age (current: {student['Age']}): ") or student['Age']
    student['Roll No'] = input(f"Enter new roll number (current: {student['Roll No']}): ") or student['Roll No']
    student['Phone No'] = input(f"Enter new phone number (current: {student['Phone No']}): ") or student['Phone No']
    student['Email ID'] = input(f"Enter new email ID (current: {student['Email ID']}): ") or student['Email ID']
    student['GR No'] = input(f"Enter new Gr no (current: {student['GR No']}): ") or student['GR No']
    student['Grade'] = input(f"Enter new grade (current: {student['Grade']}): ") or student['Grade']
    student['Section'] = input(f"Enter new section (current: {student['Section']}): ").upper() or student['Section']
    print("Student data updated successfully.")

def edit_marks():
    gr_no = input("Enter student GR number: ")
    term = input("Enter Term (PT1, PT2, Term1, Term2): ").upper()
    subject = input("Enter subject: ").upper()

    mark = next((m for m in marks if m['GR No'] == gr_no and m['Term'] == term and m['Subject'] == subject), None)

    if not mark:
        print("Marks record not found.")
        return

    print("Leave blank to keep the current value.")
    new_marks_obtained = input(f"Enter new marks obtained (current: {mark['Marks Obtained']}): ")
    new_total_marks = input(f"Enter new total marks (current: {mark['Total Marks']}): ")

    if new_marks_obtained:
        mark['Marks Obtained'] = int(new_marks_obtained)
    if new_total_marks:
        mark['Total Marks'] = int(new_total_marks)

    mark['Percentage'] = str(round((mark['Marks Obtained'] / mark['Total Marks']) * 100, 2)) + "%"
    print("Marks record updated successfully.")

def edit_attendance():
    gr_no = input("Enter student GR number: ")
    date = input("Enter date (DD-MM-YYYY): ")
    record = next((a for a in attendance if a['GR No'] == gr_no and a['Date'] == date), None)

    if not record:
        print("Attendance record not found.")
        return

    print("Leave blank to keep the current value.")
    record['Status'] = input(f"Enter new status (current: {record['Status']}): ").lower() or record['Status']
    print("Attendance record updated successfully.")

def edit_assignment():
    gr_no = input("Enter student GR number: ")
    subject = input("Enter subject: ").upper()
    assignment_name = input("Enter assignment name: ").upper().strip()

    assignment = next((a for a in assignments if a['GR No'] == gr_no and a['Subject'] == subject and a['Assignment Name'] == assignment_name), None)

    if not assignment:
        print("Assignment record not found.")
        return

    print("Leave blank to keep the current value.")
    assignment['Assignment Name'] = input(f"Enter new assignment name (current: {assignment['Assignment Name']}): ").upper() or assignment['Assignment Name']
    assignment['Status'] = input(f"Enter new status (current: {assignment['Status']}): ").capitalize() or assignment['Status']
    assignment['Submission Date'] = input(f"Enter new submission date (current: {assignment['Submission Date']}): ") or assignment['Submission Date']
    assignment['Late Submission'] = input(f"Enter new late submission status (current: {assignment['Late Submission']}): ").capitalize() or assignment['Late Submission']

    print("Assignment record updated successfully.")

def date_converter(o):
    if isinstance(o, date):
        return o.strftime("%d-%m-%Y")
    raise TypeError(f"Object of type {o.__class__.__name__} is not serializable")

def save_data():
    data = {
        "students": students,
        "marks": marks,
        "attendance": attendance,
        "assignments": assignments
    }
    with open("student_data.json", "w") as f:
        json.dump(data, f, default=date_converter)
    print("Data saved successfully.")

def load_data():
    global students, marks, attendance, assignments
    try:
        with open("student_data.json", "r") as f:
            data = json.load(f)
            students = data.get("students", [])
            marks = data.get("marks", [])
            attendance = data.get("attendance", [])
            assignments = data.get("assignments", [])
    except FileNotFoundError:
        students = []
        marks = []
        attendance = []
        assignments = []

def get_unique_filename(base_filename):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_filename}_{timestamp}.xlsx"

def generate_progress_report(students, marks, attendance, assignments):
    report_type = input("Which report do you want to generate? (class/student): ").lower()

    if report_type == 'class':
        grade = input("Enter the grade: ")
        section = input("Enter the section: ").upper()
        report_options = input("What information do you need? (details/marks/attendance/assignments): ").lower()
        generate_class_progress_report(students, marks, attendance, assignments, grade, section, report_options)
    elif report_type == 'student':
        gr_no = input("Enter the GR number of the student: ")
        report_options = input("What information do you need? (details/marks/attendance/assignments): ").lower()
        generate_student_progress_report(students, marks, attendance, assignments, gr_no, report_options)
    else:
        print("Invalid report type.")

def generate_class_progress_report(students, marks, attendance, assignments, grade, section, report_options):
    if report_options == 'details':
        filename = get_unique_filename(f"{grade}_{section}_Student_Details")
    elif report_options == 'marks':
        term = input("Enter the term (type 'all' to view all terms or leave empty): ").upper()
        subject = input("Enter the subject (type 'all' to view all subjects or leave empty): ").upper()
        filename = get_unique_filename(f"{grade}_{section}_Marks_Report")
    elif report_options == 'attendance':
        date_option = input("Enter 'all' for all recorded attendance or specify a date (dd-mm-yyyy): ").lower()
        filename = get_unique_filename(f"{grade}_{section}_Attendance_Report")
    elif report_options == 'assignments':
        subject = input("Enter the subject (type 'all' to view all subjects or leave empty): ").upper()
        assignment_name = input("Enter the assignment name (type 'all' to view all assignments or leave empty): ").upper()
        filename = get_unique_filename(f"{grade}_{section}_Assignments_Report")
    else:
        print("Invalid option.")
        return

    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    class_students = [student for student in students if student['Grade'] == grade and student['Section'] == section]

    if report_options == 'details':
        sno = 1
        student_details_data = []
        for student in class_students:
            student_details_data.append({
                'Sno': str(sno),
                'Name': student.get('Name', 'N/A'),
                'Age': str(student.get('Age', 'N/A')),
                'Roll No': student.get('Roll No', 'N/A'),
                'Phone No': student.get('Phone No', 'N/A'),
                'Email ID': student.get('Email ID', 'N/A'),
                'GR No': student.get('GR No', 'N/A'),
                'Grade': student.get('Grade', 'N/A'),
                'Section': student.get('Section', 'N/A')
            })
            sno += 1

        student_details_df = pd.DataFrame(student_details_data)
        student_details_df.to_excel(writer, sheet_name="Student_Details", index=False)

    if report_options == 'marks':
        sno = 1
        marks_data = []
        for student in class_students:
            if term.lower() == 'all' or term == '':
                if subject.lower() == 'all' or subject == '':
                    student_marks = [mark for mark in marks if mark['GR No'] == student['GR No']]
                else:
                    student_marks = [mark for mark in marks if mark['GR No'] == student['GR No'] and mark['Subject'] == subject]
            else:
                if subject.lower() == 'all' or subject == '':
                    student_marks = [mark for mark in marks if mark['GR No'] == student['GR No'] and mark['Term'] == term]
                else:
                    student_marks = [mark for mark in marks if mark['GR No'] == student['GR No'] and mark['Term'] == term and mark['Subject'] == subject]

            for mark in student_marks:
                marks_data.append({
                    'Sno': str(sno),
                    'Name': student.get('Name', 'N/A'),
                    'Roll No': student.get('Roll No', 'N/A'),
                    'GR No': student.get('GR No', 'N/A'),
                    'Term': mark.get('Term', 'N/A'),
                    'Subject': mark.get('Subject', 'N/A'),
                    'Marks Obtained': mark.get('Marks Obtained', 'N/A'),
                    'Total Marks': mark.get('Total Marks', 'N/A'),
                    'Percentage': mark.get('Percentage', 'N/A')
                })
                sno += 1

        marks_df = pd.DataFrame(marks_data)
        marks_df.to_excel(writer, sheet_name="Marks", index=False)

    if report_options == 'attendance':
        sno = 1
        attendance_data = []
        for student in class_students:
            if date_option == 'all':
                student_attendance = [att for att in attendance if att['GR No'] == student['GR No']]
            else:
                student_attendance = [att for att in attendance if att['GR No'] == student['GR No'] and att['Date'] == date_option]

            for att in student_attendance:
                attendance_data.append({
                    'Sno': str(sno),
                    'Name': student.get('Name', 'N/A'),
                    'Roll No': student.get('Roll No', 'N/A'),
                    'GR No': student.get('GR No', 'N/A'),
                    'Date': att.get('Date', 'N/A'),
                    'Status': att.get('Status', 'N/A')
                })
                sno += 1

        attendance_df = pd.DataFrame(attendance_data)
        attendance_df.to_excel(writer, sheet_name="Attendance", index=False)

    if report_options == 'assignments':
        sno = 1
        assignments_data = []
        for student in class_students:
            if subject.lower() == 'all' or subject == '':
                if assignment_name.lower() == 'all' or assignment_name == '':
                    student_assignments = [assignment for assignment in assignments if assignment['GR No'] == student['GR No']]
                else:
                    student_assignments = [assignment for assignment in assignments if assignment['GR No'] == student['GR No'] and assignment['Assignment Name'].upper() == assignment_name]
            else:
                if assignment_name.lower() == 'all' or assignment_name == '':
                    student_assignments = [assignment for assignment in assignments if assignment['GR No'] == student['GR No'] and assignment['Subject'].upper() == subject]
                else:
                    student_assignments = [assignment for assignment in assignments if assignment['GR No'] == student['GR No'] and assignment['Subject'].upper() == subject and assignment['Assignment Name'].upper() == assignment_name]

            for assignment in student_assignments:
                assignments_data.append({
                    'Sno': str(sno),
                    'Name': student.get('Name', 'N/A'),
                    'Roll No': student.get('Roll No', 'N/A'),
                    'GR No': student.get('GR No', 'N/A'),
                    'Subject': assignment.get('Subject', 'N/A'),
                    'Assignment Name': assignment.get('Assignment Name', 'N/A'),
                    'Status': assignment.get('Status', 'N/A'),
                    'Submission Date': assignment.get('Submission Date', 'N/A'),
                    'Late Submission': assignment.get('Late Submission', 'N/A')
                })
                sno += 1

        assignments_df = pd.DataFrame(assignments_data)
        assignments_df.to_excel(writer, sheet_name="Assignments", index=False)

    writer.close()
    print(f"Class progress report generated and saved in: {filename}")

    open_file = input("Do you want to open the generated progress report? (yes/no): ").lower()
    if open_file == 'yes':
        try:
            os.startfile(filename)
        except Exception as e:
            print(f"Unable to open the file. Error: {e}")
    else:
        print(f"Report generated and saved in: {filename}")

def generate_student_progress_report(students, marks, attendance, assignments, gr_no, report_options):
    student = next((stu for stu in students if stu['GR No'] == gr_no), None)
    if not student:
        print(f"No student found with GR No: {gr_no}")
        return

    if report_options == 'details':
        filename = get_unique_filename(f"{student['Name']}_Student_Details")
    elif report_options == 'marks':
        term = input("Enter the term (type 'all' to view all terms or leave empty): ").upper()
        subject = input("Enter the subject (type 'all' to view all subjects or leave empty): ").upper()
        filename = get_unique_filename(f"{student['Name']}_Marks_Report")
    elif report_options == 'attendance':
        date_option = input("Enter 'all' for all recorded attendance or specify a date (dd-mm-yyyy): ").lower()
        filename = get_unique_filename(f"{student['Name']}_Attendance_Report")
    elif report_options == 'assignments':
        subject = input("Enter the subject (type 'all' to view all subjects or leave empty): ").upper()
        assignment_name = input("Enter the assignment name (type 'all' to view all assignments or leave empty): ").upper()
        filename = get_unique_filename(f"{student['Name']}_Assignments_Report")
    else:
        print("Invalid option.")
        return

    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    if report_options == 'details':
        student_details_data = [{
            'Sno': "1",
            'Name': student.get('Name', 'N/A'),
            'Age': str(student.get('Age', 'N/A')),
            'Roll No': student.get('Roll No', 'N/A'),
            'Phone No': student.get('Phone No', 'N/A'),
            'Email ID': student.get('Email ID', 'N/A'),
            'GR No': student.get('GR No', 'N/A'),
            'Grade': student.get('Grade', 'N/A'),
            'Section': student.get('Section', 'N/A')
        }]

        student_details_df = pd.DataFrame(student_details_data)
        student_details_df.to_excel(writer, sheet_name="Student_Details", index=False)

    if report_options == 'marks':
        if term.lower() == 'all' or term == '':
            if subject.lower() == 'all' or subject == '':
                student_marks = [mark for mark in marks if mark['GR No'] == student['GR No']]
            else:
                student_marks = [mark for mark in marks if mark['GR No'] == student['GR No'] and mark['Subject'] == subject]
        else:
            if subject.lower() == 'all' or subject == '':
                student_marks = [mark for mark in marks if mark['GR No'] == student['GR No'] and mark['Term'] == term]
            else:
                student_marks = [mark for mark in marks if mark['GR No'] == student['GR No'] and mark['Term'] == term and mark['Subject'] == subject]

        marks_data = [{
            'Sno': str(1 + idx),
            'Name': student.get('Name', 'N/A'),
            'Roll No': student.get('Roll No', 'N/A'),
            'GR No': student.get('GR No', 'N/A'),
            'Term': mark.get('Term', 'N/A'),
            'Subject': mark.get('Subject', 'N/A'),
            'Marks Obtained': mark.get('Marks Obtained', 'N/A'),
            'Total Marks': mark.get('Total Marks', 'N/A'),
            'Percentage': mark.get('Percentage', 'N/A')
        } for idx, mark in enumerate(student_marks)]

        marks_df = pd.DataFrame(marks_data)
        marks_df.to_excel(writer, sheet_name="Marks", index=False)

    if report_options == 'attendance':
        if date_option == 'all':
            student_attendance = [att for att in attendance if att['GR No'] == student['GR No']]
        else:
            student_attendance = [att for att in attendance if att['GR No'] == student['GR No'] and att['Date'] == date_option]

        attendance_data = [{
            'Sno': str(1 + idx),
            'Name': student.get('Name', 'N/A'),
            'Roll No': student.get('Roll No', 'N/A'),
            'GR No': student.get('GR No', 'N/A'),
            'Date': att.get('Date', 'N/A'),
            'Status': att.get('Status', 'N/A')
        } for idx, att in enumerate(student_attendance)]

        attendance_df = pd.DataFrame(attendance_data)
        attendance_df.to_excel(writer, sheet_name="Attendance", index=False)

    if report_options == 'assignments':
        if subject.lower() == 'all' or subject == '':
            if assignment_name.lower() == 'all' or assignment_name == '':
                student_assignments = [assignment for assignment in assignments if assignment['GR No'] == student['GR No']]
            else:
                student_assignments = [assignment for assignment in assignments if assignment['GR No'] == student['GR No'] and assignment['Assignment Name'].upper() == assignment_name]
        else:
            if assignment_name.lower() == 'all' or assignment_name == '':
                student_assignments = [assignment for assignment in assignments if assignment['GR No'] == student['GR No'] and assignment['Subject'].upper() == subject]
            else:
                student_assignments = [assignment for assignment in assignments if assignment['GR No'] == student['GR No'] and assignment['Subject'].upper() == subject and assignment['Assignment Name'].upper() == assignment_name]

        assignments_data = [{
            'Sno': str(1 + idx),
            'Name': student.get('Name', 'N/A'),
            'Roll No': student.get('Roll No', 'N/A'),
            'GR No': student.get('GR No', 'N/A'),
            'Subject': assignment.get('Subject', 'N/A'),
            'Assignment Name': assignment.get('Assignment Name', 'N/A'),
            'Status': assignment.get('Status', 'N/A'),
            'Submission Date': assignment.get('Submission Date', 'N/A'),
            'Late Submission': assignment.get('Late Submission', 'N/A')
        } for idx, assignment in enumerate(student_assignments)]

        assignments_df = pd.DataFrame(assignments_data)
        assignments_df.to_excel(writer, sheet_name="Assignments", index=False)

    writer.close()
    print(f"Student progress report generated and saved in: {filename}")

    open_file = input("Do you want to open the generated progress report? (yes/no): ").lower()
    if open_file == 'yes':
        try:
            os.startfile(filename)
        except Exception as e:
            print(f"Unable to open the file. Error: {e}")
    else:
        print(f"Report generated and saved in: {filename}")

def calculate_class_average():
    grade = input("Enter grade: ")
    section = input("Enter section: ").upper()
    subject = input("Enter subject: ").upper()
    term = input("Enter Term(PT1, PT2, Term1, Term2): ").upper()
    filtered_students = [student for student in students if student['Grade'] == grade and student['Section'] == section]

    if not filtered_students:
        print("No students found for the provided grade and section.")
        return

    gr_numbers = [student['GR No'] for student in filtered_students]

    filtered_marks = [mark['Marks Obtained'] for mark in marks if mark['Subject'] == subject
                      and mark['Term'] == term
                      and mark['GR No'] in gr_numbers]

    if not filtered_marks:
        print("No marks found for the provided criteria.")
        return

    class_average = sum(filtered_marks) / len(filtered_marks)
    print(f"Class average for {grade} {section} in {subject} {term}: {class_average}")

def clear_data():
    print("\nWhat data would you like to clear?")
    print("1. Clear student details")
    print("2. Clear student marks")
    print("3. Clear student attendance")
    print("4. Clear student assignments")
    print("5. Clear all data")

    choice = input("Enter your choice: ").strip()

    if choice in ['1', '2', '3', '4']:
        print("\nWould you like to clear data for:")
        print("1. A specific student")
        print("2. All students in a grade and section")
        sub_choice = input("Enter your choice: ").strip()

        if sub_choice == '1':
            gr_no = input("Enter the GR number of the student: ").strip()
            if choice == '1':
                clear_specific_type('details', gr_no)
            elif choice == '2':
                clear_specific_type('marks', gr_no)
            elif choice == '3':
                clear_specific_type('attendance', gr_no)
            elif choice == '4':
                clear_specific_type('assignments', gr_no)
        elif sub_choice == '2':
            grade = input("Enter grade: ").strip()
            section = input("Enter section: ").strip().upper()
            if choice == '1':
                clear_grade_section('details', grade, section)
            elif choice == '2':
                clear_grade_section('marks', grade, section)
            elif choice == '3':
                clear_grade_section('attendance', grade, section)
            elif choice == '4':
                clear_grade_section('assignments', grade, section)
        else:
            print("Invalid choice. Please try again.")

    elif choice == '5':
        clear_all_data()
    else:
        print("Invalid choice. Please try again.")

def clear_specific_type(data_type, gr_no):
    global students, marks, attendance, assignments

    if data_type == 'details':
        students = [student for student in students if student['GR No'] != gr_no]
        marks = [mark for mark in marks if mark['GR No'] != gr_no]
        attendance = [record for record in attendance if record['GR No'] != gr_no]
        assignments = [assignment for assignment in assignments if assignment['GR No'] != gr_no]
        print(f"Details for student with GR number {gr_no} cleared successfully.")

    elif data_type == 'marks':
        marks = [mark for mark in marks if mark['GR No'] != gr_no]
        print(f"Marks for student with GR number {gr_no} cleared successfully.")

    elif data_type == 'attendance':
        attendance = [record for record in attendance if record['GR No'] != gr_no]
        print(f"Attendance for student with GR number {gr_no} cleared successfully.")

    elif data_type == 'assignments':
        assignments = [assignment for assignment in assignments if assignment['GR No'] != gr_no]
        print(f"Assignments for student with GR number {gr_no} cleared successfully.")

    else:
        print("Invalid data type. Please try again.")

def clear_grade_section(data_type, grade, section):
    global students, marks, attendance, assignments

    gr_numbers = [student['GR No'] for student in students if student['Grade'] == grade and student['Section'] == section]

    if data_type == 'details':
        students = [student for student in students if student['GR No'] not in gr_numbers]
        marks = [mark for mark in marks if mark['GR No'] not in gr_numbers]
        attendance = [record for record in attendance if record['GR No'] not in gr_numbers]
        assignments = [assignment for assignment in assignments if assignment['GR No'] not in gr_numbers]
        print(f"Details for students in grade {grade} and section {section} cleared successfully.")

    elif data_type == 'marks':
        marks = [mark for mark in marks if mark['GR No'] not in gr_numbers]
        print(f"Marks for students in grade {grade} and section {section} cleared successfully.")

    elif data_type == 'attendance':
        attendance = [record for record in attendance if record['GR No'] not in gr_numbers]
        print(f"Attendance for students in grade {grade} and section {section} cleared successfully.")

    elif data_type == 'assignments':
        assignments = [assignment for assignment in assignments if assignment['GR No'] not in gr_numbers]
        print(f"Assignments for students in grade {grade} and section {section} cleared successfully.")

    else:
        print("Invalid data type. Please try again.")

def clear_all_data():
    global students, marks, attendance, assignments
    students.clear()
    marks.clear()
    attendance.clear()
    assignments.clear()
    print("All data in the database cleared successfully.")


def generate_grade_section_performance_graph(grade, section, term=None, subject=None):
    filtered_students = [student for student in students if student['Grade'] == grade and student['Section'] == section]

    if not filtered_students:
        print("No students found for the provided grade and section.")
        return

    performance_data = []

    for student in filtered_students:
        student_marks = [mark for mark in marks if mark['GR No'] == student['GR No']]
        if term:
            student_marks = [mark for mark in student_marks if mark['Term'] == term]
        if subject and subject.lower() != 'all':
            student_marks = [mark for mark in student_marks if mark['Subject'].lower() == subject.lower()]

        for mark in student_marks:
            performance_data.append({
                'Student': student['Name'],
                'Subject': mark['Subject'],
                'Percentage': float(mark['Percentage'].strip('%')),
                'Term': mark['Term'],
                'Marks Obtained': mark['Marks Obtained'],
                'Total Marks': mark['Total Marks']
            })

    if not performance_data:
        print("No marks data available for the provided grade, section, term, and subject.")
        return

    df = pd.DataFrame(performance_data)

    fig = px.bar(df, x='Student', y='Percentage', color='Term',
                 text='Percentage',
                 labels={'Percentage': 'Percentage'},
                 title=f'Performance of Grade {grade} Section {section}',
                 hover_name='Subject',
                 hover_data={'Percentage': True, 'Term': True, 'Marks Obtained': True, 'Total Marks': True })

    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(
        xaxis_title='Student',
        yaxis_title='Percentage',
        legend_title='Term',
        xaxis_tickangle=-45
    )

    fig.show()

def generate_student_performance_graph(gr_no, term=None, subject=None):

    student = next((s for s in students if s['GR No'] == gr_no), None)
    if not student:
        print(f"No student found with GR No: {gr_no}")
        return

    student_marks = [m for m in marks if m['GR No'] == gr_no]
    if term:
        student_marks = [m for m in student_marks if m['Term'] == term]
    if subject and subject.lower() != 'all':
        student_marks = [m for m in student_marks if m['Subject'].lower() == subject.lower()]

    if not student_marks:
        print(f"No marks found for student with GR No: {gr_no} for the selected term and subject.")
        return

    df = pd.DataFrame(student_marks)
    df['Percentage'] = df['Percentage'].str.rstrip('%').astype('float')

    fig = px.bar(df, x='Subject', y='Percentage', color='Term',
                 labels={'Percentage': 'Percentage'},
                 title=f"Performance of {student['Name']} (GR No: {gr_no})",
                 text='Percentage',
                 hover_data={'Percentage': True, 'Term': True, 'Marks Obtained': True, 'Total Marks': True })

    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(
        xaxis_title='Subject',
        yaxis_title='Percentage',
        legend_title='Term',
        xaxis_tickangle=-45
    )

    fig.show()

def generate_class_attendance_graph(grade, section):
    filtered_students = [student for student in students if student['Grade'] == grade and student['Section'] == section]

    if not filtered_students:
        print("No students found for the provided grade and section.")
        return

    attendance_data = []

    for student in filtered_students:
        student_attendance = [record for record in attendance if record['GR No'] == student['GR No']]
        present_days = sum(1 for record in student_attendance if record['Status'] == 'present')
        absent_days = sum(1 for record in student_attendance if record['Status'] == 'absent')
        holidays = sum(1 for record in student_attendance if record['Status'] == 'holiday')

        attendance_data.append({
            'Student': student['Name'],
            'Present Days': present_days,
            'Absent Days': absent_days,
            'Holidays': holidays
        })

    df = pd.DataFrame(attendance_data)

    fig = px.bar(df, x='Student', y=['Present Days', 'Absent Days', 'Holidays'],
                 title=f'Attendance for Grade {grade} Section {section}',
                 labels={'value': 'Days', 'variable': 'Attendance Status'},
                 text_auto=True)

    fig.update_layout(
        barmode='group',
        xaxis_title='Student',
        yaxis_title='Days',
        legend_title='Attendance Status',
        xaxis_tickangle=-45
    )

    fig.show()

def generate_student_attendance_graph(gr_no):
    student = next((s for s in students if s['GR No'] == gr_no), None)
    if not student:
        print(f"No student found with GR No: {gr_no}")
        return

    student_attendance = [record for record in attendance if record['GR No'] == gr_no]
    present_days = sum(1 for record in student_attendance if record['Status'] == 'present')
    absent_days = sum(1 for record in student_attendance if record['Status'] == 'absent')
    holidays = sum(1 for record in student_attendance if record['Status'] == 'holiday')

    attendance_data = {
        'Status': ['Present Days', 'Absent Days', 'Holidays'],
        'Days': [present_days, absent_days, holidays]
    }

    df = pd.DataFrame(attendance_data)


    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    fig = px.bar(df, x='Status', y='Days', text='Days',
                 title=f'Attendance for {student["Name"]} (GR No: {gr_no})',
                 labels={'Days': 'Days'},
                 color='Status',
                 color_discrete_sequence=colors)

    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(
        xaxis_title='Attendance Status',
        yaxis_title='Days',
        xaxis_tickangle=-45
    )

    fig.show()

def add_data():
    print("\n1. Add Student\n2. Add Marks\n3. Record Attendance\n4. Add Assignment Status")
    choice = input("Enter your choice: ").lower()
    if choice in ['1', 'add student']:
        add_student()
    elif choice in ['2', 'add marks']:
        add_marks()
    elif choice in ['3', 'record attendance']:
        record_attendance()
    elif choice in ['4', 'add assignment status']:
        add_assignment()
    else:
        print("Invalid choice. Please try again.")

def edit_data():
    print("\n1. Edit Student\n2. Edit Marks\n3. Edit Attendance\n4. Edit Assignment Status")
    choice = input("Enter your choice: ").lower()
    if choice in ['1', 'edit student']:
        edit_student()
    elif choice in ['2', 'edit marks']:
        edit_marks()
    elif choice in ['3', 'edit attendance']:
        edit_attendance()
    elif choice in ['4', 'edit assignment status']:
        edit_assignment()
    else:
        print("Invalid choice. Please try again.")


def main_menu_options(role):
    restrictions = load_restrictions()
    available_functions = {
        'profile': profile,
        'add data': add_data,
        'edit data': edit_data,
        'view data': view_data,
        'calculate class average': calculate_class_average,
        'generate report': generate_progress_report,
        'clear data': clear_data,
        'save data': save_data,
        'exit': exit_program
    }

    restricted_functions = restrictions.get(role, [])

    options = {str(i + 1): (func, available_functions[func]) for i, func in enumerate(restricted_functions) if func in available_functions}

    options[str(len(options) + 1)] = ('exit', available_functions['exit'])

    return options

def display_main_menu(role):
    options = main_menu_options(role)
    if not options:
        print("Access denied.")
        return

    while True:
        print("\nMain Menu:")
        for key, (desc, _) in options.items():
            print(f"{key}. {desc}")

        choice = input("Enter your choice: ").strip()
        if choice in options:
            if options[choice][1] == generate_progress_report:
                options[choice][1](students, marks, attendance, assignments)
            else:
                options[choice][1]()
        else:
            print("Invalid choice. Please try again.")

def exit_program():
    choicesave = input("Do you want to save the data before exiting (yes/no): ").lower()
    if choicesave == "yes":
        save_data()
        print("Exiting program.")
    elif choicesave == "no":
        print("Exiting program without saving data.")
    else:
        print("Invalid choice. Exiting without saving data.")
    sys.exit()


def main():
    print("Welcome to Student Management System!")
    load_data()
    global current_role
    current_role = login()
    if current_role:
        display_main_menu(current_role)
    else:
        print("Login failed. Exiting.")
        sys.exit()

if __name__ == "__main__":
    main()
