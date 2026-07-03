# 🎓 School Management System — Streamlit UI

A JSON-backed School Management System with an object-oriented Python core
(abstract base class + `Student` / `Teacher` subclasses) and a clean,
interactive **Streamlit** front end.

## ✨ Features

- **Dashboard** — live metrics (students, teachers, grade entries, average marks) and charts
- **Register Student / Teacher** — validated forms with duplicate checks (roll no. / employee ID)
- **Add Grades** — attach subject-wise marks to any student
- **Student & Teacher Directories** — search, expand for full details, delete records
- **CSV Export** — download student/teacher data for reporting
- Data persisted locally to `school_data.json` — no external database required

## 🧱 Tech / Design

- `abc.ABC` abstract base class (`Person`) enforcing a common contract (`get_role`, `register`)
- `Student` and `Teacher` subclasses implementing role-specific behavior
- Streamlit `session_state` for in-memory state, synced to disk on every write
- `pandas` for tabular views, charts, and CSV export

## 🚀 Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## 📁 Project Structure

```
school-management-system/
├── app.py              # Streamlit application
├── requirements.txt    # Python dependencies
├── school_data.json    # Auto-created local database (git-ignored)
└── README.md
```

## 🙋 Author

**Dheeraj Kumar Sahu**
📧 dheerajkumarsahu827@gmail.com
