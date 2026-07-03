"""
School Management System
-------------------------
A Streamlit UI for a JSON-backed school management system built with
an OOP core (abstract base class + Student/Teacher subclasses).

Author : Dheeraj Kumar Sahu
Contact: dheerajkumarsahu827@gmail.com
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------------------------------- #
# Configuration & data persistence
# --------------------------------------------------------------------------- #

DATABASE = Path(__file__).parent / "school_data.json"


def load_data() -> dict:
    """Load the JSON database, creating a fresh structure if it doesn't exist."""
    if DATABASE.exists():
        content = DATABASE.read_text().strip()
        if content:
            return json.loads(content)
    return {"Students": [], "Teachers": []}


def save_data(data: dict) -> None:
    """Persist the in-memory database back to disk."""
    with open(DATABASE, "w") as file:
        json.dump(data, file, indent=4)


if "data" not in st.session_state:
    st.session_state.data = load_data()


# --------------------------------------------------------------------------- #
# OOP core — kept faithful to the original design
# --------------------------------------------------------------------------- #

class Person(ABC):
    """Abstract base class shared by Student and Teacher."""

    @abstractmethod
    def get_role(self) -> str:
        ...

    @abstractmethod
    def register(self, payload: dict) -> tuple[bool, str]:
        ...

    @staticmethod
    def validate_email(email: str) -> bool:
        return "@" in email and "." in email and len(email) > 5


class Student(Person):
    def get_role(self) -> str:
        return "Student"

    def register(self, payload: dict) -> tuple[bool, str]:
        data = st.session_state.data
        if not Person.validate_email(payload["email"]):
            return False, "Invalid email address."
        if any(s["roll_no"] == payload["roll_no"] for s in data["Students"]):
            return False, f"Roll No. {payload['roll_no']} already exists."

        data["Students"].append(
            {
                "name": payload["name"],
                "age": payload["age"],
                "email": payload["email"],
                "roll_no": payload["roll_no"],
                "grades": {},
                "joined": datetime.now().strftime("%Y-%m-%d"),
            }
        )
        save_data(data)
        return True, f"Student '{payload['name']}' registered successfully."

    def add_grade(self, roll_no: int, subject: str, marks: float) -> tuple[bool, str]:
        data = st.session_state.data
        for s in data["Students"]:
            if s["roll_no"] == roll_no:
                s["grades"][subject] = marks
                save_data(data)
                return True, f"Grade added for Roll No. {roll_no}."
        return False, "Student not found."

    def delete(self, roll_no: int) -> None:
        data = st.session_state.data
        data["Students"] = [s for s in data["Students"] if s["roll_no"] != roll_no]
        save_data(data)


class Teacher(Person):
    def get_role(self) -> str:
        return "Teacher"

    def register(self, payload: dict) -> tuple[bool, str]:
        data = st.session_state.data
        if not Person.validate_email(payload["email"]):
            return False, "Invalid email address."
        if any(t["emp_id"] == payload["emp_id"] for t in data["Teachers"]):
            return False, f"Employee ID {payload['emp_id']} already exists."

        data["Teachers"].append(
            {
                "name": payload["name"],
                "age": payload["age"],
                "email": payload["email"],
                "subject": payload["subject"],
                "emp_id": payload["emp_id"],
                "joined": datetime.now().strftime("%Y-%m-%d"),
            }
        )
        save_data(data)
        return True, f"Teacher '{payload['name']}' registered successfully."

    def delete(self, emp_id: str) -> None:
        data = st.session_state.data
        data["Teachers"] = [t for t in data["Teachers"] if t["emp_id"] != emp_id]
        save_data(data)


stu_manager = Student()
tea_manager = Teacher()

# --------------------------------------------------------------------------- #
# Streamlit page setup & styling
# --------------------------------------------------------------------------- #

st.set_page_config(
    page_title="School Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .main > div { padding-top: 1.5rem; }
        .stMetric {
            background: #ffffff0d;
            border: 1px solid #ffffff1a;
            border-radius: 12px;
            padding: 1rem;
        }
        div[data-testid="stMetricValue"] { font-size: 1.8rem; }
        .app-title {
            font-size: 2.1rem;
            font-weight: 700;
            margin-bottom: 0;
        }
        .app-subtitle {
            color: #9aa0a6;
            margin-top: 0.1rem;
            margin-bottom: 1.5rem;
        }
        section[data-testid="stSidebar"] .stButton button {
            width: 100%;
            text-align: left;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Sidebar navigation
# --------------------------------------------------------------------------- #

st.sidebar.markdown("## 🎓 School MS")
st.sidebar.caption("JSON-backed · Streamlit · OOP core")

page = st.sidebar.radio(
    "Navigate",
    [
        "📊 Dashboard",
        "🧑‍🎓 Register Student",
        "🧑‍🏫 Register Teacher",
        "📝 Add Grades",
        "📁 Student Directory",
        "📁 Teacher Directory",
    ],
    label_visibility="collapsed",
)

st.sidebar.divider()
st.sidebar.caption(f"Database file: `{DATABASE.name}`")
st.sidebar.caption("Built by Dheeraj Kumar Sahu")

data = st.session_state.data

# --------------------------------------------------------------------------- #
# Dashboard
# --------------------------------------------------------------------------- #

if page == "📊 Dashboard":
    st.markdown('<p class="app-title">Dashboard</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="app-subtitle">A quick overview of your school\'s records</p>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    total_students = len(data["Students"])
    total_teachers = len(data["Teachers"])
    graded_entries = sum(len(s["grades"]) for s in data["Students"])
    avg_mark = (
        round(
            sum(m for s in data["Students"] for m in s["grades"].values())
            / graded_entries,
            2,
        )
        if graded_entries
        else 0
    )

    col1.metric("Total Students", total_students)
    col2.metric("Total Teachers", total_teachers)
    col3.metric("Grade Entries", graded_entries)
    col4.metric("Average Marks", avg_mark)

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Students per Subject (grade entries)")
        subject_counts: dict[str, int] = {}
        for s in data["Students"]:
            for subj in s["grades"]:
                subject_counts[subj] = subject_counts.get(subj, 0) + 1
        if subject_counts:
            st.bar_chart(pd.Series(subject_counts, name="Entries"))
        else:
            st.info("No grades recorded yet.")

    with right:
        st.subheader("Teachers by Subject")
        teacher_subjects: dict[str, int] = {}
        for t in data["Teachers"]:
            teacher_subjects[t["subject"]] = teacher_subjects.get(t["subject"], 0) + 1
        if teacher_subjects:
            st.bar_chart(pd.Series(teacher_subjects, name="Teachers"))
        else:
            st.info("No teachers registered yet.")

    st.divider()
    st.subheader("Recently Registered Students")
    if data["Students"]:
        recent = sorted(
            data["Students"], key=lambda s: s.get("joined", ""), reverse=True
        )[:5]
        st.dataframe(
            pd.DataFrame(recent)[["roll_no", "name", "age", "email", "joined"]],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No students registered yet.")

# --------------------------------------------------------------------------- #
# Register Student
# --------------------------------------------------------------------------- #

elif page == "🧑‍🎓 Register Student":
    st.markdown('<p class="app-title">Register a Student</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="app-subtitle">Add a new student record to the database</p>',
        unsafe_allow_html=True,
    )

    with st.form("student_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name")
        age = c2.number_input("Age", min_value=3, max_value=100, step=1)
        email = c1.text_input("Email")
        roll_no = c2.number_input("Roll No.", min_value=1, step=1)

        submitted = st.form_submit_button("Register Student", type="primary")
        if submitted:
            if not name.strip():
                st.error("Name is required.")
            else:
                ok, msg = stu_manager.register(
                    {"name": name.strip(), "age": int(age), "email": email.strip(), "roll_no": int(roll_no)}
                )
                st.success(msg) if ok else st.error(msg)

# --------------------------------------------------------------------------- #
# Register Teacher
# --------------------------------------------------------------------------- #

elif page == "🧑‍🏫 Register Teacher":
    st.markdown('<p class="app-title">Register a Teacher</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="app-subtitle">Add a new teacher record to the database</p>',
        unsafe_allow_html=True,
    )

    with st.form("teacher_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name")
        age = c2.number_input("Age", min_value=18, max_value=100, step=1)
        email = c1.text_input("Email")
        subject = c2.text_input("Subject Taught")
        emp_id = st.text_input("Employee ID")

        submitted = st.form_submit_button("Register Teacher", type="primary")
        if submitted:
            if not name.strip() or not emp_id.strip():
                st.error("Name and Employee ID are required.")
            else:
                ok, msg = tea_manager.register(
                    {
                        "name": name.strip(),
                        "age": int(age),
                        "email": email.strip(),
                        "subject": subject.strip(),
                        "emp_id": emp_id.strip(),
                    }
                )
                st.success(msg) if ok else st.error(msg)

# --------------------------------------------------------------------------- #
# Add Grades
# --------------------------------------------------------------------------- #

elif page == "📝 Add Grades":
    st.markdown('<p class="app-title">Add Grades</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="app-subtitle">Record marks for a subject against a student</p>',
        unsafe_allow_html=True,
    )

    if not data["Students"]:
        st.info("No students registered yet. Add a student first.")
    else:
        options = {f"{s['roll_no']} — {s['name']}": s["roll_no"] for s in data["Students"]}
        choice = st.selectbox("Select Student", list(options.keys()))
        roll_no = options[choice]

        with st.form("grade_form", clear_on_submit=True):
            subject = st.text_input("Subject")
            marks = st.number_input("Marks", min_value=0.0, max_value=100.0, step=0.5)
            submitted = st.form_submit_button("Add Grade", type="primary")
            if submitted:
                if not subject.strip():
                    st.error("Subject is required.")
                else:
                    ok, msg = stu_manager.add_grade(roll_no, subject.strip(), marks)
                    st.success(msg) if ok else st.error(msg)

        current = next(s for s in data["Students"] if s["roll_no"] == roll_no)
        if current["grades"]:
            st.subheader(f"Grades for {current['name']}")
            st.dataframe(
                pd.DataFrame(
                    [{"Subject": k, "Marks": v} for k, v in current["grades"].items()]
                ),
                use_container_width=True,
                hide_index=True,
            )

# --------------------------------------------------------------------------- #
# Student Directory
# --------------------------------------------------------------------------- #

elif page == "📁 Student Directory":
    st.markdown('<p class="app-title">Student Directory</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="app-subtitle">Search, review, and manage student records</p>',
        unsafe_allow_html=True,
    )

    search = st.text_input("🔍 Search by name or roll number")
    students = data["Students"]
    if search:
        students = [
            s
            for s in students
            if search.lower() in s["name"].lower() or search == str(s["roll_no"])
        ]

    if not students:
        st.info("No matching students found.")
    else:
        for s in students:
            with st.expander(f"{s['name']} — Roll No. {s['roll_no']}"):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**Age:** {s['age']}")
                    st.write(f"**Email:** {s['email']}")
                    st.write(f"**Joined:** {s.get('joined', 'N/A')}")
                    if s["grades"]:
                        st.dataframe(
                            pd.DataFrame(
                                [{"Subject": k, "Marks": v} for k, v in s["grades"].items()]
                            ),
                            use_container_width=True,
                            hide_index=True,
                        )
                    else:
                        st.caption("No grades recorded yet.")
                with c2:
                    if st.button("🗑️ Delete", key=f"del_stu_{s['roll_no']}"):
                        stu_manager.delete(s["roll_no"])
                        st.rerun()

        st.divider()
        csv = pd.DataFrame(data["Students"]).to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export Students as CSV", csv, "students.csv", "text/csv")

# --------------------------------------------------------------------------- #
# Teacher Directory
# --------------------------------------------------------------------------- #

elif page == "📁 Teacher Directory":
    st.markdown('<p class="app-title">Teacher Directory</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="app-subtitle">Search, review, and manage teacher records</p>',
        unsafe_allow_html=True,
    )

    search = st.text_input("🔍 Search by name or employee ID")
    teachers = data["Teachers"]
    if search:
        teachers = [
            t
            for t in teachers
            if search.lower() in t["name"].lower() or search.lower() == t["emp_id"].lower()
        ]

    if not teachers:
        st.info("No matching teachers found.")
    else:
        for t in teachers:
            with st.expander(f"{t['name']} — {t['subject']}"):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**Age:** {t['age']}")
                    st.write(f"**Email:** {t['email']}")
                    st.write(f"**Employee ID:** {t['emp_id']}")
                    st.write(f"**Joined:** {t.get('joined', 'N/A')}")
                with c2:
                    if st.button("🗑️ Delete", key=f"del_tea_{t['emp_id']}"):
                        tea_manager.delete(t["emp_id"])
                        st.rerun()

        st.divider()
        csv = pd.DataFrame(data["Teachers"]).to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export Teachers as CSV", csv, "teachers.csv", "text/csv")
