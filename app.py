from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='password123',
        database='students'
    )

# Function to create database table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students
                     (id INT AUTO_INCREMENT PRIMARY KEY,
                     name VARCHAR(255),
                     email VARCHAR(255),
                     phone VARCHAR(20))''')
    conn.commit()
    conn.close()

create_table()

# Home route to display all students
@app.route('/')
def home():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Route to add a new student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('add.html')

# Update a student
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    conn = connect_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        if name and email and phone:
            cursor.execute("UPDATE students SET name=%s, email=%s, phone=%s WHERE id=%s", (name, email, phone, id))
            conn.commit()
            
            conn.close()
            print( 'Student updated successfully', 'success')
            return redirect(url_for('home'))
        else:
            print( 'All fields are required', 'danger')
    else:
        cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
        student = cursor.fetchone()
        conn.close()
        return render_template('edit.html', student=student)
    

# Delete a student
@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    print('Student deleted successfully', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
