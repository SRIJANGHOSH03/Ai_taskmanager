![image](https://github.com/user-attachments/assets/5cac886c-96e5-4d57-a35a-d4ab169b4127)


# 🧠 AI Task Manager


An intelligent task management desktop app built with Python, spaCy, and Tkinter. This tool uses natural language processing (NLP) to help you create, prioritize, and manage your daily tasks more efficiently.

---



## 🚀 Features

- 📝 **Natural Language Task Parsing**  
  Add tasks by simply describing them in plain English (e.g., "Remind me to call John tomorrow").

- 🧠 **AI-Powered Priority Suggestions**  
  Automatically assigns task priority based on urgency keywords.

- 📆 **Deadline & Status Tracking**  
  Tracks deadlines and updates task status (e.g., "Due Today", "Overdue").

- 🔐 **User Authentication**  
  Register/login functionality with per-user task storage.

- ✅ **Interactive Desktop GUI**  
  Simple and clean interface using `tkinter` and `ttk`.

---

## 📂 Project Structure

ai_task_manager/ 

├── ai_module.py # NLP logic for parsing tasks and suggesting priorities

├── data_module.py # Data handling, deadlines, and status logic 

├── ui_module.py # GUI application (Tkinter) 

├── database.db # SQLite database (created automatically) 

└── README.md # This file


yaml
Copy
Edit

---

## 🛠️ Requirements

- Python 3.8+
- [spaCy](https://spacy.io/)
- spaCy model: `en_core_web_sm`

Install dependencies:
```bash
pip install spacy
python -m spacy download en_core_web_sm
▶️ How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/ai-task-manager.git
cd ai-task-manager
Run the app:

bash
Copy
Edit
python ui_module.py
Register a new user or log in with existing credentials.

🧠 Using the AI Features
Click "Add via AI (NLP)" and type a natural task like:

vbnet
Copy
Edit
Remind me to submit the report by Friday
The app will extract the title, deadline, and suggest a priority automatically.

🗂 Example Task Structure
Each task contains:

Title

Description

Deadline (auto-parsed or manual)

Priority (Low, Medium, High — suggested by AI if unspecified)

Status (To Do, Done, Due Today, Overdue, Upcoming)

🧩 Extending the Project
✅ Add support for recurring tasks

📱 Build a web version (Flask + React)

🌐 Improve NLP with date parsing libraries like dateparser

☁️ Sync tasks to cloud (Google Tasks, Notion API)
