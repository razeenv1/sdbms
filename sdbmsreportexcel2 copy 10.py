import json
import datetime
from rich.console import Console
from rich.table import Table as RichTable
import os
import pandas as pd
import sys, msvcrt
import keyboard
import time
from fuzzywuzzy import process
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



students = []
marks = []
attendance = []

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
    attempts = 0
    attempts_set = 0
    max_attempts = 3

    while True:
        if attempts >= max_attempts:
            attempts_set += 1
            enforce_timeout(attempts_set)
            attempts = 0

        username = input("Enter username: ")
        password = get_password()
        if username == "admin" and password == "password":
            print("Login successful")
            return True
        else:
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts > 0:
                print(f"Incorrect username or password. {remaining_attempts} attempts remaining. Please try again.")
            else:
                print("Maximum login attempts reached.")


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
        return input("Enter student roll number: ").strip()

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
            gr_no = input("Enter student GR number: ").strip()
            if gr_no.isdigit():
                return gr_no
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
    age = get_valid_age()
    roll_no = get_valid_roll_no()
    phone_no = get_valid_phone_no()
    email = get_valid_email()
    gr_no = get_valid_gr_no()
    grade = get_valid_grade()
    section = get_valid_section()

    existing_students = [student for student in students if student['Grade'] == grade and student['Section'] == section]
    sno = len(existing_students) + 1

    students.append({
        'Sno': sno,
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
                return gr_no
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

    term = get_valid_term()
    gr_no = get_valid_gr_no()
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
    gr_no = input("Enter student GR number: ")

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

    status = input("Enter attendance status (present/absent): ").upper()
    attendance.append({'GR No': gr_no, 'Date': today_date, 'Status': status})
    print("Attendance recorded successfully.")

def paginate_data(data, page_size):
    for i in range(0, len(data), page_size):
        yield data[i:i + page_size]

def display_paginated_data(data, display_function, page_size=10):
    pages = list(paginate_data(data, page_size))
    total_pages = len(pages)

    if total_pages == 0:
        print("No data to display.")
        return

    current_page = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  #Clear console
        display_function(pages[current_page])
        print(f"\nPage {current_page + 1}/{total_pages}")

        if total_pages == 1:
            break

        print("\nNavigation: [left arrow] Previous, [right arrow] Next, [esc] Exit")

        key_event = keyboard.read_event(suppress=True)

        if key_event.event_type == keyboard.KEY_DOWN:
            if key_event.name == 'left':
                current_page = (current_page - 1) % total_pages  #last page if at the first page
            elif key_event.name == 'right':
                current_page = (current_page + 1) % total_pages  #first page if at the last page
            elif key_event.name == 'esc':
                break

def view_options(student_list, choice):
    if choice == '1':
        display_paginated_data(student_list, display_students)
    elif choice == '2':
        term = input("Enter the Term (leave empty for all): ").upper() or None
        subject = input("Enter the subject (type 'all' for all subjects): ").upper() or 'all'
        marks_data = gather_marks_data(student_list, term, subject)
        display_paginated_data(marks_data, display_marks)
    elif choice == '3':
        date = input("Enter the date (dd-mm-yyyy): ")
        attendance_data = gather_attendance_data(student_list, date)
        display_paginated_data(attendance_data, display_attendance)
    elif choice == '4':
        grade = input("Enter grade: ")
        section = input("Enter section: ").upper()
        term = input("Enter the Term (leave empty for all): ").upper() or None
        subject = input("Enter the subject (type 'all' for all subjects): ").upper() or 'all'
        generate_grade_section_performance_graph(grade, section, term, subject)
    elif choice == '5':
        gr_no = input("Enter student GR number: ")
        term = input("Enter the Term (leave empty for all): ").upper() or None
        subject = input("Enter the subject (type 'all' for all subjects): ").upper() or 'all'
        generate_student_performance_graph(gr_no, term, subject)
    else:
        print("Invalid choice.")

def view_data():
    print("\nWhat would you like to view?")
    print("1. Student Details")
    print("2. Student Marks")
    print("3. Student Attendance")
    print("4. Grade and Section Performance Graph")
    print("5. Individual Student Performance Graph")
    choice = input("Enter your choice: ")

    if choice in ['1', '2', '3']:
        grade = input("Enter grade: ")
        section = input("Enter section: ").upper()

        filtered_students = [student for student in students if student['Grade'] == grade and student['Section'] == section]

        if not filtered_students:
            print("No students found for the provided grade and section.")
            return

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
    elif choice in ['4', '5']:
        view_options([], choice)
    else:
        print("Invalid choice.")

def gather_marks_data(student_list, term, subject):
    marks_data = []
    for student in student_list:
        gr_no = student.get('GR No', 'N/A')
        if subject.lower() == 'all':
            filtered_marks = [mark for mark in marks if mark.get('GR No', 'N/A') == gr_no and mark.get('Term') == term]
        else:
            filtered_marks = [mark for mark in marks if mark.get('GR No', 'N/A') == gr_no and mark.get('Term') == term and mark.get('Subject') == subject]
        for mark in filtered_marks:
            marks_data.append({
                'Roll No': student.get('Roll No', 'N/A'),
                'Name': student.get('Name', 'N/A'),
                'Grade': student.get('Grade', 'N/A'),
                'Section': student.get('Section', 'N/A'),
                'Subject': mark.get('Subject', 'N/A'),
                'Marks Obtained': mark.get('Marks Obtained', 'N/A'),
                'Total Marks': mark.get('Total Marks', 'N/A'),
                'Percentage': mark.get('Percentage', 'N/A')
            })
    return marks_data

def gather_attendance_data(student_list, date):
    attendance_data = []
    for student in student_list:
        gr_no = student.get('GR No', 'N/A')
        filtered_attendance = [record for record in attendance if record.get('GR No', 'N/A') == gr_no and record.get('Date') == date]
        for record in filtered_attendance:
            attendance_data.append({
                'Roll No': student.get('Roll No', 'N/A'),
                'Name': student.get('Name', 'N/A'),
                'Grade': student.get('Grade', 'N/A'),
                'Section': student.get('Section', 'N/A'),
                'Date': record.get('Date', 'N/A'),
                'Status': record.get('Status', 'N/A')
            })
    return attendance_data

def display_students(student_list):
    console = Console()
    table = RichTable(title="Student Details")
    table.add_column("Sno", style="cyan")
    table.add_column("Name")
    table.add_column("Age")
    table.add_column("Roll No")
    table.add_column("Phone No")
    table.add_column("Email ID")
    table.add_column("GR No")
    table.add_column("Grade")
    table.add_column("Section")

    for student in student_list:
        row = [
            str(student.get('Sno', 'N/A')),
            str(student.get('Name', 'N/A')),
            str(student.get('Age', 'N/A')),
            str(student.get('Roll No', 'N/A')),
            str(student.get('Phone No', 'N/A')),
            str(student.get('Email ID', 'N/A')),
            str(student.get('GR No', 'N/A')),
            str(student.get('Grade', 'N/A')),
            str(student.get('Section', 'N/A'))
        ]
        table.add_row(*row)

    console.print(table)

def display_marks(marks_data):
    console = Console()
    table = RichTable(title="Student Marks")
    table.add_column("Roll No", style="cyan")
    table.add_column("Name")
    table.add_column("Grade")
    table.add_column("Section")
    table.add_column("Subject")
    table.add_column("Marks Obtained")
    table.add_column("Total Marks")
    table.add_column("Percentage")

    for mark in marks_data:
        row = [
            str(mark.get('Roll No', 'N/A')),
            str(mark.get('Name', 'N/A')),
            str(mark.get('Grade', 'N/A')),
            str(mark.get('Section', 'N/A')),
            str(mark.get('Subject', 'N/A')),
            str(mark.get('Marks Obtained', 'N/A')),
            str(mark.get('Total Marks', 'N/A')),
            str(mark.get('Percentage', 'N/A'))
        ]
        table.add_row(*row)

    console.print(table)

def display_attendance(attendance_data):
    console = Console()
    table = RichTable(title="Student Attendance")
    table.add_column("Roll No", style="cyan")
    table.add_column("Name")
    table.add_column("Grade")
    table.add_column("Section")
    table.add_column("Date")
    table.add_column("Status")

    for record in attendance_data:
        row = [
            str(record.get('Roll No', 'N/A')),
            str(record.get('Name', 'N/A')),
            str(record.get('Grade', 'N/A')),
            str(record.get('Section', 'N/A')),
            str(record.get('Date', 'N/A')),
            str(record.get('Status', 'N/A'))
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
    term = input("Enter Term (PT1, PT2, Term1, Term2): ").upper()
    gr_no = input("Enter student GR number: ")
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
    record['Status'] = input(f"Enter new status (current: {record['Status']}): ") or record['Status']
    print("Attendance record updated successfully.")

def save_data():
    data = {
        "students": students,
        "marks": marks,
        "attendance": attendance
    }
    with open("student_data.json", "w") as f:
        json.dump(data, f)
    print("Data saved successfully.")

def load_data():
    global students, marks, attendance
    try:
        with open("student_data.json", "r") as f:
            data = json.load(f)
            students = data.get("students", [])
            marks = data.get("marks", [])
            attendance = data.get("attendance", [])
    except FileNotFoundError:
        students = []
        marks = []
        attendance = []

def generate_progress_report(students, marks, attendance):
    report_type = input("Which report do you want to generate? (class/student): ").lower()

    if report_type == 'class':
        grade = input("Enter the grade: ")
        section = input("Enter the section: ").upper()
        report_options = input("What information do you need? (details/marks/attendance): ").lower()
        generate_class_progress_report(students, marks, attendance, grade, section, report_options)
    elif report_type == 'student':
        gr_no = input("Enter the GR number of the student: ")
        report_options = input("What information do you need? (details/marks/attendance): ").lower()
        generate_student_progress_report(students, marks, attendance, gr_no, report_options)
    else:
        print("Invalid report type.")

def generate_class_progress_report(students, marks, attendance, grade, section, report_options):
    if report_options == 'details':
        filename = f"{grade}_{section}_Student_Details.xlsx"
    elif report_options == 'marks':
        term = input("Enter the term: ").upper()
        subject = input("Enter the subject (type 'all' to view all subjects): ").upper()
        filename = f"{grade}_{section}_Marks_Report.xlsx"
    elif report_options == 'attendance':
        date_option = input("Enter 'all' for all recorded attendance or specify a date (dd-mm-yyyy): ").lower()
        filename = f"{grade}_{section}_Attendance_Report.xlsx"
    else:
        print("Invalid option.")
        return

    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    # Filter based on grade and section
    class_students = [student for student in students if student['Grade'] == grade and student['Section'] == section]

    if report_options == 'details':
        # Student Details
        student_details_data = []
        for student in class_students:
            student_details_data.append({
                'Sno': student.get('Sno', 'N/A'),
                'Name': student.get('Name', 'N/A'),
                'Age': str(student.get('Age', 'N/A')),
                'Roll No': student.get('Roll No', 'N/A'),
                'Phone No': student.get('Phone No', 'N/A'),
                'Email ID': student.get('Email ID', 'N/A'),
                'GR No': student.get('GR No', 'N/A'),
                'Grade': student.get('Grade', 'N/A'),
                'Section': student.get('Section', 'N/A')
            })

        student_details_df = pd.DataFrame(student_details_data)
        student_details_df.to_excel(writer, sheet_name="Student_Details", index=False)

    if report_options == 'marks':
        # Marks
        marks_data = []
        for student in class_students:
            if subject.lower() == 'all':
                student_marks = [mark for mark in marks if mark['GR No'] == student['GR No'] and mark['Term'] == term]
            else:
                student_marks = [mark for mark in marks if mark['GR No'] == student['GR No'] and mark['Term'] == term and mark['Subject'] == subject]

            for mark in student_marks:
                marks_data.append({
                    'Sno': student.get('Sno', 'N/A'),
                    'Name': student.get('Name', 'N/A'),
                    'Roll No': student.get('Roll No', 'N/A'),
                    'GR No': student.get('GR No', 'N/A'),
                    'Term': mark.get('Term', 'N/A'),
                    'Subject': mark.get('Subject', 'N/A'),
                    'Marks Obtained': mark.get('Marks Obtained', 'N/A'),
                    'Total Marks': mark.get('Total Marks', 'N/A'),
                    'Percentage': mark.get('Percentage', 'N/A')
                })

        marks_df = pd.DataFrame(marks_data)
        marks_df.to_excel(writer, sheet_name="Marks", index=False)

    if report_options == 'attendance':
        # Attendance
        attendance_data = []
        for student in class_students:
            if date_option == 'all':
                student_attendance = [att for att in attendance if att['GR No'] == student['GR No']]
            else:
                student_attendance = [att for att in attendance if att['GR No'] == student['GR No'] and att['Date'] == date_option]

            for att in student_attendance:
                attendance_data.append({
                    'Sno': student.get('Sno', 'N/A'),
                    'Name': student.get('Name', 'N/A'),
                    'Roll No': student.get('Roll No', 'N/A'),
                    'GR No': student.get('GR No', 'N/A'),
                    'Date': att.get('Date', 'N/A'),
                    'Status': att.get('Status', 'N/A')
                })

        attendance_df = pd.DataFrame(attendance_data)
        attendance_df.to_excel(writer, sheet_name="Attendance", index=False)

    writer.close()
    print(f"Class progress report generated and saved in: {filename}")

    open_file = input("Do you want to open the generated progress report? (yes/no): ").lower()
    if open_file == 'yes':
        try:
            os.startfile(filename)
        except Exception as e:
            print(f"Unable to open the file. Error: {e}")
    else:
        if report_options == 'details':
            print("Class Details report generated successfully.")
        elif report_options == 'marks':
            print("Class Marks report generated successfully.")
        elif report_options == 'attendance':
            print("Class Attendance report generated successfully.")
        else:
            pass

def generate_student_progress_report(students, marks, attendance, gr_no, report_options):
    student = next((stu for stu in students if stu['GR No'] == gr_no), None)
    if not student:
        print(f"No student found with GR No: {gr_no}")
        return

    if report_options == 'details':
        filename = f"{student['Name']}_Student_Details.xlsx"
    elif report_options == 'marks':
        term = input("Enter the term: ").upper()
        subject = input("Enter the subject (type 'all' to view all subjects): ").upper()
        filename = f"{student['Name']}_Marks_Report.xlsx"
    elif report_options == 'attendance':
        date_option = input("Enter 'all' for all recorded attendance or specify a date (dd-mm-yyyy): ").lower()
        filename = f"{student['Name']}_Attendance_Report.xlsx"
    else:
        print("Invalid option.")
        return

    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    if report_options == 'details':
        # Student Details
        student_details_data = [{
            'Sno': student.get('Sno', 'N/A'),
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
        # Marks
        if subject.lower() == 'all':
            student_marks = [mark for mark in marks if mark['GR No'] == student['GR No'] and mark['Term'] == term]
        else:
            student_marks = [mark for mark in marks if mark['GR No'] == student['GR No'] and mark['Term'] == term and mark['Subject'] == subject]

        marks_data = []
        for mark in student_marks:
            marks_data.append({
                'Sno': student.get('Sno', 'N/A'),
                'Name': student.get('Name', 'N/A'),
                'Roll No': student.get('Roll No', 'N/A'),
                'GR No': student.get('GR No', 'N/A'),
                'Term': mark.get('Term', 'N/A'),
                'Subject': mark.get('Subject', 'N/A'),
                'Marks Obtained': mark.get('Marks Obtained', 'N/A'),
                'Total Marks': mark.get('Total Marks', 'N/A'),
                'Percentage': mark.get('Percentage', 'N/A')
            })

        marks_df = pd.DataFrame(marks_data)
        marks_df.to_excel(writer, sheet_name="Marks", index=False)

    if report_options == 'attendance':
        # Attendance
        if date_option == 'all':
            student_attendance = [att for att in attendance if att['GR No'] == student['GR No']]
        else:
            student_attendance = [att for att in attendance if att['GR No'] == student['GR No'] and att['Date'] == date_option]

        attendance_data = []
        for att in student_attendance:
            attendance_data.append({
                'Sno': student.get('Sno', 'N/A'),
                'Name': student.get('Name', 'N/A'),
                'Roll No': student.get('Roll No', 'N/A'),
                'GR No': student.get('GR No', 'N/A'),
                'Date': att.get('Date', 'N/A'),
                'Status': att.get('Status', 'N/A')
            })

        attendance_df = pd.DataFrame(attendance_data)
        attendance_df.to_excel(writer, sheet_name="Attendance", index=False)

    writer.close()
    print(f"Student progress report generated and saved in: {filename}")

    open_file = input("Do you want to open the generated progress report? (yes/no): ").lower()
    if open_file == 'yes':
        try:
            os.startfile(filename)
        except Exception as e:
            print(f"Unable to open the file. Error: {e}")
    else:
        if report_options == 'details':
            print("Student Details report generated successfully.")
        elif report_options == 'marks':
            print("Student Marks report generated successfully.")
        elif report_options == 'attendance':
            print("Student Attendance report generated successfully.")
        else:
            pass

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
    print("1. Clear data of a specific student")
    print("2. Clear data of all students in a specific grade and section")
    print("3. Clear all data in the database")
    choice = input("Enter your choice: ")

    if choice == '1':
        gr_no = input("Enter student GR number to clear data: ")
        confirm_clear = input(f"Are you sure you want to clear data for student with GR number {gr_no}? (yes/no): ").lower()
        if confirm_clear == 'yes':
            clear_specific_student(gr_no)
        else:
            print("Operation cancelled.")
    elif choice == '2':
        grade = input("Enter grade: ")
        section = input("Enter section: ").upper
        confirm_clear = input(f"Are you sure you want to clear data for all students in grade {grade} and section {section}? (yes/no): ").lower()
        if confirm_clear == 'yes':
            clear_grade_section(grade, section)
        else:
            print("Operation cancelled.")
    elif choice == '3':
        confirm_clear = input("Are you sure you want to clear all data in the database? (yes/no): ").lower()
        if confirm_clear == 'yes':
            clear_all_data()
        else:
            print("Operation cancelled.")
    else:
        print("Invalid choice. Please try again.")

def clear_specific_student(gr_no):
    global students, marks, attendance
    students = [student for student in students if student['GR No'] != gr_no]
    marks = [mark for mark in marks if mark['GR No'] != gr_no]
    attendance = [record for record in attendance if record['GR No'] != gr_no]
    print(f"Data for student with GR number {gr_no} cleared successfully.")

def clear_grade_section(grade, section):
    global students, marks, attendance
    gr_numbers = [student['GR No'] for student in students if student['Grade'] == grade and student['Section'] == section]
    students = [student for student in students if student['GR No'] not in gr_numbers]
    marks = [mark for mark in marks if mark['GR No'] not in gr_numbers]
    attendance = [record for record in attendance if record['GR No'] not in gr_numbers]
    print(f"Data for students in grade {grade} and section {section} cleared successfully.")

def clear_all_data():
    global students, marks, attendance
    students.clear()
    marks.clear()
    attendance.clear()
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
                'Term': mark['Term']
            })

    if not performance_data:
        print("No marks data available for the provided grade, section, term, and subject.")
        return

    df = pd.DataFrame(performance_data)

    plt.figure(figsize=(12, 8))
    sns.barplot(x='Student', y='Percentage', hue='Subject', data=df)
    plt.title(f'Performance of Grade {grade} Section {section}')
    plt.xticks(rotation=45)
    plt.xlabel('Student')
    plt.ylabel('Percentage')
    plt.legend(title='Subject')
    plt.tight_layout()
    plt.show()

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
    df['Percentage'] = df['Percentage'].str.rstrip('%').astype('float')  # Ensure percentage is numeric

    plt.figure(figsize=(12, 8))
    sns.barplot(x='Subject', y='Percentage', hue='Term', data=df)
    plt.title(f"Performance of {student['Name']} (GR No: {gr_no})")
    plt.ylabel('Percentage')
    plt.xlabel('Subject')
    plt.xticks(rotation=45)
    plt.legend(title='Term')
    plt.tight_layout()
    plt.show()
    
def main():
    print("Welcome to Student Management System!")
    load_data()
    if login():
        while True:
            print("\n1. Add Student\n2. Edit Student\n3. Add Marks\n4. Edit Marks\n5. Record Attendance\n6. View Data\n7. Calculate Class Average\n8. Generate Report\n9. Clear Data\n10. Save Data\n11. Exit")
            choice = input("Enter your choice: ").lower()

            if choice in ['1', 'add student']:
                add_student()
            elif choice in ['2', 'edit student']:
                edit_student()
            elif choice in ['3', 'add marks']:
                add_marks()
            elif choice in ['4', 'edit marks']:
                edit_marks()
            elif choice in ['5', 'record attendance']:
                record_attendance()
            elif choice in ['6', 'view data']:
                view_data()
            elif choice in ['7', 'calculate class average']:
                calculate_class_average()
            elif choice in ['8', 'generate report']:
                generate_progress_report(students, marks, attendance)
            elif choice in ['9', 'clear data']:
                clear_data()
            elif choice in ['10', 'save data']:
                save_data()
            elif choice in ['11', 'exit']:
                choicesave = input("Do you want to save the data before exiting (yes/no): ").lower()
                if choicesave == "yes":
                   save_data()
                   print("Exiting program.")
                   break
                elif choicesave == "no":
                    print("Exiting program Without Saving Data")
                    break
                else:
                    print("Invalid choice.")
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
