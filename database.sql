-- Create Database
CREATE DATABASE StudentData;
USE StudentData;

-- Departments
CREATE TABLE Departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

-- Students
CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    dob DATE,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

-- Admins
CREATE TABLE Admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    admin_name VARCHAR(100),
    phone_no VARCHAR(50) NOT NULL,
    email_id VARCHAR(100) NOT NULL,
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Faculty
CREATE TABLE Faculty (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

-- Courses
CREATE TABLE Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    department_id INT,
    faculty_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id)
);

-- Enrollment
CREATE TABLE Enrollment (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Attendance
CREATE TABLE Attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_id INT,
    faculty_id INT, -- who marked attendance
    date DATE,
    status ENUM('Present','Absent') NOT NULL,
    FOREIGN KEY (enrollment_id) REFERENCES Enrollment(enrollment_id),
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id)
);

-- Exams
CREATE TABLE Exams (
    exam_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT,
    exam_date DATE NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- StudentExam
CREATE TABLE StudentExam (
    student_exam_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    exam_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (exam_id) REFERENCES Exams(exam_id)
);

-- Results
CREATE TABLE Results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    student_exam_id INT NOT NULL,
    marks INT,
    grade VARCHAR(5),
    FOREIGN KEY (student_exam_id) REFERENCES StudentExam(student_exam_id)
);
use collgedatabase;
-- Users
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin','faculty','student') NOT NULL,
    admin_id INT,
    faculty_id INT,
    student_id INT,
    FOREIGN KEY (admin_id) REFERENCES Admins(admin_id),
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);
