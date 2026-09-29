"""
Database Seeding Script for College Placement System
Adds extensive sample data:
- 40+ Companies across various departments (IT, ECE, EEE, MECH, All)
- 30+ Student profiles with detailed information, CGPAs, and skills
- 50+ Applications with various recruitment statuses (Applied, Shortlisted, Selected, Rejected)
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
        # Batch 1
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

        # Batch 2 (New recruiters across domains)
        ("Google", "Cloud Solutions Engineer", 8.5, "IT", "22 LPA", "python, linux, networking, gcp, cloud"),
        ("Oracle", "Associate Database Engineer", 7.5, "IT", "11 LPA", "sql, java, database, linux, python"),
        ("Cisco", "Network Software Engineer", 7.8, "IT", "13 LPA", "python, networking, linux, c++, tcp/ip"),
        ("Adobe", "Software Quality Engineer", 7.2, "IT", "14 LPA", "python, selenium, automation, java"),
        ("Goldman Sachs", "Operations Analyst", 7.5, "All", "16 LPA", "problem solving, excel, python, communication"),
        ("JPMorgan Chase", "Software Associate", 8.0, "IT", "15 LPA", "java, spring boot, react, sql, git"),
        ("Intel", "Firmware Validation Engineer", 8.0, "ECE", "16 LPA", "c, c++, python, linux, digital electronics"),
        ("NVIDIA", "Hardware QA Engineer", 8.2, "ECE", "18 LPA", "verilog, vlsi, c++, python, linux"),
        ("AMD", "Silicon Design Trainee", 8.0, "ECE", "14 LPA", "digital electronics, vlsi, verilog, c"),
        ("LTIMindtree", "Full Stack Developer", 6.8, "IT", "5 LPA", "javascript, html, css, react, nodejs"),
        ("Hyundai Mobis", "Automotive R&D Engineer", 7.2, "MECH", "6.5 LPA", "solidworks, catia, autocad, manufacturing"),
        ("Ashok Leyland", "Vehicle Systems Engineer", 7.0, "MECH", "5.5 LPA", "autocad, ansys, thermal, solidworks"),
        ("BHEL", "Graduate Trainee Engineer", 7.5, "EEE", "6 LPA", "power systems, electrical machines, switchgear"),
        ("Crompton Greaves", "Power Automation Engineer", 7.0, "EEE", "5.5 LPA", "plc, scada, autocad, power systems"),
        ("IBM", "Associate System Engineer", 6.5, "All", "4.5 LPA", "python, java, cloud, communication"),

        # Batch 3 (Premier Global IT Companies)
        ("Apple", "iOS & Systems Software Engineer", 8.5, "IT", "25 LPA", "swift, c++, python, objective-c, operating systems"),
        ("Meta", "Full Stack Software Engineer", 8.5, "IT", "28 LPA", "react, python, c++, distributed systems"),
        ("Netflix", "Cloud Infrastructure Engineer", 8.5, "IT", "30 LPA", "java, python, aws, microservices, docker, kubernetes"),
        ("Salesforce", "Associate Member of Technical Staff", 8.0, "IT", "16 LPA", "java, apex, javascript, react, cloud"),
        ("SAP Labs", "Developer Associate", 7.5, "IT", "12 LPA", "java, python, sql, sap abap, docker"),
        ("Uber", "Software Development Engineer 1", 8.2, "IT", "24 LPA", "python, go, java, microservices, kafka"),
        ("PayPal", "Software Engineer 1", 8.0, "IT", "14 LPA", "java, nodejs, rest apis, sql, react"),
        ("Atlassian", "Junior Software Engineer", 8.2, "IT", "17 LPA", "java, react, typescript, aws, docker"),
        ("Intuit", "Software Engineer Trainee", 7.8, "IT", "15 LPA", "java, spring boot, aws, react, algorithms"),
        ("Walmart Global Tech", "Software Engineer", 7.5, "IT", "13 LPA", "java, python, spring boot, kafka, cloud"),
        ("Morgan Stanley", "Technology Analyst", 8.0, "IT", "16 LPA", "java, c++, python, algorithms, sql"),
        ("ServiceNow", "Associate Software Engineer", 7.8, "IT", "14 LPA", "javascript, angular, react, java, database"),
        ("Twitter", "Backend Platform Engineer", 8.0, "IT", "20 LPA", "python, scala, java, redis, distributed systems"),
        ("VMware", "Member of Technical Staff", 8.0, "IT", "15 LPA", "c++, python, virtualization, linux, networking"),
        ("HashedIn", "Software Engineer - Products", 7.2, "IT", "8 LPA", "python, django, react, javascript, aws"),
    ]

    new_companies_count = 0
    for comp in companies_data:
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
        # Batch 1
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

        # Batch 2 (New students)
        ("Rohit Verma", "Ashok Verma", "Manju Verma", "2003-02-11", "Male", "9876543220", "rohit.verma@example.com", "password123", "IT", 8.3, "python, django, sql, docker, git"),
        ("Priyanka Sen", "Debashis Sen", "Aparna Sen", "2003-06-18", "Female", "9876543221", "priyanka.sen@example.com", "password123", "IT", 9.1, "java, spring boot, microservices, sql, git"),
        ("Abhinav Mishra", "Pradeep Mishra", "Sangeeta Mishra", "2002-10-04", "Male", "9876543222", "abhinav.mishra@example.com", "password123", "IT", 7.7, "react, javascript, html, css, nodejs"),
        ("Harini Venkat", "Venkatesan G", "Uma Devi V", "2003-07-29", "Female", "9876543223", "harini.venkat@example.com", "password123", "IT", 8.5, "python, machine learning, pandas, sql, power bi"),
        ("Manoj Pradeep", "Pradeep Kumar", "Gayathri P", "2002-09-14", "Male", "9876543224", "manoj.pradeep@example.com", "password123", "ECE", 8.2, "c, c++, embedded, microcontrollers, iot"),
        ("Shalini Raj", "Rajendran K", "Chitra R", "2003-04-03", "Female", "9876543225", "shalini.raj@example.com", "password123", "ECE", 7.8, "vlsi, verilog, digital electronics, c"),
        ("Tarun Tej", "Narayana Swamy", "Shailaja N", "2002-12-20", "Male", "9876543226", "tarun.tej@example.com", "password123", "ECE", 8.6, "analog electronics, circuit design, c++, linux"),
        ("Bhavya Sri", "Chandrasekhar Rao", "Padma C", "2003-03-15", "Female", "9876543227", "bhavya.sri@example.com", "password123", "EEE", 8.4, "power systems, matlab, simulink, autocad"),
        ("Nithish Kumar", "Sampath Kumar", "Vasanthi S", "2002-08-08", "Male", "9876543228", "nithish.kumar@example.com", "password123", "EEE", 7.3, "plc, scada, electrical machines, industrial automation"),
        ("Sandeep Reddy", "Prabhakar Reddy", "Madhavi R", "2002-11-25", "Male", "9876543229", "sandeep.reddy@example.com", "password123", "MECH", 8.1, "solidworks, ansys, catia, autocad"),
        ("Keerthana S", "Selvaraj M", "Revathi S", "2003-01-30", "Female", "9876543230", "keerthana.s@example.com", "password123", "MECH", 7.5, "autocad, manufacturing, mechanical design, python"),
        ("Deepa Krishnan", "Krishnamurthy N", "Shobana K", "2003-05-22", "Female", "9876543231", "deepa.krishnan@example.com", "password123", "IT", 8.7, "python, aws, linux, bash, kubernetes"),
        ("Vigneshwar R", "Ramaswamy T", "Pushpa R", "2002-06-12", "Male", "9876543232", "vigneshwar.r@example.com", "password123", "IT", 7.1, "excel, power bi, sql, python, communication"),
        ("Aditi Saxena", "Rajesh Saxena", "Nita Saxena", "2003-09-17", "Female", "9876543233", "aditi.saxena@example.com", "password123", "IT", 9.4, "c++, algorithms, data structures, python, cloud"),
        ("Naveen Balaji", "Balaji Raghavan", "Karpagam B", "2002-10-19", "Male", "9876543234", "naveen.balaji@example.com", "password123", "EEE", 7.9, "electrical machines, power electronics, matlab"),
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
    all_students = cursor.execute("SELECT id, email, department, cgpa FROM students").fetchall()
    all_companies = cursor.execute("SELECT id, company_name, department, min_cgpa FROM companies").fetchall()

    student_map = {row["email"]: row for row in all_students}
    company_map = {f"{row['company_name']}": row for row in all_companies}

    applications_spec = [
        # Batch 1
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

        # Batch 2 (New applications)
        ("rohit.verma@example.com", "Oracle", "Selected", "2026-09-20 11:00:00"),
        ("rohit.verma@example.com", "JPMorgan Chase", "Shortlisted", "2026-09-22 14:30:00"),
        ("priyanka.sen@example.com", "Google", "Selected", "2026-09-21 16:00:00"),
        ("priyanka.sen@example.com", "JPMorgan Chase", "Selected", "2026-09-23 10:15:00"),
        ("abhinav.mishra@example.com", "LTIMindtree", "Selected", "2026-09-24 09:30:00"),
        ("abhinav.mishra@example.com", "Adobe", "Applied", "2026-09-25 15:00:00"),
        ("harini.venkat@example.com", "Goldman Sachs", "Selected", "2026-09-22 12:00:00"),
        ("harini.venkat@example.com", "Google", "Shortlisted", "2026-09-24 14:45:00"),
        ("manoj.pradeep@example.com", "Intel", "Selected", "2026-09-25 10:30:00"),
        ("manoj.pradeep@example.com", "NVIDIA", "Shortlisted", "2026-09-26 11:15:00"),
        ("shalini.raj@example.com", "AMD", "Selected", "2026-09-25 14:00:00"),
        ("shalini.raj@example.com", "Texas Instruments", "Shortlisted", "2026-09-26 16:30:00"),
        ("tarun.tej@example.com", "NVIDIA", "Selected", "2026-09-24 15:20:00"),
        ("tarun.tej@example.com", "Intel", "Selected", "2026-09-26 09:45:00"),
        ("bhavya.sri@example.com", "BHEL", "Selected", "2026-09-23 10:00:00"),
        ("bhavya.sri@example.com", "Siemens", "Shortlisted", "2026-09-25 13:30:00"),
        ("nithish.kumar@example.com", "Crompton Greaves", "Selected", "2026-09-24 11:15:00"),
        ("nithish.kumar@example.com", "ABB", "Applied", "2026-09-26 14:00:00"),
        ("sandeep.reddy@example.com", "Hyundai Mobis", "Selected", "2026-09-25 15:30:00"),
        ("sandeep.reddy@example.com", "Tata Motors", "Shortlisted", "2026-09-27 12:00:00"),
        ("keerthana.s@example.com", "Ashok Leyland", "Selected", "2026-09-26 10:45:00"),
        ("keerthana.s@example.com", "Larsen & Toubro", "Applied", "2026-09-27 16:20:00"),
        ("deepa.krishnan@example.com", "Cisco", "Selected", "2026-09-24 14:10:00"),
        ("deepa.krishnan@example.com", "Amazon", "Selected", "2026-09-26 11:30:00"),
        ("vigneshwar.r@example.com", "IBM", "Selected", "2026-09-25 09:20:00"),
        ("aditi.saxena@example.com", "Google", "Selected", "2026-09-22 17:00:00"),
        ("aditi.saxena@example.com", "Microsoft", "Selected", "2026-09-24 10:00:00"),
        ("aditi.saxena@example.com", "Apple", "Selected", "2026-09-26 14:00:00"),
        ("priyanka.sen@example.com", "Meta", "Selected", "2026-09-25 15:30:00"),
        ("rahul.sharma@example.com", "Netflix", "Shortlisted", "2026-09-26 11:20:00"),
        ("ananya.iyer@example.com", "Salesforce", "Selected", "2026-09-24 16:45:00"),
        ("harini.venkat@example.com", "Uber", "Shortlisted", "2026-09-25 10:15:00"),
        ("rohit.verma@example.com", "PayPal", "Selected", "2026-09-26 13:00:00"),
        ("swathi.reddy@example.com", "Atlassian", "Selected", "2026-09-25 16:00:00"),
        ("mohammed.faiz@example.com", "Intuit", "Shortlisted", "2026-09-27 09:30:00"),
        ("sneha.patel@example.com", "Walmart Global Tech", "Selected", "2026-09-26 15:10:00"),
        ("deepa.krishnan@example.com", "Morgan Stanley", "Selected", "2026-09-27 11:00:00"),
        ("abhinav.mishra@example.com", "ServiceNow", "Shortlisted", "2026-09-27 14:30:00"),
        ("naveen.balaji@example.com", "Schneider Electric", "Shortlisted", "2026-09-26 15:00:00"),
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

    print("\n--- Updated Database Summary ---")
    print(f"Total Students: {total_studs}")
    print(f"Total Companies: {total_comps}")
    print(f"Total Applications: {total_apps}")

    conn.close()


if __name__ == "__main__":
    seed_database()
