import tkinter as tk
from tkinter import ttk, messagebox

STUDENT_FILE_PATH = "studentMarks.txt"  # Path to the student data file

def fetch_students(file_path):
    """
    Fetch student data from the given file.
    Returns a list of dictionaries containing student information.
    """
    student_list = []  # List to hold all student data
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()  # Read lines from the file
            for line in lines:
                student_info = line.strip().split(',')  # Split line by commas
                if len(student_info) == 6:  # Ensure the data is complete
                    student = {
                        "student_id": int(student_info[0]),  # Student ID as integer
                        "student_name": student_info[1],  # Name of the student
                        "course_marks": list(map(int, student_info[2:5])),  # Coursework marks as integers
                        "exam_score": int(student_info[5])  # Exam score as integer
                    }
                    student_list.append(student)  # Add to student list
    except FileNotFoundError:
        messagebox.showerror("File Not Found", f"Could not find the file '{file_path}'.")
    return student_list

def write_students(file_path, student_list):
    """
    Save the student data back to the file.
    """
    try:
        with open(file_path, 'w') as f:
            for student in student_list:
                student_record = f"{student['student_id']},{student['student_name']},{','.join(map(str, student['course_marks']))},{student['exam_score']}\n"
                f.write(student_record)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {e}")

def compute_totals(student):
    """
    Compute the total marks and percentage for a student.
    """
    coursework_total = sum(student["course_marks"])  # Total coursework marks
    overall_total = coursework_total + student["exam_score"]  # Total marks (coursework + exam)
    percentage_score = (overall_total / 160) * 100  # Percentage based on total marks
    grade = determine_grade(percentage_score)  # Get the grade based on the percentage
    return coursework_total, student["exam_score"], overall_total, percentage_score, grade

def determine_grade(percentage_score):
    """
    Determine the grade based on the calculated percentage.
    """
    if percentage_score >= 70:
        return 'A'
    elif percentage_score >= 60:
        return 'B'
    elif percentage_score >= 50:
        return 'C'
    elif percentage_score >= 40:
        return 'D'
    else:
        return 'F'

def display_students():
    """
    Display all student data in a table.
    """
    for item in student_table.get_children():
        student_table.delete(item)

    for student in student_data:
        coursework_total, exam_score, overall_total, percentage_score, grade = compute_totals(student)
        student_table.insert("", "end", values=(student["student_id"], student["student_name"], coursework_total, exam_score, overall_total, f"{percentage_score:.2f}%", grade))

def add_new_student():
    """
    Add a new student's data.
    """
    try:
        student_id = int(id_input.get())  # Student ID
        student_name = name_input.get().strip()  # Student name
        marks = list(map(int, marks_input.get().split(',')))  # Marks (coursework) as list of integers
        exam_score = int(exam_input.get())  # Exam score

        if len(marks) != 3:
            raise ValueError("Coursework marks must consist of exactly 3 values.")  # Validation for marks

        student_data.append({"student_id": student_id, "student_name": student_name, "course_marks": marks, "exam_score": exam_score})
        write_students(STUDENT_FILE_PATH, student_data)  # Save the updated data to file
        display_students()  # Update the table
        reset_inputs()  # Clear input fields
        messagebox.showinfo("Success", "Student successfully added.")
    except ValueError as e:
        messagebox.showerror("Invalid Input", f"Error: {e}")

def remove_student():
    """
    Remove a student from the list.
    """
    selected_item = student_table.selection()  # Get the selected row
    if not selected_item:
        messagebox.showwarning("Selection Required", "Please select a student to delete.")
        return

    student_id_to_delete = int(student_table.item(selected_item[0], "values")[0])  # Get student ID from the selected row
    global student_data
    student_data = [student for student in student_data if student["student_id"] != student_id_to_delete]  # Remove student by ID

    write_students(STUDENT_FILE_PATH, student_data)  # Save updated data to file
    display_students()  # Refresh the table
    messagebox.showinfo("Success", "Student deleted successfully.")

def reset_inputs():
    """
    Clear the input fields for adding a new student.
    """
    id_input.delete(0, tk.END)
    name_input.delete(0, tk.END)
    marks_input.delete(0, tk.END)
    exam_input.delete(0, tk.END)

# Fetch the initial student data from file
student_data = fetch_students(STUDENT_FILE_PATH)

# Initialize the Tkinter window
window = tk.Tk()
window.title("Student Management System")
window.geometry("900x500")

# Layout frames
input_frame = tk.Frame(window, padx=10, pady=10)
input_frame.pack(side=tk.TOP, fill=tk.X)

table_frame = tk.Frame(window, padx=10, pady=10)
table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Input fields for adding new students
tk.Label(input_frame, text="Student ID:").grid(row=0, column=0)
id_input = tk.Entry(input_frame)
id_input.grid(row=0, column=1)

tk.Label(input_frame, text="Name:").grid(row=0, column=2)
name_input = tk.Entry(input_frame)
name_input.grid(row=0, column=3)

tk.Label(input_frame, text="Coursework Marks (3 values, comma-separated):").grid(row=0, column=4)
marks_input = tk.Entry(input_frame)
marks_input.grid(row=0, column=5)

tk.Label(input_frame, text="Exam Score:").grid(row=0, column=6)
exam_input = tk.Entry(input_frame)
exam_input.grid(row=0, column=7)

# Action buttons
add_student_btn = tk.Button(input_frame, text="Add New Student", command=add_new_student)
add_student_btn.grid(row=1, column=0, columnspan=2)

delete_student_btn = tk.Button(input_frame, text="Remove Student", command=remove_student)
delete_student_btn.grid(row=1, column=2, columnspan=2)

view_all_btn = tk.Button(input_frame, text="View All Students", command=display_students)
view_all_btn.grid(row=1, column=4, columnspan=2)

# Table for showing students
columns = ("Student ID", "Name", "Coursework", "Exam Score", "Total", "Percentage", "Grade")
student_table = ttk.Treeview(table_frame, columns=columns, show="headings")
student_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Define column headers and properties
for col in columns:
    student_table.heading(col, text=col)
    student_table.column(col, anchor="center", width=100)

# Add vertical scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=student_table.yview)
student_table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Load initial data into the table
display_students()

# Start the application
window.mainloop()
