
INSERT INTO Departments (department_name) VALUES
('CSE'),
('IT'),
('AI & DS');

-- ===============================
-- 2. Faculty
-- ===============================
-- CSE Faculty (department_id = 1)
INSERT INTO Faculty (first_name, last_name, email, phone, department_id) VALUES
('Anita', 'Sharma', 'anita@example.com', '8888888888', 1),
('Ravi', 'Kumar', 'ravi@example.com', '7777777777', 1);

-- IT Faculty (department_id = 2)
INSERT INTO Faculty (first_name, last_name, email, phone, department_id) VALUES
('Suresh', 'Patel', 'suresh@example.com', '6666666666', 2),
('Priya', 'Singh', 'priya@example.com', '5555555555', 2);

-- AI & DS Faculty (department_id = 3)
INSERT INTO Faculty (first_name, last_name, email, phone, department_id) VALUES
('Raj', 'Verma', 'raj@example.com', '9998887771', 3),
('Neha', 'Sharma', 'neha@example.com', '9998887772', 3);

-- ===============================
-- 3. Courses (5 courses per department)
-- ===============================
-- CSE Courses (department_id = 1)
INSERT INTO Courses (course_name, department_id, faculty_id) VALUES
('Database Systems', 1, 1),
('Computer Networks', 1, 2),
('Operating Systems', 1, 1),
('Software Engineering', 1, 2),
('Data Structures & Algorithms', 1, 1);

-- IT Courses (department_id = 2)
INSERT INTO Courses (course_name, department_id, faculty_id) VALUES
('Web Development', 2, 3),
('Mobile App Development', 2, 4),
('Cloud Computing', 2, 3),
('Information Security', 2, 4),
('Networking Basics', 2, 3);

-- AI & DS Courses (department_id = 3)
INSERT INTO Courses (course_name, department_id, faculty_id) VALUES
('Introduction to AI', 3, 5),
('Machine Learning', 3, 6),
('Deep Learning', 3, 5),
('Data Mining', 3, 6),
('Natural Language Processing', 3, 5);

-- ===============================
-- 4. Students
-- ===============================
INSERT INTO Students (first_name, last_name, dob, email, phone, department_id) VALUES
-- CSE Students (department_id = 1)
('Alice', 'Smith', '2003-05-10', 'alice@example.com', '9999999991', 1),
('Bob', 'Johnson', '2004-08-20', 'bob@example.com', '9999999992', 1),
('Charlie', 'Sharma', '2003-12-15', 'charlie@example.com', '9999999993', 1),
('David', 'Verma', '2003-03-22', 'david@example.com', '9999999994', 1),
('Eve', 'Patel', '2004-07-30', 'eve@example.com', '9999999995', 1),

-- IT Students (department_id = 2)
('Fiona', 'Singh', '2003-02-12', 'fiona@example.com', '9999999996', 2),
('George', 'Kumar', '2004-09-25', 'george@example.com', '9999999997', 2),
('Hannah', 'Sharma', '2003-11-18', 'hannah@example.com', '9999999998', 2),
('Ian', 'Patel', '2003-06-30', 'ian@example.com', '9999999999', 2),
('Jack', 'Verma', '2004-01-05', 'jack@example.com', '9999999988', 2),

-- AI & DS Students (department_id = 3)
('Karen', 'Singh', '2003-04-14', 'karen@example.com', '9999999987', 3),
('Leo', 'Kumar', '2004-12-19', 'leo@example.com', '9999999986', 3),
('Mia', 'Sharma', '2003-08-22', 'mia@example.com', '9999999985', 3),
('Nina', 'Patel', '2003-03-11', 'nina@example.com', '9999999984', 3),
('Oscar', 'Verma', '2004-05-27', 'oscar@example.com', '9999999983', 3);

-- ===============================
-- 5. Admins
-- ===============================
INSERT INTO Admins (admin_name, phone_no, email_id) VALUES
('System Admin', '9999999999', 'admin@example.com');

-- ===============================
-- 6. Users
-- ===============================
-- Admin
INSERT INTO Users (username, password_hash, role, admin_id, faculty_id, student_id) VALUES
('sysadmin', 'admin123', 'admin', 1, NULL, NULL);

-- Faculty Users
INSERT INTO Users (username, password_hash, role, admin_id, faculty_id, student_id) VALUES
('anita', 'anita123', 'faculty', NULL, 1, NULL),
('ravi', 'ravi123', 'faculty', NULL, 2, NULL),
('suresh', 'suresh123', 'faculty', NULL, 3, NULL),
('priya', 'priya123', 'faculty', NULL, 4, NULL),
('raj', 'raj123', 'faculty', NULL, 5, NULL),
('neha', 'neha123', 'faculty', NULL, 6, NULL);

-- Student Users
INSERT INTO Users (username, password_hash, role, admin_id, faculty_id, student_id) VALUES
('alice', 'alice123', 'student', NULL, NULL, 1),
('bob', 'bob123', 'student', NULL, NULL, 2),
('charlie', 'charlie123', 'student', NULL, NULL, 3),
('david', 'david123', 'student', NULL, NULL, 4),
('eve', 'eve123', 'student', NULL, NULL, 5),
('fiona', 'fiona123', 'student', NULL, NULL, 6),
('george', 'george123', 'student', NULL, NULL, 7),
('hannah', 'hannah123', 'student', NULL, NULL, 8),
('ian', 'ian123', 'student', NULL, NULL, 9),
('jack', 'jack123', 'student', NULL, NULL, 10),
('karen', 'karen123', 'student', NULL, NULL, 11),
('leo', 'leo123', 'student', NULL, NULL, 12),
('mia', 'mia123', 'student', NULL, NULL, 13),
('nina', 'nina123', 'student', NULL, NULL, 14),
('oscar', 'oscar123', 'student', NULL, NULL, 15);

-- ===============================
-- 7. Enrollment (sample)
-- ===============================
-- Enrollment for CSE students (students 1-5, courses 1-5)
INSERT INTO Enrollment (student_id, course_id, enrollment_date) VALUES
(1,1,'2025-01-10'),(1,2,'2025-01-11'),(1,3,'2025-01-12'),(1,4,'2025-01-13'),(1,5,'2025-01-14'),
(2,1,'2025-01-10'),(2,2,'2025-01-11'),(2,3,'2025-01-12'),(2,4,'2025-01-13'),(2,5,'2025-01-14'),
(3,1,'2025-01-10'),(3,2,'2025-01-11'),(3,3,'2025-01-12'),(3,4,'2025-01-13'),(3,5,'2025-01-14'),
(4,1,'2025-01-10'),(4,2,'2025-01-11'),(4,3,'2025-01-12'),(4,4,'2025-01-13'),(4,5,'2025-01-14'),
(5,1,'2025-01-10'),(5,2,'2025-01-11'),(5,3,'2025-01-12'),(5,4,'2025-01-13'),(5,5,'2025-01-14');

-- Enrollment for IT students (students 6-10, courses 6-10)
INSERT INTO Enrollment (student_id, course_id, enrollment_date) VALUES
(6,6,'2025-01-10'),(6,7,'2025-01-11'),(6,8,'2025-01-12'),(6,9,'2025-01-13'),(6,10,'2025-01-14'),
(7,6,'2025-01-10'),(7,7,'2025-01-11'),(7,8,'2025-01-12'),(7,9,'2025-01-13'),(7,10,'2025-01-14'),
(8,6,'2025-01-10'),(8,7,'2025-01-11'),(8,8,'2025-01-12'),(8,9,'2025-01-13'),(8,10,'2025-01-14'),
(9,6,'2025-01-10'),(9,7,'2025-01-11'),(9,8,'2025-01-12'),(9,9,'2025-01-13'),(9,10,'2025-01-14'),
(10,6,'2025-01-10'),(10,7,'2025-01-11'),(10,8,'2025-01-12'),(10,9,'2025-01-13'),(10,10,'2025-01-14');

-- Enrollment for AI & DS students (students 11-15, courses 11-15)
INSERT INTO Enrollment (student_id, course_id, enrollment_date) VALUES
(11,11,'2025-01-10'),(11,12,'2025-01-11'),(11,13,'2025-01-12'),(11,14,'2025-01-13'),(11,15,'2025-01-14'),
(12,11,'2025-01-10'),(12,12,'2025-01-11'),(12,13,'2025-01-12'),(12,14,'2025-01-13'),(12,15,'2025-01-14'),
(13,11,'2025-01-10'),(13,12,'2025-01-11'),(13,13,'2025-01-12'),(13,14,'2025-01-13'),(13,15,'2025-01-14'),
(14,11,'2025-01-10'),(14,12,'2025-01-11'),(14,13,'2025-01-12'),(14,14,'2025-01-13'),(14,15,'2025-01-14'),
(15,11,'2025-01-10'),(15,12,'2025-01-11'),(15,13,'2025-01-12'),(15,14,'2025-01-13'),(15,15,'2025-01-14');

-- ===============================
-- 8. Attendance (sample)
-- ===============================
INSERT INTO Attendance (enrollment_id, faculty_id, date, status) VALUES
(1,1,'2025-02-01','Present'),
(2,2,'2025-02-02','Present'),
(3,1,'2025-02-03','Absent'),
(4,2,'2025-02-04','Present'),
(5,1,'2025-02-05','Present'),
(6,3,'2025-02-01','Present'),
(7,4,'2025-02-02','Present'),
(8,3,'2025-02-03','Absent'),
(9,4,'2025-02-04','Present'),
(10,3,'2025-02-05','Present'),
(11,5,'2025-02-01','Present'),
(12,6,'2025-02-02','Present'),
(13,5,'2025-02-03','Absent'),
(14,6,'2025-02-04','Present'),
(15,5,'2025-02-05','Present');


-- ===============================
-- 9. Exams
-- ===============================
INSERT INTO Exams (course_id, exam_date) VALUES
(1,'2025-03-10'),(2,'2025-03-11'),(3,'2025-03-12'),(4,'2025-03-13'),(5,'2025-03-14'),
(6,'2025-03-15'),(7,'2025-03-16'),(8,'2025-03-17'),(9,'2025-03-18'),(10,'2025-03-19'),
(11,'2025-03-20'),(12,'2025-03-21'),(13,'2025-03-22'),(14,'2025-03-23'),(15,'2025-03-24');


-- ===============================
-- 10. StudentExam (sample)
-- ===============================
-- CSE Students (1-5)
INSERT INTO StudentExam (student_id, exam_id, exam_date) VALUES
(1,1,'2025-03-10'),(1,2,'2025-03-11'),(1,3,'2025-03-12'),(1,4,'2025-03-13'),(1,5,'2025-03-14'),
(2,1,'2025-03-10'),(2,2,'2025-03-11'),(2,3,'2025-03-12'),(2,4,'2025-03-13'),(2,5,'2025-03-14'),
(3,1,'2025-03-10'),(3,2,'2025-03-11'),(3,3,'2025-03-12'),(3,4,'2025-03-13'),(3,5,'2025-03-14'),
(4,1,'2025-03-10'),(4,2,'2025-03-11'),(4,3,'2025-03-12'),(4,4,'2025-03-13'),(4,5,'2025-03-14'),
(5,1,'2025-03-10'),(5,2,'2025-03-11'),(5,3,'2025-03-12'),(5,4,'2025-03-13'),(5,5,'2025-03-14');

-- IT Students (6-10)
INSERT INTO StudentExam (student_id, exam_id, exam_date) VALUES
(6,6,'2025-03-15'),(6,7,'2025-03-16'),(6,8,'2025-03-17'),(6,9,'2025-03-18'),(6,10,'2025-03-19'),
(7,6,'2025-03-15'),(7,7,'2025-03-16'),(7,8,'2025-03-17'),(7,9,'2025-03-18'),(7,10,'2025-03-19'),
(8,6,'2025-03-15'),(8,7,'2025-03-16'),(8,8,'2025-03-17'),(8,9,'2025-03-18'),(8,10,'2025-03-19'),
(9,6,'2025-03-15'),(9,7,'2025-03-16'),(9,8,'2025-03-17'),(9,9,'2025-03-18'),(9,10,'2025-03-19'),
(10,6,'2025-03-15'),(10,7,'2025-03-16'),(10,8,'2025-03-17'),(10,9,'2025-03-18'),(10,10,'2025-03-19');

-- AI & DS Students (11-15)
INSERT INTO StudentExam (student_id, exam_id, exam_date) VALUES
(11,11,'2025-03-20'),(11,12,'2025-03-21'),(11,13,'2025-03-22'),(11,14,'2025-03-23'),(11,15,'2025-03-24'),
(12,11,'2025-03-20'),(12,12,'2025-03-21'),(12,13,'2025-03-22'),(12,14,'2025-03-23'),(12,15,'2025-03-24'),
(13,11,'2025-03-20'),(13,12,'2025-03-21'),(13,13,'2025-03-22'),(13,14,'2025-03-23'),(13,15,'2025-03-24'),
(14,11,'2025-03-20'),(14,12,'2025-03-21'),(14,13,'2025-03-22'),(14,14,'2025-03-23'),(14,15,'2025-03-24'),
(15,11,'2025-03-20'),(15,12,'2025-03-21'),(15,13,'2025-03-22'),(15,14,'2025-03-23'),(15,15,'2025-03-24');


-- ===============================
-- 11. Results (sample)
-- ===============================
-- CSE Students
INSERT INTO Results (student_exam_id, marks, grade) VALUES
(1,85,'A'),(2,78,'B'),(3,90,'A+'),(4,88,'A'),(5,92,'A+'),
(6,80,'B'),(7,75,'C'),(8,82,'B'),(9,78,'B'),(10,85,'A'),
(11,88,'A'),(12,91,'A+'),(13,77,'B'),(14,85,'A'),(15,89,'A'),
(16,82,'B'),(17,79,'C'),(18,84,'B'),(19,81,'B'),(20,86,'A'),
(21,87,'A'),(22,83,'B'),(23,90,'A+'),(24,85,'A'),(25,88,'A');

-- IT Students
INSERT INTO Results (student_exam_id, marks, grade) VALUES
(26,78,'B'),(27,82,'B'),(28,79,'C'),(29,85,'A'),(30,88,'A'),
(31,80,'B'),(32,77,'C'),(33,83,'B'),(34,79,'B'),(35,81,'B'),
(36,84,'B'),(37,86,'A'),(38,78,'B'),(39,82,'B'),(40,85,'A'),
(41,88,'A'),(42,90,'A+'),(43,87,'A'),(44,83,'B'),(45,89,'A');

-- AI & DS Students
INSERT INTO Results (student_exam_id, marks, grade) VALUES
(46,85,'A'),(47,82,'B'),(48,88,'A'),(49,90,'A+'),(50,87,'A'),
(51,80,'B'),(52,85,'A'),(53,78,'B'),(54,82,'B'),(55,84,'B'),
(56,86,'A'),(57,88,'A'),(58,90,'A+'),(59,85,'A'),(60,87,'A'),
(61,79,'C'),(62,83,'B'),(63,82,'B'),(64,88,'A'),(65,90,'A+'),
(66,84,'B'),(67,86,'A'),(68,81,'B'),(69,83,'B'),(70,85,'A');


