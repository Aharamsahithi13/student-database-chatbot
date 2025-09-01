Student Database Chatbot

A Flask-based web application that allows users to query a student database using natural language. 
The chatbot can answer questions about student counts, fees, specializations, and more.
---

Features

- Natural Language Queries: Ask questions like "How many students in Mechanical Engineering?" or "What is the name of the student with student ID 369372?"
- Student Statistics: Get counts, averages, minimums, and maximums for student data.
- Specialization and Field of Study: Query students by their field of study or specialization.
- Table Display: View student data in a neat table format.

---
Project Structure

```
student-database-chatbot/
│
├── app.py                # Flask app and routes
├── query_processor.py   # Query processing logic
├── templates/
│   └── index.html        # HTML frontend
├── static/
│   └── style.css         # CSS styles
└── README.md              # Project documentation
```

---
Running the Application

1. Start the Flask app:
  
   python app.py

2. Open your browser and navigate to:
   
   http://127.0.0.1:5000
   

---

Usage Examples

Here are some example queries you can try:

- How many students in Mechanical Engineering?
- How many students in Data Science?
- What is the name of the student with student ID 369372?
- What is the average fees?
- Show students with high fees.
- List all students in Computer Engineering.

---

Supported Fields of Study and Specializations

Fields of Study
- Mechanical Engineering
- Electrical Engineering
- Computer Engineering
- Civil Engineering
- Chemical Engineering

Specializations
- Web Development
- Data Science
- Artificial Intelligence
- Network Security
- Machine Learning

---

License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
