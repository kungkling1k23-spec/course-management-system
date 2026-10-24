import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-super-secret-key')

# ตั้งค่า Database (รองรับทั้ง PostgreSQL บน Render และ SQLite สำหรับรันเทสบนเครื่อง)
database_url = os.environ.get('DATABASE_URL', 'sqlite:///courses.db')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- Database Models ---
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    enrollments = db.relationship('Enrollment', backref='course_info', lazy=True)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

@login_manager.user_loader
detailload_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('อีเมลนี้ถูกใช้งาน, กรุณาใช้อีเมลอื่น', 'danger')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('อีเมลหรือรหัสผ่านไม่ถูกต้อง', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    all_courses = Course.query.all()
    my_enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    enrolled_course_ids = [e.course_id for e in my_enrollments]
    total_credits = sum(e.course_info.credits for e in my_enrollments)
    
    return render_template('dashboard.html', 
                           courses=all_courses, 
                           enrolled_ids=enrolled_course_ids, 
                           my_enrollments=my_enrollments,
                           total_credits=total_credits)

@app.route('/add/<int:course_id>')
@login_required
def add_course(course_id):
    existing = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if not existing:
        # เช็คหน่วยกิตรวมไม่ให้เกิน 22 หน่วยกิต
        my_enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
        current_credits = sum(e.course_info.credits for e in my_enrollments)
        course_to_add = Course.query.get_or_404(course_id)
        
        if current_credits + course_to_add.credits > 22:
            flash('ไม่สามารถเพิ่มรายวิชาได้ เนื่องจากหน่วยกิตรวมเกิน 22 หน่วยกิต', 'danger')
        else:
            new_enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
            db.session.add(new_enrollment)
            db.session.commit()
            flash('เพิ่มรายวิชาสำเร็จ!', 'success')
            
    return redirect(url_for('dashboard'))

@app.route('/drop/<int:course_id>')
@login_required
def drop_course(course_id):
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        flash('ถอนรายวิชาสำเร็จ', 'info')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ฟังก์ชันสร้างข้อมูลจำลองรายวิชาครั้งแรก (ถ้าฐานข้อมูลยังว่าง)
def init_db():
    with app.app_context():
        db.create_all()
        if Course.query.count() == 0:
            sample_courses = [
                Course(code="CS101", name="Introduction to Computer Science", credits=3, capacity=50),
                Course(code="MATH201", name="Calculus for Engineers", credits=4, capacity=40),
                Course(code="GEN111", name="Digital Literacy and Modern Life", credits=2, capacity=100),
                Course(code="ENG102", name="English for Academic Purposes", credits=3, capacity=60),
                Course(code="PHYS101", name="General Physics I", credits=4, capacity=45)
            ]
            db.session.bulk_save_objects(sample_courses)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
