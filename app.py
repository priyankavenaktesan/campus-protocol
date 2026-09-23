from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

import sqlite3
import os
import re
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.secret_key = "college-placement-secret-key"

DATABASE = "database.db"

UPLOAD_FOLDER = os.path.join(
    "static",
    "uploads"
)

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}

MAX_FILE_SIZE = 5 * 1024 * 1024

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# =========================================================
# TEXT / SKILL HELPERS
# =========================================================

def normalize_text(text):
    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9+#.\- ]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def normalize_skills(text):
    if not text:
        return []

    if isinstance(text, list):
        skills = text
    else:
        skills = re.split(
            r"[,;\n|]+",
            str(text)
        )

    result = []

    for skill in skills:
        skill = normalize_text(skill)

        if skill and skill not in result:
            result.append(skill)

    return result


def department_matches(
    student_department,
    company_department
):
    student_department = normalize_text(
        student_department
    )

    company_department = normalize_text(
        company_department
    )

    if not company_department:
        return True

    if company_department in [
        "all",
        "all departments",
        "*"
    ]:
        return True

    return student_department == company_department


# =========================================================
# KNOWN SKILLS
# =========================================================

KNOWN_SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "bootstrap",
    "react",
    "angular",
    "vue",
    "node.js",
    "nodejs",
    "flask",
    "django",
    "sql",
    "mysql",
    "sqlite",
    "mongodb",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "google cloud",
    "gcp",
    "linux",
    "bash",
    "selenium",
    "junit",
    "testng",
    "machine learning",
    "data science",
    "pandas",
    "numpy",
    "power bi",
    "excel",
    "tableau",
    "communication",
    "problem solving"
]


# =========================================================
# RESUME FUNCTIONS
# =========================================================

def allowed_file(filename):
    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in ALLOWED_EXTENSIONS


def extract_resume_text(filepath):

    extension = filepath.rsplit(
        ".",
        1
    )[1].lower()

    text = ""

    try:

        # PDF
        if extension == "pdf":

            try:
                import fitz

                document = fitz.open(filepath)

                pages = []

                for page in document:
                    page_text = page.get_text("text")

                    if page_text:
                        pages.append(page_text)

                document.close()

                text = "\n".join(pages)

            except Exception as error:
                print(
                    "PyMuPDF error:",
                    error
                )

            # Fallback to PyPDF2
            if not text.strip():

                try:
                    from PyPDF2 import PdfReader

                    reader = PdfReader(filepath)

                    fallback_pages = []

                    for page in reader.pages:

                        page_text = page.extract_text()

                        if page_text:
                            fallback_pages.append(page_text)

                    text = "\n".join(
                        fallback_pages
                    )

                except Exception as fallback_error:

                    print(
                        "PyPDF2 fallback error:",
                        fallback_error
                    )

        # DOCX
        elif extension == "docx":

            from docx import Document

            document = Document(filepath)

            paragraphs = []

            for paragraph in document.paragraphs:

                if paragraph.text:
                    paragraphs.append(
                        paragraph.text
                    )

            text = "\n".join(
                paragraphs
            )

        # TXT
        elif extension == "txt":

            with open(
                filepath,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                text = file.read()

    except Exception as error:

        print(
            "Resume extraction error:",
            error
        )

        text = ""

    return text


def extract_skills_from_resume(text):

    normalized = normalize_text(text)

    detected = []

    for skill in KNOWN_SKILLS:

        skill_normalized = normalize_text(
            skill
        )

        if not skill_normalized:
            continue

        if skill_normalized in [
            "c",
            "c++"
        ]:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(skill_normalized)
                + r"(?![a-z0-9])"
            )

            if re.search(
                pattern,
                normalized
            ):
                detected.append(skill)

        else:

            if skill_normalized in normalized:
                detected.append(skill)

    final_skills = []

    for skill in detected:

        if skill not in final_skills:
            final_skills.append(skill)

    return final_skills


# =========================================================
# MATCHING
# =========================================================

def calculate_match(
    student,
    company
):

    student_skills = normalize_skills(
        student["skills"]
    )

    required_skills = normalize_skills(
        company["required_skills"]
    )

    student_skills_set = set(
        student_skills
    )

    required_skills_set = set(
        required_skills
    )

    if required_skills_set:

        matched_skills = sorted(
            student_skills_set
            & required_skills_set
        )

        skill_score = (
            len(matched_skills)
            / len(required_skills_set)
        ) * 100

    else:

        matched_skills = []

        skill_score = 100

    # CGPA

    try:

        student_cgpa = float(
            student["cgpa"] or 0
        )

    except:

        student_cgpa = 0

    try:

        min_cgpa = float(
            company["min_cgpa"] or 0
        )

    except:

        min_cgpa = 0

    if min_cgpa <= 0:

        cgpa_score = 100

    elif student_cgpa >= min_cgpa:

        cgpa_score = 100

    else:

        cgpa_score = (
            student_cgpa
            / min_cgpa
        ) * 100

        cgpa_score = max(
            0,
            min(
                100,
                cgpa_score
            )
        )

    # Department

    department_score = (
        100
        if department_matches(
            student["department"],
            company["department"]
        )
        else 0
    )

    percentage = round(
        (
            skill_score * 0.60
            + cgpa_score * 0.30
            + department_score * 0.10
        ),
        2
    )

    eligible = (
        student_cgpa >= min_cgpa
        and department_matches(
            student["department"],
            company["department"]
        )
    )

    return {
        "percentage": percentage,
        "skill_score": round(
            skill_score,
            2
        ),
        "cgpa_score": round(
            cgpa_score,
            2
        ),
        "department_score": round(
            department_score,
            2
        ),
        "matched_skills": matched_skills,
        "required_skills": required_skills,
        "eligible": eligible
    }


# =========================================================
# DATABASE CREATION / MIGRATION
# =========================================================

def create_database():

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    conn = get_db_connection()

    # STUDENTS

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            father_name TEXT,
            mother_name TEXT,
            date_of_birth TEXT,
            gender TEXT,
            phone TEXT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            department TEXT,
            cgpa REAL,
            skills TEXT,
            resume_filename TEXT
        )
    """)

    # COMPANIES

    conn.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            job_role TEXT NOT NULL,
            min_cgpa REAL,
            department TEXT,
            package TEXT,
            required_skills TEXT
        )
    """)

    # APPLICATIONS

    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            company_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Applied',
            applied_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id)
                REFERENCES students(id),
            FOREIGN KEY(company_id)
                REFERENCES companies(id),
            UNIQUE(
                student_id,
                company_id
            )
        )
    """)

    # Add missing student columns

    student_columns = [
        row["name"]
        for row in conn.execute(
            "PRAGMA table_info(students)"
        ).fetchall()
    ]

    if "skills" not in student_columns:

        conn.execute("""
            ALTER TABLE students
            ADD COLUMN skills TEXT
        """)

    if "resume_filename" not in student_columns:

        conn.execute("""
            ALTER TABLE students
            ADD COLUMN resume_filename TEXT
        """)

    # Add missing company column

    company_columns = [
        row["name"]
        for row in conn.execute(
            "PRAGMA table_info(companies)"
        ).fetchall()
    ]

    if "required_skills" not in company_columns:

        conn.execute("""
            ALTER TABLE companies
            ADD COLUMN required_skills TEXT
        """)

    # Add missing application column

    application_columns = [
        row["name"]
        for row in conn.execute(
            "PRAGMA table_info(applications)"
        ).fetchall()
    ]

    if "applied_at" not in application_columns:

        conn.execute("""
            ALTER TABLE applications
            ADD COLUMN applied_at TEXT
        """)

    conn.commit()

    conn.close()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        father_name = request.form.get(
            "father_name",
            ""
        ).strip()

        mother_name = request.form.get(
            "mother_name",
            ""
        ).strip()

        date_of_birth = request.form.get(
            "date_of_birth",
            ""
        ).strip()

        gender = request.form.get(
            "gender",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        department = request.form.get(
            "department",
            ""
        ).strip()

        cgpa = request.form.get(
            "cgpa",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        if not name or not email or not password:

            flash(
                "Please fill all required fields.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        if phone and (
            not phone.isdigit()
            or len(phone) != 10
        ):

            flash(
                "Phone number must contain 10 digits.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        try:

            cgpa_value = float(cgpa)

            if cgpa_value < 0 or cgpa_value > 10:
                raise ValueError

        except:

            flash(
                "CGPA must be between 0 and 10.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        conn = get_db_connection()

        try:

            conn.execute("""
                INSERT INTO students (
                    name,
                    father_name,
                    mother_name,
                    date_of_birth,
                    gender,
                    phone,
                    email,
                    password,
                    department,
                    cgpa,
                    skills
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                father_name,
                mother_name,
                date_of_birth,
                gender,
                phone,
                email,
                password,
                department,
                cgpa_value,
                skills
            ))

            conn.commit()

            flash(
                "Registration successful. Please login.",
                "success"
            )

            return redirect(
                url_for("login")
            )

        except sqlite3.IntegrityError:

            flash(
                "Email already registered.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        finally:

            conn.close()

    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        conn = get_db_connection()

        student = conn.execute("""
            SELECT *
            FROM students
            WHERE email = ?
            AND password = ?
        """, (
            email,
            password
        )).fetchone()

        conn.close()

        if student:

            session["student_id"] = student["id"]

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template(
        "login.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if not session.get("student_id"):

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (
        session["student_id"],
    )).fetchone()

    application_count = conn.execute("""
        SELECT COUNT(*) AS count
        FROM applications
        WHERE student_id = ?
    """, (
        session["student_id"],
    )).fetchone()["count"]

    conn.close()

    return render_template(
        "dashboard.html",
        student=student,
        application_count=application_count
    )

# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if not session.get("student_id"):
        return redirect(url_for("login"))

    conn = get_db_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (
        session["student_id"],
    )).fetchone()

    conn.close()

    return render_template(
        "profile.html",
        student=student
    )


# =========================================================
# EDIT PROFILE
# =========================================================

@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if not session.get("student_id"):
        return redirect(url_for("login"))

    conn = get_db_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (
        session["student_id"],
    )).fetchone()

    if not student:
        conn.close()
        flash("Student profile not found.", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        father_name = request.form.get("father_name", "").strip()
        mother_name = request.form.get("mother_name", "").strip()
        date_of_birth = request.form.get("date_of_birth", "").strip()
        gender = request.form.get("gender", "").strip()
        phone = request.form.get("phone", "").strip()
        department = request.form.get("department", "").strip()
        cgpa = request.form.get("cgpa", "").strip()
        skills = request.form.get("skills", "").strip()

        if not name or not department or not cgpa:
            flash("Please fill all required fields.", "error")
            conn.close()
            return redirect(url_for("edit_profile"))

        if phone and (not phone.isdigit() or len(phone) != 10):
            flash("Phone number must contain 10 digits.", "error")
            conn.close()
            return redirect(url_for("edit_profile"))

        try:
            cgpa_value = float(cgpa)

            if cgpa_value < 0 or cgpa_value > 10:
                raise ValueError

        except ValueError:
            flash("CGPA must be between 0 and 10.", "error")
            conn.close()
            return redirect(url_for("edit_profile"))

        conn.execute("""
            UPDATE students
            SET
                name = ?,
                father_name = ?,
                mother_name = ?,
                date_of_birth = ?,
                gender = ?,
                phone = ?,
                department = ?,
                cgpa = ?,
                skills = ?
            WHERE id = ?
        """, (
            name,
            father_name,
            mother_name,
            date_of_birth,
            gender,
            phone,
            department,
            cgpa_value,
            skills,
            session["student_id"]
        ))

        conn.commit()
        conn.close()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("profile"))

    conn.close()

    return render_template(
        "edit_profile.html",
        student=student
    )

# =========================================================
# COMPANIES
# =========================================================

@app.route("/companies")
def companies():

    if not session.get("student_id"):

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (
        session["student_id"],
    )).fetchone()

    companies_data = conn.execute("""
        SELECT *
        FROM companies
        ORDER BY company_name
    """).fetchall()

    conn.close()

    company_list = []

    for company in companies_data:

        match = calculate_match(
            student,
            company
        )

        company_list.append({
            "company": company,
            "match": match
        })

    return render_template(
        "companies.html",
        companies=company_list
    )


# =========================================================
# COMPANY DETAILS
# =========================================================

@app.route(
    "/company/<int:company_id>"
)
def company_details(company_id):

    if not session.get("student_id"):

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (
        session["student_id"],
    )).fetchone()

    company = conn.execute("""
        SELECT *
        FROM companies
        WHERE id = ?
    """, (
        company_id,
    )).fetchone()

    conn.close()

    if not company:

        flash(
            "Company not found.",
            "error"
        )

        return redirect(
            url_for("companies")
        )

    match = calculate_match(
        student,
        company
    )

    return render_template(
        "company_details.html",
        company=company,
        match=match
    )


# =========================================================
# APPLY
# =========================================================

@app.route(
    "/apply/<int:company_id>",
    methods=["GET", "POST"]
)
def apply(company_id):

    if not session.get("student_id"):

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (
        session["student_id"],
    )).fetchone()

    company = conn.execute("""
        SELECT *
        FROM companies
        WHERE id = ?
    """, (
        company_id,
    )).fetchone()

    conn.close()

    if not company:

        flash(
            "Company not found.",
            "error"
        )

        return redirect(
            url_for("companies")
        )

    match = calculate_match(
        student,
        company
    )

    if request.method == "POST":

        if not match["eligible"]:

            flash(
                "You are not eligible for this job.",
                "error"
            )

            return redirect(
                url_for(
                    "company_details",
                    company_id=company_id
                )
            )

        conn = get_db_connection()

        try:

            conn.execute("""
                INSERT INTO applications (
                    student_id,
                    company_id,
                    status,
                    applied_at
                )
                VALUES (?, ?, 'Applied', CURRENT_TIMESTAMP)
            """, (
                session["student_id"],
                company_id
            ))

            conn.commit()

            flash(
                "Application submitted successfully.",
                "success"
            )

        except sqlite3.IntegrityError:

            flash(
                "You have already applied for this company.",
                "error"
            )

        finally:

            conn.close()

        return redirect(
            url_for("my_applications")
        )

    return render_template(
        "apply.html",
        student=student,
        company=company,
        match=match
    )


# =========================================================
# MY APPLICATIONS
# =========================================================

@app.route("/my-applications")
def my_applications():

    if not session.get("student_id"):

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    applications = conn.execute("""
        SELECT
            applications.*,
            companies.company_name,
            companies.job_role,
            companies.package
        FROM applications
        JOIN companies
            ON applications.company_id = companies.id
        WHERE applications.student_id = ?
        ORDER BY applications.id DESC
    """, (
        session["student_id"],
    )).fetchall()

    conn.close()

    return render_template(
        "my_applications.html",
        applications=applications
    )


# =========================================================
# RESUME ANALYZER
# =========================================================

@app.route(
    "/resume",
    methods=["GET", "POST"]
)
def resume():

    if not session.get("student_id"):

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (
        session["student_id"],
    )).fetchone()

    if request.method == "POST":

        file = request.files.get(
            "resume"
        )

        if not file or not file.filename:

            flash(
                "Please select a resume file.",
                "error"
            )

        elif not allowed_file(
            file.filename
        ):

            flash(
                "Only PDF, DOCX and TXT files are allowed.",
                "error"
            )

        else:

            filename = secure_filename(
                file.filename
            )

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            try:

                file.save(filepath)

                resume_text = extract_resume_text(
                    filepath
                )

                detected_skills = extract_skills_from_resume(
                    resume_text
                )

                skills_text = ", ".join(
                    detected_skills
                )

                conn.execute("""
                    UPDATE students
                    SET
                        resume_filename = ?,
                        skills = ?
                    WHERE id = ?
                """, (
                    filename,
                    skills_text,
                    session["student_id"]
                ))

                conn.commit()

                if detected_skills:

                    flash(
                        "Resume uploaded and analyzed successfully.",
                        "success"
                    )

                else:

                    flash(
                        "Resume uploaded successfully, but no skills were detected.",
                        "error"
                    )

                student = conn.execute("""
                    SELECT *
                    FROM students
                    WHERE id = ?
                """, (
                    session["student_id"],
                )).fetchone()

            except Exception as error:

                print(
                    "Resume upload error:",
                    error
                )

                flash(
                    "Resume could not be analyzed. Please try another file.",
                    "error"
                )

    conn.close()

    detected_skills = normalize_skills(
        student["skills"]
    )

    return render_template(
        "resume.html",
        student=student,
        detected_skills=detected_skills
    )


# =========================================================
# RECOMMENDATIONS
# =========================================================

@app.route("/recommendations")
def recommendations():

    if not session.get("student_id"):

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (
        session["student_id"],
    )).fetchone()

    companies_data = conn.execute("""
        SELECT *
        FROM companies
    """).fetchall()

    conn.close()

    recommendations_list = []

    for company in companies_data:

        match = calculate_match(
            student,
            company
        )

        recommendations_list.append({
            "company": company,
            "match": match
        })

    recommendations_list.sort(
        key=lambda item:
            item["match"]["percentage"],
        reverse=True
    )

    return render_template(
        "recommendations.html",
        recommendations=recommendations_list
    )


# =========================================================
# SKILL GAP
# =========================================================

@app.route("/skill-gap")
def skill_gap():

    if not session.get("student_id"):

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (
        session["student_id"],
    )).fetchone()

    companies_data = conn.execute("""
        SELECT *
        FROM companies
        ORDER BY company_name
    """).fetchall()

    conn.close()

    return render_template(
        "skill_gap.html",
        student=student,
        companies=companies_data
    )


# =========================================================
# SKILL GAP FOR COMPANY
# =========================================================

@app.route(
    "/skill-gap/<int:company_id>"
)
def skill_gap_company(company_id):

    if not session.get("student_id"):

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (
        session["student_id"],
    )).fetchone()

    company = conn.execute("""
        SELECT *
        FROM companies
        WHERE id = ?
    """, (
        company_id,
    )).fetchone()

    conn.close()

    if not company:

        flash(
            "Company not found.",
            "error"
        )

        return redirect(
            url_for("skill_gap")
        )

    current_skills = set(
        normalize_skills(
            student["skills"]
        )
    )

    required_skills = set(
        normalize_skills(
            company["required_skills"]
        )
    )

    matched_skills = sorted(
        current_skills
        & required_skills
    )

    missing_skills = sorted(
        required_skills
        - current_skills
    )

    return render_template(
        "skill_gap.html",
        student=student,
        companies=[company],
        selected_company=company,
        current_skills=sorted(
            current_skills
        ),
        required_skills=sorted(
            required_skills
        ),
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin-login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        )

        password = request.form.get(
            "password",
            ""
        )

        if (
            username == "admin"
            and password == "admin123"
        ):

            session["admin"] = True

            return redirect(
                url_for("admin")
            )

        flash(
            "Invalid admin credentials.",
            "error"
        )

    return render_template(
        "admin_login.html"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin():

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    conn = get_db_connection()

    total_students = conn.execute("""
        SELECT COUNT(*) AS count
        FROM students
    """).fetchone()["count"]

    total_companies = conn.execute("""
        SELECT COUNT(*) AS count
        FROM companies
    """).fetchone()["count"]

    total_applications = conn.execute("""
        SELECT COUNT(*) AS count
        FROM applications
    """).fetchone()["count"]

    selected = conn.execute("""
        SELECT COUNT(*) AS count
        FROM applications
        WHERE status = 'Selected'
    """).fetchone()["count"]

    conn.close()

    return render_template(
        "admin.html",
        total_students=total_students,
        total_companies=total_companies,
        total_applications=total_applications,
        selected=selected
    )


# =========================================================
# ADD COMPANY
# =========================================================

@app.route(
    "/add-company",
    methods=["GET", "POST"]
)
def add_company():

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    if request.method == "POST":

        company_name = request.form.get(
            "company_name",
            ""
        ).strip()

        job_role = request.form.get(
            "job_role",
            ""
        ).strip()

        min_cgpa = request.form.get(
            "min_cgpa",
            ""
        ).strip()

        department = request.form.get(
            "department",
            ""
        ).strip()

        package = request.form.get(
            "package",
            ""
        ).strip()

        required_skills = request.form.get(
            "required_skills",
            ""
        ).strip()

        # Validation

        if not company_name or not job_role or not min_cgpa or not department or not package:

            flash(
                "Please fill all required fields.",
                "error"
            )

            return redirect(
                url_for("add_company")
            )

        try:

            min_cgpa_value = float(
                min_cgpa
            )

            if (
                min_cgpa_value < 0
                or min_cgpa_value > 10
            ):
                raise ValueError

        except ValueError:

            flash(
                "Minimum CGPA must be between 0 and 10.",
                "error"
            )

            return redirect(
                url_for("add_company")
            )

        conn = get_db_connection()

        try:

            # IMPORTANT:
            # 6 columns = 6 values

            conn.execute("""
                INSERT INTO companies (
                    company_name,
                    job_role,
                    min_cgpa,
                    department,
                    package,
                    required_skills
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                company_name,
                job_role,
                min_cgpa_value,
                department,
                package,
                required_skills
            ))

            conn.commit()

            flash(
                "Company added successfully!",
                "success"
            )

        except sqlite3.Error as error:

            conn.rollback()

            print(
                "Add company error:",
                error
            )

            flash(
                "Unable to add company. Please try again.",
                "error"
            )

        finally:

            conn.close()

        return redirect(
            url_for("admin")
        )

    return render_template(
        "add_company.html"
    )


# =========================================================
# ADMIN APPLICATIONS
# =========================================================

@app.route("/admin-applications")
def admin_applications():

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    conn = get_db_connection()

    applications = conn.execute("""
        SELECT
            applications.*,
            students.name,
            students.email,
            students.department,
            students.cgpa,
            companies.company_name,
            companies.job_role,
            companies.package
        FROM applications
        JOIN students
            ON applications.student_id = students.id
        JOIN companies
            ON applications.company_id = companies.id
        ORDER BY applications.id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin_applications.html",
        applications=applications
    )


# =========================================================
# UPDATE APPLICATION STATUS
# =========================================================

@app.route(
    "/update-application/<int:application_id>",
    methods=["GET", "POST"]
)
def update_application(application_id):

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    if request.method == "GET":

        status = request.args.get(
            "status",
            "Applied"
        )

    else:

        status = request.form.get(
            "status",
            "Applied"
        )

    allowed_statuses = {
        "Applied",
        "Shortlisted",
        "Selected",
        "Rejected"
    }

    if status not in allowed_statuses:
        status = "Applied"

    conn = get_db_connection()

    conn.execute("""
        UPDATE applications
        SET status = ?
        WHERE id = ?
    """, (
        status,
        application_id
    ))

    conn.commit()

    conn.close()

    flash(
        "Application status updated successfully.",
        "success"
    )

    return redirect(
        url_for("admin_applications")
    )


# =========================================================
# ANALYTICS
# =========================================================

@app.route("/analytics")
def analytics():

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    conn = get_db_connection()

    total_students = conn.execute("""
        SELECT COUNT(*) AS count
        FROM students
    """).fetchone()["count"]

    total_companies = conn.execute("""
        SELECT COUNT(*) AS count
        FROM companies
    """).fetchone()["count"]

    total_applications = conn.execute("""
        SELECT COUNT(*) AS count
        FROM applications
    """).fetchone()["count"]

    selected = conn.execute("""
        SELECT COUNT(*) AS count
        FROM applications
        WHERE status = 'Selected'
    """).fetchone()["count"]

    shortlisted = conn.execute("""
        SELECT COUNT(*) AS count
        FROM applications
        WHERE status = 'Shortlisted'
    """).fetchone()["count"]

    rejected = conn.execute("""
        SELECT COUNT(*) AS count
        FROM applications
        WHERE status = 'Rejected'
    """).fetchone()["count"]

    applied = conn.execute("""
        SELECT COUNT(*) AS count
        FROM applications
        WHERE status = 'Applied'
    """).fetchone()["count"]

    department_stats = conn.execute("""
        SELECT
            department,
            COUNT(*) AS count
        FROM students
        WHERE department IS NOT NULL
        AND TRIM(department) != ''
        GROUP BY department
        ORDER BY department
    """).fetchall()

    company_stats = conn.execute("""
        SELECT
            companies.company_name,
            COUNT(applications.id) AS count
        FROM companies
        LEFT JOIN applications
            ON companies.id = applications.company_id
        GROUP BY companies.id
        ORDER BY companies.company_name
    """).fetchall()

    conn.close()

    return render_template(
        "analytics.html",
        total_students=total_students,
        total_companies=total_companies,
        total_applications=total_applications,
        selected=selected,
        shortlisted=shortlisted,
        rejected=rejected,
        applied=applied,
        department_stats=department_stats,
        company_stats=company_stats
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.pop(
        "student_id",
        None
    )

    return redirect(
        url_for("index")
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin-logout")
def admin_logout():

    session.pop(
        "admin",
        None
    )

    return redirect(
        url_for("index")
    )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    create_database()

    app.run(
        debug=True
    )