"""
Database Seeding Script for College Placement System
Adds comprehensive sample data:
- Companies across various departments (IT, ECE, EEE, MECH, All)
- Student profiles with detailed information, CGPAs, and skills
- Applications with various recruitment statuses (Applied, Shortlisted, Selected, Rejected)
"""

import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")


def seed_database():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print(f"Connected to database: {DATABASE}")

    # =========================================================
    # 1. SEED COMPANIES
    # =========================================================
    companies_data = [
        # (company_name, job_role, min_cgpa, department, package, required_skills)
        ("Microsoft", "Software Development Engineer", 8.5, "IT", "18 LPA", "python, c++, algorithms, cloud"),
        ("Amazon", "Cloud Support Associate", 7.5, "IT", "12 LPA", "python, linux, networking, aws"),
        ("Zoho Corporation", "Full Stack Web Developer", 7.0, "IT", "8.5 LPA", "java, javascript, html, css, react"),
        ("Deloitte", "Technology Analyst", 7.5, "IT", "9 LPA", "python, sql, communication, problem solving"),
        ("Capgemini", "Data Analyst", 7.0, "IT", "5.5 LPA", "python, sql, power bi, excel, pandas"),
        ("Cognizant", "Junior DevOps Engineer", 7.2, "IT", "6 LPA", "docker, git, linux, python, bash"),
        ("Accenture", "Associate Software Engineer", 6.5, "IT", "4.5 LPA", "java, sql, python, problem solving"),
        ("Qualcomm", "Embedded Software Engineer", 8.0, "ECE", "14 LPA", "c, c++, embedded, linux, microcontrollers"),
        ("Texas Instruments", "Analog & VLSI Design Engineer", 8.2, "ECE", "15 LPA", "analog electronics, vlsi, verilog, c"),
        ("Bosch", "Automotive Firmware Engineer", 7.5, "ECE", "7 LPA", "c, c++, microcontrollers, can protocol"),
        ("Schneider Electric", "Power Systems Engineer", 7.0, "EEE", "6.5 LPA", "power systems, matlab, autocad, plc"),
        ("Siemens", "Automation & SCADA Engineer", 7.5, "EEE", "7.5 LPA", "plc, scada, electrical machines, c"),
        ("ABB", "Electrical Design Specialist", 7.2, "EEE", "6 LPA", "electrical design, circuit analysis, autocad"),
        ("Tata Motors", "Design & CAE Engineer", 7.0, "MECH", "6.5 LPA", "autocad, solidworks, ansys, catia"),
        ("Larsen & Toubro", "Graduate Engineer Trainee", 7.0, "MECH", "6 LPA", "mechanical design, manufacturing, cad"),
        ("Mu Sigma", "Decision Scientist", 7.0, "All", "7 LPA", "problem solving, python, communication, statistics"),
    ]

    new_companies_count = 0
    for comp in companies_data:
        # Check if already exists
        cursor.execute(
            "SELECT id FROM companies WHERE LOWER(company_name) = LOWER(?) AND LOWER(job_role) = LOWER(?)",
            (comp[0], comp[1]),
        )
        if not cursor.fetchone():
            cursor.execute(
                """
                INSERT INTO companies (company_name, job_role, min_cgpa, department, package, required_skills)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                comp,
            )
            new_companies_count += 1

    print(f"Added {new_companies_count} new companies.")

    # =========================================================
    # 2. SEED STUDENTS
    # =========================================================
    students_data = [
        # (name, father_name, mother_name, dob, gender, phone, email, password, dept, cgpa, skills)
        ("Rahul Sharma", "Ramesh Sharma", "Sunita Sharma", "2003-04-15", "Male", "9876543210", "rahul.sharma@example.com", "password123", "IT", 8.8, "python, flask, sql, git, docker"),
        ("Ananya Iyer", "Subramanian Iyer", "Lakshmi Iyer", "2003-08-22", "Female", "9876543211", "ananya.iyer@example.com", "password123", "IT", 9.3, "java, react, html, css, javascript, nodejs"),
        ("Karthik Raja", "Rajagopal M", "Meena R", "2002-11-10", "Male", "9876543212", "karthik.raja@example.com", "password123", "ECE", 8.4, "c, c++, embedded, microcontrollers, linux"),
        ("Divya Nair", "Suresh Nair", "Radhika Nair", "2003-01-19", "Female", "9876543213", "divya.nair@example.com", "password123", "ECE", 7.9, "analog electronics, digital electronics, vlsi, verilog"),
        ("Arun Kumar", "Mohan Kumar", "Shanthi Kumar", "2002-06-30", "Male", "9876543214", "arun.kumar@example.com", "password123", "EEE", 8.1, "power systems, autocad, matlab, electrical machines"),
        ("Sneha Patel", "Dinesh Patel", "Bhavna Patel", "2003-09-05", "Female", "9876543215", "sneha.patel@example.com", "password123", "IT", 7.4, "python, sql, pandas, excel, power bi"),
        ("Mohammed Faiz", "Abdul Kareem", "Amina Begum", "2002-12-14", "Male", "9876543216", "mohammed.faiz@example.com", "password123", "IT", 8.6, "python, aws, linux, docker, git"),
        ("Pooja Sundaram", "Sundaramurthy", "Kavitha S", "2003-03-25", "Female", "9876543217", "pooja.sundaram@example.com", "password123", "EEE", 7.6, "plc, scada, circuit analysis, autocad"),
        ("Vigneshwaran K", "Krishnan S", "Geetha K", "2002-07-18", "Male", "9876543218", "vignesh.k@example.com", "password123", "MECH", 7.8, "solidworks, autocad, ansys, python"),
        ("Swathi Reddy", "Venkat Reddy", "Sujatha Reddy", "2003-05-12", "Female", "9876543219", "swathi.reddy@example.com", "password123", "IT", 8.9, "react, nodejs, javascript, mongodb, html"),
    ]

    new_students_count = 0
    for stud in students_data:
        cursor.execute("SELECT id FROM students WHERE LOWER(email) = LOWER(?)", (stud[6],))
        if not cursor.fetchone():
            cursor.execute(
                """
                INSERT INTO students (
                    name, father_name, mother_name, date_of_birth, gender,
                    phone, email, password, department, cgpa, skills
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                stud,
            )
            new_students_count += 1

    print(f"Added {new_students_count} new students.")

    # =========================================================
    # 3. SEED APPLICATIONS
    # =========================================================
    # Fetch map of students and companies
    all_students = cursor.execute("SELECT id, email, department, cgpa FROM students").fetchall()
    all_companies = cursor.execute("SELECT id, company_name, department, min_cgpa FROM companies").fetchall()

    student_map = {row["email"]: row for row in all_students}
    company_map = {f"{row['company_name']}": row for row in all_companies}

    # Structured applications with diverse statuses
    applications_spec = [
        # (student_email, company_name, status, applied_at)
        ("rahul.sharma@example.com", "Microsoft", "Shortlisted", "2026-09-15 10:30:00"),
        ("rahul.sharma@example.com", "Amazon", "Selected", "2026-09-18 14:20:00"),
        ("rahul.sharma@example.com", "Infosys", "Applied", "2026-09-20 09:15:00"),
        ("ananya.iyer@example.com", "Microsoft", "Selected", "2026-09-16 11:00:00"),
        ("ananya.iyer@example.com", "Zoho Corporation", "Selected", "2026-09-17 15:30:00"),
        ("karthik.raja@example.com", "Qualcomm", "Shortlisted", "2026-09-19 13:45:00"),
        ("karthik.raja@example.com", "Bosch", "Selected", "2026-09-22 16:10:00"),
        ("divya.nair@example.com", "Texas Instruments", "Applied", "2026-09-21 10:00:00"),
        ("divya.nair@example.com", "Tata Elxsi", "Shortlisted", "2026-09-23 11:30:00"),
        ("arun.kumar@example.com", "Schneider Electric", "Selected", "2026-09-20 14:00:00"),
        ("arun.kumar@example.com", "Siemens", "Shortlisted", "2026-09-22 09:40:00"),
        ("sneha.patel@example.com", "Capgemini", "Selected", "2026-09-24 10:50:00"),
        ("sneha.patel@example.com", "Deloitte", "Rejected", "2026-09-25 12:15:00"),
        ("mohammed.faiz@example.com", "Amazon", "Shortlisted", "2026-09-23 15:20:00"),
        ("mohammed.faiz@example.com", "Cognizant", "Selected", "2026-09-26 14:30:00"),
        ("pooja.sundaram@example.com", "ABB", "Applied", "2026-09-25 11:10:00"),
        ("pooja.sundaram@example.com", "Schneider Electric", "Rejected", "2026-09-26 16:00:00"),
        ("vignesh.k@example.com", "Tata Motors", "Selected", "2026-09-24 13:00:00"),
        ("vignesh.k@example.com", "Larsen & Toubro", "Shortlisted", "2026-09-27 10:30:00"),
        ("swathi.reddy@example.com", "Zoho Corporation", "Selected", "2026-09-22 17:00:00"),
        ("swathi.reddy@example.com", "Deloitte", "Shortlisted", "2026-09-25 11:45:00"),
    ]

    new_apps_count = 0
    for email, comp_name, status, applied_at in applications_spec:
        stud = student_map.get(email)
        comp = company_map.get(comp_name)

        if stud and comp:
            cursor.execute(
                "SELECT id FROM applications WHERE student_id = ? AND company_id = ?",
                (stud["id"], comp["id"]),
            )
            if not cursor.fetchone():
                cursor.execute(
                    """
                    INSERT INTO applications (student_id, company_id, status, applied_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (stud["id"], comp["id"], status, applied_at),
                )
                new_apps_count += 1

    print(f"Added {new_apps_count} new job applications.")

    conn.commit()

    # Summary
    total_studs = cursor.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    total_comps = cursor.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    total_apps = cursor.execute("SELECT COUNT(*) FROM applications").fetchone()[0]

    print("\n--- Database Summary ---")
    print(f"Total Students: {total_studs}")
    print(f"Total Companies: {total_comps}")
    print(f"Total Applications: {total_apps}")

    conn.close()


if __name__ == "__main__":
    seed_database()
