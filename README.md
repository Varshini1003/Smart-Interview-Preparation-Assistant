# 🧠 Smart Interview Preparation Assistant

An AI-powered interview preparation platform built using **Python, Streamlit, NLP, and Machine Learning** that helps students and job seekers prepare for technical interviews, HR rounds, aptitude tests, and government exams.

The application provides question practice, answer evaluation, performance analysis, weak area identification, and progress tracking through an interactive dashboard.

---

# 🚀 Features

## 🔐 User Authentication

- User Login
- User Registration
- Session-based user management
- Logout functionality


---

# 📚 Interview Preparation Modules

## 1. Technical Interview Preparation

Supports:

- Python
- Java
- C
- C++
- Data Structures
- OOP
- DBMS
- SQL
- Computer Networks
- Operating System


Features:

- Technical questions
- User answer submission
- AI-based answer evaluation
- Expected answer display
- Performance scoring


---

## 2. HR Interview Preparation

Includes:

- Self introduction
- Strengths and weaknesses
- Career goals
- Teamwork questions
- Situational questions

Features:

- Answer evaluation
- Improvement suggestions
- Interview tips


---

## 3. Aptitude Preparation

Categories:

- Profit and Loss
- Percentage
- Simple Interest
- Compound Interest
- Ratio and Proportion
- Average
- Time and Work
- Time Speed Distance
- Probability
- Permutation and Combination
- Logical Reasoning
- Data Interpretation


Features:

- Multiple choice questions
- Instant result checking
- Explanation support
- Score calculation


---

## 4. Government Exam Preparation

Supports:

- TSPSC
- APPSC
- SSC
- RRB
- Banking
- UPSC

Subjects:

- Current Affairs
- Indian Polity
- History
- Geography
- Economy
- Computer Awareness


Features:

- Exam-based questions
- Practice tests
- Performance tracking


---

# 🤖 AI Answer Evaluation

The application uses Natural Language Processing techniques:

### Technologies Used:

- TF-IDF Vectorization
- Cosine Similarity


Process:
User Answer
|
↓
Text Processing
|
↓
TF-IDF Conversion
|
↓
Similarity Calculation
|
↓
Score Generation


The system compares user answers with expected answers and generates a similarity score.

---

# 🏆 Daily Challenge

Features:

- Random daily question generation
- Technical questions
- Aptitude MCQs
- Government exam questions
- Answer evaluation


---

# 📊 Performance Report

The dashboard provides:

- Total questions attempted
- Average score
- Highest score
- Lowest score
- Category-wise performance
- Topic-wise performance
- Score trend visualization


---

# 📜 Interview History

Tracks:

- Attempted questions
- Category
- Topic
- Scores


Features:

- Search questions
- Filter by category
- Filter by topic
- Download history report


---

# ⚠ Weak Areas Analysis

Identifies:

- Low-scoring questions
- Weak categories
- Weak topics


Provides:

- Improvement suggestions
- Performance charts


---

# 🏅 Leaderboard

Displays:

- User ranking
- Average score
- Highest score
- Achievements and badges


Badges:

- Beginner
- Intermediate
- Advanced
- Interview Champion
- Perfect Score


---

# 🛠 Technologies Used

## Programming Language

- Python


## Frontend

- Streamlit


## Data Processing

- Pandas
- NumPy


## Machine Learning / NLP

- Scikit-learn
- TF-IDF
- Cosine Similarity


## Visualization

- Matplotlib


## Database / Storage

- CSV-based question database


---

# 📂 Project Structure
Smart-Interview-Assistant/

│
├── app.py
│
├── requirements.txt
│
├── README.md
│
│
├── questions/
│
│ ├── technical/
│ │
│ ├── hr/
│ │
│ ├── aptitude/
│ │
│ └── government_sector/
│
│
└── assets/

---

# 📁 CSV Question Format

Each CSV file should contain:

### Aptitude CSV

```csv
ID,Question,Option_A,Option_B,Option_C,Option_D,Answer,Explanation,Difficulty
1,"What is 2+2?","3","4","5","6","4","2+2=4","Easy"
ID,Question,Answer,Difficulty
1,"Explain OOP concepts","OOP is a programming approach based on objects","Medium"
Installation
Step 1: Clone Repository
git clone https://github.com/yourusername/smart-interview-assistant.git
Step 2: Navigate Project Folder
cd smart-interview-assistant
Step 3: Install Dependencies
pip install -r requirements.txt
Step 4: Run Application
streamlit run app.py
📦 Requirements

Create requirements.txt

streamlit
pandas
numpy
matplotlib
scikit-learn
🖥 Application Workflow
Login/Register

        ↓

Select Category

        ↓

Choose Topic

        ↓

Practice Questions

        ↓

Submit Answer

        ↓

AI Evaluation

        ↓

Performance Analysis

        ↓

Improve Weak Areas
🎯 Objectives
Provide an interactive interview preparation platform
Improve technical and aptitude skills
Evaluate descriptive answers automatically
Track learning progress
Identify weak areas
Support placement and government exam preparation
🌟 Advantages

✔ AI-based answer evaluation
✔ Multiple preparation categories
✔ Performance analytics
✔ Easy-to-use interface
✔ Personalized practice
✔ Progress tracking

🔮 Future Enhancements
Voice-based mock interviews
Speech recognition
AI interviewer chatbot
Resume analyzer
Resume builder
Company-specific interview preparation
Online database integration
Mobile application
Advanced recommendation system
👩‍💻 Author

Varshini Gurija

B.Tech Computer Science Engineering

Project: Smart Interview Preparation Assistant
