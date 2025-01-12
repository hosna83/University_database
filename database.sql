CREATE TABLE "User" (
    "user_id" SERIAL PRIMARY KEY,
    "first_name" VARCHAR(50) NOT NULL,
    "last_name" VARCHAR(50) NOT NULL,
    "guardian_name" VARCHAR(50),
    "primary_phone" VARCHAR(10) UNIQUE NOT NULL CHECK (primary_phone ~ '^[0-9]{10}$'),
    "secondary_phone" VARCHAR(10) CHECK (secondary_phone ~ '^[0-9]{10}$'),
    "address" TEXT NOT NULL,
    "date_of_birth" DATE NOT NULL CHECK (date_of_birth < CURRENT_DATE),
    "gender" CHAR(1) NOT NULL,
    "start_date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "Faculty" (
    "faculty_id" SERIAL PRIMARY KEY,
    "name" VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE "Department" (
    "department_id" SERIAL PRIMARY KEY,
    "faculty_id" INTEGER NOT NULL REFERENCES "Faculty" (faculty_id) ON DELETE CASCADE,
    "name" VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE "Student" (
    "student_id" SERIAL PRIMARY KEY,
    "user_id" INTEGER NOT NULL UNIQUE REFERENCES "User" (user_id) ON DELETE CASCADE,
    "department_id" INTEGER NOT NULL REFERENCES "Department" (department_id) ON DELETE SET NULL,
    "degree_status" VARCHAR(15) NOT NULL,
    "status" VARCHAR(15) NOT NULL
);

CREATE TABLE "Lesson" (
    "lesson_id" SERIAL PRIMARY KEY,
    "department_id" INTEGER NOT NULL REFERENCES "Department" (department_id) ON DELETE SET NULL,
    "type" VARCHAR(50) NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "credits" INTEGER NOT NULL CHECK (credits > 0)
);

CREATE TABLE "Professor" (
    "professor_id" SERIAL PRIMARY KEY,
    "user_id" INTEGER NOT NULL UNIQUE REFERENCES "User" (user_id) ON DELETE CASCADE,
    "department_id" INTEGER NOT NULL REFERENCES "Department" (department_id) ON DELETE SET NULL,
    "room_number" VARCHAR(10),
    "academic_rank" VARCHAR(50) NOT NULL
);

CREATE TABLE "Semester" (
    "semester_id" SERIAL PRIMARY KEY,
    "start_date" DATE NOT NULL CHECK (start_date < end_date),
    "end_date" DATE NOT NULL,
    "type" VARCHAR(10) NOT NULL
);

CREATE TABLE "Course" (
    "course_id" SERIAL PRIMARY KEY,
    "semester_id" INTEGER NOT NULL REFERENCES "Semester" (semester_id) ON DELETE CASCADE,
    "lesson_id" INTEGER NOT NULL REFERENCES "Lesson" (lesson_id) ON DELETE CASCADE,
    "exam_date" TIMESTAMP CHECK (exam_date IS NULL OR exam_date > CURRENT_TIMESTAMP),
    "class" VARCHAR(50) NOT NULL,
    "maximum_capacity" INTEGER NOT NULL CHECK (maximum_capacity > 0),
    "class_date" DATE NOT NULL,
    "class_time" TIME NOT NULL
);

CREATE TABLE "Enrollment" (
    "student_id" INTEGER NOT NULL REFERENCES "Student" (student_id) ON DELETE CASCADE,
    "course_id" INTEGER NOT NULL REFERENCES "Course" (course_id) ON DELETE CASCADE,
    "final_grade" FLOAT CHECK (final_grade >= 0 AND final_grade <= 20),
    PRIMARY KEY ("student_id", "course_id")
);

CREATE TABLE "Specialized" (
    "department_id" INTEGER NOT NULL REFERENCES "Department" (department_id) ON DELETE CASCADE,
    "course_id" INTEGER NOT NULL REFERENCES "Course" (course_id) ON DELETE CASCADE,
    PRIMARY KEY ("department_id", "course_id")
);

CREATE TABLE "Requirement" (
    "dependent_lesson_id" INTEGER NOT NULL REFERENCES "Lesson" (lesson_id) ON DELETE CASCADE,
    "independent_lesson_id" INTEGER NOT NULL REFERENCES "Lesson" (lesson_id) ON DELETE CASCADE,
    "lesson_dependency" VARCHAR(255),
    PRIMARY KEY ("dependent_lesson_id", "independent_lesson_id")
);

CREATE TABLE "Advisement" (
    "course_id" INTEGER NOT NULL REFERENCES "Course" (course_id) ON DELETE CASCADE,
    "professor_id" INTEGER NOT NULL REFERENCES "Professor" (professor_id) ON DELETE CASCADE,
    PRIMARY KEY ("course_id", "professor_id")
);
