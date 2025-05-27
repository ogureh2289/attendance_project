import sqlite3

DB_NAME = 'school.db'


def connect():
    conn = sqlite3.connect(DB_NAME)
    return conn


def init_db():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        '''
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        class TEXT NOT NULL,
        email TEXT NOT NULL,
        qr_token TEXT UNIQUE NOT NULL 
    )
    '''
    )
    cursor.execute(
        '''
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_name TEXT NOT NULL,
        lesson_date TEXT NOT NULL,
        class TEXT NOT NULL,
        student_id INTEGER NOT NULL,
        lesson_start TEXT NOT NULL,
        arrival_time TEXT,
        status TEXT CHECK(status IN('присутствовал','отсутствовал','опоздал')),
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
    '''
    )
    conn.commit()
    conn.close()


def add_student(full_name, student_class, email, qr_token):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (full_name, class, email, qr_token)
        VALUES (?, ?, ?, ?)
        ''', (full_name, student_class, email, qr_token))
    conn.commit()
    conn.close()


def record_attendance(lesson_name, lesson_date, student_id, student_class, lesson_start, arrival_time, status):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO attendance (lesson_name, lesson_date, student_id, class, lesson_start, arrival_time, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
         ''', (lesson_name, lesson_date, student_id, student_class, lesson_start, arrival_time, status))
    conn.commit()
    conn.close()


def get_student_by_token(qr_token):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, full_name, class FROM students WHERE qr_token = ?
    ''', (qr_token,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_attendance(date, student_class):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
            SELECT 
                a.id, 
                s.full_name, 
                a.class, 
                a.lesson_name, 
                a.lesson_date, 
                a.lesson_start, 
                a.arrival_time, 
                a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            WHERE a.lesson_date = ? AND a.class = ?
        ''', (date, student_class))
    result = cursor.fetchall()
    conn.close()
    return result

def get_all_students_by_class(s_class):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, class, qr_token FROM students WHERE class = ?", (s_class,))
    students = cursor.fetchall()
    conn.close()
    return students

