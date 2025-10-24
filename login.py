from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime, timedelta, date

app = Flask(__name__)
# IMPORTANT: Use a strong, unique secret key for production
app.secret_key = "your_secret_key" 

# ==========================
# DATABASE CONNECTION
# ==========================
# Make sure these credentials match your MySQL setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shaqeeq@123",
    database="collgeDatabase",
    auth_plugin="mysql_native_password"
)

# Helper function to check role
def is_faculty(faculty_id):
    """Checks if the current session user is the specified faculty member."""
    return 'role' in session and session['role'] == 'faculty' and session.get('faculty_id') == faculty_id

def is_admin():
    """Checks if the current session user is an admin."""
    return 'role' in session and session['role'] == 'admin'

# ==========================
# ADMIN DASHBOARD (Handles all POST/GET requests for Admin UI)
# ==========================
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if not is_admin():
        flash("Access Denied or Session Expired.", "danger")
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Departments")
    departments = cursor.fetchall()

    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        try:
            if form_type == 'add_student':
                # --- ADD STUDENT LOGIC ---
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                dob = request.form['dob']
                email = request.form['email']
                phone = request.form['phone']
                department_id = request.form['department_id']
                username = request.form['username']
                password = request.form['password']

                # 1. Insert student
                cursor.execute("""
                    INSERT INTO Students (first_name, last_name, dob, email, phone, department_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (first_name, last_name, dob, email, phone, department_id))
                db.commit()
                new_student_id = cursor.lastrowid

                # 2. Create login for student
                cursor.execute("""
                    INSERT INTO Users (username, password_hash, role, student_id)
                    VALUES (%s, %s, 'student', %s)
                """, (username, password, new_student_id))
                db.commit()

                # 3. Enroll in department courses + assign exams automatically
                cursor.execute("SELECT course_id FROM Courses WHERE department_id=%s", (department_id,))
                courses_in_dept = cursor.fetchall()
                enrollment_date = datetime.now().strftime('%Y-%m-%d')

                for course in courses_in_dept:
                    # Enrollment
                    cursor.execute("INSERT INTO Enrollment (student_id, course_id, enrollment_date) VALUES (%s,%s,%s)",
                                   (new_student_id, course['course_id'], enrollment_date))
                    # Exam setup (re-using existing course exams or creating default)
                    cursor.execute("SELECT exam_id, exam_date FROM Exams WHERE course_id=%s LIMIT 1", (course['course_id'],))
                    exam = cursor.fetchone()
                    
                    if not exam:
                        exam_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
                        cursor.execute("INSERT INTO Exams (course_id, exam_date) VALUES (%s, %s)", (course['course_id'], exam_date))
                        db.commit()
                        exam_id = cursor.lastrowid
                        exam_date_val = exam_date
                    else:
                        exam_id = exam['exam_id']
                        # Handle date object conversion if necessary
                        exam_date_val = exam['exam_date'].isoformat() if isinstance(exam['exam_date'], date) else exam['exam_date']
                    
                    cursor.execute("INSERT INTO StudentExam (student_id, exam_id, exam_date) VALUES (%s, %s, %s)",
                                   (new_student_id, exam_id, exam_date_val))
                db.commit()
                flash("Student added successfully with courses and exams!", "success")
                
            elif form_type == 'add_faculty':
                # --- ADD FACULTY LOGIC ---
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                email = request.form['email']
                phone = request.form['phone']
                department_id = request.form['department_id']
                username = request.form['username']
                password = request.form['password']

                # 1. Insert faculty
                cursor.execute("""
                    INSERT INTO Faculty (first_name, last_name, email, phone, department_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (first_name, last_name, email, phone, department_id))
                db.commit()
                new_faculty_id = cursor.lastrowid

                # 2. Create login for faculty
                cursor.execute("""
                    INSERT INTO Users (username, password_hash, role, faculty_id)
                    VALUES (%s, %s, 'faculty', %s)
                """, (username, password, new_faculty_id))
                db.commit()

                flash("Faculty member added successfully!", "success")

            elif form_type == 'add_course':
                # --- ADD COURSE LOGIC ---
                course_name = request.form['course_name']
                department_id = request.form['department_id']
                faculty_id_raw = request.form['faculty_id']
                
                # Handle 'NULL' selection
                faculty_id = None if faculty_id_raw == 'NULL' else faculty_id_raw

                # Insert the new course
                cursor.execute("""
                    INSERT INTO Courses (course_name, department_id, faculty_id)
                    VALUES (%s, %s, %s)
                """, (course_name, department_id, faculty_id))
                db.commit()

                flash(f"Course '{course_name}' added and assigned!", "success")
            
            elif form_type == 'edit_course':
                # --- EDIT COURSE ASSIGNMENT LOGIC ---
                course_id = request.form['course_id']
                faculty_id_raw = request.form['faculty_id']
                
                # Convert 'NULL' string from form back to None for MySQL
                faculty_id = None if faculty_id_raw == 'NULL' else faculty_id_raw

                cursor.execute("""
                    UPDATE Courses SET faculty_id = %s WHERE course_id = %s
                """, (faculty_id, course_id))
                db.commit()
                
                flash(f"Course ID {course_id} faculty assignment updated successfully!", "success")

            else:
                flash("Invalid form submission.", "danger")

        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error during operation: {err}")
            flash("Error: Could not process request. Check database constraints/uniqueness.", "danger")

    # --- Fetch Data for GET/POST completion ---
    
    # Students
    cursor.execute("""
        SELECT s.student_id, s.first_name, s.last_name, s.email, s.phone, d.department_name
        FROM Students s
        JOIN Departments d ON s.department_id = d.department_id
    """)
    students = cursor.fetchall()
    
    # Faculty
    cursor.execute("""
        SELECT f.faculty_id, f.first_name, f.last_name, f.email, f.phone, d.department_name
        FROM Faculty f
        JOIN Departments d ON f.department_id = d.department_id
    """)
    faculty = cursor.fetchall()

    # Courses (Includes department_id and faculty_id for the EDIT form)
    cursor.execute("""
        SELECT 
            c.course_id, 
            c.course_name, 
            c.department_id,  
            c.faculty_id,     
            d.department_name, 
            CONCAT(f.first_name, ' ', f.last_name) AS faculty_name
        FROM Courses c
        JOIN Departments d ON c.department_id = d.department_id
        LEFT JOIN Faculty f ON c.faculty_id = f.faculty_id
        ORDER BY c.department_id, c.course_name
    """)
    courses = cursor.fetchall()
    
    cursor.close()

    return render_template('admin_dashboard.html', 
                            students=students, 
                            faculty=faculty, 
                            courses=courses,
                            departments=departments)

# ==========================
# DELETE ROUTES (Unchanged)
# ==========================
@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    if not is_admin():
        flash("Access Denied or Session Expired.", "danger")
        return redirect(url_for('login'))

    cursor = db.cursor()
    try:
        # Delete related records due to foreign key constraints
        cursor.execute("DELETE r FROM Results r JOIN StudentExam se ON r.student_exam_id = se.student_exam_id WHERE se.student_id = %s", (student_id,))
        cursor.execute("DELETE FROM StudentExam WHERE student_id = %s", (student_id,))
        cursor.execute("DELETE a FROM Attendance a JOIN Enrollment e ON a.enrollment_id = e.enrollment_id WHERE e.student_id = %s", (student_id,))
        cursor.execute("DELETE FROM Enrollment WHERE student_id = %s", (student_id,))
        cursor.execute("DELETE FROM Users WHERE student_id = %s", (student_id,))
        cursor.execute("DELETE FROM Students WHERE student_id = %s", (student_id,))
        db.commit()
        flash(f"Student ID {student_id} and all related records deleted successfully!", "success")
    except mysql.connector.Error as err:
        db.rollback()
        flash("An error occurred during deletion. Please check database constraints.", "danger")
    finally:
        cursor.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_faculty/<int:faculty_id>', methods=['POST'])
def delete_faculty(faculty_id):
    if not is_admin():
        flash("Access Denied or Session Expired.", "danger")
        return redirect(url_for('login'))

    cursor = db.cursor()
    try:
        # 1. Update Courses taught by this faculty to NULL
        cursor.execute("UPDATE Courses SET faculty_id = NULL WHERE faculty_id = %s", (faculty_id,))
        # 2. Delete User account
        cursor.execute("DELETE FROM Users WHERE faculty_id = %s", (faculty_id,))
        # 3. Delete Faculty record
        cursor.execute("DELETE FROM Faculty WHERE faculty_id = %s", (faculty_id,))
        db.commit()
        flash(f"Faculty ID {faculty_id} and their user account deleted successfully. Associated courses are unassigned.", "success")
    except mysql.connector.Error as err:
        db.rollback()
        flash("An error occurred during faculty deletion.", "danger")
    finally:
        cursor.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    if not is_admin():
        flash("Access Denied or Session Expired.", "danger")
        return redirect(url_for('login'))

    cursor = db.cursor()
    try:
        # Complex deletion: Results -> StudentExam -> Exams/Attendance -> Enrollment -> Courses
        cursor.execute("SELECT enrollment_id FROM Enrollment WHERE course_id = %s", (course_id,))
        enrollment_ids = [row[0] for row in cursor.fetchall()]
        if enrollment_ids:
            enrollment_placeholders = ', '.join(['%s'] * len(enrollment_ids))
            cursor.execute(f"DELETE FROM Attendance WHERE enrollment_id IN ({enrollment_placeholders})", tuple(enrollment_ids))

        cursor.execute("SELECT exam_id FROM Exams WHERE course_id = %s", (course_id,))
        exam_ids = [row[0] for row in cursor.fetchall()]
        if exam_ids:
            exam_placeholders = ', '.join(['%s'] * len(exam_ids))
            
            cursor.execute(f"""
                DELETE r FROM Results r
                JOIN StudentExam se ON r.student_exam_id = se.student_exam_id
                WHERE se.exam_id IN ({exam_placeholders})
            """, tuple(exam_ids))
            
            cursor.execute(f"DELETE FROM StudentExam WHERE exam_id IN ({exam_placeholders})", tuple(exam_ids))
            cursor.execute(f"DELETE FROM Exams WHERE exam_id IN ({exam_placeholders})", tuple(exam_ids))

        cursor.execute("DELETE FROM Enrollment WHERE course_id = %s", (course_id,))
        cursor.execute("DELETE FROM Courses WHERE course_id = %s", (course_id,))

        db.commit()
        flash(f"Course ID {course_id} and all related records deleted successfully!", "success")
    except mysql.connector.Error as err:
        db.rollback()
        flash("An error occurred during course deletion.", "danger")
    finally:
        cursor.close()
    return redirect(url_for('admin_dashboard'))


# ==========================
# LOGIN, STUDENT, FACULTY, LOGOUT routes (FULL IMPLEMENTATION)
# ==========================
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        # NOTE: Using plain text password here, recommend hashing in production
        cursor.execute("SELECT * FROM Users WHERE username=%s AND password_hash=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user_id'] = user['user_id']
            session['role'] = user['role']

            if user['role'] == 'student':
                session['student_id'] = user['student_id']
                return redirect(url_for('student_dashboard'))
            elif user['role'] == 'faculty':
                session['faculty_id'] = user['faculty_id']
                return redirect(url_for('faculty_dashboard', faculty_id=user['faculty_id']))
            elif user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('login'))
    
    return render_template('login.html') 

@app.route('/student')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    student_id = session['student_id']
    cursor = db.cursor(dictionary=True)

    # Fetching student details
    cursor.execute("""
        SELECT s.student_id, s.first_name, s.last_name, s.dob, s.email, s.phone, d.department_name
        FROM Students s JOIN Departments d ON s.department_id = d.department_id WHERE s.student_id = %s
    """, (student_id,))
    student = cursor.fetchone()

    # Fetching courses and enrollment IDs for attendance calculation
    cursor.execute("""
        SELECT e.enrollment_id, c.course_name, c.course_id, 
               COALESCE(f.first_name, 'N/A') AS faculty_first, 
               COALESCE(f.last_name, 'N/A') AS faculty_last
        FROM Enrollment e 
        JOIN Courses c ON e.course_id = c.course_id 
        LEFT JOIN Faculty f ON c.faculty_id = f.faculty_id 
        WHERE e.student_id = %s
    """, (student_id,))
    courses = cursor.fetchall()

    # --- ATTENDANCE CHART LOGIC: Calculate and attach percentage to each course ---
    for course in courses:
        # Get attendance counts for this specific enrollment
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS present_count,
                COUNT(attendance_id) AS total_count
            FROM Attendance 
            WHERE enrollment_id = %s
        """, (course['enrollment_id'],))
        
        attendance_counts = cursor.fetchone()
        
        present_count = attendance_counts['present_count'] or 0
        total_count = attendance_counts['total_count'] or 0
        
        if total_count > 0:
            # Calculate percentage and round to one decimal place
            percentage = round((present_count / total_count) * 100, 1)
        else:
            percentage = 0
            
        # Attach the calculated percentage to the course dictionary
        course['attendance_percentage'] = percentage

    # Fetching exams
    cursor.execute("""
        SELECT c.course_name, COALESCE(se.exam_date, ex.exam_date) AS exam_date
        FROM StudentExam se JOIN Exams ex ON se.exam_id = ex.exam_id
        JOIN Courses c ON ex.course_id = c.course_id WHERE se.student_id = %s
    """, (student_id,))
    exams = cursor.fetchall()

    # Fetching attendance
    cursor.execute("""
        SELECT c.course_name, a.date, a.status, 
               COALESCE(f.first_name, 'N/A') AS faculty_first, 
               COALESCE(f.last_name, 'N/A') AS faculty_last
        FROM Enrollment e 
        JOIN Courses c ON e.course_id = c.course_id 
        LEFT JOIN Attendance a ON a.enrollment_id = e.enrollment_id
        LEFT JOIN Faculty f ON a.faculty_id = f.faculty_id 
        WHERE e.student_id = %s
        ORDER BY a.date DESC
    """, (student_id,))
    attendance = cursor.fetchall()

    # Fetching results
    cursor.execute("""
        SELECT c.course_name, r.marks, r.grade
        FROM StudentExam se 
        JOIN Exams ex ON se.exam_id = ex.exam_id
        JOIN Courses c ON ex.course_id = c.course_id
        LEFT JOIN Results r ON se.student_exam_id = r.student_exam_id 
        WHERE se.student_id = %s
    """, (student_id,))
    results = cursor.fetchall()

    cursor.close()
    return render_template("student_dashboard.html", student=student, courses=courses, exams=exams, attendance=attendance, results=results)

@app.route('/faculty/<int:faculty_id>', methods=['GET', 'POST'])
def faculty_dashboard(faculty_id):
    if not is_faculty(faculty_id):
        flash("Access Denied or Session Expired.", "danger")
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    
    # 1. Handle POST Requests for Attendance/Grading
    if request.method == 'POST':
        action = request.form.get('action')

        try:
            if action == 'mark_attendance':
                course_id = request.form['course_id']
                attendance_date = request.form['attendance_date']
                
                # Check if attendance is already marked for this date/course/faculty
                cursor.execute("""
                    SELECT a.attendance_id
                    FROM Attendance a
                    JOIN Enrollment e ON a.enrollment_id = e.enrollment_id
                    WHERE e.course_id = %s AND a.date = %s AND a.faculty_id = %s
                    LIMIT 1
                """, (course_id, attendance_date, faculty_id))
                
                if cursor.fetchone():
                    flash(f"Attendance for Course ID {course_id} on {attendance_date} has already been marked by you.", "warning")
                    return redirect(url_for('faculty_dashboard', faculty_id=faculty_id))
                
                # Insert attendance records
                for key, value in request.form.items():
                    # FIX: The key is now expected to be 'status_enrollment_<enrollment_id>'
                    if key.startswith('status_enrollment_'):
                        # Extract the enrollment_id from the key
                        enrollment_id = key.split('_')[-1]
                        status = value # 'Present' or 'Absent' from the select value
                        
                        cursor.execute("""
                            INSERT INTO Attendance (enrollment_id, faculty_id, date, status)
                            VALUES (%s, %s, %s, %s)
                        """, (enrollment_id, faculty_id, attendance_date, status))
                
                db.commit()
                flash("Attendance successfully recorded!", "success")

            elif action == 'record_grade':
                student_exam_id = request.form['student_exam_id']
                # Convert marks to integer for safe DB insertion
                marks = int(request.form['marks'])
                grade = request.form['grade']

                # Update or Insert result
                cursor.execute("SELECT result_id FROM Results WHERE student_exam_id = %s", (student_exam_id,))
                if cursor.fetchone():
                    cursor.execute("UPDATE Results SET marks = %s, grade = %s WHERE student_exam_id = %s", (marks, grade, student_exam_id))
                    flash("Grade updated successfully!", "success")
                else:
                    cursor.execute("INSERT INTO Results (student_exam_id, marks, grade) VALUES (%s, %s, %s)", (student_exam_id, marks, grade))
                    flash("Grade recorded successfully!", "success")
                
                db.commit()

        except mysql.connector.Error as err:
            db.rollback()
            flash(f"An error occurred while processing the request: {err}", "danger")
        except ValueError:
            db.rollback()
            flash("Error: Marks must be a valid number.", "danger")
        
        return redirect(url_for('faculty_dashboard', faculty_id=faculty_id))
    

    # 2. Fetch Data for Display (GET Request)
    
    # Faculty Details
    cursor.execute("""
        SELECT f.first_name, f.last_name, f.email, f.phone, d.department_name
        FROM Faculty f JOIN Departments d ON f.department_id = d.department_id WHERE f.faculty_id = %s
    """, (faculty_id,))
    faculty = cursor.fetchone()

    # Courses taught by this faculty
    cursor.execute("SELECT course_id, course_name FROM Courses WHERE faculty_id = %s", (faculty_id,))
    courses = cursor.fetchall()
    
    course_data = []

    for course in courses:
        course_id = course['course_id']
        
        # Enrolled Students (for attendance and grading forms)
        # IMPORTANT: Select enrollment_id here for attendance submission
        cursor.execute("""
            SELECT e.enrollment_id, s.student_id, s.first_name, s.last_name, s.email
            FROM Enrollment e JOIN Students s ON e.student_id = s.student_id WHERE e.course_id = %s
        """, (course_id,))
        students = cursor.fetchall()
        
        # Grades/Exams
        cursor.execute("""
            SELECT 
                se.student_exam_id, s.first_name, s.last_name, ex.exam_date,  
                COALESCE(r.marks, 'N/A') AS marks,
                COALESCE(r.grade, 'N/A') AS grade
            FROM Exams ex 
            JOIN StudentExam se ON ex.exam_id = se.exam_id
            JOIN Students s ON se.student_id = s.student_id
            LEFT JOIN Results r ON se.student_exam_id = r.student_exam_id
            WHERE ex.course_id = %s
        """, (course_id,))
        grades = cursor.fetchall()

        course_data.append({
            'course_id': course_id,
            'course_name': course['course_name'],
            'students': students,
            'grades': grades
        })

    cursor.close()
    return render_template('faculty_dashboard.html', 
                            faculty=faculty, 
                            course_data=course_data, 
                            current_date=date.today().isoformat())


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)