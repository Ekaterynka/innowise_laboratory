-- 1. Create tables
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    full_name TEXT,
    birth_year INTEGER
);

CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    subject TEXT,
    grade INTEGER
);

-- 2. Insert data
INSERT INTO students (full_name, birth_year) VALUES
('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

INSERT INTO grades (student_id, subject, grade) VALUES
(1, 'Math', 88),
(1, 'English', 92),
(1, 'Science', 85),
(2, 'Math', 75),
(2, 'History', 83),
(2, 'English', 79),
(3, 'Science', 95),
(3, 'Math', 91),
(3, 'Art', 89),
(4, 'Math', 84),
(4, 'Science', 88),
(4, 'Physical Education', 93),
(5, 'English', 90),
(5, 'History', 85),
(5, 'Math', 88),
(6, 'Science', 72),
(6, 'Math', 78),
(6, 'English', 81),
(7, 'Art', 94),
(7, 'Science', 87),
(7, 'Math', 90),
(8, 'History', 77),
(8, 'Math', 83),
(8, 'Science', 80),
(9, 'English', 96),
(9, 'Math', 89),
(9, 'Art', 92);

-- 3. Find all grades for a specific student (Alice Johnson)
SELECT subject, grade FROM grades 
WHERE student_id = (SELECT id FROM students WHERE full_name = 'Alice Johnson');

-- 4. Calculate the average grade per student
SELECT s.full_name, AVG(g.grade) as average_grade 
FROM students s 
JOIN grades g ON s.id = g.student_id 
GROUP BY s.id;

-- 5. List all students born after 2004
SELECT full_name, birth_year FROM students 
WHERE birth_year > 2004;

-- 6. Create a query that lists all subjects and their average grades
SELECT subject, AVG(grade) as average_grade 
FROM grades 
GROUP BY subject;

-- 7. Find the top 3 students with the highest average grades
SELECT s.full_name, AVG(g.grade) as average_grade 
FROM students s 
JOIN grades g ON s.id = g.student_id 
GROUP BY s.id 
ORDER BY average_grade DESC 
LIMIT 3;

-- 8. Show all students who have scored below 80 in any subject
SELECT DISTINCT s.full_name 
FROM students s 
JOIN grades g ON s.id = g.student_id 
WHERE g.grade < 80;

-- create indexes to optimize these queries. Feel free to do so.
CREATE INDEX idx_grades_student_id ON grades(student_id);
CREATE INDEX idx_students_birth_year ON students(birth_year);