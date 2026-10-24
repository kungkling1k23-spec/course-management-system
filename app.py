import os
import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ.get('DATABASE_URL', 'ใส่ลิงก์เชื่อมต่อ PostgreSQL ของคุณที่นี่')

def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key-for-dev')

DATABASE = 'course_app.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        # ตารางผู้ใช้งาน
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # ตารางรายวิชา
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                credits INTEGER NOT NULL,
                instructor TEXT,
                semester TEXT,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()

# สร้าง Table เมื่อแอปเริ่มทำงาน
init_db()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    
    # ดึงรายวิชาของผู้ใช้ที่ล็อกอินอยู่
    cursor.execute('SELECT * FROM courses WHERE user_id = ? ORDER BY id DESC', (user_id,))
    courses = cursor.fetchall()
    
    # คำนวณสถิติ
    total_courses = len(courses)
    total_credits = sum(c['credits'] for c in courses)
    required_count = sum(1 for c in courses if c['category'] == 'วิชาบังคับ')
    elective_count = sum(1 for c in courses if c['category'] == 'วิชาเลือก')
    
    return render_template(
        'dashboard.html', 
        courses=courses, 
        stats={
            'total': total_courses,
            'credits': total_credits,
            'required': required_count,
            'elective': elective_count
        }
    )

# --- Authenication Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['fullname'] = user['fullname']
            flash('เข้าสู่ระบบสำเร็จ', 'success')
            return redirect(url_for('index'))
        else:
            flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname'].strip()
        username = request.form['username'].strip()
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (fullname, username, password) VALUES (?, ?, ?)',
                (fullname, username, hashed_password)
            )
            conn.commit()
            flash('สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('ชื่อผู้ใช้งานนี้ถูกใช้ไปแล้ว', 'danger')
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('ออกจากระบบเรียบร้อยแล้ว', 'info')
    return redirect(url_for('login'))

# --- Course CRUD Routes ---

@app.route('/course/add', methods=['POST'])
def add_course():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        user_id = session['user_id']
        course_code = request.form.get('course_code', '').strip()
        course_name = request.form.get('course_name', '').strip()
        category = request.form.get('category', '').strip()
        institution = request.form.get('institution', '').strip()
        online_lesson = request.form.get('online_lesson', '').strip()
        
        # ป้องกันกรณีช่องตัวเลขเป็นค่าว่างแล้วแปลง int ไม่ผ่าน
        hours_raw = request.form.get('hours', '0')
        hours = int(hours_raw) if hours_raw.isdigit() else 0
        
        credits_raw = request.form.get('credits', '3')
        credits = int(credits_raw) if credits_raw.isdigit() else 3
        
        conn = get_db()
        cursor = conn.cursor()
        
        # บันทึกข้อมูลลงตาราง course
        cursor.execute('''
            INSERT INTO course (user_id, course_code, course_name, category, institution, online_lesson, hours, credits)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (user_id, course_code, course_name, category, institution, online_lesson, hours, credits))
        
        conn.commit()
        conn.close()
        
        flash('เพิ่มรายวิชาสำเร็จ', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        # หากเกิดข้อผิดพลาด ระบบจะแสดง Error ออกมาทางหน้าจอเว็บชั่วคราวเพื่อให้เราอ่านเจอ
        return f"เกิดข้อผิดพลาด (Error): {str(e)}"

@app.route('/course/edit/<int:course_id>', methods=['POST'])
def edit_course(course_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    code = request.form['code'].strip()
    name = request.form['name'].strip()
    category = request.form['category']
    credits = int(request.form['credits'])
    instructor = request.form.get('instructor', '').strip()
    semester = request.form.get('semester', '').strip()
    description = request.form.get('description', '').strip()
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE courses 
        SET code=?, name=?, category=?, credits=?, instructor=?, semester=?, description=?
        WHERE id=? AND user_id=?
    ''', (code, name, category, credits, instructor, semester, description, course_id, session['user_id']))
    conn.commit()
    
    flash('แก้ไขข้อมูลวิชาเรียบร้อยแล้ว', 'success')
    return redirect(url_for('index'))

@app.route('/course/delete/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM courses WHERE id=? AND user_id=?', (course_id, session['user_id']))
    conn.commit()
    
    flash('ลบรายวิชาเรียบร้อยแล้ว', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
